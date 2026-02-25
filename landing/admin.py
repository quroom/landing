from django.contrib import admin

from .mailers import deliver_inquiry_email
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "inquiry_type",
        "marketing_opt_in",
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
        "marketing_opted_in_at",
        "emailed_at",
        "email_error",
    )
    actions = ("resend_selected_emails",)

    @admin.action(description="선택 문의 메일 재전송")
    def resend_selected_emails(self, request, queryset):
        success_count = 0
        failure_count = 0

        for inquiry in queryset:
            if deliver_inquiry_email(inquiry):
                success_count += 1
            else:
                failure_count += 1

        self.message_user(
            request,
            f"재전송 완료: 성공 {success_count}건, 실패 {failure_count}건",
        )
