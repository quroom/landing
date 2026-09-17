from collections import Counter
from html.parser import HTMLParser

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from landing.models import ContactInquiry, FunnelEvent


class ElementParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL_ASYNC=False,
)
class ContactUXTests(TestCase):
    def test_diagnosis_has_unique_field_ids_and_preserves_intent(self):
        response = self.client.get(reverse("landing:free_diagnosis"))
        ids = ElementParser(response.content.decode()).ids
        self.assertEqual([key for key, count in Counter(ids).items() if count > 1], [])
        form = response.context["form"]
        self.assertEqual(form["page_key"].value(), "free_diagnosis")
        self.assertEqual(form["lead_source"].value(), "free_diagnosis_vibe")
        self.assertEqual(form["inquiry_type"].value(), "vibe_diagnosis")
        self.assertContains(response, 'hx-target="#contact-form-wrap"')

    def test_nameless_long_email_submission_fits_database_and_does_not_opt_in(self):
        email = "a" * 64 + "@example.com"
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "page_key": "free_diagnosis",
                "lead_source": "free_diagnosis_vibe",
                "email": email,
                "inquiry_type": "vibe_diagnosis",
                "message": "Deployment diagnosis",
                "agree_privacy": "on",
                "utm_source": "naver",
                "utm_campaign": "diagnosis",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        inquiry = ContactInquiry.objects.get(email=email)
        self.assertEqual(inquiry.name, "a" * 50)
        self.assertFalse(inquiry.marketing_opt_in)
        event = FunnelEvent.objects.get(event_name="contact_submit")
        self.assertEqual(event.page_key, "free_diagnosis")
        self.assertEqual(event.metadata["utm_campaign"], "diagnosis")
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_htmx_form_keeps_input_and_returns_visible_error(self):
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "email": "review@example.com",
                "inquiry_type": "outsourcing",
                "message": "Preserve my project details",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "data-contact-status", status_code=400)
        self.assertContains(response, "Preserve my project details", status_code=400)
        self.assertFalse(ContactInquiry.objects.exists())

    def test_non_javascript_submit_has_complete_page(self):
        response = self.client.post(
            reverse("landing:contact_submit"),
            {
                "email": "review@example.com",
                "inquiry_type": "other",
                "message": "Question",
                "agree_privacy": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<html")
        self.assertContains(response, 'id="contact-form-wrap"')

    def test_english_slim_form_and_portfolio_labels_are_translated(self):
        response = self.client.get(reverse("landing:index"), {"lang": "en"})
        self.assertContains(response, "Project Inquiry")
        self.assertContains(response, "Tell us what you want to build or fix")
        self.assertNotContains(response, "GitHub 코드 보기")
        self.assertNotContains(response, "웹스토어 보기")
        self.assertNotContains(response, 'name="name"')
        self.assertNotContains(response, 'name="company_name"')
        self.assertNotContains(response, 'name="agree_marketing"')
