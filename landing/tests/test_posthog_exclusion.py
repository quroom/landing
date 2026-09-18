from django.test import TestCase, override_settings

from landing.models import AnalyticsExcludedIP


class PostHogExclusionTests(TestCase):
    def test_database_exclusion_omits_sdk_on_all_public_templates(self):
        AnalyticsExcludedIP.objects.create(ip_address="192.0.2.10", is_active=True)
        for path in ("/", "/free-diagnosis/", "/privacy/"):
            with self.subTest(path=path):
                response = self.client.get(path, REMOTE_ADDR="192.0.2.10")
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "posthog.init(")
                self.assertNotContains(response, "us.i.posthog.com")
                other = self.client.get(path, REMOTE_ADDR="192.0.2.11")
                self.assertContains(other, "posthog.init(")

    @override_settings(ANALYTICS_EXCLUDED_IPS=["192.0.2.10"])
    def test_proxy_ip_uses_existing_exclusion_settings(self):
        response = self.client.get(
            "/",
            HTTP_X_FORWARDED_FOR="173.245.48.1",
            HTTP_CF_CONNECTING_IP="192.0.2.10",
        )
        self.assertNotContains(response, "posthog.init(")

    def test_inactive_exclusion_keeps_sdk(self):
        AnalyticsExcludedIP.objects.create(ip_address="192.0.2.10", is_active=False)
        response = self.client.get("/", REMOTE_ADDR="192.0.2.10")
        self.assertContains(response, "posthog.init(")
