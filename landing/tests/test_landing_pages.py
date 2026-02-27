from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch

from landing.models import ContactInquiry, FunnelEvent


class LandingPageTests(TestCase):
    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "자동화 실행 파트")
        self.assertContains(response, "외주용역 집중 트랙")
        self.assertContains(response, "창업 기본 인프라 구축")
        self.assertTrue(
            FunnelEvent.objects.filter(event_name="lp_view", page_key="home").exists()
        )

    def test_free_diagnosis_page_renders(self) -> None:
        response = self.client.get(reverse("landing:free_diagnosis"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 자동화 실행 진단 (3분 / 8문항)")

    def test_free_diagnosis_report_preview_renders(self) -> None:
        response = self.client.get(reverse("landing:lead_magnet_report_preview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 진단 결과 메시지 시뮬레이션")
        self.assertContains(response, "핵심 보완 카테고리")
        self.assertContains(response, "전체 4개 항목 보기")
        self.assertContains(response, "2주 실행 우선 1개")
        self.assertContains(response, 'href="/#contact"')
        self.assertNotContains(response, "Top 5")

    def test_founders_page_redirects_to_home(self) -> None:
        response = self.client.get(reverse("landing:founders"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("landing:index"))

    def test_foreign_developers_page_renders(self) -> None:
        response = self.client.get(reverse("landing:foreign_developers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "외국인 개발자 제공 서비스")
        self.assertContains(response, "개발사 네트워크 연결 지원")
        self.assertContains(response, "외국인 개발자 커리어/네트워크 관련 정보 메일 수신")
        self.assertContains(response, "개발사 네트워크 연결")
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="lp_view", page_key="foreign_developers"
            ).exists()
        )

    def test_policy_pages_render(self) -> None:
        privacy = self.client.get(reverse("landing:privacy"))
        terms = self.client.get(reverse("landing:terms"))
        self.assertEqual(privacy.status_code, 200)
        self.assertEqual(terms.status_code, 200)

    def test_admin_dashboard_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_dashboard_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff",
            password="pass1234",
            is_staff=True,
        )
        ContactInquiry.objects.create(
            name="대시보드 테스트",
            email="dashboard@example.com",
            inquiry_type="development",
            message="문의",
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의 운영 대시보드")
        self.assertContains(response, "대시보드 테스트")

    def test_admin_dashboard_filters_by_date_range(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff2",
            password="pass1234",
            is_staff=True,
        )
        old_inquiry = ContactInquiry.objects.create(
            name="오래된 문의",
            email="old@example.com",
            inquiry_type="development",
            message="old",
        )
        ContactInquiry.objects.filter(id=old_inquiry.id).update(
            created_at=timezone.now() - timedelta(days=10)
        )
        ContactInquiry.objects.create(
            name="오늘 문의",
            email="today@example.com",
            inquiry_type="development",
            message="today",
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_dashboard"), {"range": "today"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "오늘 문의")
        self.assertNotContains(response, "오래된 문의")

    def test_admin_dashboard_filters_by_inquiry_type(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff5",
            password="pass1234",
            is_staff=True,
        )
        ContactInquiry.objects.create(
            name="리드마그넷 문의",
            email="lead-type@example.com",
            inquiry_type="lead_magnet_diagnosis",
            message="lead",
        )
        ContactInquiry.objects.create(
            name="일반 문의",
            email="normal-type@example.com",
            inquiry_type="development",
            message="normal",
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("landing:admin_dashboard"), {"type": "lead_magnet_diagnosis"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "리드마그넷 문의")
        self.assertNotContains(response, "일반 문의")

    def test_admin_resend_inquiry_updates_status(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff3",
            password="pass1234",
            is_staff=True,
        )
        inquiry = ContactInquiry.objects.create(
            name="재전송 대상",
            email="retry@example.com",
            inquiry_type="development",
            message="retry",
            email_delivery_status=ContactInquiry.DeliveryStatus.FAILED,
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("landing:admin_resend_inquiry", kwargs={"inquiry_id": inquiry.id})
        )
        self.assertEqual(response.status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.SUCCESS)

    @patch("landing.mailers.send_mail", side_effect=RuntimeError("smtp failed"))
    def test_admin_resend_inquiry_keeps_failed_on_send_error(self, _send_mail: object) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff4",
            password="pass1234",
            is_staff=True,
        )
        inquiry = ContactInquiry.objects.create(
            name="재전송 실패",
            email="retry-fail@example.com",
            inquiry_type="development",
            message="retry fail",
            email_delivery_status=ContactInquiry.DeliveryStatus.FAILED,
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("landing:admin_resend_inquiry", kwargs={"inquiry_id": inquiry.id})
        )
        self.assertEqual(response.status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.FAILED)
        self.assertIn("smtp failed", inquiry.email_error)
