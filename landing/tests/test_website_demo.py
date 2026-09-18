from django.test import TestCase
from django.urls import reverse


class WebsiteDemoLinkTests(TestCase):
    def test_homepage_links_to_public_website_demo(self):
        response = self.client.get(reverse("landing:index"))
        self.assertContains(response, 'href="https://website.quroom.kr/"', count=2)
        self.assertContains(response, "홈페이지 데모 보기")
