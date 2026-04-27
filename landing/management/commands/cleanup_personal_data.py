from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, QuerySet
from django.utils import timezone

from landing.models import ContactInquiry, FunnelEvent

CONTACT_INQUIRY_RETENTION_DAYS = 365 * 3
MARKETING_CONSENT_RETENTION_DAYS = 365 * 2
FUNNEL_EVENT_RETENTION_MONTHS = 26


@dataclass(frozen=True)
class CleanupPlan:
    inquiry_delete_cutoff: timezone.datetime
    marketing_expire_cutoff: timezone.datetime
    funnel_event_delete_cutoff: timezone.datetime
    expired_inquiry_count: int
    expired_marketing_count: int
    expired_event_count: int


def _subtract_months(value: timezone.datetime, months: int) -> timezone.datetime:
    month_index = value.month - 1 - months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _expired_inquiries(cutoff: timezone.datetime) -> QuerySet[ContactInquiry]:
    return ContactInquiry.objects.filter(updated_at__lte=cutoff)


def _expired_marketing_consents(
    cutoff: timezone.datetime,
    *,
    exclude_inquiry_ids: QuerySet[ContactInquiry],
) -> QuerySet[ContactInquiry]:
    return (
        ContactInquiry.objects.filter(marketing_opt_in=True)
        .exclude(id__in=exclude_inquiry_ids.values("id"))
        .filter(
            Q(marketing_opted_in_at__lte=cutoff) | Q(marketing_opted_in_at__isnull=True)
        )
    )


def _expired_funnel_events(cutoff: timezone.datetime) -> QuerySet[FunnelEvent]:
    return FunnelEvent.objects.filter(created_at__lte=cutoff)


def build_cleanup_plan(now: timezone.datetime | None = None) -> CleanupPlan:
    now = now or timezone.now()
    inquiry_delete_cutoff = now - timedelta(days=CONTACT_INQUIRY_RETENTION_DAYS)
    marketing_expire_cutoff = now - timedelta(days=MARKETING_CONSENT_RETENTION_DAYS)
    funnel_event_delete_cutoff = _subtract_months(now, FUNNEL_EVENT_RETENTION_MONTHS)

    expired_inquiries = _expired_inquiries(inquiry_delete_cutoff)
    expired_marketing_consents = _expired_marketing_consents(
        marketing_expire_cutoff,
        exclude_inquiry_ids=expired_inquiries,
    )
    expired_events = _expired_funnel_events(funnel_event_delete_cutoff)

    return CleanupPlan(
        inquiry_delete_cutoff=inquiry_delete_cutoff,
        marketing_expire_cutoff=marketing_expire_cutoff,
        funnel_event_delete_cutoff=funnel_event_delete_cutoff,
        expired_inquiry_count=expired_inquiries.count(),
        expired_marketing_count=expired_marketing_consents.count(),
        expired_event_count=expired_events.count(),
    )


class Command(BaseCommand):
    help = "Clean up personal data according to the published retention policy."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply cleanup. Without this flag, the command only prints a dry-run plan.",
        )

    def handle(self, *args: object, **options: object) -> None:
        apply_cleanup = bool(options["apply"])
        plan = build_cleanup_plan()

        self.stdout.write(
            "Personal data cleanup plan "
            f"({'apply' if apply_cleanup else 'dry-run'} mode)"
        )
        self.stdout.write(
            "- contact_inquiries.delete: "
            f"{plan.expired_inquiry_count} "
            f"(updated_at <= {plan.inquiry_delete_cutoff.isoformat()})"
        )
        self.stdout.write(
            "- contact_inquiries.expire_marketing_consent: "
            f"{plan.expired_marketing_count} "
            f"(marketing_opted_in_at <= {plan.marketing_expire_cutoff.isoformat()})"
        )
        self.stdout.write(
            "- funnel_events.delete: "
            f"{plan.expired_event_count} "
            f"(created_at <= {plan.funnel_event_delete_cutoff.isoformat()})"
        )

        if not apply_cleanup:
            self.stdout.write(
                self.style.WARNING(
                    "No changes applied. Re-run with --apply to execute."
                )
            )
            return

        with transaction.atomic():
            expired_inquiries = _expired_inquiries(plan.inquiry_delete_cutoff)
            expired_marketing_consents = _expired_marketing_consents(
                plan.marketing_expire_cutoff,
                exclude_inquiry_ids=expired_inquiries,
            )
            expired_events = _expired_funnel_events(plan.funnel_event_delete_cutoff)

            marketing_updates = expired_marketing_consents.update(
                marketing_opt_in=False,
                marketing_opted_in_at=None,
            )
            inquiry_deletes, _ = expired_inquiries.delete()
            event_deletes, _ = expired_events.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Applied cleanup: "
                f"{inquiry_deletes} inquiry rows deleted, "
                f"{marketing_updates} marketing consents expired, "
                f"{event_deletes} funnel event rows deleted."
            )
        )
