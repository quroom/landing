from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch

from landing.content import CAREER_RANGES
from landing.models import ContactInquiry, FunnelEvent


class LandingPageTests(TestCase):
    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "자동화 실행 파트")
        self.assertContains(response, "외주용역 집중 트랙")
        self.assertContains(response, "창업 기본 인프라 구축")
        self.assertContains(response, "공인중개사 자격 취득")
        self.assertContains(response, "중개업 활동, 자동화로 업무 효율화")
        self.assertContains(response, "쉐어하우스 창업 및 확장")
        self.assertEqual(response.context["career_ranges"], CAREER_RANGES)
        body = response.content.decode("utf-8")
        self.assertLess(
            body.index("공인중개사 자격 취득"),
            body.index("중개업 활동, 자동화로 업무 효율화"),
        )
        self.assertLess(
            body.index("중개업 활동, 자동화로 업무 효율화"),
            body.index("쉐어하우스 창업 및 확장"),
        )
        self.assertTrue(
            FunnelEvent.objects.filter(event_name="lp_view", page_key="home").exists()
        )

    def test_free_diagnosis_page_renders(self) -> None:
        response = self.client.get(reverse("landing:free_diagnosis"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 자동화 실행 진단 (3분 / 8문항)")
        self.assertContains(response, "8개 문항 모두 필수 응답입니다.")
        self.assertNotContains(response, "업무 흐름 명확성")
        self.assertNotContains(response, "데이터/운영 기반")

    def test_free_diagnosis_report_preview_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:lead_magnet_report_preview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_free_diagnosis_report_preview_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="preview_staff",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:lead_magnet_report_preview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 진단 결과 메시지 시뮬레이션")
        self.assertContains(response, "16점 만점 시나리오 (정밀)")
        self.assertContains(response, "16/16")
        self.assertContains(response, "핵심 보완 포인트")
        self.assertContains(response, "Intent Coverage")
        preview_reports = response.context["preview_reports"]
        perfect_items = [
            item for item in preview_reports if item.get("is_perfect_preview")
        ]
        self.assertEqual(len(perfect_items), 1)
        self.assertEqual(perfect_items[0]["score"], perfect_items[0]["max_score"])
        one_action_titles = [
            item["one_action"]["title"]
            for item in preview_reports
            if not item.get("is_perfect_preview")
        ]
        self.assertEqual(len(one_action_titles), len(set(one_action_titles)))
        intent_keys = {
            item["one_action"]["intent_key"]
            for item in preview_reports
            if not item.get("is_perfect_preview")
        }
        expected_cta_count = sum(
            1 for item in preview_reports if not item.get("is_perfect_preview")
        )
        self.assertEqual(len(intent_keys), 8)
        self.assertContains(response, "2주 내 끝낼 작업 1개")
        self.assertContains(response, "정밀 진단")
        self.assertNotContains(response, "간단 진단")
        self.assertContains(
            response,
            'href="/?inquiry_type=ax_diagnosis&amp;lead_context=lead_magnet_diagnosis#contact"',
            count=expected_cta_count,
        )
        self.assertNotContains(response, "핵심 보완 카테고리")
        self.assertNotContains(response, "Top 5")
        self.assertNotContains(response, "전체 4개 항목 보기")

    def test_index_applies_recommended_inquiry_type_from_diagnosis_context(self) -> None:
        response = self.client.get(
            reverse("landing:index"),
            {
                "inquiry_type": "ax_diagnosis",
                "lead_context": "lead_magnet_diagnosis",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<option value="ax_diagnosis" selected>자동화 실행 진단</option>',
            html=False,
        )
        self.assertContains(
            response,
            'name="lead_source" value="founder_contact_from_diagnosis"',
            html=False,
        )

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

    def test_healthz_returns_ok(self) -> None:
        response = self.client.get(reverse("landing:healthz"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_admin_dashboard_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_operation_links_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_operation_links"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_operation_links_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_operation_links",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_operation_links"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "운영 링크 모음")
        self.assertContains(response, reverse("landing:healthz"))
        self.assertContains(response, reverse("landing:admin_dashboard"))

    def test_admin_index_shows_operation_link_next_to_dashboard(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_admin_index",
            password="pass1234",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의 대시보드")
        self.assertContains(response, "운영 링크")

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
        self.assertContains(response, "리드마그넷 퍼널 (간단 확인)")
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

    def test_admin_dashboard_uses_user_mail_event_for_conversion_rate(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff6",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        FunnelEvent.objects.create(
            event_name="lead_magnet_start",
            page_key="home",
            lead_source="founder_lead_magnet",
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_submit_user",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent_user",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B", "lead_context": "lead_magnet_diagnosis"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent_admin",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"lead_context": "lead_magnet_diagnosis"},
        )

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "메일 발송 성공 (사용자)")
        self.assertContains(response, "관리자 알림: 1")
        self.assertContains(response, "성공률 100.0%")

    def test_admin_dashboard_falls_back_to_legacy_mail_event(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff7",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        FunnelEvent.objects.create(
            event_name="lead_magnet_start",
            page_key="home",
            lead_source="founder_lead_magnet",
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_submit",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "legacy 이벤트 기준으로 임시 집계 중")
        self.assertContains(response, "제출은 legacy 이벤트 기준으로 임시 집계 중")
        self.assertContains(response, "성공률 100.0%")

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
