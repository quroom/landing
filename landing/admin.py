from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone

from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "inquiry_type",
        "email_delivery_status",
        "created_at",
        "emailed_at",
    )
    list_filter = ("email_delivery_status", "inquiry_type", "created_at")
    search_fields = ("name", "email", "company_name", "message")
    readonly_fields = (
        "created_at",
        "updated_at",
        "privacy_agreed_at",
        "emailed_at",
        "email_error",
    )
    actions = ("resend_selected_emails",)

    @admin.action(description="선택 문의 메일 재전송")
    def resend_selected_emails(self, request, queryset):
        success_count = 0
        failure_count = 0

        for inquiry in queryset:
            mail_subject = f"[QuRoom 문의] {inquiry.name} / {inquiry.inquiry_type}"
            mail_body = (
                "큐룸 홈페이지 문의가 접수되었습니다.\n\n"
                f"이름: {inquiry.name}\n"
                f"회사명: {inquiry.company_name or '-'}\n"
                f"연락 채널: {inquiry.contact or '-'}\n"
                f"이메일: {inquiry.email}\n"
                f"문의 유형: {inquiry.inquiry_type}\n\n"
                f"문의 내용:\n{inquiry.message}\n"
            )

            try:
                send_mail(
                    subject=mail_subject,
                    message=mail_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.QUROOM_CONTACT_EMAIL],
                    fail_silently=False,
                )
                inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.SUCCESS
                inquiry.emailed_at = timezone.now()
                inquiry.email_error = ""
                success_count += 1
            except Exception as exc:
                inquiry.email_delivery_status = ContactInquiry.DeliveryStatus.FAILED
                inquiry.email_error = str(exc)[:1000]
                failure_count += 1
            finally:
                inquiry.save(
                    update_fields=["email_delivery_status", "emailed_at", "email_error"]
                )

        self.message_user(
            request,
            f"재전송 완료: 성공 {success_count}건, 실패 {failure_count}건",
        )
