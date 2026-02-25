from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from landing.models import ContactInquiry


class LandingPageTests(TestCase):
    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AX 실행 파트")
        self.assertContains(response, "외주용역 집중 트랙")
        self.assertContains(response, "창업 기본 인프라 구축")

    def test_founders_page_redirects_to_home(self) -> None:
        response = self.client.get(reverse("landing:founders"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("landing:index"))

    def test_foreign_developers_page_renders(self) -> None:
        response = self.client.get(reverse("landing:foreign_developers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "외국인 개발자 제공 서비스")
        self.assertContains(response, "개발사 네트워크 연결 지원")

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
