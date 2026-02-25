from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from landing.models import ContactInquiry


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class ContactFormTests(TestCase):
    def test_contact_submit_invalid_returns_400(self) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "",
                "email": "invalid-email",
                "inquiry_type": "development",
                "message": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "필수 항목을 확인해 주세요.", status_code=400)

    def test_contact_submit_valid_returns_success_and_sends_mail(self) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "테스트 사용자",
                "company_name": "QuRoom",
                "contact": "https://linkedin.com/in/test",
                "email": "tester@example.com",
                "inquiry_type": "development",
                "message": "서비스 문의 테스트",
                "agree_all": "on",
                "agree_privacy": "on",
                "agree_marketing": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의가 접수되었습니다.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["help@quroom.kr"])
        self.assertIn("테스트 사용자", mail.outbox[0].body)
        inquiry = ContactInquiry.objects.get(email="tester@example.com")
        self.assertEqual(inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.SUCCESS)
        self.assertIsNotNone(inquiry.emailed_at)
        self.assertEqual(inquiry.email_error, "")
        self.assertTrue(inquiry.marketing_opt_in)
        self.assertIsNotNone(inquiry.marketing_opted_in_at)

    @patch("landing.mailers.send_mail", side_effect=RuntimeError("smtp failed"))
    def test_contact_submit_email_failure_still_persists_and_returns_success(
        self, _send_mail: object
    ) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "실패 테스트",
                "company_name": "QuRoom",
                "contact": "",
                "email": "failure@example.com",
                "inquiry_type": "other",
                "message": "이메일 실패 처리 테스트",
                "agree_privacy": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의가 접수되었습니다.")
        inquiry = ContactInquiry.objects.get(email="failure@example.com")
        self.assertEqual(inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.FAILED)
        self.assertIn("smtp failed", inquiry.email_error)
        self.assertFalse(inquiry.marketing_opt_in)
        self.assertIsNone(inquiry.marketing_opted_in_at)

    def test_contact_submit_with_agree_all_sets_marketing_opt_in(self) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "전체동의 사용자",
                "email": "all@example.com",
                "inquiry_type": "other",
                "message": "전체 동의 테스트",
                "agree_privacy": "on",
                "agree_all": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        inquiry = ContactInquiry.objects.get(email="all@example.com")
        self.assertTrue(inquiry.marketing_opt_in)
        self.assertIsNotNone(inquiry.marketing_opted_in_at)
