from datetime import timedelta

from django.contrib import admin
from django.urls import reverse
from django.utils import timezone

from .mailers import deliver_inquiry_email
from .models import ContactInquiry, FunnelEvent, Testimonial, TestimonialInvite


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


@admin.register(FunnelEvent)
class FunnelEventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "page_key", "lead_source", "created_at")
    list_filter = ("event_name", "page_key", "lead_source", "created_at")
    search_fields = ("event_name", "page_key", "lead_source")
    readonly_fields = (
        "event_name",
        "page_key",
        "lead_source",
        "metadata",
        "created_at",
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "role_title",
        "company_name",
        "status",
        "consent_public",
        "created_at",
        "approved_at",
    )
    list_filter = ("status", "consent_public", "created_at", "approved_at")
    search_fields = ("name", "role_title", "company_name", "content")
    readonly_fields = ("created_at", "updated_at", "approved_at")
    actions = ("mark_approved", "mark_rejected", "mark_pending")

    @admin.action(description="선택 후기를 승인 처리")
    def mark_approved(self, request, queryset):
        updated = queryset.update(
            status=Testimonial.Status.APPROVED,
            approved_at=timezone.now(),
        )
        self.message_user(request, f"승인 처리: {updated}건")

    @admin.action(description="선택 후기를 반려 처리")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(
            status=Testimonial.Status.REJECTED,
            approved_at=None,
        )
        self.message_user(request, f"반려 처리: {updated}건")

    @admin.action(description="선택 후기를 검토 대기로 되돌리기")
    def mark_pending(self, request, queryset):
        updated = queryset.update(
            status=Testimonial.Status.PENDING,
            approved_at=None,
        )
        self.message_user(request, f"검토 대기 처리: {updated}건")


@admin.register(TestimonialInvite)
class TestimonialInviteAdmin(admin.ModelAdmin):
    list_display = (
        "token_short",
        "target_note",
        "expires_at",
        "is_active",
        "consumed_at",
        "invite_link",
        "created_at",
    )
    list_filter = ("is_active", "expires_at", "consumed_at", "created_at")
    search_fields = ("token", "target_note")
    readonly_fields = (
        "token",
        "created_at",
        "updated_at",
        "consumed_at",
        "invite_link",
    )
    actions = ("reissue_selected_invites",)

    @admin.display(description="Token")
    def token_short(self, obj):
        return obj.token[:12]

    @admin.display(description="Invite URL")
    def invite_link(self, obj):
        path = reverse("landing:testimonial_invite", kwargs={"token": obj.token})
        return f"{obj.token[:8]}... {path}"

    @admin.action(description="선택 초대 링크 재발급")
    def reissue_selected_invites(self, request, queryset):
        count = 0
        for invite in queryset:
            invite.reissue()
            count += 1
        self.message_user(request, f"재발급 완료: {count}건")

    def save_model(self, request, obj, form, change):
        if not obj.expires_at:
            obj.expires_at = timezone.now() + timedelta(days=7)
        super().save_model(request, obj, form, change)
