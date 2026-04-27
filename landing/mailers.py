import re
from html import escape
from threading import Thread

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils import timezone

from .ax_tool_stack import DIAGNOSIS_AXES
from .lead_magnet_sections import build_lead_magnet_section_ast, render_sections_to_text
from .models import ContactInquiry, FunnelEvent

INQUIRY_TYPE_LABELS = {
    "ax_diagnosis": "자동화 실행 진단",
    "ax_build": "자동화 실행 구축",
    "infra_setup": "창업 기본 인프라 구축",
    "outsourcing": "외주용역 집중 트랙",
    "gwangju_scope": "프로젝트 범위/견적 정리",
    "gwangju_homepage": "광주 홈페이지 제작",
    "gwangju_web": "광주 웹개발",
    "gwangju_app": "광주 앱개발",
    "outsourcing_check": "외주 전 체크리스트 점검",
    "development": "서비스 개발(기존 유형)",
    "matching": "개발자 연계(기존 유형)",
    "lead_magnet_diagnosis": "무료 자동화 실행 진단",
    "other": "기타",
    "network": "개발사 네트워크 연결",
    "career": "취업/실무 커리어 상담",
    "settlement": "정착/생활 연계 상담",
}


def _extract_grade_from_report(report_text: str) -> str:
    match = re.search(r"등급[:\s]+([ABC])", report_text)
    return match.group(1) if match else "B"


def _extract_weakest_axis_from_report(report_text: str) -> str:
    key_match = re.search(
        r"핵심 보완 (?:카테고리|포인트)[:\s]+([a-z_]+)\s*\(", report_text
    )
    if key_match and key_match.group(1) in DIAGNOSIS_AXES:
        return key_match.group(1)

    label_match = re.search(
        r"\[(?:핵심 보완 카테고리|핵심 보완 포인트)\]\s*-\s*([^\n(]+)",
        report_text,
        re.MULTILINE,
    )
    if label_match:
        label = label_match.group(1).strip()
        for axis_key, axis in DIAGNOSIS_AXES.items():
            if axis["label"] == label:
                return axis_key

    return "automation_design"


def _extract_score_and_max_from_report(report_text: str) -> tuple[int, int]:
    match = re.search(r"점수[:\s]+(\d+)\s*/\s*(\d+)", report_text)
    if not match:
        return 0, 0
    return int(match.group(1)), int(match.group(2))


def _lead_magnet_cta_for_grade(grade: str) -> tuple[str, str]:
    return ("생산성 개선 상담 요청", "#contact")


def _grade_mail_copy(grade: str) -> tuple[str, str]:
    if grade == "A":
        return (
            "현재 운영 기반이 좋아 1인 운영과 팀 운영 모두 개선 체감을 빠르게 얻을 수 있습니다.",
            "리포트의 1개 과제를 먼저 실행해 주세요.",
        )
    if grade == "B":
        return (
            "핵심 운영은 가능하지만 반복 손실이 누적되는 단계이며, 1인/팀 모두 구조 정리가 필요합니다.",
            "리포트의 1개 과제로 2주 파일럿을 진행해 보세요.",
        )
    return (
        "기초 운영 체계 정비가 먼저 필요한 단계로, 1인/팀 공통 기준을 먼저 세우는 것이 중요합니다.",
        "리포트의 1개 과제를 시작점으로 잡고 실행해 주세요.",
    )


def _grade_axis_mail_copy(grade: str, axis_key: str) -> tuple[str, str]:
    matrix = {
        "workflow_clarity": {
            "A": (
                "업무 흐름은 안정적입니다.",
                "1인 운영은 체크리스트를, 팀 운영은 인수인계 기준 1개를 문서화해 처리 시간을 줄이세요.",
            ),
            "B": (
                "업무 흐름 연결부에서 지연이 발생합니다.",
                "1인/팀 모두 시작-종료-담당자(또는 책임자) 기준을 한 페이지로 고정하세요.",
            ),
            "C": (
                "흐름 정의 부족이 가장 큰 리스크입니다.",
                "핵심 업무 1개를 기준으로 1인/팀 공용 단계표부터 만드세요.",
            ),
        },
        "data_operation_base": {
            "A": (
                "데이터 기반은 좋습니다.",
                "1인은 입력 단순화, 팀은 상태값 통일로 리드 추적 정확도를 높이세요.",
            ),
            "B": (
                "데이터 표준화가 부족합니다.",
                "1인/팀 공통으로 필수 컬럼/상태값 1세트를 먼저 고정하세요.",
            ),
            "C": (
                "데이터 분산으로 의사결정이 느립니다.",
                "단일 시트로 통합해 1인/팀 공통 기준 데이터를 먼저 확정하세요.",
            ),
        },
        "automation_design": {
            "A": (
                "자동화 준비도가 높습니다.",
                "1인은 시간 절감, 팀은 반복 품질 개선이 큰 작업 1개를 자동화하세요.",
            ),
            "B": (
                "자동화 후보가 있으나 우선순위가 모호합니다.",
                "1인/팀 모두 효과/노력 기준으로 1개 후보만 선택하세요.",
            ),
            "C": (
                "자동화 후보 선정부터 필요합니다.",
                "1인은 가장 반복되는 작업 1개, 팀은 누락이 잦은 작업 1개를 우선 과제로 지정하세요.",
            ),
        },
        "execution_system": {
            "A": (
                "실행 루틴은 작동 중입니다.",
                "1인은 개인 검증 항목, 팀은 공통 검증 항목 1개를 추가해 성과 속도를 높이세요.",
            ),
            "B": (
                "실행은 되지만 점검 루틴이 약합니다.",
                "1인/팀 모두 2주 종료 점검 기준(완료/보류/개선)을 먼저 정하세요.",
            ),
            "C": (
                "실행 체계 정비가 급합니다.",
                "1인/팀 공통으로 담당자(또는 책임자)/기한/완료기준을 한 번에 고정하세요.",
            ),
        },
    }
    axis_map = matrix.get(axis_key)
    if not axis_map:
        return _grade_mail_copy(grade)
    return axis_map.get(grade, _grade_mail_copy(grade))


def _default_result_from_report(report_text: str) -> dict:
    score, max_score = _extract_score_and_max_from_report(report_text)
    grade = _extract_grade_from_report(report_text)
    weakest_axis = _extract_weakest_axis_from_report(report_text)
    answered_count = max_score // 2 if max_score else 8
    cta_label, cta_anchor = _lead_magnet_cta_for_grade(grade)
    return {
        "score": score,
        "max_score": max_score,
        "grade": grade,
        "coverage_mode": "detailed",
        "coverage_label": f"정밀 진단 ({answered_count}문항)",
        "summary": _grade_mail_copy(grade)[0],
        "category_insights": [],
        "one_action": {
            "title": "핵심 보완 포인트 기준으로 작업 1개 끝내기",
            "tools": "Make, Google Sheets",
            "execution": "담당자·기한·검증 기준을 문서에 남기고 실제로 1회 실행하면 완료입니다.",
        },
        "profile_tools": ["Make", "Google Sheets", "Notion"],
        "cta": {
            "label": cta_label,
            "href": cta_anchor,
            "note": "홈페이지에서 상담으로 연결할 수 있습니다.",
        },
        "contact_context": {
            "inquiry_type": "ax_diagnosis",
            "lead_context": "lead_magnet_diagnosis",
        },
        "weakest_axis_key": weakest_axis,
    }


def _is_perfect_result(payload: dict) -> bool:
    score = int(payload.get("score", 0) or 0)
    max_score = int(payload.get("max_score", 0) or 0)
    return max_score > 0 and score == max_score


def _build_lead_magnet_user_email(
    inquiry: ContactInquiry,
    *,
    report_text: str,
    result: dict | None = None,
) -> tuple[str, str, str]:
    recipient_display_name = inquiry.name
    if inquiry.company_name:
        recipient_display_name = f"{inquiry.name} ({inquiry.company_name})"

    payload = result or _default_result_from_report(report_text)
    is_perfect_result = _is_perfect_result(payload)
    grade = payload.get("grade", "B")
    weakest_axis = payload.get("weakest_axis_key", "automation_design")
    _, action_copy = _grade_axis_mail_copy(grade, weakest_axis)

    sections = payload.get("sections") or build_lead_magnet_section_ast(payload)
    if is_perfect_result:
        sections = [
            section
            for section in sections
            if section.get("id") in {"summary", "one_action"}
        ]
    section_map = {item.get("id"): item for item in sections}
    weakest_section = section_map.get("weakest") or section_map.get(
        "weakest_category", {}
    )
    one_action_section = section_map.get("one_action", {})
    tools_section = section_map.get("tools", {})
    next_action_section = section_map.get("next_action", {})
    cta = next_action_section.get("cta", {})

    base_url = settings.SITE_BASE_URL.rstrip("/")
    homepage_url = f"{base_url}/"
    normalized_cta_href = cta.get("href", "/#contact")
    if normalized_cta_href.startswith("/"):
        cta_url = f"{base_url}{normalized_cta_href}"
    else:
        cta_url = normalized_cta_href
    weakest_insight = weakest_section.get("weakest_insight") or weakest_section.get(
        "weakest_category"
    )
    text_sections = render_sections_to_text(sections)
    if is_perfect_result:
        text_body = (
            f"{recipient_display_name}님,\n\n"
            "요청하신 무료 자동화 실행 진단 결과입니다.\n\n"
            f"{text_sections}"
        )
    else:
        text_body = (
            f"{recipient_display_name}님,\n\n"
            "요청하신 무료 자동화 실행 진단 결과입니다.\n\n"
            f"{text_sections}\n"
            f"- {cta.get('label', '상담 문의하기')}: {cta_url}\n"
            f"- 홈페이지: {homepage_url}\n\n"
            "이 메일에 회신으로 지금 가장 불편한 반복업무 1가지만 알려주세요.\n"
            "바로 실행 가능한 다음 단계를 제안드리겠습니다."
        )

    if is_perfect_result:
        insight_html = ""
    elif weakest_insight:
        insight_html = (
            "<div style='border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;'>"
            "<p style='margin: 0 0 8px; font-weight: 700;'>핵심 보완 포인트</p>"
            f"<p style='margin: 0; font-weight: 600;'>{escape(weakest_insight.get('label', '-'))}"
            f"{f' ({escape(weakest_insight.get("grade", ""))})' if weakest_insight.get('grade_visible') else ''}</p>"
            f"<p style='margin: 6px 0 0;'>- {escape(weakest_insight.get('message_primary', ''))}</p>"
            f"<p style='margin: 4px 0 0;'>- {escape(weakest_insight.get('message_secondary', ''))}</p>"
            "</div>"
        )
    else:
        insight_html = (
            "<div style='border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;'>"
            "<p style='margin: 0;'>핵심 보완 항목을 추출하지 못했습니다. 상담으로 확인해 주세요.</p>"
            "</div>"
        )

    summary_rows = section_map.get("summary", {}).get("rows", [])
    one_action_rows = one_action_section.get("rows", [])
    tools_value = (tools_section.get("rows") or ["Make, Google Sheets, Notion"])[0]
    score_row = next(
        (row for row in summary_rows if row.startswith("점수:")),
        f"점수: {payload.get('score', 0)}/{payload.get('max_score', 0)}",
    )
    grade_row = next(
        (row for row in summary_rows if row.startswith("등급:")),
        f"등급: {grade}",
    )
    coverage_row = next(
        (row for row in summary_rows if row.startswith("진단 유형:")),
        "",
    )
    summary_row = next(
        (row for row in summary_rows if row.startswith("한 줄 요약:")),
        f"한 줄 요약: {payload.get('summary', '')}",
    )
    one_action_title = (
        one_action_rows[0].replace("작업: ", "") if one_action_rows else "-"
    )
    one_action_exec = (
        one_action_rows[1].replace("완료 기준: ", "")
        if len(one_action_rows) > 1
        else action_copy
    )
    one_action_exec_html = escape(one_action_exec).replace("\n", "<br>")
    tools_html = ""
    cta_html = ""
    footer_html = ""
    if not is_perfect_result:
        tools_html = f"""
      <div style="margin-bottom: 16px;">
        <p style="margin: 0 0 6px; font-weight: 700;">주요 추천 툴</p>
        <p style="margin: 0;">{escape(tools_value)}</p>
      </div>
        """
        cta_html = f"""
      <div style="margin-top: 18px;">
        <a href="{escape(cta_url)}" style="display: inline-block; background: #0ea5e9; color: #fff; text-decoration: none; padding: 11px 16px; border-radius: 10px; font-weight: 600;">
          {escape(cta.get("label", "상담 문의하기"))}
        </a>
      </div>
        """
        footer_html = f"""
      <p style="margin: 10px 0 0;"><a href="{escape(homepage_url)}" style="color: #0f172a;">홈페이지 바로가기</a></p>
      <p style="margin: 14px 0 0;">이 메일에 회신으로 지금 가장 불편한 반복업무 1가지만 알려주세요. 바로 실행 가능한 다음 단계를 제안드리겠습니다.</p>
        """

    html_body = f"""
    <div style="font-family: Pretendard, Arial, sans-serif; color: #0f172a; line-height: 1.8;">
      <p style="margin: 0 0 14px;">{escape(recipient_display_name)}님,</p>
      <p style="margin: 0 0 16px;">요청하신 <strong>무료 자동화 실행 진단 결과</strong>를 전달드립니다.</p>

      <div style="border: 1px solid #dbeafe; background: #f8fbff; border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;">
        <p style="margin: 0 0 6px; font-weight: 700;">진단 요약</p>
        <p style="margin: 0;">{escape(score_row)}</p>
        <p style="margin: 8px 0 0;">{escape(grade_row)}</p>
        {f"<p style='margin: 8px 0 0;'>{escape(coverage_row)}</p>" if coverage_row else ""}
        <p style="margin: 8px 0 0;">{escape(summary_row)}</p>
      </div>

      {insight_html}

      <div style="border: 1px solid #bae6fd; background: #f0f9ff; border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;">
        <p style="margin: 0 0 6px; font-weight: 700;">2주 내 끝낼 작업 1개</p>
        <p style="margin: 0;"><strong>{escape(one_action_title)}</strong></p>
        <p style="margin: 4px 0 0;">완료 기준: {one_action_exec_html}</p>
      </div>

      {tools_html}
      {cta_html}
      {footer_html}
    </div>
    """
    return "[큐룸] 무료 자동화 실행 진단 결과", text_body, html_body


def _build_inquiry_mail(inquiry: ContactInquiry) -> tuple[str, str]:
    inquiry_type_label = INQUIRY_TYPE_LABELS.get(
        inquiry.inquiry_type, inquiry.inquiry_type
    )
    subject = f"[QuRoom 문의] {inquiry.name} / {inquiry.inquiry_type}"
    body = (
        "큐룸 홈페이지 문의가 접수되었습니다.\n\n"
        f"이름: {inquiry.name}\n"
        f"회사명: {inquiry.company_name or '-'}\n"
        f"연락 채널: {inquiry.contact or '-'}\n"
        f"이메일: {inquiry.email}\n"
        f"문의 유형: {inquiry_type_label}\n\n"
        f"문의 내용:\n{inquiry.message}\n"
    )
    return subject, body


def deliver_inquiry_email(
    inquiry: ContactInquiry,
    *,
    lead_magnet_result: dict | None = None,
) -> bool:
    subject, body = _build_inquiry_mail(inquiry)
    success = True
    admin_mail_sent = False
    user_mail_sent = False

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.QUROOM_CONTACT_EMAIL],
            fail_silently=False,
        )
        admin_mail_sent = True
    except Exception as exc:
        success = False
        inquiry.email_error = str(exc)[:1000]

    if success and inquiry.inquiry_type == "lead_magnet_diagnosis":
        try:
            user_subject, text_body, html_body = _build_lead_magnet_user_email(
                inquiry,
                report_text=inquiry.message,
                result=lead_magnet_result,
            )
            message = EmailMultiAlternatives(
                subject=user_subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[inquiry.email],
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)
            user_mail_sent = True
        except Exception as exc:
            success = False
            inquiry.email_error = str(exc)[:1000]

    if success and inquiry.inquiry_type == "lead_magnet_diagnosis":
        grade_value = str(
            (lead_magnet_result or {}).get("grade", "")
        ).strip() or _extract_grade_from_report(inquiry.message)
        base_metadata = {
            "inquiry_id": inquiry.id,
            "lead_context": "lead_magnet_diagnosis",
        }
        if admin_mail_sent:
            FunnelEvent.objects.create(
                event_name="lead_magnet_email_sent_admin",
                page_key="home",
                lead_source="founder_lead_magnet",
                metadata=base_metadata,
            )
        if user_mail_sent:
            FunnelEvent.objects.create(
                event_name="lead_magnet_email_sent_user",
                page_key="home",
                lead_source="founder_lead_magnet",
                metadata={**base_metadata, "grade": grade_value},
            )

    if success:
        inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.SUCCESS
        inquiry.emailed_at = timezone.now()
        inquiry.email_error = ""
    else:
        inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.FAILED

    inquiry.save(update_fields=["email_delivery_status", "emailed_at", "email_error"])
    return success


def deliver_inquiry_email_async(
    inquiry_id: int,
    *,
    event_name: str = "",
    page_key: str = "",
    lead_source: str = "",
    lead_magnet_result: dict | None = None,
) -> None:
    def _worker() -> None:
        inquiry = ContactInquiry.objects.get(id=inquiry_id)
        success = deliver_inquiry_email(inquiry, lead_magnet_result=lead_magnet_result)
        if success and event_name:
            FunnelEvent.objects.create(
                event_name=event_name,
                page_key=page_key,
                lead_source=lead_source,
                metadata={"inquiry_id": inquiry_id},
            )

    Thread(target=_worker, daemon=True).start()
