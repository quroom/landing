from django.test import RequestFactory, TestCase, override_settings

from landing.analytics import track_event
from landing.models import AnalyticsExcludedIP, FunnelEvent


class AnalyticsTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_track_event_records_when_ip_not_excluded(self) -> None:
        request = self.factory.get("/", REMOTE_ADDR="203.0.113.10")

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        event = FunnelEvent.objects.get(event_name="lp_view", page_key="home")
        self.assertEqual(event.client_ip, "203.0.113.10")

    def test_track_event_records_cf_connecting_ip_when_proxy_is_trusted(self) -> None:
        request = self.factory.get(
            "/",
            REMOTE_ADDR="10.0.0.11",
            HTTP_X_FORWARDED_FOR="173.245.48.9",
            HTTP_CF_CONNECTING_IP="198.51.100.41",
        )

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        event = FunnelEvent.objects.get(event_name="lp_view", page_key="home")
        self.assertEqual(event.client_ip, "198.51.100.41")

    @override_settings(ANALYTICS_EXCLUDED_IPS=["203.0.113.11"])
    def test_track_event_skips_when_remote_addr_is_excluded(self) -> None:
        request = self.factory.get("/", REMOTE_ADDR="203.0.113.11")

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        self.assertFalse(FunnelEvent.objects.filter(event_name="lp_view").exists())

    @override_settings(ANALYTICS_EXCLUDED_IPS=["198.51.100.10"])
    def test_track_event_skips_when_x_forwarded_for_first_hop_is_excluded(
        self,
    ) -> None:
        request = self.factory.get(
            "/",
            REMOTE_ADDR="10.0.0.1",
            HTTP_X_FORWARDED_FOR="198.51.100.10, 10.0.0.1",
        )

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        self.assertFalse(FunnelEvent.objects.filter(event_name="lp_view").exists())

    @override_settings(ANALYTICS_EXCLUDED_IPS=["198.51.100.20"])
    def test_track_event_skips_when_cf_connecting_ip_is_excluded_from_trusted_proxy(
        self,
    ) -> None:
        request = self.factory.get(
            "/",
            REMOTE_ADDR="10.0.0.2",
            HTTP_X_FORWARDED_FOR="173.245.48.9",
            HTTP_CF_CONNECTING_IP="198.51.100.20",
        )

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        self.assertFalse(FunnelEvent.objects.filter(event_name="lp_view").exists())

    @override_settings(ANALYTICS_EXCLUDED_IPS=["198.51.100.30"])
    def test_track_event_ignores_cf_connecting_ip_when_proxy_is_untrusted(self) -> None:
        request = self.factory.get(
            "/",
            REMOTE_ADDR="10.0.0.3",
            HTTP_X_FORWARDED_FOR="203.0.113.8",
            HTTP_CF_CONNECTING_IP="198.51.100.30",
        )

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        event = FunnelEvent.objects.get(event_name="lp_view")
        self.assertEqual(event.client_ip, "203.0.113.8")

    def test_track_event_skips_when_ip_is_excluded_in_db(self) -> None:
        AnalyticsExcludedIP.objects.create(ip_address="203.0.113.77", is_active=True)
        request = self.factory.get("/", REMOTE_ADDR="203.0.113.77")

        track_event(request, "lp_view", page_key="home", lead_source="landing")

        self.assertFalse(FunnelEvent.objects.filter(event_name="lp_view").exists())
