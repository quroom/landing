from __future__ import annotations

from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from landing.management.commands.cleanup_personal_data import build_cleanup_plan
from landing.models import ContactInquiry, FunnelEvent


class PersonalDataCleanupCommandTests(TestCase):
    def _inquiry(self, email: str, *, marketing: bool = False) -> ContactInquiry:
        return ContactInquiry.objects.create(
            name="테스터",
            company_name="",
            contact="",
            email=email,
            inquiry_type="other",
            message="문의 내용",
            marketing_opt_in=marketing,
            marketing_opted_in_at=timezone.now() if marketing else None,
        )

    def test_dry_run_does_not_modify_data(self) -> None:
        now = timezone.now()
        old_inquiry = self._inquiry("old@example.com")
        ContactInquiry.objects.filter(id=old_inquiry.id).update(
            updated_at=now - timedelta(days=365 * 3 + 3)
        )
        marketing_inquiry = self._inquiry("marketing@example.com", marketing=True)
        ContactInquiry.objects.filter(id=marketing_inquiry.id).update(
            marketing_opted_in_at=now - timedelta(days=365 * 2 + 3)
        )
        old_event = FunnelEvent.objects.create(event_name="lp_view", page_key="home")
        FunnelEvent.objects.filter(id=old_event.id).update(
            created_at=now - timedelta(days=31 * 27)
        )

        out = StringIO()
        call_command("cleanup_personal_data", stdout=out)

        self.assertIn("dry-run", out.getvalue())
        self.assertTrue(ContactInquiry.objects.filter(id=old_inquiry.id).exists())
        marketing_inquiry.refresh_from_db()
        self.assertTrue(marketing_inquiry.marketing_opt_in)
        self.assertTrue(FunnelEvent.objects.filter(id=old_event.id).exists())

    def test_apply_deletes_expired_rows_and_expires_marketing_consent(self) -> None:
        now = timezone.now()
        expired_inquiry = self._inquiry("expired@example.com")
        recent_inquiry = self._inquiry("recent@example.com")
        marketing_inquiry = self._inquiry("marketing@example.com", marketing=True)
        ContactInquiry.objects.filter(id=expired_inquiry.id).update(
            updated_at=now - timedelta(days=365 * 3 + 3)
        )
        ContactInquiry.objects.filter(id=marketing_inquiry.id).update(
            updated_at=now - timedelta(days=30),
            marketing_opted_in_at=now - timedelta(days=365 * 2 + 3),
        )
        expired_event = FunnelEvent.objects.create(
            event_name="lp_view", page_key="home"
        )
        recent_event = FunnelEvent.objects.create(
            event_name="contact_submit",
            page_key="home",
        )
        FunnelEvent.objects.filter(id=expired_event.id).update(
            created_at=now - timedelta(days=31 * 27)
        )

        out = StringIO()
        call_command("cleanup_personal_data", "--apply", stdout=out)

        self.assertIn("Applied cleanup", out.getvalue())
        self.assertFalse(ContactInquiry.objects.filter(id=expired_inquiry.id).exists())
        self.assertTrue(ContactInquiry.objects.filter(id=recent_inquiry.id).exists())
        marketing_inquiry.refresh_from_db()
        self.assertFalse(marketing_inquiry.marketing_opt_in)
        self.assertIsNone(marketing_inquiry.marketing_opted_in_at)
        self.assertFalse(FunnelEvent.objects.filter(id=expired_event.id).exists())
        self.assertTrue(FunnelEvent.objects.filter(id=recent_event.id).exists())

    def test_cleanup_plan_reports_expected_counts(self) -> None:
        now = timezone.now()
        expired_inquiry = self._inquiry("expired@example.com")
        marketing_inquiry = self._inquiry("marketing@example.com", marketing=True)
        ContactInquiry.objects.filter(id=expired_inquiry.id).update(
            updated_at=now - timedelta(days=365 * 3 + 3)
        )
        ContactInquiry.objects.filter(id=marketing_inquiry.id).update(
            updated_at=now - timedelta(days=30),
            marketing_opted_in_at=now - timedelta(days=365 * 2 + 3),
        )
        expired_event = FunnelEvent.objects.create(
            event_name="lp_view", page_key="home"
        )
        FunnelEvent.objects.filter(id=expired_event.id).update(
            created_at=now - timedelta(days=31 * 27)
        )

        plan = build_cleanup_plan(now=now)

        self.assertEqual(plan.expired_inquiry_count, 1)
        self.assertEqual(plan.expired_marketing_count, 1)
        self.assertEqual(plan.expired_event_count, 1)
