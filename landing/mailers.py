from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import ContactInquiry

INQUIRY_TYPE_LABELS = {
    "development": "서비스 개발",
    "matching": "개발자 연계",
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

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.QUROOM_CONTACT_EMAIL],
            fail_silently=False,
        )
        inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.SUCCESS
        inquiry.emailed_at = timezone.now()
        inquiry.email_error = ""
        success = True
    except Exception as exc:
        inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.FAILED
        inquiry.email_error = str(exc)[:1000]
        success = False

    inquiry.save(update_fields=["email_delivery_status", "emailed_at", "email_error"])
    return success
