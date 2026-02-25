from django.contrib import admin

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
