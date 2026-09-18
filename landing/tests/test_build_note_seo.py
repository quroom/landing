import json
from html.parser import HTMLParser

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone

from landing.models import BuildNote


class SchemaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.schemas = []

    def handle_starttag(self, tag, attrs):
        self.active = (
            tag == "script" and dict(attrs).get("type") == "application/ld+json"
        )

    def handle_data(self, data):
        if self.active:
            self.schemas.append(json.loads(data))

    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False


@override_settings(SITE_BASE_URL="https://quroom.kr")
class BuildNoteSeoTests(TestCase):
    def test_www_redirect_preserves_article_path_and_query(self):
        response = self.client.get(
            "/build-notes/?utm_source=threads", HTTP_HOST="www.quroom.kr"
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"], "https://quroom.kr/build-notes/?utm_source=threads"
        )

    def test_sitemap_has_article_modification_date(self):
        response = self.client.get("/sitemap.xml")
        self.assertContains(
            response,
            f"<lastmod>{max(self.note.published_at, self.note.updated_at).isoformat()}</lastmod>",
        )

    def setUp(self):
        self.note, _ = BuildNote.objects.update_or_create(
            slug="vibe-coding-deploy-troubleshooting",
            defaults={
                "title": "배포 점검",
                "summary": "배포 경로",
                "body_markdown": "본문",
                "status": "published",
                "published_at": timezone.now(),
            },
        )

    def test_detail_includes_parseable_schemas_and_matching_visible_cover(self):
        response = self.client.get(f"/build-notes/{self.note.slug}/")
        parser = SchemaParser()
        parser.feed(response.content.decode())
        self.assertEqual(
            [s["@type"] for s in parser.schemas],
            ["Organization", "WebSite", "BlogPosting"],
        )
        url = parser.schemas[-1]["image"][0]
        self.assertTrue(url.startswith("https://quroom.kr/static/"))
        self.assertContains(response, f'src="{url}"')
        self.assertContains(response, f'content="{url}"')
        self.assertContains(response, "posthog.init(")
        self.assertNotContains(response, "googletagmanager")
        self.assertNotContains(response, '<script type="application/ld+json"></script>')
        self.assertTrue(
            (
                settings.REPO_ROOT
                / "landing/static/landing/images/build-notes/deploy.png"
            ).is_file()
        )

    def test_list_has_common_seo_context(self):
        response = self.client.get("/build-notes/")
        parser = SchemaParser()
        parser.feed(response.content.decode())
        self.assertEqual(
            [s["@type"] for s in parser.schemas], ["Organization", "WebSite"]
        )
        self.assertContains(response, 'content="https://quroom.kr/static/')
        self.assertContains(response, "landing/images/build-notes/deploy.png")
        self.assertContains(response, 'loading="lazy"')
        self.assertContains(
            response,
            'alt="바이브코딩 실서버 배포 오류: DNS, Nginx, 정적 파일"',
        )

    def test_article_text_cannot_terminate_schema_script(self):
        self.note.seo_title = '</script><script>alert("test")</script>'
        self.note.save()
        response = self.client.get(f"/build-notes/{self.note.slug}/")
        parser = SchemaParser()
        parser.feed(response.content.decode())
        self.assertEqual(parser.schemas[-1]["headline"], self.note.seo_title)
        self.assertNotContains(response, '<script>alert("test")</script>')
