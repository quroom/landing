from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path("", views.index, name="index"),
    path("healthz/", views.healthz, name="healthz"),
    path("healthz/live/", views.healthz_live, name="healthz_live"),
    path("healthz/ready/", views.healthz_ready, name="healthz_ready"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path(
        "admin-operation-links/",
        views.admin_operation_links,
        name="admin_operation_links",
    ),
    path(
        "admin-review-guide/",
        views.admin_review_guide,
        name="admin_review_guide",
    ),
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
    path("it/", views.foreign_developers, name="foreign_developers_short"),
    path(
        "foreign/quick-intake/submit/",
        views.foreign_quick_intake_submit,
        name="foreign_quick_intake_submit",
    ),
    path(
        "foreign/matching-profile/submit/",
        views.foreign_matching_profile_submit,
        name="foreign_matching_profile_submit",
    ),
    path(
        "foreign/community-waitlist/submit/",
        views.foreign_community_waitlist_submit,
        name="foreign_community_waitlist_submit",
    ),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("lead-magnet/submit/", views.lead_magnet_submit, name="lead_magnet_submit"),
    path(
        "testimonials/invite/<str:token>/",
        views.testimonial_invite,
        name="testimonial_invite",
    ),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
