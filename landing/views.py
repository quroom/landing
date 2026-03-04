from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .analytics import track_event
from .ax_tool_stack import (
    DIAGNOSIS_AXES,
    DIAGNOSIS_QUESTION_META,
    DIAGNOSIS_QUESTIONS,
    diagnosis_question_keys,
)
from .content import CAREER_RANGES, SHARED_CONTENT, build_page_content
from .forms import ContactForm, LeadMagnetForm
from .lead_magnet_sections import (
    build_lead_magnet_section_ast,
    normalize_contact_cta_href,
    render_sections_to_text,
)
from .mailers import deliver_inquiry_email, deliver_inquiry_email_async
from .models import ContactInquiry, FunnelEvent

INTENT_TOOLS_MAP: dict[str, tuple[list[str], str]] = {
    "find_repetitive_work": (
        ["Google Sheets", "Notion"],
        "반복 작업을 먼저 가시화하면 자동화 후보를 빠르게 고를 수 있습니다.",
    ),
    "document_workflow": (
        ["Notion", "Obsidian"],
        "업무 흐름을 문서화하면 누락과 재작업을 줄일 수 있습니다.",
    ),
    "identify_bottleneck": (
        ["Trello", "Notion", "Google Sheets"],
        "병목 구간을 먼저 고정하면 실행 순서를 명확하게 잡을 수 있습니다.",
    ),
    "unify_operational_data": (
        ["Google Sheets", "Codex", "Notion"],
        "데이터 기준을 하나로 맞추면 판단 속도와 정확도가 올라갑니다.",
    ),
    "pick_automation_candidate": (
        ["Make", "n8n", "OpenClaw"],
        "자동화 후보 1개를 확정하면 2주 파일럿이 현실화됩니다.",
    ),
    "prioritize_automation": (
        ["Make", "Google Sheets", "GPT"],
        "효과 대비 노력 기준으로 우선순위를 정하면 시행착오를 줄일 수 있습니다.",
    ),
    "set_owner_and_goal": (
        ["Trello", "Notion", "Google Calendar"],
        "담당자와 완료기준을 먼저 정하면 실행 지연을 크게 줄일 수 있습니다.",
    ),
    "run_review_loop": (
        ["Notion", "Slack", "Google Docs"],
        "주간 점검 루틴을 고정하면 개선이 누적됩니다.",
    ),
}

INTENT_RESPONSE_PATTERNS: dict[str, dict] = {
    "find_repetitive_work": {
        "id": "intent-find-repetitive-work",
        "name": "반복작업 가시화형",
        "related_intents": ["document_workflow", "pick_automation_candidate"],
    },
    "document_workflow": {
        "id": "intent-document-workflow",
        "name": "흐름 문서화형",
        "related_intents": ["find_repetitive_work", "set_owner_and_goal"],
    },
    "identify_bottleneck": {
        "id": "intent-identify-bottleneck",
        "name": "병목 진단형",
        "related_intents": ["unify_operational_data", "prioritize_automation"],
    },
    "unify_operational_data": {
        "id": "intent-unify-operational-data",
        "name": "데이터 기준 통합형",
        "related_intents": ["identify_bottleneck", "run_review_loop"],
    },
    "pick_automation_candidate": {
        "id": "intent-pick-automation-candidate",
        "name": "자동화 후보 확정형",
        "related_intents": ["prioritize_automation", "find_repetitive_work"],
    },
    "prioritize_automation": {
        "id": "intent-prioritize-automation",
        "name": "자동화 우선순위형",
        "related_intents": ["pick_automation_candidate", "set_owner_and_goal"],
    },
    "set_owner_and_goal": {
        "id": "intent-set-owner-and-goal",
        "name": "실행 책임 고정형",
        "related_intents": ["run_review_loop", "document_workflow"],
    },
    "run_review_loop": {
        "id": "intent-run-review-loop",
        "name": "점검 루프 정착형",
        "related_intents": ["set_owner_and_goal", "unify_operational_data"],
    },
}

FALLBACK_TOOL_RECOMMENDATION = (
    ["Notion", "Google Sheets"],
    "기본 실행 구조를 먼저 정리하면 다음 개선 단계를 설계하기 쉬워집니다.",
)


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _months_between(start: date, end: date) -> int:
    months = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:
        months -= 1
    return max(months, 0)


def _career_duration() -> str:
    today = date.today()
    total_months = 0
    for item in CAREER_RANGES:
        start = _parse_date(item["start"])
        end = _parse_date(item["end"]) if item["end"] else today
        total_months += _months_between(start, end)

    years, months = divmod(total_months, 12)
    return f"{years}년 {months}개월"


def _build_metrics(content: dict, career_duration: str) -> list[dict]:
    metrics = []
    for item in content["metrics"]:
        value = item["value_template"].format(career_duration=career_duration)
        metrics.append(
            {
                "label": item["label"],
                "value": value,
                "description": item["description"],
                "dynamic": "{career_duration}" in item["value_template"],
            }
        )
    return metrics


def _diagnosis_fields(form: LeadMagnetForm) -> list[dict]:
    items: list[dict] = []
    for question_key in diagnosis_question_keys():
        meta = DIAGNOSIS_QUESTION_META[question_key]
        items.append(
            {
                "key": question_key,
                "field": form[question_key],
                "required": bool(meta["required"]),
            }
        )
    return items


def _base_context(
    content: dict,
    page_key: str,
    *,
    recommended_inquiry_type: str = "",
    lead_context: str = "",
) -> dict:
    career_duration = _career_duration()
    lead_magnet_form = LeadMagnetForm()
    form_kwargs: dict = {"page_key": page_key}
    if recommended_inquiry_type.strip():
        form_kwargs["recommended_inquiry_type"] = recommended_inquiry_type
    if lead_context.strip():
        form_kwargs["lead_context"] = lead_context
    return {
        "content": content,
        "career_ranges": CAREER_RANGES,
        "career_duration": career_duration,
        "metrics": _build_metrics(content, career_duration),
        "form": ContactForm(**form_kwargs),
        "lead_magnet_form": lead_magnet_form,
        "lead_magnet_fields": _diagnosis_fields(lead_magnet_form),
        "ga4_measurement_id": settings.GA4_MEASUREMENT_ID,
        "page_key": page_key,
    }


def index(request: HttpRequest) -> HttpResponse:
    track_event(request, "lp_view", page_key="home", lead_source="landing")
    if request.GET.get("lead_magnet") == "start":
        track_event(
            request,
            "lead_magnet_start",
            page_key="home",
            lead_source="founder_lead_magnet",
        )
    context = _base_context(
        build_page_content(),
        page_key="home",
        recommended_inquiry_type=request.GET.get("inquiry_type", ""),
        lead_context=request.GET.get("lead_context", ""),
    )
    return render(request, "landing/index.html", context)


def founders(request: HttpRequest) -> HttpResponse:
    return redirect("landing:index")


def foreign_developers(request: HttpRequest) -> HttpResponse:
    track_event(
        request,
        "lp_view",
        page_key="foreign_developers",
        lead_source="foreign_developers",
    )
    context = _base_context(
        build_page_content("foreign_developers"),
        page_key="foreign_developers",
        recommended_inquiry_type=request.GET.get("inquiry_type", ""),
        lead_context=request.GET.get("lead_context", ""),
    )
    return render(request, "landing/foreign_developers.html", context)


def free_diagnosis(request: HttpRequest) -> HttpResponse:
    track_event(
        request,
        "lp_view",
        page_key="free_diagnosis",
        lead_source="founder_lead_magnet",
    )
    if request.GET.get("lead_magnet") == "start":
        track_event(
            request,
            "lead_magnet_start",
            page_key="free_diagnosis",
            lead_source="founder_lead_magnet",
        )
    context = _base_context(
        build_page_content(),
        page_key="home",
        recommended_inquiry_type=request.GET.get("inquiry_type", ""),
        lead_context=request.GET.get("lead_context", ""),
    )
    return render(request, "landing/free_diagnosis.html", context)


def _render_contact_form(
    request: HttpRequest,
    form: ContactForm,
    status: str | None = None,
    status_message: str = "",
) -> HttpResponse:
    html = render_to_string(
        "landing/partials/contact_form.html",
        {"form": form, "status": status, "status_message": status_message},
        request=request,
    )
    status_code = 200 if status != "error" else 400
    return HttpResponse(html, status=status_code)


def _grade_from_score(score: int, max_score: int) -> str:
    ratio = score / max_score if max_score else 0
    if ratio >= 0.8:
        return "A"
    if ratio >= 0.5:
        return "B"
    return "C"


def _bridge_cta(grade: str) -> dict[str, str]:
    return {
        "label": "생산성 개선 상담 요청",
        "href": "#contact",
        "note": "직접 진행이 어렵다면 상담으로 우선순위부터 함께 정리해드립니다.",
    }


def _grade_summary(grade: str) -> str:
    if grade == "A":
        return "기본 운영은 잘 갖춰져 있습니다. 이제 반복 업무 자동화와 표준화로 속도를 더 높일 단계입니다."
    if grade == "B":
        return "기본 운영은 가능하지만 반복 업무에서 시간 손실이 큽니다. 2주 동안 핵심 작업 1개 개선을 권장합니다."
    return "수작업 비중이 높아 운영이 자주 끊기는 상태입니다. 업무 우선순위와 반복 작업부터 정리하는 것이 좋습니다."


def _result_summary(total_score: int, max_score: int, grade: str) -> str:
    if max_score and total_score == max_score:
        return (
            "현재 운영 수준이 매우 안정적이며 실행 체계를 잘 유지하고 있습니다. "
            "추가 질의가 있으면 상담을 요청해 주세요."
        )
    return _grade_summary(grade)


def _question_meta(question_key: str) -> dict:
    return DIAGNOSIS_QUESTION_META.get(question_key, {})


def _all_intent_keys() -> list[str]:
    keys: list[str] = []
    for question_key in diagnosis_question_keys():
        intent_key = str(_question_meta(question_key).get("intent_key", "")).strip()
        if intent_key and intent_key not in keys:
            keys.append(intent_key)
    return keys


def _intent_pattern_coverage() -> dict[str, object]:
    expected = set(_all_intent_keys())
    pattern_keys = set(INTENT_RESPONSE_PATTERNS)
    tool_keys = set(INTENT_TOOLS_MAP)
    missing_patterns = sorted(expected - pattern_keys)
    missing_tools = sorted(expected - tool_keys)
    return {
        "expected_intents": sorted(expected),
        "pattern_count": len(INTENT_RESPONSE_PATTERNS),
        "is_pattern_count_valid": len(INTENT_RESPONSE_PATTERNS) >= 8,
        "missing_patterns": missing_patterns,
        "missing_tools": missing_tools,
        "is_covered": not missing_patterns and not missing_tools,
    }


def _resolve_response_pattern(intent_key: str) -> dict[str, object]:
    pattern = INTENT_RESPONSE_PATTERNS.get(intent_key)
    if pattern:
        return {
            "id": pattern["id"],
            "name": pattern["name"],
            "primary_intent": intent_key,
            "related_intents": list(pattern.get("related_intents") or []),
        }
    return {
        "id": "intent-fallback",
        "name": "기본 실행 패턴",
        "primary_intent": intent_key,
        "related_intents": [],
    }


def _tools_for_priority(question_key: str) -> tuple[list[str], str]:
    intent_key = _question_meta(question_key).get("intent_key", "")
    return INTENT_TOOLS_MAP.get(intent_key, FALLBACK_TOOL_RECOMMENDATION)


def _coverage_mode(score_map: dict[str, int]) -> tuple[str, str, int]:
    answered_count = len(score_map)
    return "detailed", f"정밀 진단 ({answered_count}문항)", answered_count


def _build_support_summary(priorities: list[str]) -> dict[str, list[str]]:
    direct_items: list[str] = []
    for question_key in priorities:
        label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        direct_items.append(label)
    return {"direct": direct_items}


def _priority_candidates(score_map: dict[str, int]) -> list[dict]:
    candidates: list[dict] = []
    for question_key, score in score_map.items():
        if score >= 2:
            continue
        meta = _question_meta(question_key)
        impact_weight = float(meta.get("impact_weight", 1.0))
        priority_score = (2 - score) * impact_weight
        candidates.append(
            {
                "key": question_key,
                "score": score,
                "impact_weight": impact_weight,
                "priority_score": priority_score,
                "order": int(meta.get("order", 99)),
            }
        )

    if not candidates:
        for question_key, score in score_map.items():
            meta = _question_meta(question_key)
            candidates.append(
                {
                    "key": question_key,
                    "score": score,
                    "impact_weight": float(meta.get("impact_weight", 1.0)),
                    "priority_score": 0.0,
                    "order": int(meta.get("order", 99)),
                }
            )

    candidates.sort(
        key=lambda item: (-item["priority_score"], item["score"], item["order"])
    )
    return candidates


def _priority_keys_from_score_map(score_map: dict[str, int]) -> list[str]:
    return [item["key"] for item in _priority_candidates(score_map)[:3]]


def _axis_scores(score_map: dict[str, int]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for axis_key, axis in DIAGNOSIS_AXES.items():
        answered_scores = [
            score_map[question_key]
            for question_key in axis["questions"]
            if question_key in score_map
        ]
        axis_sum = sum(answered_scores)
        axis_max = 2 * len(answered_scores)
        result[axis_key] = {
            "score": axis_sum,
            "max": axis_max,
            "ratio": axis_sum / axis_max if axis_max else 0,
            "label": axis["label"],
            "answered": len(answered_scores),
            "total": len(axis["questions"]),
        }
    return result


def _segmentation_labels(axis_scores: dict[str, dict[str, float]]) -> dict[str, str]:
    workflow_ratio = axis_scores["workflow_clarity"]["ratio"]
    data_ratio = axis_scores["data_operation_base"]["ratio"]
    automation_ratio = axis_scores["automation_design"]["ratio"]
    execution_ratio = axis_scores["execution_system"]["ratio"]

    if workflow_ratio >= 0.75 and data_ratio >= 0.75:
        operation_type = "운영 구조화형"
    elif workflow_ratio >= 0.5:
        operation_type = "실행 확장형"
    else:
        operation_type = "초기 정리형"

    weakest_axis = min(axis_scores.items(), key=lambda item: item[1]["ratio"])[0]
    bottleneck_map = {
        "workflow_clarity": "업무 흐름 정리 필요",
        "data_operation_base": "데이터 운영 기반 보완 필요",
        "automation_design": "자동화 설계 보완 필요",
        "execution_system": "실행 루틴 정착 필요",
    }
    bottleneck_type = bottleneck_map.get(weakest_axis, "운영 구조 보완 필요")

    if execution_ratio >= 0.75:
        readiness_type = "즉시 실행 가능형"
    elif execution_ratio >= 0.5:
        readiness_type = "가이드 기반 실행형"
    else:
        readiness_type = "기초 정비 필요형"

    return {
        "operation_type": operation_type,
        "bottleneck_type": bottleneck_type,
        "readiness_type": readiness_type,
    }


def _profile_tool_recommendations(
    primary_question_key: str, labels: dict[str, str]
) -> list[str]:
    tools, _ = _tools_for_priority(primary_question_key)
    recommended = list(tools)

    if labels["readiness_type"] == "기초 정비 필요형":
        recommended.append("Notion")

    deduped: list[str] = []
    for item in recommended:
        if item and item not in deduped:
            deduped.append(item)
    return deduped[:3]


def _weakest_axis_key(axis_scores: dict[str, dict[str, float]]) -> str:
    return min(
        axis_scores.items(),
        key=lambda item: (item[1]["ratio"], item[1]["score"], item[0]),
    )[0]


def _axis_key_from_question(question_key: str) -> str:
    axis_key = str(_question_meta(question_key).get("axis", "")).strip()
    if axis_key in DIAGNOSIS_AXES:
        return axis_key
    for candidate_axis_key, axis in DIAGNOSIS_AXES.items():
        if question_key in axis["questions"]:
            return candidate_axis_key
    return ""


def _primary_axis_key(
    axis_scores: dict[str, dict[str, float]],
    score_map: dict[str, int],
    preferred_question_key: str,
) -> str:
    preferred_axis_key = _axis_key_from_question(preferred_question_key)
    if preferred_axis_key and preferred_axis_key in axis_scores:
        if (
            preferred_question_key in score_map
            or axis_scores[preferred_axis_key]["answered"]
        ):
            return preferred_axis_key
    return _weakest_axis_key(axis_scores)


def _weakest_question_in_axis(
    axis_key: str,
    score_map: dict[str, int],
    *,
    preferred_question_key: str = "",
) -> str:
    axis_questions = [
        question_key
        for question_key in DIAGNOSIS_AXES[axis_key]["questions"]
        if question_key in score_map
    ]
    if preferred_question_key and preferred_question_key in axis_questions:
        return preferred_question_key

    if not axis_questions:
        return DIAGNOSIS_AXES[axis_key]["questions"][0]

    def _sort_key(question_key: str) -> tuple:
        score = score_map.get(question_key, 2)
        meta = _question_meta(question_key)
        return (
            score,
            -float(meta.get("impact_weight", 1.0)),
            int(meta.get("order", 99)),
        )

    return sorted(axis_questions, key=_sort_key)[0]


def _category_grade_insights(
    axis_scores: dict[str, dict[str, float]],
    score_map: dict[str, int],
    *,
    preferred_anchor_question: str = "",
) -> list[dict[str, str]]:
    messages = {
        "workflow_clarity": {
            "A": (
                "업무 흐름이 안정적으로 정리되어 있습니다.",
                "현재 문서를 기준으로 자동화 후보 1개를 연결해 실행 속도를 높여보세요.",
            ),
            "B": (
                "업무 흐름은 있으나 단계 기준이 아직 느슨합니다.",
                "시작-처리-완료 기준을 한 페이지로 고정하면 실행 편차를 줄일 수 있습니다.",
            ),
            "C": (
                "업무 흐름 정의가 부족해 반복 손실이 큽니다.",
                "핵심 업무 1개부터 시작-종료 단계를 정해 운영 기준을 먼저 만드세요.",
            ),
        },
        "data_operation_base": {
            "A": (
                "데이터 운영 기반이 안정적입니다.",
                "핵심 지표 1~2개를 주간 단위로 점검해 실행 정확도를 유지하세요.",
            ),
            "B": (
                "데이터는 모이지만 기준 통일이 부족합니다.",
                "필수 입력값과 상태값을 먼저 고정하면 누락/혼선을 줄일 수 있습니다.",
            ),
            "C": (
                "데이터가 분산되어 판단과 대응이 늦어지고 있습니다.",
                "고객/리드/진행상태를 한곳에 모아 운영 기준부터 맞추세요.",
            ),
        },
        "automation_design": {
            "A": (
                "자동화 후보가 명확하게 정리되어 있습니다.",
                "효과가 큰 후보 1개를 파일럿으로 실행해 성과를 확정하세요.",
            ),
            "B": (
                "자동화 후보는 있으나 우선순위 기준이 약합니다.",
                "효과 대비 노력 기준으로 후보를 1개로 압축해 먼저 실행하세요.",
            ),
            "C": (
                "자동화 후보 선정이 아직 시작되지 않았습니다.",
                "반복 빈도가 가장 높은 작업 1개를 먼저 골라 파일럿으로 지정하세요.",
            ),
        },
        "execution_system": {
            "A": (
                "실행 루틴이 안정적으로 운영되고 있습니다.",
                "완료 기준과 점검 주기를 유지하며 개선 로그만 더 보강해보세요.",
            ),
            "B": (
                "실행은 되고 있지만 점검 루틴이 약한 상태입니다.",
                "주간 리뷰 기준을 고정해 완료/보류/개선 상태를 매주 점검하세요.",
            ),
            "C": (
                "실행 체계가 불안정해 과제가 자주 밀리고 있습니다.",
                "담당자·기한·완료기준을 먼저 정하고 2주 실행 루틴을 고정하세요.",
            ),
        },
    }
    insights: list[dict[str, str]] = []
    for axis_key, axis in DIAGNOSIS_AXES.items():
        axis_score = axis_scores[axis_key]
        axis_grade = _grade_from_score(int(axis_score["score"]), int(axis_score["max"]))
        primary, secondary = messages[axis_key][axis_grade]
        preferred_for_axis = (
            preferred_anchor_question
            if _axis_key_from_question(preferred_anchor_question) == axis_key
            else ""
        )
        anchor_question_key = _weakest_question_in_axis(
            axis_key,
            score_map,
            preferred_question_key=preferred_for_axis,
        )
        intent_key = _question_meta(anchor_question_key).get("intent_key", "")
        insights.append(
            {
                "key": axis_key,
                "label": axis["label"],
                "grade": axis_grade,
                "grade_visible": axis_grade != "A",
                "message_primary": primary,
                "message_secondary": secondary,
                "anchor_question_key": anchor_question_key,
                "intent_key": intent_key,
            }
        )
    return insights


def _primary_anchor_question(
    axis_scores: dict[str, dict[str, float]],
    score_map: dict[str, int],
) -> tuple[str, str]:
    weakest_axis_key = _weakest_axis_key(axis_scores)
    anchor_question_key = _weakest_question_in_axis(weakest_axis_key, score_map)
    return weakest_axis_key, anchor_question_key


def _best_single_action(
    score_map: dict[str, int], *, anchor_question_key: str = ""
) -> dict[str, str]:
    candidates = _priority_candidates(score_map)
    fallback_primary = (
        candidates[0]
        if candidates
        else {"key": diagnosis_question_keys()[0], "priority_score": 0.0}
    )
    question_key = (
        anchor_question_key
        if anchor_question_key and anchor_question_key in score_map
        else fallback_primary["key"]
    )
    primary = next((item for item in candidates if item["key"] == question_key), None)
    if not primary:
        primary = {
            "key": question_key,
            "priority_score": (2 - score_map.get(question_key, 2))
            * float(_question_meta(question_key).get("impact_weight", 1.0)),
        }

    intent_key = _question_meta(question_key).get("intent_key", "")

    action_titles = {
        "document_workflow": "핵심 업무 1개의 시작-종료 흐름을 문서로 고정하기",
        "find_repetitive_work": "반복 수작업 1개를 먼저 찾아 자동화 후보로 확정하기",
        "identify_bottleneck": "누락/지연이 자주 나는 병목 구간 1개를 먼저 특정하기",
        "unify_operational_data": "고객/리드/진행상태 데이터를 한곳으로 통합하기",
        "pick_automation_candidate": "자동화 후보 1개를 선정해 2주 파일럿 준비하기",
        "prioritize_automation": "자동화 후보를 효과 대비 노력 기준으로 1개만 선택하기",
        "set_owner_and_goal": "2주 실행의 담당자·기한·완료기준을 확정하기",
        "run_review_loop": "주간 점검 루틴(리뷰/체크리스트)을 운영 캘린더에 고정하기",
    }
    execution_criteria = {
        "find_repetitive_work": "반복 작업 1개를 지정하고 현재 소요시간·주간 반복 횟수를 기록하면 완료입니다.",
        "document_workflow": "시작-처리-완료 단계와 담당자를 한 페이지 문서로 확정하면 완료입니다.",
        "identify_bottleneck": "병목 구간 1개와 지연 원인 3가지를 문서로 정리하면 완료입니다.",
        "unify_operational_data": "고객/리드/진행상태 핵심 컬럼을 단일 시트로 통합하면 완료입니다.",
        "pick_automation_candidate": "자동화 후보 1개를 선정하고 입력/출력 조건을 정의하면 완료입니다.",
        "prioritize_automation": "후보별 기대효과와 준비 난이도를 비교해 1개를 자동화하면 완료입니다.",
        "set_owner_and_goal": "담당자·일정·검증지표를 문서에 고정하고 1회 실행하면 완료입니다.",
        "run_review_loop": "주간 리뷰 일정을 캘린더에 고정하고 체크리스트 점검 2회를 수행하면 완료입니다.",
    }
    tools, reason = _tools_for_priority(question_key)
    return {
        "question_key": question_key,
        "intent_key": intent_key,
        "title": action_titles.get(
            intent_key, DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        ),
        "tools": ", ".join(tools),
        "reason": reason,
        "execution": execution_criteria.get(
            intent_key,
            "담당자·기한·검증 기준을 문서에 남기고 실제로 1회 실행하면 완료입니다.",
        ),
        "priority_score": round(float(primary.get("priority_score", 0.0)), 2),
    }


def _preview_report_signature(item: dict) -> tuple:
    one_action = item.get("one_action") or {}
    cta = item.get("cta") or {}
    return (
        bool(item.get("is_perfect_preview", False)),
        one_action.get("title", ""),
        one_action.get("execution", ""),
        one_action.get("tools", ""),
        cta.get("label", ""),
        item.get("cta_url", ""),
    )


def _weakest_insight_signature(insight: dict) -> tuple:
    return (
        insight.get("label", ""),
        insight.get("grade", ""),
        bool(insight.get("grade_visible", False)),
        insight.get("message_primary", ""),
        insight.get("message_secondary", ""),
    )


def _group_preview_reports(preview_reports: list[dict]) -> list[dict]:
    grouped: dict[tuple, dict] = {}
    ordered_keys: list[tuple] = []
    for item in preview_reports:
        signature = _preview_report_signature(item)
        title = item.get("title", "")
        weakest_insight = item.get("weakest_insight") or {}
        if signature not in grouped:
            weakest_insights = [weakest_insight] if weakest_insight else []
            grouped[signature] = {
                **item,
                "scenario_titles": [title] if title else [],
                "scenario_count": 1,
                "weakest_insights": weakest_insights,
            }
            ordered_keys.append(signature)
            continue

        group_item = grouped[signature]
        if title and title not in group_item["scenario_titles"]:
            group_item["scenario_titles"].append(title)
        if weakest_insight:
            existing_signatures = {
                _weakest_insight_signature(candidate)
                for candidate in group_item["weakest_insights"]
            }
            weakest_signature = _weakest_insight_signature(weakest_insight)
            if weakest_signature not in existing_signatures:
                group_item["weakest_insights"].append(weakest_insight)
        group_item["scenario_count"] = len(group_item["scenario_titles"]) or 1

    return [grouped[key] for key in ordered_keys]


def _build_detailed_lead_magnet_report(
    total_score: int,
    max_score: int,
    grade: str,
    score_map: dict[str, int],
) -> str:
    intent_coverage = _intent_pattern_coverage()
    axis_scores = _axis_scores(score_map)
    coverage_mode, coverage_label, answered_count = _coverage_mode(score_map)
    labels = _segmentation_labels(axis_scores)
    weakest_axis_key, anchor_question_key = _primary_anchor_question(
        axis_scores, score_map
    )
    one_action = _best_single_action(
        score_map,
        anchor_question_key=anchor_question_key,
    )
    anchor_intent_key = _question_meta(anchor_question_key).get("intent_key", "")
    if (
        one_action.get("question_key") != anchor_question_key
        or one_action.get("intent_key") != anchor_intent_key
    ):
        one_action = _best_single_action(
            score_map,
            anchor_question_key=anchor_question_key,
        )
    response_pattern = _resolve_response_pattern(one_action.get("intent_key", ""))
    profile_tools = _profile_tool_recommendations(one_action["question_key"], labels)
    category_insights = _category_grade_insights(
        axis_scores,
        score_map,
        preferred_anchor_question=anchor_question_key,
    )
    weakest_insight = next(
        (item for item in category_insights if item["key"] == weakest_axis_key),
        category_insights[0],
    )
    payload = {
        "score": total_score,
        "max_score": max_score,
        "grade": grade,
        "coverage_mode": coverage_mode,
        "coverage_label": coverage_label,
        "answered_count": answered_count,
        "summary": _result_summary(total_score, max_score, grade),
        "response_pattern": response_pattern,
        "intent_coverage": intent_coverage,
        "profile_tools": profile_tools,
        "one_action": one_action,
        "category_insights": category_insights,
        "weakest_insight": weakest_insight,
        "weakest_category_insight": weakest_insight,
        "weakest_axis_key": weakest_axis_key,
        "cta": _bridge_cta(grade),
        "contact_context": {
            "inquiry_type": "ax_diagnosis",
            "lead_context": "lead_magnet_diagnosis",
        },
    }
    sections = build_lead_magnet_section_ast(payload)
    report_text = render_sections_to_text(sections, include_all_categories=False)
    return (
        "요청하신 무료 자동화 실행 진단 리포트입니다.\n\n"
        f"{report_text}\n\n"
        "추가 상담이 필요하면 이 메일에 회신하거나 홈페이지 문의를 남겨주세요."
    )


def _build_lead_magnet_result(score_map: dict[str, int]) -> tuple[dict, str]:
    intent_coverage = _intent_pattern_coverage()
    coverage_mode, coverage_label, answered_count = _coverage_mode(score_map)
    total_score = sum(score_map.values())
    max_score = answered_count * 2
    grade = _grade_from_score(total_score, max_score)
    axis_scores = _axis_scores(score_map)
    labels = _segmentation_labels(axis_scores)
    priorities = _priority_keys_from_score_map(score_map)
    weakest_axis_key, anchor_question_key = _primary_anchor_question(
        axis_scores, score_map
    )
    one_action = _best_single_action(
        score_map,
        anchor_question_key=anchor_question_key,
    )
    anchor_intent_key = _question_meta(anchor_question_key).get("intent_key", "")
    if (
        one_action.get("question_key") != anchor_question_key
        or one_action.get("intent_key") != anchor_intent_key
    ):
        one_action = _best_single_action(
            score_map,
            anchor_question_key=anchor_question_key,
        )
    response_pattern = _resolve_response_pattern(one_action.get("intent_key", ""))
    profile_tools = _profile_tool_recommendations(one_action["question_key"], labels)
    category_insights = _category_grade_insights(
        axis_scores,
        score_map,
        preferred_anchor_question=anchor_question_key,
    )
    weakest_insight = next(
        (item for item in category_insights if item["key"] == weakest_axis_key),
        category_insights[0],
    )
    result = {
        "score": total_score,
        "max_score": max_score,
        "grade": grade,
        "coverage_mode": coverage_mode,
        "coverage_label": coverage_label,
        "answered_count": answered_count,
        "priorities": [DIAGNOSIS_QUESTIONS.get(key, key) for key in priorities[:3]],
        "segmentation": labels,
        "axis_summary": [
            {
                "label": DIAGNOSIS_AXES[axis_key]["label"],
                "score": int(axis["score"]),
                "max": int(axis["max"]),
                "answered": int(axis["answered"]),
                "total": int(axis["total"]),
            }
            for axis_key, axis in axis_scores.items()
        ],
        "profile_tools": profile_tools,
        "support_summary": _build_support_summary(priorities[:3]),
        "cta": _bridge_cta(grade),
        "summary": _result_summary(total_score, max_score, grade),
        "response_pattern": response_pattern,
        "intent_coverage": intent_coverage,
        "one_action": one_action,
        "category_insights": category_insights,
        "weakest_insight": weakest_insight,
        "weakest_category_insight": weakest_insight,
        "weakest_axis_key": weakest_axis_key,
        "weakest_axis_label": DIAGNOSIS_AXES[weakest_axis_key]["label"],
        "contact_context": {
            "inquiry_type": "ax_diagnosis",
            "lead_context": "lead_magnet_diagnosis",
        },
    }
    result["sections"] = build_lead_magnet_section_ast(result)
    next_action = next(
        (
            section
            for section in result["sections"]
            if section.get("id") == "next_action"
        ),
        {},
    )
    result["cta"] = next_action.get("cta", result["cta"])
    report_text = _build_detailed_lead_magnet_report(
        total_score, max_score, grade, score_map
    )
    return result, report_text


@staff_member_required
def lead_magnet_report_preview(request: HttpRequest) -> HttpResponse:
    keys = diagnosis_question_keys()
    intent_coverage = _intent_pattern_coverage()

    def _make_intent_score_map(target_question_key: str) -> dict[str, int]:
        score_map = {key: 2 for key in keys}
        score_map[target_question_key] = 0
        return score_map

    scenarios: list[tuple[str, dict[str, int], bool]] = [
        ("16점 만점 시나리오 (정밀)", {key: 2 for key in keys}, True),
    ]
    for question_key in keys:
        intent_key = _question_meta(question_key).get("intent_key", "")
        label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        scenarios.append(
            (
                f"intent 시나리오 · {intent_key} · {label}",
                _make_intent_score_map(question_key),
                False,
            )
        )
    preview_reports = []
    for title, score_map, is_perfect_preview in scenarios:
        result, report = _build_lead_magnet_result(score_map)
        normalized_cta_href = normalize_contact_cta_href(result["cta"]["href"])
        cta_url = (
            reverse("landing:index") + "#contact"
            if normalized_cta_href == "/#contact"
            else normalized_cta_href
        )
        preview_reports.append(
            {
                "title": title,
                "score": result["score"],
                "max_score": result["max_score"],
                "grade": result["grade"],
                "coverage_label": result["coverage_label"],
                "summary": result["summary"],
                "cta": result["cta"],
                "cta_url": cta_url,
                "priorities": result["priorities"],
                "one_action": result["one_action"],
                "weakest_insight": result["weakest_insight"],
                "weakest_axis_label": result["weakest_axis_label"],
                "sections": result["sections"],
                "report": report,
                "is_perfect_preview": is_perfect_preview,
            }
        )
    preview_reports = _group_preview_reports(preview_reports)

    return render(
        request,
        "landing/lead_magnet_report_preview.html",
        {
            "preview_reports": preview_reports,
            "intent_coverage": intent_coverage,
        },
    )


def _render_lead_magnet_form(
    request: HttpRequest,
    form: LeadMagnetForm,
    result: dict | None = None,
    status: str | None = None,
    status_message: str = "",
) -> HttpResponse:
    html = render_to_string(
        "landing/partials/lead_magnet_form.html",
        {
            "form": form,
            "lead_magnet_fields": _diagnosis_fields(form),
            "result": result,
            "status": status,
            "status_message": status_message,
        },
        request=request,
    )
    status_code = 200 if status != "error" else 400
    return HttpResponse(html, status=status_code)


@require_POST
def contact_submit(request: HttpRequest) -> HttpResponse:
    page_key = request.POST.get("page_key", "home")
    form = ContactForm(request.POST, page_key=page_key)

    if not form.is_valid():
        return _render_contact_form(
            request,
            form,
            status="error",
            status_message="필수 항목을 확인해 주세요.",
        )

    data = form.cleaned_data
    lead_source = data.get("lead_source") or "contact_form"
    lead_context = (
        "lead_magnet_diagnosis"
        if lead_source == "founder_contact_from_diagnosis"
        else ""
    )
    marketing_opt_in = bool(data.get("agree_marketing") or data.get("agree_all"))
    inquiry = ContactInquiry.objects.create(
        name=data["name"],
        company_name=data.get("company_name") or "",
        contact=data.get("contact") or "",
        email=data["email"],
        inquiry_type=data["inquiry_type"],
        message=data["message"],
        marketing_opt_in=marketing_opt_in,
        marketing_opted_in_at=timezone.now() if marketing_opt_in else None,
    )

    if settings.CONTACT_EMAIL_ASYNC:
        deliver_inquiry_email_async(inquiry.id)
    else:
        deliver_inquiry_email(inquiry)
    track_event(
        request,
        "contact_submit",
        page_key=page_key,
        lead_source=lead_source,
        metadata={
            "inquiry_type": data["inquiry_type"],
            "marketing_opt_in": marketing_opt_in,
            "lead_context": lead_context,
        },
    )

    return _render_contact_form(
        request,
        ContactForm(page_key=page_key),
        status="success",
        status_message="문의가 접수되었습니다. 영업일 기준 1~2일 내 답변드리겠습니다.",
    )


@require_POST
def lead_magnet_submit(request: HttpRequest) -> HttpResponse:
    form = LeadMagnetForm(request.POST)
    if not form.is_valid():
        return _render_lead_magnet_form(
            request,
            form,
            status="error",
            status_message="필수 항목을 확인해 주세요.",
        )

    data = form.cleaned_data
    question_keys = diagnosis_question_keys()
    missing_keys = [key for key in question_keys if data.get(key) in {None, ""}]
    if missing_keys:
        return _render_lead_magnet_form(
            request,
            form,
            status="error",
            status_message="8개 문항 모두 응답해 주세요.",
        )
    score_map = {
        question_key: int(data[question_key]) for question_key in question_keys
    }
    result, report_text = _build_lead_magnet_result(score_map)
    total_score = result["score"]
    grade = result["grade"]

    marketing_opt_in = bool(data.get("agree_marketing"))
    inquiry = ContactInquiry.objects.create(
        name=data["name"],
        company_name=data.get("company_name") or "",
        contact="",
        email=data["email"],
        inquiry_type="lead_magnet_diagnosis",
        message=report_text,
        marketing_opt_in=marketing_opt_in,
        marketing_opted_in_at=timezone.now() if marketing_opt_in else None,
    )
    if settings.CONTACT_EMAIL_ASYNC:
        deliver_inquiry_email_async(
            inquiry.id,
            lead_magnet_result=result,
        )
        email_success = True
    else:
        email_success = deliver_inquiry_email(inquiry, lead_magnet_result=result)

    track_event(
        request,
        "lead_magnet_submit_user",
        page_key="home",
        lead_source=data.get("lead_source") or "founder_lead_magnet",
        metadata={
            "score": total_score,
            "grade": grade,
            "lead_context": "lead_magnet_diagnosis",
        },
    )

    success_message = (
        "진단이 완료되었습니다. 전체 리포트/체크리스트를 이메일로 전달했습니다."
        if not settings.CONTACT_EMAIL_ASYNC
        else "진단이 완료되었습니다. 리포트 메일 발송을 처리 중입니다. 잠시 후 이메일을 확인해 주세요."
    )

    return _render_lead_magnet_form(
        request,
        LeadMagnetForm(),
        status="success",
        status_message=success_message,
    )


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "landing/privacy.html", {"content": SHARED_CONTENT})


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "landing/terms.html", {"content": SHARED_CONTENT})


def healthz(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"status": "ok"})


@staff_member_required
def admin_operation_links(request: HttpRequest) -> HttpResponse:
    links = [
        {"label": "헬스체크", "url": reverse("landing:healthz")},
        {"label": "문의 대시보드", "url": reverse("landing:admin_dashboard")},
        {"label": "홈페이지", "url": reverse("landing:index")},
        {"label": "무료 진단", "url": reverse("landing:free_diagnosis")},
        {
            "label": "진단 시뮬레이션 Preview",
            "url": reverse("landing:lead_magnet_report_preview"),
        },
    ]
    return render(request, "landing/admin_operation_links.html", {"links": links})


@staff_member_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    selected_status = request.GET.get("status", "all")
    selected_range = request.GET.get("range", "all")
    selected_type = request.GET.get("type", "all")
    valid_statuses = {choice[0] for choice in ContactInquiry.DeliveryStatus.choices}
    valid_types = {
        "all",
        "lead_magnet_diagnosis",
        "ax_diagnosis",
        "ax_build",
        "infra_setup",
        "development",
        "outsourcing",
        "matching",
        "network",
        "career",
        "settlement",
        "other",
    }

    inquiries = ContactInquiry.objects.all()
    if selected_status in valid_statuses:
        inquiries = inquiries.filter(email_delivery_status=selected_status)
    else:
        selected_status = "all"

    today = timezone.localdate()
    if selected_range == "today":
        inquiries = inquiries.filter(created_at__date=today)
    elif selected_range == "7d":
        inquiries = inquiries.filter(created_at__date__gte=today - timedelta(days=6))
    elif selected_range == "30d":
        inquiries = inquiries.filter(created_at__date__gte=today - timedelta(days=29))
    else:
        selected_range = "all"

    if selected_type in valid_types and selected_type != "all":
        inquiries = inquiries.filter(inquiry_type=selected_type)
    else:
        selected_type = "all"

    status_counts = {
        "total": ContactInquiry.objects.count(),
        "success": ContactInquiry.objects.filter(
            email_delivery_status=ContactInquiry.DeliveryStatus.SUCCESS
        ).count(),
        "failed": ContactInquiry.objects.filter(
            email_delivery_status=ContactInquiry.DeliveryStatus.FAILED
        ).count(),
        "pending": ContactInquiry.objects.filter(
            email_delivery_status=ContactInquiry.DeliveryStatus.PENDING
        ).count(),
        "today": ContactInquiry.objects.filter(
            created_at__date=timezone.localdate()
        ).count(),
        "lead_magnet": ContactInquiry.objects.filter(
            inquiry_type="lead_magnet_diagnosis"
        ).count(),
    }

    inquiry_type_stats = list(
        ContactInquiry.objects.values("inquiry_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    inquiry_type_labels = {
        "lead_magnet_diagnosis": "무료 자동화 실행 진단",
        "ax_diagnosis": "자동화 실행 진단",
        "ax_build": "자동화 실행 구축",
        "infra_setup": "창업 기본 인프라 구축",
        "outsourcing": "외주용역 집중 트랙",
        "network": "개발사 네트워크 연결",
        "career": "취업/실무 커리어 상담",
        "settlement": "정착/생활 연계 상담",
        "other": "기타",
        "development": "서비스 개발(기존 유형)",
        "matching": "개발자 연계(기존 유형)",
    }
    for stat in inquiry_type_stats:
        key = stat.get("inquiry_type", "")
        stat["inquiry_type_label"] = inquiry_type_labels.get(key, key)
    event_counts = {
        "lp_view_home": FunnelEvent.objects.filter(
            event_name="lp_view", page_key="home"
        ).count(),
        "lp_view_foreign": FunnelEvent.objects.filter(
            event_name="lp_view", page_key="foreign_developers"
        ).count(),
        "contact_submit_total": FunnelEvent.objects.filter(
            event_name="contact_submit"
        ).count(),
        "contact_submit_founder": FunnelEvent.objects.filter(
            event_name="contact_submit", lead_source="founder_contact"
        ).count(),
        "contact_submit_foreign": FunnelEvent.objects.filter(
            event_name="contact_submit", lead_source="foreign_developer_contact"
        ).count(),
        "lead_magnet_start": FunnelEvent.objects.filter(
            event_name="lead_magnet_start"
        ).count(),
        "lead_magnet_submit": FunnelEvent.objects.filter(
            event_name="lead_magnet_submit_user"
        ).count(),
        "lead_magnet_submit_legacy": FunnelEvent.objects.filter(
            event_name="lead_magnet_submit"
        ).count(),
        "lead_magnet_email_sent_user": FunnelEvent.objects.filter(
            event_name="lead_magnet_email_sent_user"
        ).count(),
        "lead_magnet_email_sent_admin": FunnelEvent.objects.filter(
            event_name="lead_magnet_email_sent_admin"
        ).count(),
        "lead_magnet_email_sent_legacy": FunnelEvent.objects.filter(
            event_name="lead_magnet_email_sent"
        ).count(),
        "lead_magnet_contact_submit": FunnelEvent.objects.filter(
            event_name="contact_submit",
            lead_source="founder_contact_from_diagnosis",
        ).count(),
    }

    def _rate(numerator: int, denominator: int) -> float:
        if denominator <= 0:
            return 0.0
        return round((numerator / denominator) * 100, 1)

    submit_count = event_counts["lead_magnet_submit"]
    submit_legacy_count = event_counts["lead_magnet_submit_legacy"]
    effective_submit_count = submit_count if submit_count > 0 else submit_legacy_count
    user_mail_sent = event_counts["lead_magnet_email_sent_user"]
    legacy_mail_sent = event_counts["lead_magnet_email_sent_legacy"]
    # Backward compatibility for historical data before *_user/*_admin split.
    effective_user_mail_sent = user_mail_sent if user_mail_sent > 0 else legacy_mail_sent
    if submit_count > 0:
        effective_user_mail_sent = min(effective_user_mail_sent, submit_count)

    lead_magnet_funnel = {
        "start": event_counts["lead_magnet_start"],
        "submit": effective_submit_count,
        "submit_user": submit_count,
        "submit_legacy": submit_legacy_count,
        "is_legacy_submit_fallback": submit_count == 0 and submit_legacy_count > 0,
        "mail_sent_user": event_counts["lead_magnet_email_sent_user"],
        "mail_sent_admin": event_counts["lead_magnet_email_sent_admin"],
        "mail_sent_legacy": event_counts["lead_magnet_email_sent_legacy"],
        "mail_sent_effective_user": effective_user_mail_sent,
        "is_legacy_mail_fallback": user_mail_sent == 0 and legacy_mail_sent > 0,
        "contact_submit": event_counts["lead_magnet_contact_submit"],
        "submit_rate": _rate(
            effective_submit_count, event_counts["lead_magnet_start"]
        ),
        "mail_success_rate": _rate(
            effective_user_mail_sent,
            effective_submit_count,
        ),
        "contact_conversion_rate": _rate(
            event_counts["lead_magnet_contact_submit"],
            effective_user_mail_sent,
        ),
    }

    recent_inquiries = list(inquiries[:25])
    for inquiry in recent_inquiries:
        inquiry.inquiry_type_label = inquiry_type_labels.get(
            inquiry.inquiry_type, inquiry.inquiry_type
        )

    context = {
        "status_counts": status_counts,
        "selected_status": selected_status,
        "selected_range": selected_range,
        "selected_type": selected_type,
        "recent_inquiries": recent_inquiries,
        "inquiry_type_stats": inquiry_type_stats,
        "event_counts": event_counts,
        "lead_magnet_funnel": lead_magnet_funnel,
    }
    return render(request, "landing/admin_dashboard.html", context)


@staff_member_required
@require_POST
def admin_resend_inquiry(request: HttpRequest, inquiry_id: int) -> HttpResponse:
    inquiry = get_object_or_404(ContactInquiry, id=inquiry_id)
    deliver_inquiry_email(inquiry)
    return redirect(f"{reverse('landing:admin_dashboard')}?status=failed")
