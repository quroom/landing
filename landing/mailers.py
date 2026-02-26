from threading import Thread

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.utils import timezone

from .models import ContactInquiry, FunnelEvent

INQUIRY_TYPE_LABELS = {
    "development": "서비스 개발",
    "matching": "개발자 연계",
    "outsourcing": "고액 외주 상담",
    "lead_magnet_diagnosis": "무료 자동화 실행 진단",
    "other": "기타",
}


def _build_inquiry_mail(inquiry: ContactInquiry) -> tuple[str, str]:
    inquiry_type_label = INQUIRY_TYPE_LABELS.get(inquiry.inquiry_type, inquiry.inquiry_type)
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


def deliver_inquiry_email(inquiry: ContactInquiry) -> bool:
    subject, body = _build_inquiry_mail(inquiry)
    success = True

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.QUROOM_CONTACT_EMAIL],
            fail_silently=False,
        )
    except Exception as exc:
        success = False
        inquiry.email_error = str(exc)[:1000]

    if success and inquiry.inquiry_type == "lead_magnet_diagnosis":
        try:
            recipient_display_name = inquiry.name
            if inquiry.company_name:
                recipient_display_name = f"{inquiry.name} ({inquiry.company_name})"
            homepage_url = f"{settings.SITE_BASE_URL}/"
            contact_url = f"{settings.SITE_BASE_URL}/#contact"
            diagnosis_url = f"{settings.SITE_BASE_URL}/free-diagnosis/"

            text_body = (
                f"{recipient_display_name}님,\n\n"
                "요청하신 무료 자동화 실행 진단 리포트입니다.\n\n"
                f"{inquiry.message}\n\n"
                f"홈페이지 보기: {homepage_url}\n"
                f"문의 남기기: {contact_url}\n"
                f"무료 진단 다시하기: {diagnosis_url}\n\n"
                "추가 상담이 필요하면 이 메일에 회신하거나 홈페이지 문의를 남겨주세요."
            )
            html_body = f"""
            <div style="font-family: Pretendard, Arial, sans-serif; line-height: 1.6; color: #0f172a;">
              <p style="margin: 0 0 10px;">{recipient_display_name}님,</p>
              <h2 style="margin: 0 0 12px;">무료 자동화 실행 진단 리포트</h2>
              <p style="margin: 0 0 16px;">요청하신 진단 결과(운영 유형/병목 유형/실행 준비도 세분화 포함)를 전달드립니다.</p>
              <div style="background: #f3f8ff; border: 1px solid #dbeafe; border-radius: 12px; padding: 14px; white-space: pre-line;">{inquiry.message}</div>
              <div style="margin-top: 20px;">
                <a href="{homepage_url}" style="display: inline-block; margin-right: 8px; background: #0f172a; color: #fff; text-decoration: none; padding: 10px 14px; border-radius: 10px;">홈페이지 보기</a>
                <a href="{contact_url}" style="display: inline-block; margin-right: 8px; background: #0ea5e9; color: #fff; text-decoration: none; padding: 10px 14px; border-radius: 10px;">문의 남기기</a>
                <a href="{diagnosis_url}" style="display: inline-block; background: #fff; color: #0f172a; text-decoration: none; border: 1px solid #cbd5e1; padding: 10px 14px; border-radius: 10px;">진단 다시하기</a>
              </div>
            </div>
            """
            message = EmailMultiAlternatives(
                subject="[QuRoom] 무료 자동화 실행 진단 리포트",
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[inquiry.email],
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)
        except Exception as exc:
            success = False
            inquiry.email_error = str(exc)[:1000]

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
) -> None:
    def _worker() -> None:
        inquiry = ContactInquiry.objects.get(id=inquiry_id)
        success = deliver_inquiry_email(inquiry)
        if success and event_name:
            FunnelEvent.objects.create(
                event_name=event_name,
                page_key=page_key,
                lead_source=lead_source,
                metadata={"inquiry_id": inquiry_id},
            )

    Thread(target=_worker, daemon=True).start()
