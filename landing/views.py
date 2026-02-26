from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .analytics import track_event
from .ax_tool_stack import (
    DIAGNOSIS_AXES,
    DIAGNOSIS_QUESTIONS,
    diagnosis_question_keys,
)
from .content import CAREER_RANGES, SHARED_CONTENT, build_page_content
from .forms import ContactForm, LeadMagnetForm
from .mailers import deliver_inquiry_email, deliver_inquiry_email_async
from .models import ContactInquiry, FunnelEvent


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


def _diagnosis_field_groups(form: LeadMagnetForm) -> list[dict]:
    groups = []
    for axis_key, axis in DIAGNOSIS_AXES.items():
        groups.append(
            {
                "key": axis_key,
                "label": axis["label"],
                "description": axis["description"],
                "fields": [form[question_key] for question_key in axis["questions"]],
            }
        )
    return groups


def _base_context(content: dict, page_key: str) -> dict:
    career_duration = _career_duration()
    lead_magnet_form = LeadMagnetForm()
    return {
        "content": content,
        "career_ranges": CAREER_RANGES,
        "career_duration": career_duration,
        "metrics": _build_metrics(content, career_duration),
        "form": ContactForm(page_key=page_key),
        "lead_magnet_form": lead_magnet_form,
        "lead_magnet_field_groups": _diagnosis_field_groups(lead_magnet_form),
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
    context = _base_context(build_page_content(), page_key="home")
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
        build_page_content("foreign_developers"), page_key="foreign_developers"
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
    context = _base_context(build_page_content(), page_key="home")
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
    if grade == "A":
        return {
            "label": "단발성 생산성 개선 상담 요청",
            "href": "#contact",
            "note": "빠른 실행 병목 해소 중심 상담으로 연결합니다.",
        }
    if grade == "B":
        return {
            "label": "자동화 실행 구축 상담 요청",
            "href": "#contact",
            "note": "2~4주 실행체계 구축 상담으로 연결합니다.",
        }
    return {
        "label": "외주 집중 트랙 상담 요청",
        "href": "#contact",
        "note": "외주 집중 트랙은 동시 1개사만 진행합니다.",
    }


def _grade_summary(grade: str) -> str:
    if grade == "A":
        return "실행 기반은 갖춰져 있으며, 1인 운영이든 팀 운영이든 자동화/표준화 최적화로 속도를 더 높일 단계입니다."
    if grade == "B":
        return "핵심 실행은 가능하지만 반복 운영 손실이 누적되는 단계입니다. 1인/팀 모두 2주 집중 개선이 효과적입니다."
    return "구조화되지 않은 수작업 비중이 높아 1인/팀 운영 모두 우선순위 정리와 실행체계 재설계가 필요한 단계입니다."


def _question_key(position: int) -> str:
    keys = diagnosis_question_keys()
    if 1 <= position <= len(keys):
        return keys[position - 1]
    return f"q{position}"


def _tools_for_priority(question_key: str) -> tuple[str, str]:
    k1 = _question_key(1)
    k2 = _question_key(2)
    k3 = _question_key(3)
    k4 = _question_key(4)
    k5 = _question_key(5)
    k6 = _question_key(6)
    k7 = _question_key(7)
    k8 = _question_key(8)
    tools_map = {
        k1: (
            "Google Sheets, Notion",
            "핵심 업무 흐름을 한 화면에서 확인할 수 있게 정리합니다.",
        ),
        k2: (
            "Google Sheets, Make",
            "반복 수작업 구간을 수집하고 자동화 후보를 빠르게 찾습니다.",
        ),
        k3: (
            "Trello, Notion",
            "누락/지연이 나는 병목 지점을 우선순위로 정리합니다.",
        ),
        k4: (
            "Google Sheets, Notion",
            "업무/리드/진행상태 데이터를 한 곳에 통합합니다.",
        ),
        k5: (
            "Make, Google Apps Script",
            "규칙형 업무를 자동화 후보로 정리해 파일럿 대상을 명확히 합니다.",
        ),
        k6: (
            "OpenClaw, Codex/Claude Code",
            "효과 대비 노력 기준으로 자동화 우선순위를 정렬합니다.",
        ),
        k7: (
            "Trello, Notion",
            "2주 실험에 필요한 담당자/시간/검증 기준을 고정합니다.",
        ),
        k8: (
            "Notion 체크리스트, Telegram/Discord",
            "주간 점검 루틴을 고정해 실행 누락을 줄입니다.",
        ),
    }
    return tools_map.get(
        question_key,
        (
            "Notion, Google Sheets",
            "기본 실행/협업 구조를 빠르게 정리합니다.",
        ),
    )


def _score_level(score: int) -> str:
    if score == 2:
        return "운영 중"
    if score == 1:
        return "부분 적용"
    return "미적용"


def _score_feedback(score: int, question_key: str) -> str:
    if score == 2:
        return "이미 운영 중입니다. 현재 방식의 반복 가능성과 문서화를 유지하세요."
    if score == 1:
        return "부분 적용 상태입니다. 템플릿/자동화 규칙을 추가해 운영 편차를 줄이는 것이 좋습니다."
    tools, _ = _tools_for_priority(question_key)
    return (
        f"미적용 상태입니다. 우선 {tools} 조합으로 1개 파일럿을 2주 안에 실행해 보세요."
    )


def _build_support_summary(priorities: list[str]) -> dict[str, list[str]]:
    direct_items: list[str] = []
    for question_key in priorities:
        label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        direct_items.append(label)
    return {"direct": direct_items}


def _priority_keys_from_score_map(score_map: dict[str, int]) -> list[str]:
    deficits = sorted(
        [
            (question_key, score)
            for question_key, score in score_map.items()
            if score < 2
        ],
        key=lambda item: item[1],
    )
    priorities = [question_key for question_key, _ in deficits[:3]]
    if not priorities:
        priorities = list(score_map.keys())[:3]
    return priorities


def _axis_scores(score_map: dict[str, int]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for axis_key, axis in DIAGNOSIS_AXES.items():
        axis_sum = sum(
            score_map.get(question_key, 0) for question_key in axis["questions"]
        )
        axis_max = 2 * len(axis["questions"])
        result[axis_key] = {
            "score": axis_sum,
            "max": axis_max,
            "ratio": axis_sum / axis_max if axis_max else 0,
            "label": axis["label"],
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
    priorities: list[str], labels: dict[str, str]
) -> list[str]:
    recommended: list[str] = []
    for question_key in priorities[:2]:
        tools, _ = _tools_for_priority(question_key)
        recommended.extend([item.strip() for item in tools.split(",")])

    if labels["readiness_type"] == "기초 정비 필요형":
        recommended.append("Trello")

    deduped: list[str] = []
    for item in recommended:
        if item and item not in deduped:
            deduped.append(item)
    return deduped[:3]


def _weakest_axis_key(axis_scores: dict[str, dict[str, float]]) -> str:
    return min(axis_scores.items(), key=lambda item: item[1]["ratio"])[0]


def _category_grade_insights(
    axis_scores: dict[str, dict[str, float]],
) -> list[dict[str, str]]:
    messages = {
        "workflow_clarity": {
            "A": (
                "업무 흐름이 명확합니다.",
                "1인 운영은 체크리스트 고정, 팀 운영은 인수인계 기준 고정으로 효율을 더 높일 수 있습니다.",
            ),
            "B": (
                "흐름은 잡혀 있으나 인수 인계 기준이 약합니다.",
                "1인 운영은 단계별 완료 기준을, 팀 운영은 역할별 인계 기준을 먼저 고정하세요.",
            ),
            "C": (
                "업무 시작-종료 흐름이 불명확합니다.",
                "1인/팀 모두 공통으로 쓰는 최소 프로세스(시작-처리-완료)를 1순위로 정의하세요.",
            ),
        },
        "data_operation_base": {
            "A": (
                "데이터 관리 기반이 안정적입니다.",
                "1인은 핵심 지표 1~2개, 팀은 공통 대시보드 1개로 운영 일관성을 높이세요.",
            ),
            "B": (
                "데이터는 모이지만 표준화가 약합니다.",
                "1인은 입력 규칙 단순화, 팀은 상태값 통일로 협업 혼선을 줄이세요.",
            ),
            "C": (
                "데이터가 분산되어 판단이 어렵습니다.",
                "1인/팀 모두 먼저 단일 데이터 보드를 만들고 그 위에서 자동화를 시작하세요.",
            ),
        },
        "automation_design": {
            "A": (
                "자동화 대상이 선별되어 있습니다.",
                "1인은 시간 절감, 팀은 반복 품질 개선 효과가 큰 작업부터 우선 적용하세요.",
            ),
            "B": (
                "자동화 후보는 있으나 우선순위 기준이 약합니다.",
                "1인/팀 공통으로 효과 대비 노력 기준을 넣어 후보를 1개로 압축하세요.",
            ),
            "C": (
                "자동화 후보 정의가 없습니다.",
                "1인은 가장 자주 하는 반복작업 1개, 팀은 누락이 많은 반복작업 1개를 먼저 지정하세요.",
            ),
        },
        "execution_system": {
            "A": (
                "2주 실행 루틴이 안정적입니다.",
                "1인은 실행 속도, 팀은 회고 품질 관점으로 루틴을 확장하면 됩니다.",
            ),
            "B": (
                "실행은 가능하지만 점검 루틴이 약합니다.",
                "1인은 개인 주간 리뷰, 팀은 공통 주간 리뷰를 고정해 실행 편차를 줄이세요.",
            ),
            "C": (
                "실행 체계가 불안정합니다.",
                "1인/팀 모두 담당자(또는 책임자)·기준일·완료조건부터 먼저 설정하세요.",
            ),
        },
    }
    insights: list[dict[str, str]] = []
    for axis_key, axis in DIAGNOSIS_AXES.items():
        axis_score = axis_scores[axis_key]
        axis_grade = _grade_from_score(int(axis_score["score"]), int(axis_score["max"]))
        primary, secondary = messages[axis_key][axis_grade]
        insights.append(
            {
                "key": axis_key,
                "label": axis["label"],
                "grade": axis_grade,
                "grade_visible": axis_grade != "A",
                "message_primary": primary,
                "message_secondary": secondary,
            }
        )
    return insights


def _best_single_action(score_map: dict[str, int]) -> dict[str, str]:
    lowest_key = min(score_map, key=lambda key: (score_map[key], key))
    question_label = DIAGNOSIS_QUESTIONS.get(lowest_key, lowest_key)
    tools, reason = _tools_for_priority(lowest_key)
    main_tools = ", ".join([item.strip() for item in tools.split(",")][:2])
    return {
        "title": question_label,
        "tools": main_tools,
        "reason": reason,
        "execution": "2주 동안 이 항목 1개만 완료 기준으로 실행하세요.",
    }


def _build_detailed_lead_magnet_report(
    total_score: int,
    max_score: int,
    grade: str,
    priorities: list[str],
    score_map: dict[str, int],
) -> str:
    axis_scores = _axis_scores(score_map)
    labels = _segmentation_labels(axis_scores)
    profile_tools = _profile_tool_recommendations(priorities, labels)
    category_insights = _category_grade_insights(axis_scores)
    weakest_axis_key = _weakest_axis_key(axis_scores)
    weakest_axis_label = DIAGNOSIS_AXES[weakest_axis_key]["label"]
    weakest_insight = next(
        (item for item in category_insights if item["key"] == weakest_axis_key),
        category_insights[0],
    )
    one_action = _best_single_action(score_map)
    cta = _bridge_cta(grade)

    lines = [
        "요청하신 무료 자동화 실행 진단 리포트입니다.",
        "",
        f"[진단 요약] 점수 {total_score}/{max_score}, 등급 {grade}",
        _grade_summary(grade),
        "",
        "[핵심 보완 카테고리]",
        (
            f"- {weakest_insight['label']}"
            f"{f' ({weakest_insight['grade']})' if weakest_insight['grade_visible'] else ''}: "
            f"{weakest_insight['message_primary']}"
        ),
        f"  -> {weakest_insight['message_secondary']}",
        "",
        "[2주 실행 우선 1개]",
        f"- 실행 과제: {one_action['title']}",
        f"- 추천 툴: {one_action['tools']}",
        f"- 수행 기준: {one_action['execution']}",
        f"- 선택 이유: {one_action['reason']}",
    ]

    lines.extend(
        [
            "",
            "[주요 추천 툴]",
            f"- {', '.join(profile_tools)}",
            "",
            "[다음 액션]",
            f"- {cta['label']} ({cta['href']})",
            "",
            "추가 상담이 필요하면 이 메일에 회신하거나 홈페이지 문의를 남겨주세요.",
        ]
    )
    return "\n".join(lines)


def _build_lead_magnet_result(score_map: dict[str, int]) -> tuple[dict, str]:
    total_score = sum(score_map.values())
    max_score = len(score_map) * 2
    grade = _grade_from_score(total_score, max_score)
    axis_scores = _axis_scores(score_map)
    labels = _segmentation_labels(axis_scores)
    priorities = _priority_keys_from_score_map(score_map)
    profile_tools = _profile_tool_recommendations(priorities, labels)
    one_action = _best_single_action(score_map)
    category_insights = _category_grade_insights(axis_scores)
    weakest_axis_key = _weakest_axis_key(axis_scores)
    weakest_category_insight = next(
        (item for item in category_insights if item["key"] == weakest_axis_key),
        category_insights[0],
    )
    result = {
        "score": total_score,
        "max_score": max_score,
        "grade": grade,
        "priorities": [DIAGNOSIS_QUESTIONS.get(key, key) for key in priorities[:3]],
        "segmentation": labels,
        "axis_summary": [
            {
                "label": DIAGNOSIS_AXES[axis_key]["label"],
                "score": int(axis["score"]),
                "max": int(axis["max"]),
            }
            for axis_key, axis in axis_scores.items()
        ],
        "profile_tools": profile_tools,
        "support_summary": _build_support_summary(priorities[:3]),
        "cta": _bridge_cta(grade),
        "summary": _grade_summary(grade),
        "one_action": one_action,
        "category_insights": category_insights,
        "weakest_category_insight": weakest_category_insight,
        "weakest_axis_key": weakest_axis_key,
        "weakest_axis_label": DIAGNOSIS_AXES[weakest_axis_key]["label"],
    }
    report_text = _build_detailed_lead_magnet_report(
        total_score, max_score, grade, priorities, score_map
    )
    return result, report_text


def lead_magnet_report_preview(request: HttpRequest) -> HttpResponse:
    keys = diagnosis_question_keys()

    axis_items = list(DIAGNOSIS_AXES.items())

    def _make_score_map_for_preview(grade: str, weak_axis_key: str) -> dict[str, int]:
        # Show all branches: overall grade(A/B/C) x weakest category(4)
        if grade == "A":
            score_map = {key: 2 for key in keys}
            for q in DIAGNOSIS_AXES[weak_axis_key]["questions"]:
                score_map[q] = 1
            return score_map

        if grade == "B":
            score_map = {key: 1 for key in keys}
            for axis_key, axis in axis_items:
                if axis_key == weak_axis_key:
                    continue
                score_map[axis["questions"][0]] = 2
            return score_map

        # grade == "C"
        score_map = {key: 0 for key in keys}
        for axis_key, axis in axis_items:
            if axis_key == weak_axis_key:
                continue
            for q in axis["questions"]:
                score_map[q] = 1
        return score_map

    scenarios: list[tuple[str, dict[str, int]]] = []
    for grade in ["A", "B", "C"]:
        for axis_key, axis in axis_items:
            title = f"{grade} 등급 · 핵심 보완: {axis['label']}"
            scenarios.append((title, _make_score_map_for_preview(grade, axis_key)))
    preview_reports = []
    for title, score_map in scenarios:
        result, report = _build_lead_magnet_result(score_map)
        cta_href = result["cta"]["href"]
        cta_url = (
            f"{reverse('landing:index')}{cta_href}"
            if cta_href.startswith("#")
            else cta_href
        )
        preview_reports.append(
            {
                "title": title,
                "score": result["score"],
                "max_score": result["max_score"],
                "grade": result["grade"],
                "cta": result["cta"],
                "cta_url": cta_url,
                "priorities": result["priorities"],
                "one_action": result["one_action"],
                "category_insights": result["category_insights"],
                "weakest_category_insight": result["weakest_category_insight"],
                "weakest_axis_label": result["weakest_axis_label"],
                "report": report,
            }
        )

    return render(
        request,
        "landing/lead_magnet_report_preview.html",
        {"preview_reports": preview_reports},
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
            "lead_magnet_field_groups": _diagnosis_field_groups(form),
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
    score_keys = diagnosis_question_keys()
    score_map = {key: int(data[key]) for key in score_keys}
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
            event_name="lead_magnet_email_sent",
            page_key="home",
            lead_source="founder_lead_magnet",
            lead_magnet_result=result,
        )
        email_success = True
    else:
        email_success = deliver_inquiry_email(inquiry, lead_magnet_result=result)

    track_event(
        request,
        "lead_magnet_submit",
        page_key="home",
        lead_source=data.get("lead_source") or "founder_lead_magnet",
        metadata={"score": total_score, "grade": grade},
    )
    if email_success:
        track_event(
            request,
            "lead_magnet_email_sent",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": grade},
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
            event_name="lead_magnet_submit"
        ).count(),
        "lead_magnet_email_sent": FunnelEvent.objects.filter(
            event_name="lead_magnet_email_sent"
        ).count(),
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
    }
    return render(request, "landing/admin_dashboard.html", context)


@staff_member_required
@require_POST
def admin_resend_inquiry(request: HttpRequest, inquiry_id: int) -> HttpResponse:
    inquiry = get_object_or_404(ContactInquiry, id=inquiry_id)
    deliver_inquiry_email(inquiry)
    return redirect(f"{reverse('landing:admin_dashboard')}?status=failed")
