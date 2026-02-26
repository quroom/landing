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
    POSSIBLE_TOOLS,
    QUESTION_SUPPORT_SCOPE,
    USED_TOOLS,
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
        return "실행 기반은 갖춰져 있으나, 자동화/표준화 최적화로 속도를 더 높일 단계입니다."
    if grade == "B":
        return "핵심 실행은 가능하지만 반복 운영 손실이 누적되는 단계입니다. 2주 집중 개선이 효과적입니다."
    return "구조화되지 않은 수작업 비중이 높아 우선순위 정리와 실행체계 재설계가 필요한 단계입니다."


def _tools_for_priority(question_key: str) -> tuple[str, str]:
    tools_map = {
        "q1": (
            "Make, Google Apps Script, Google Sheets",
            "반복 업무 후보를 선정해 자동화 난이도/효과를 빠르게 비교하고 파일럿을 시작합니다.",
        ),
        "q2": (
            "Google Sheets + Make + 메신저 웹훅(텔레그램/디스코드)",
            "문의 접수→분류→담당자 알림→후속 액션 흐름을 표준화해 초기 응답 지연과 누락을 줄입니다.",
        ),
        "q3": (
            "Notion 백로그, Trello, Impact/Effort 매트릭스",
            "효과/노력 기준으로 우선순위를 정리해 2주 실행 백로그를 명확히 만듭니다.",
        ),
        "q4": (
            "Google Sheets, NotebookLM, Obsidian",
            "문의/작업/진행상태를 한 곳에 정리해 현재 운영 상태를 빠르게 파악하고 회고 인사이트를 축적합니다.",
        ),
        "q5": (
            "OpenAI GPT/Codex, Claude/Claude Code, Gemini, Perplexity, Notion 템플릿",
            "초안 생성과 리서치/검증을 분리해 작성 시간을 단축하고 품질을 일정하게 유지합니다.",
        ),
        "q6": (
            "Notion 표준 작업 문서 + Gmail 템플릿(기본), 메신저 상담 흐름(텔레그램/디스코드)",
            "응대/배포/장애 대응 체크리스트를 고정하고 메신저 알림 흐름을 연결해 운영 편차를 줄입니다.",
        ),
        "q7": (
            "Notion 스프린트 보드, Trello, Google Sheets",
            "2주 스프린트 기준으로 목표-작업-검증 루프를 만듭니다.",
        ),
        "q8": (
            "Impact/Effort 매트릭스, OpenClaw, Codex/Claude Code(바이브코딩)",
            "자동화 후보를 정리한 뒤 바이브코딩 기반 시험 구현을 빠르게 검증해 우선순위를 확정합니다.",
        ),
        "q9": (
            "Trello, Notion 스프린트 보드, Google Sheets",
            "2주 실행 단위로 담당자/일정/검증 기준을 명확히 만들어 실행률을 높입니다.",
        ),
        "q10": (
            "Notion 운영 체크리스트, Gmail 템플릿, Telegram/Discord 알림",
            "운영 점검 루틴을 표준화해 누락 없이 개선 루프를 유지합니다.",
        ),
    }
    return tools_map.get(
        question_key,
        (
            "Notion, Google Sheets, GPT/Claude",
            "기본 실행/협업 구조를 빠르게 정리합니다.",
        ),
    )


def _extended_tools_for_priority(question_key: str) -> str:
    extended_map = {
        "q1": "Zapier, n8n",
        "q2": "Slack, Zapier",
        "q3": "GitHub Projects, Supabase",
        "q4": "Slack, Zapier",
        "q5": "Canva, Figma",
        "q6": "Slack, Zapier",
        "q7": "GitHub Projects",
        "q8": "Supabase, GitHub",
        "q9": "Slack, GitHub Projects",
        "q10": "Zapier, Slack",
    }
    return extended_map.get(question_key, ", ".join(POSSIBLE_TOOLS[:3]))


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
    return f"미적용 상태입니다. 우선 {tools} 조합으로 1개 파일럿을 2주 안에 실행해 보세요."


def _support_scope_label(question_key: str) -> str:
    scope = QUESTION_SUPPORT_SCOPE.get(question_key, "direct")
    if scope == "direct":
        return "직접 지원 가능"
    return "직접 지원 가능"


def _build_support_summary(priorities: list[str]) -> dict[str, list[str]]:
    direct_items: list[str] = []
    for question_key in priorities:
        label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        direct_items.append(label)
    return {"direct": direct_items}


def _priority_keys_from_score_map(score_map: dict[str, int]) -> list[str]:
    deficits = sorted(
        [(question_key, score) for question_key, score in score_map.items() if score < 2],
        key=lambda item: item[1],
    )
    priorities = [question_key for question_key, _ in deficits[:5]]
    if not priorities:
        priorities = list(score_map.keys())[:3]
    return priorities


def _axis_scores(score_map: dict[str, int]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for axis_key, axis in DIAGNOSIS_AXES.items():
        axis_sum = sum(score_map.get(question_key, 0) for question_key in axis["questions"])
        axis_max = 2 * len(axis["questions"])
        result[axis_key] = {
            "score": axis_sum,
            "max": axis_max,
            "ratio": axis_sum / axis_max if axis_max else 0,
            "label": axis["label"],
        }
    return result


def _segmentation_labels(axis_scores: dict[str, dict[str, float]]) -> dict[str, str]:
    operating_ratio = axis_scores["operating_context"]["ratio"]
    data_ratio = axis_scores["data_consistency_visibility"]["ratio"]
    repetitive_ratio = axis_scores["repetitive_bottlenecks"]["ratio"]
    automation_ratio = axis_scores["automation_fit"]["ratio"]
    readiness_ratio = axis_scores["execution_readiness"]["ratio"]

    if operating_ratio >= 0.75 and data_ratio >= 0.75:
        operation_type = "운영 구조화형"
    elif operating_ratio >= 0.5:
        operation_type = "실행 확장형"
    else:
        operation_type = "초기 정리형"

    if repetitive_ratio < 0.5:
        bottleneck_type = "반복 병목 집중형"
    elif data_ratio < 0.5:
        bottleneck_type = "데이터 정합성 보완형"
    elif automation_ratio < 0.5:
        bottleneck_type = "자동화 설계 보완형"
    else:
        bottleneck_type = "운영 안정형"

    if readiness_ratio >= 0.75:
        readiness_type = "즉시 실행 가능형"
    elif readiness_ratio >= 0.5:
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
    recommended = []
    for question_key in priorities[:3]:
        tools, _ = _tools_for_priority(question_key)
        recommended.append(tools)

    if labels["bottleneck_type"] == "반복 병목 집중형":
        recommended.append("Make, Google Apps Script, Telegram/Discord 알림 웹훅")
    if labels["readiness_type"] == "기초 정비 필요형":
        recommended.append("Notion 운영 템플릿, Trello 실행 보드")

    deduped: list[str] = []
    for item in recommended:
        if item not in deduped:
            deduped.append(item)
    return deduped[:4]


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
    support_summary = _build_support_summary(priorities)
    lines = [
        "요청하신 무료 자동화 실행 진단 리포트입니다.",
        "본 리포트는 실제 사용 경험이 있는 툴 중심으로 작성되었습니다.",
        "",
        "1) 진단 요약",
        f"- 총점: {total_score}/{max_score}",
        f"- 등급: {grade}",
        f"- 해석: {_grade_summary(grade)}",
        f"- 운영 유형: {labels['operation_type']}",
        f"- 병목 유형: {labels['bottleneck_type']}",
        f"- 실행 준비도 유형: {labels['readiness_type']}",
        "",
        "2) 축별 점검 결과",
    ]
    for axis_key, axis in DIAGNOSIS_AXES.items():
        axis_score = axis_scores[axis_key]
        lines.append(
            f"- {axis['label']}: {int(axis_score['score'])}/{int(axis_score['max'])}"
        )

    lines.extend(
        [
            "",
            "3) 2주 실행 우선순위 Top 5",
        ]
    )
    for idx, question_key in enumerate(priorities, start=1):
        tools, reason = _tools_for_priority(question_key)
        level = _score_level(score_map.get(question_key, 0))
        question_label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        lines.extend(
            [
                f"- 우선순위 {idx}: {question_label}",
                f"  - 현재 수준: {level}",
                f"  - 지원 방식: {_support_scope_label(question_key)}",
                f"  - 추천 툴(실사용 중심): {tools}",
                f"  - 확장 추천 툴: {_extended_tools_for_priority(question_key)}",
                f"  - 적용 포인트: {reason}",
            ]
        )

    lines.extend(
        [
            "",
            "4) 프로파일 기반 추천 툴",
        ]
    )
    for tool in profile_tools:
        lines.append(f"- {tool}")

    lines.extend(
        [
            "",
            "5) 2주 실행 플랜(권장)",
            "- Week 1: 진단 결과 기준으로 현재 프로세스 시각화, 우선순위 1~2 자동화 파일럿 적용",
            "- Week 2: 우선순위 3~5 적용, 주간 운영 리뷰(문의/작업/진행상태)와 표준 작업 문서 정리",
            "",
            "6) 체크리스트",
            "- 반복업무 자동화 1개 이상 배포",
            "- 리드 응답 기준 시간 정의(예: 영업일 24시간)",
            "- 주간 운영 리뷰 루틴 운영",
            "- 핵심 운영 문서 템플릿 표준화",
            "- 다음 2주 실행 백로그 확정",
            "",
            "7) 지원 가능 범위 진단",
            f"- 직접 지원 가능 항목 수: {len(support_summary['direct'])}",
        ]
    )

    if support_summary["direct"]:
        lines.extend(
            [
                "- 직접 지원 가능 항목:",
                *[f"  - {item}" for item in support_summary["direct"]],
            ]
        )

    lines.extend(
        [
            "",
            "8) 체크 결과 상세 피드백",
        ]
    )
    for question_key in [key for key in diagnosis_question_keys() if key in score_map]:
        question_label = DIAGNOSIS_QUESTIONS.get(question_key, question_key)
        level = _score_level(score_map[question_key])
        feedback = _score_feedback(score_map[question_key], question_key)
        lines.extend(
            [
                f"- {question_label}",
                f"  - 체크 결과: {level}",
                f"  - 권장 액션: {feedback}",
            ]
        )

    lines.extend(
        [
            "",
            "9) 현재 기준 툴 스택",
            f"- 자동화/워크플로우: {', '.join(USED_TOOLS['automation_workflow'])}",
            f"- 문서/지식관리: {', '.join(USED_TOOLS['knowledge_docs'])}",
            f"- AI/LLM: {', '.join(USED_TOOLS['ai_llm'])}",
            f"- 프로젝트 관리: {', '.join(USED_TOOLS['project_management'])}",
            "",
            "추가 상담이 필요하면 이 메일에 회신하거나 홈페이지 문의를 남겨주세요.",
        ]
    )
    return "\n".join(lines)


def lead_magnet_report_preview(request: HttpRequest) -> HttpResponse:
    scenarios = [
        (
            "A 등급 예시 (고도화 단계)",
            {
                "q1": 2,
                "q2": 2,
                "q3": 2,
                "q4": 2,
                "q5": 1,
                "q6": 2,
                "q7": 2,
                "q8": 1,
                "q9": 2,
                "q10": 2,
            },
        ),
        (
            "B 등급 예시 (집중 개선 단계)",
            {
                "q1": 1,
                "q2": 1,
                "q3": 1,
                "q4": 2,
                "q5": 1,
                "q6": 1,
                "q7": 2,
                "q8": 1,
                "q9": 1,
                "q10": 1,
            },
        ),
        (
            "C 등급 예시 (기초 정비 단계)",
            {
                "q1": 0,
                "q2": 0,
                "q3": 1,
                "q4": 0,
                "q5": 1,
                "q6": 0,
                "q7": 1,
                "q8": 0,
                "q9": 0,
                "q10": 0,
            },
        ),
    ]
    preview_reports = []
    for title, score_map in scenarios:
        total_score = sum(score_map.values())
        max_score = len(score_map) * 2
        grade = _grade_from_score(total_score, max_score)
        priorities = _priority_keys_from_score_map(score_map)
        report = _build_detailed_lead_magnet_report(
            total_score, max_score, grade, priorities, score_map
        )
        preview_reports.append(
            {
                "title": title,
                "score": total_score,
                "max_score": max_score,
                "grade": grade,
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
    scored = [(key, int(data[key])) for key in score_keys]
    total_score = sum(score for _, score in scored)
    max_score = len(score_keys) * 2
    grade = _grade_from_score(total_score, max_score)
    score_map = {question_key: score for question_key, score in scored}
    axis_scores = _axis_scores(score_map)
    labels = _segmentation_labels(axis_scores)
    priorities = _priority_keys_from_score_map(score_map)
    support_summary = _build_support_summary(priorities)
    profile_tools = _profile_tool_recommendations(priorities, labels)

    result = {
        "score": total_score,
        "max_score": max_score,
        "grade": grade,
        "priorities": [DIAGNOSIS_QUESTIONS.get(key, key) for key in priorities],
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
        "support_summary": support_summary,
        "cta": _bridge_cta(grade),
    }
    report_text = _build_detailed_lead_magnet_report(
        total_score, max_score, grade, priorities, score_map
    )

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
        )
        email_success = True
    else:
        email_success = deliver_inquiry_email(inquiry)

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
        result=result,
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

    context = {
        "status_counts": status_counts,
        "selected_status": selected_status,
        "selected_range": selected_range,
        "selected_type": selected_type,
        "recent_inquiries": inquiries[:25],
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
