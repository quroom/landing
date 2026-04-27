from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from landing.ax_tool_stack import diagnosis_question_keys
from landing.models import ContactInquiry, FunnelEvent


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class ContactFormTests(TestCase):
    def test_contact_form_defaults_to_coffee_chat_for_home(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<option value="coffee_chat" selected>30분 무료 커피챗</option>',
            html=False,
        )

    def test_gwangju_contact_form_uses_local_project_choices(self) -> None:
        response = self.client.get(reverse("landing:gwangju_web_development"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<option value="gwangju_web" selected>광주 웹개발</option>',
            html=False,
        )
        self.assertContains(
            response,
            '<option value="outsourcing_check">외주 전 체크리스트 점검</option>',
            html=False,
        )
        self.assertNotContains(response, "자동화 실행 진단")

    def test_gwangju_contact_submit_accepts_local_project_choice(self) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "page_key": "gwangju_web_development",
                "name": "광주 문의",
                "company_name": "테스트 회사",
                "contact": "",
                "email": "gwangju-web@example.com",
                "inquiry_type": "gwangju_web",
                "message": "광주 웹개발 문의입니다.",
                "agree_privacy": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        inquiry = ContactInquiry.objects.get(email="gwangju-web@example.com")
        self.assertEqual(inquiry.inquiry_type, "gwangju_web")
        event = FunnelEvent.objects.get(event_name="contact_submit")
        self.assertEqual(event.page_key, "gwangju_web_development")
        self.assertEqual(event.lead_source, "gwangju_contact")
        self.assertEqual(event.metadata["inquiry_type"], "gwangju_web")

    def test_contact_submit_invalid_returns_400(self) -> None:
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "",
                "email": "invalid-email",
                "inquiry_type": "ax_build",
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
                "inquiry_type": "ax_build",
                "message": "서비스 문의 테스트",
                "agree_all": "on",
                "agree_privacy": "on",
                "agree_marketing": "on",
                "lead_source": "founder_contact",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의가 접수되었습니다.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["help@quroom.kr"])
        self.assertIn("테스트 사용자", mail.outbox[0].body)
        inquiry = ContactInquiry.objects.get(email="tester@example.com")
        self.assertEqual(
            inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.SUCCESS
        )
        self.assertIsNotNone(inquiry.emailed_at)
        self.assertEqual(inquiry.email_error, "")
        self.assertTrue(inquiry.marketing_opt_in)
        self.assertIsNotNone(inquiry.marketing_opted_in_at)
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="contact_submit", lead_source="founder_contact"
            ).exists()
        )

    def test_contact_submit_invalid_returns_english_message_when_locale_en(
        self,
    ) -> None:
        self.client.cookies["django_language"] = "en"
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "",
                "email": "invalid-email",
                "inquiry_type": "ax_build",
                "message": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Please check required fields.", status_code=400)

    def test_contact_submit_valid_returns_english_success_when_locale_en(self) -> None:
        self.client.cookies["django_language"] = "en"
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "name": "English User",
                "company_name": "QuRoom",
                "contact": "https://linkedin.com/in/test",
                "email": "eng-success@example.com",
                "inquiry_type": "ax_build",
                "message": "Testing English flow",
                "agree_all": "on",
                "agree_privacy": "on",
                "agree_marketing": "on",
                "lead_source": "founder_contact",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your inquiry has been received. We will respond within 1-2 business days.",
        )

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
        self.assertEqual(
            inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.FAILED
        )
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

    def test_foreign_quick_intake_submit_creates_inquiry_and_event(self) -> None:
        response = self.client.post(
            reverse("landing:foreign_quick_intake_submit"),
            {
                "nickname": "DevA",
                "email": "foreign-quick@example.com",
                "target_role": "Backend Engineer",
                "notes": "Need strategy first",
                "agree_privacy": "on",
                "agree_marketing": "on",
                "join_community_waitlist": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your inquiry has been received. We usually reply within 1-2 business days.",
        )
        self.assertContains(response, "Send Inquiry")
        inquiry = ContactInquiry.objects.get(email="foreign-quick@example.com")
        self.assertEqual(inquiry.inquiry_type, "foreign_quick_intake")
        self.assertIn('"funnel_stage": "quick_intake"', inquiry.message)
        self.assertIn('"fit_track": "foreign_software_engineer"', inquiry.message)
        self.assertIn('"recommended_next_step": "matching_profile"', inquiry.message)
        self.assertTrue(inquiry.marketing_opt_in)
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="foreign_quick_intake_submit",
                page_key="foreign_developers",
            ).exists()
        )
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="foreign_community_waitlist_submit",
                page_key="foreign_developers",
                metadata__source_form="quick_intake",
            ).exists()
        )
        quick_event = FunnelEvent.objects.get(
            event_name="foreign_quick_intake_submit",
            page_key="foreign_developers",
        )
        self.assertEqual(quick_event.metadata["fit_track"], "foreign_software_engineer")
        self.assertEqual(
            quick_event.metadata["recommended_next_step"], "matching_profile"
        )

    def test_foreign_quick_intake_submit_marks_adjacent_talent_path(self) -> None:
        response = self.client.post(
            reverse("landing:foreign_quick_intake_submit"),
            {
                "nickname": "DesignA",
                "email": "foreign-adjacent@example.com",
                "target_role": "Industrial Designer",
                "notes": "Exploring work in Korea",
                "agree_privacy": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        inquiry = ContactInquiry.objects.get(email="foreign-adjacent@example.com")
        self.assertIn('"fit_track": "adjacent_international_talent"', inquiry.message)
        self.assertIn(
            '"recommended_next_step": "community_or_manual_follow_up"',
            inquiry.message,
        )
        quick_event = FunnelEvent.objects.get(
            event_name="foreign_quick_intake_submit",
            page_key="foreign_developers",
        )
        self.assertEqual(
            quick_event.metadata["fit_track"], "adjacent_international_talent"
        )
        self.assertEqual(
            quick_event.metadata["recommended_next_step"],
            "community_or_manual_follow_up",
        )

    def test_foreign_matching_profile_submit_creates_matching_pending_record(
        self,
    ) -> None:
        response = self.client.post(
            reverse("landing:foreign_matching_profile_submit"),
            {
                "email": "foreign-match@example.com",
                "cv_or_linkedin": "https://linkedin.com/in/foreign-dev",
                "github_or_portfolio": "https://github.com/foreign-dev",
                "tech_stack": "Python, Django, AWS",
                "experience_level": "Mid-level",
                "visa_status": "D-10",
                "work_preference": "Full-time, Hybrid",
                "location_preference": "Seoul",
                "available_from": "Immediately",
                "agree_privacy": "on",
                "join_community_waitlist": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your inquiry has been received. We usually reply within 1-2 business days.",
        )
        self.assertContains(response, "Submit My Profile")
        inquiry = ContactInquiry.objects.get(email="foreign-match@example.com")
        self.assertEqual(inquiry.inquiry_type, "foreign_matching_profile")
        self.assertIn('"lifecycle_state": "matching_pending"', inquiry.message)
        matching_event = FunnelEvent.objects.get(
            event_name="foreign_matching_profile_complete",
            page_key="foreign_developers",
        )
        self.assertEqual(
            matching_event.metadata["fit_track"], "foreign_software_engineer"
        )
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="foreign_community_waitlist_submit",
                page_key="foreign_developers",
                metadata__source_form="matching_profile",
            ).exists()
        )

    def test_foreign_community_waitlist_submit_creates_event(self) -> None:
        response = self.client.post(
            reverse("landing:foreign_community_waitlist_submit"),
            {
                "email": "waitlist@example.com",
                "note": "Interview prep tips",
                "agree_privacy": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        inquiry = ContactInquiry.objects.get(email="waitlist@example.com")
        self.assertEqual(inquiry.inquiry_type, "foreign_community_waitlist")
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="foreign_community_waitlist_submit",
                page_key="foreign_developers",
            ).exists()
        )

    def test_lead_magnet_submit_sends_two_emails_and_tracks_event(self) -> None:
        question_values = ["2", "2", "1", "1", "2", "1", "2", "1"]
        diagnosis_payload = {
            key: question_values[idx]
            for idx, key in enumerate(diagnosis_question_keys())
        }
        response = self.client.post(
            reverse("landing:lead_magnet_submit"),
            {
                "name": "리드 유저",
                "email": "lead@example.com",
                "company_name": "Lead Co",
                "agree_privacy": "on",
                "agree_marketing": "on",
                "lead_source": "founder_lead_magnet",
                **diagnosis_payload,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "진단이 완료되었습니다.")
        self.assertNotContains(response, "진단 결과 요약")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ["help@quroom.kr"])
        self.assertEqual(mail.outbox[1].to, ["lead@example.com"])
        self.assertEqual(mail.outbox[1].subject, "[큐룸] 무료 자동화 실행 진단 결과")
        self.assertIn("[핵심 보완 포인트]", mail.outbox[1].body)
        self.assertIn("[2주 내 끝낼 작업 1개]", mail.outbox[1].body)
        self.assertIn(
            "완료 기준: 병목 구간 1개와 지연 원인 3가지를 문서로 정리하면 완료입니다.",
            mail.outbox[1].body,
        )
        self.assertIn("진단 유형: 정밀 진단 (8문항)", mail.outbox[1].body)
        self.assertIn("생산성 개선 상담 요청", mail.outbox[1].body)
        self.assertNotIn("외국인 개발자", mail.outbox[1].body)
        self.assertNotIn("Top 5", mail.outbox[1].body)
        self.assertNotIn("확장 추천 툴", mail.outbox[1].body)
        self.assertNotIn("우선 항목", mail.outbox[1].body)
        self.assertIn("[진단 요약]", mail.outbox[1].body)
        self.assertIn("생산성 개선 상담 요청", mail.outbox[1].alternatives[0][0])
        self.assertIn(
            "완료 기준: 병목 구간 1개와 지연 원인 3가지를 문서로 정리하면 완료입니다.",
            mail.outbox[1].alternatives[0][0],
        )
        self.assertNotIn("우선 항목", mail.outbox[1].alternatives[0][0])
        self.assertNotIn("외국인 개발자", mail.outbox[1].alternatives[0][0])
        self.assertNotIn("문의 남기기", mail.outbox[1].alternatives[0][0])
        inquiry = ContactInquiry.objects.get(email="lead@example.com")
        self.assertEqual(inquiry.inquiry_type, "lead_magnet_diagnosis")
        self.assertEqual(
            inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.SUCCESS
        )
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="lead_magnet_submit_user",
                lead_source="founder_lead_magnet",
            ).exists()
        )
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="lead_magnet_email_sent_user",
                lead_source="founder_lead_magnet",
            ).exists()
        )
        self.assertTrue(
            FunnelEvent.objects.filter(
                event_name="lead_magnet_email_sent_admin",
                lead_source="founder_lead_magnet",
            ).exists()
        )
        submit_event = FunnelEvent.objects.filter(
            event_name="lead_magnet_submit_user",
            lead_source="founder_lead_magnet",
        ).latest("created_at")
        self.assertEqual(
            submit_event.metadata.get("lead_context"), "lead_magnet_diagnosis"
        )
        user_mail_event = FunnelEvent.objects.filter(
            event_name="lead_magnet_email_sent_user",
            lead_source="founder_lead_magnet",
        ).latest("created_at")
        self.assertEqual(user_mail_event.metadata.get("grade"), "B")
        self.assertEqual(
            user_mail_event.metadata.get("lead_context"), "lead_magnet_diagnosis"
        )

    def test_lead_magnet_submit_requires_all_questions(self) -> None:
        payload = {
            "name": "문항 누락 사용자",
            "email": "missing@example.com",
            "agree_privacy": "on",
            "lead_source": "founder_lead_magnet",
            "q1": "1",
            "q2": "1",
            "q3": "1",
            "q4": "1",
        }

        response = self.client.post(reverse("landing:lead_magnet_submit"), payload)
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "필수 항목을 확인해 주세요.", status_code=400)
        self.assertEqual(len(mail.outbox), 0)

    def test_lead_magnet_submit_perfect_score_email_matches_preview_contract(
        self,
    ) -> None:
        payload = {
            "name": "만점 사용자",
            "email": "perfect@example.com",
            "agree_privacy": "on",
            "lead_source": "founder_lead_magnet",
        }
        for question_key in diagnosis_question_keys():
            payload[question_key] = "2"

        response = self.client.post(reverse("landing:lead_magnet_submit"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        user_mail = mail.outbox[1]
        self.assertIn("[진단 요약]", user_mail.body)
        self.assertIn("[2주 내 끝낼 작업 1개]", user_mail.body)
        self.assertNotIn("[핵심 보완 포인트]", user_mail.body)
        self.assertNotIn("[주요 추천 툴]", user_mail.body)
        self.assertNotIn("생산성 개선 상담 요청", user_mail.body)
        self.assertNotIn("홈페이지 바로가기", user_mail.alternatives[0][0])
        self.assertNotIn("핵심 보완 포인트", user_mail.alternatives[0][0])
        self.assertNotIn("주요 추천 툴", user_mail.alternatives[0][0])
        self.assertNotIn("생산성 개선 상담 요청", user_mail.alternatives[0][0])

    @override_settings(DEFAULT_FROM_EMAIL="큐룸 <help@quroom.kr>")
    def test_lead_magnet_sender_display_name_uses_brand(self) -> None:
        question_values = ["1", "1", "1", "1", "1", "1", "1", "1"]
        diagnosis_payload = {
            key: question_values[idx]
            for idx, key in enumerate(diagnosis_question_keys())
        }
        response = self.client.post(
            reverse("landing:lead_magnet_submit"),
            {
                "name": "브랜드 테스트",
                "email": "brand@example.com",
                "agree_privacy": "on",
                **diagnosis_payload,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].from_email, "큐룸 <help@quroom.kr>")
