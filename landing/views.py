from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.db.models import Count
from django.utils import timezone
from django.views.decorators.http import require_POST

from .content import CAREER_RANGES, SHARED_CONTENT, build_page_content
from .forms import ContactForm
from .mailers import deliver_inquiry_email
from .models import ContactInquiry


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


def _base_context(content: dict, page_key: str) -> dict:
    career_duration = _career_duration()
    return {
        "content": content,
        "career_ranges": CAREER_RANGES,
        "career_duration": career_duration,
        "metrics": _build_metrics(content, career_duration),
        "form": ContactForm(page_key=page_key),
        "ga4_measurement_id": settings.GA4_MEASUREMENT_ID,
        "page_key": page_key,
    }


def index(request: HttpRequest) -> HttpResponse:
    context = _base_context(build_page_content(), page_key="home")
    return render(request, "landing/index.html", context)


def founders(request: HttpRequest) -> HttpResponse:
    return redirect("landing:index")


def foreign_developers(request: HttpRequest) -> HttpResponse:
    context = _base_context(
        build_page_content("foreign_developers"), page_key="foreign_developers"
    )
    return render(request, "landing/foreign_developers.html", context)


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

    deliver_inquiry_email(inquiry)

    return _render_contact_form(
        request,
        ContactForm(page_key=page_key),
        status="success",
        status_message="문의가 접수되었습니다. 영업일 기준 1~2일 내 답변드리겠습니다.",
    )


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "landing/privacy.html", {"content": SHARED_CONTENT})


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "landing/terms.html", {"content": SHARED_CONTENT})


@staff_member_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    selected_status = request.GET.get("status", "all")
    selected_range = request.GET.get("range", "all")
    valid_statuses = {choice[0] for choice in ContactInquiry.DeliveryStatus.choices}

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
    }

    inquiry_type_stats = list(
        ContactInquiry.objects.values("inquiry_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    context = {
        "status_counts": status_counts,
        "selected_status": selected_status,
        "selected_range": selected_range,
        "recent_inquiries": inquiries[:25],
        "inquiry_type_stats": inquiry_type_stats,
    }
    return render(request, "landing/admin_dashboard.html", context)


@staff_member_required
@require_POST
def admin_resend_inquiry(request: HttpRequest, inquiry_id: int) -> HttpResponse:
    inquiry = get_object_or_404(ContactInquiry, id=inquiry_id)
    deliver_inquiry_email(inquiry)
    return redirect(f"{reverse('landing:admin_dashboard')}?status=failed")
