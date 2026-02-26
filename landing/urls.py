from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path(
        "admin-dashboard/inquiries/<int:inquiry_id>/resend/",
        views.admin_resend_inquiry,
        name="admin_resend_inquiry",
    ),
    path("for-founders/", views.founders, name="founders"),
    path("free-diagnosis/", views.free_diagnosis, name="free_diagnosis"),
    path(
        "free-diagnosis/preview/",
        views.lead_magnet_report_preview,
        name="lead_magnet_report_preview",
    ),
    path(
        "for-foreign-developers/",
        views.foreign_developers,
        name="foreign_developers",
    ),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("lead-magnet/submit/", views.lead_magnet_submit, name="lead_magnet_submit"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
