from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from landing.models import Testimonial, TestimonialInvite


class TestimonialInviteFlowTests(TestCase):
    def test_valid_invite_token_renders_form(self) -> None:
        invite = TestimonialInvite.issue(
            target_note="내일 미팅 후기", expires_in_days=7
        )

        response = self.client.get(
            reverse("landing:testimonial_invite", kwargs={"token": invite.token})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "상담 후기 남기기")
        self.assertContains(response, "내일 미팅 후기")

    def test_expired_invite_token_is_blocked(self) -> None:
        invite = TestimonialInvite.objects.create(
            token="expired-token",
            expires_at=timezone.now() - timedelta(minutes=1),
            target_note="만료 테스트",
        )

        response = self.client.get(
            reverse("landing:testimonial_invite", kwargs={"token": invite.token})
        )

        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "새 링크를 요청", status_code=403)

    def test_submit_consumes_invite_and_second_submit_is_blocked(self) -> None:
        invite = TestimonialInvite.issue(target_note="1회성 테스트", expires_in_days=7)
        url = reverse("landing:testimonial_invite", kwargs={"token": invite.token})
        payload = {
            "name": "홍길동",
            "role_title": "대표",
            "company_name": "큐룸",
            "content": "실행 우선순위 정리가 큰 도움이 됐습니다.",
        }

        first = self.client.post(url, payload)
        invite.refresh_from_db()

        self.assertEqual(first.status_code, 200)
        self.assertIsNotNone(invite.consumed_at)
        testimonial = Testimonial.objects.get(invite=invite)
        self.assertEqual(testimonial.status, Testimonial.Status.PENDING)
        self.assertTrue(testimonial.consent_public)

        second = self.client.post(url, payload)
        self.assertEqual(second.status_code, 403)

    def test_reissue_generates_new_usable_token_and_deactivates_old(self) -> None:
        invite = TestimonialInvite.issue(target_note="재발급 테스트", expires_in_days=7)
        reissued = invite.reissue(expires_in_days=7)
        invite.refresh_from_db()

        self.assertFalse(invite.is_active)
        self.assertNotEqual(invite.token, reissued.token)
        self.assertEqual(reissued.reissued_from_id, invite.id)
        self.assertTrue(reissued.is_usable())


class TestimonialHomepageGatingTests(TestCase):
    @override_settings(TESTIMONIAL_PUBLIC_THRESHOLD=2)
    def test_homepage_hides_testimonials_below_threshold(self) -> None:
        Testimonial.objects.create(
            name="A",
            role_title="대표",
            company_name="회사A",
            content="좋았습니다.",
            consent_public=True,
            status=Testimonial.Status.APPROVED,
        )

        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="testimonials"')

    @override_settings(TESTIMONIAL_PUBLIC_THRESHOLD=2)
    def test_homepage_shows_only_approved_testimonials_at_threshold(self) -> None:
        Testimonial.objects.create(
            name="A",
            role_title="대표",
            company_name="회사A",
            content="승인 후기 1",
            consent_public=True,
            status=Testimonial.Status.APPROVED,
        )
        Testimonial.objects.create(
            name="B",
            role_title="운영",
            company_name="회사B",
            content="승인 후기 2",
            consent_public=True,
            status=Testimonial.Status.APPROVED,
        )
        Testimonial.objects.create(
            name="C",
            role_title="대표",
            company_name="회사C",
            content="반려 후기",
            consent_public=True,
            status=Testimonial.Status.REJECTED,
        )

        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="testimonials"')
        self.assertContains(response, "승인 후기 1")
        self.assertContains(response, "승인 후기 2")
        self.assertNotContains(response, "반려 후기")
