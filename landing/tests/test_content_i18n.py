from django.test import TestCase

from landing.content import _localize_value, build_page_content


class ContentI18nTests(TestCase):
    def test_foreign_developer_content_defaults_to_english(self) -> None:
        content = build_page_content(
            "foreign_developers",
            locale="en",
            page_default_locale="en",
        )
        self.assertEqual(
            content["persona"]["title"],
            "Get a Korea Job Strategy Tailored to Your Stage",
        )

    def test_localize_value_falls_back_to_page_default_locale(self) -> None:
        localized = _localize_value(
            {"headline": {"ko": "기본값 제목"}},
            "en",
            "ko",
            key_path="content",
        )
        self.assertEqual(localized["headline"], "기본값 제목")

    def test_localize_value_logs_warning_and_returns_empty_when_missing(self) -> None:
        with self.assertLogs("landing.content", level="WARNING") as captured:
            localized = _localize_value(
                {"headline": {"en": "English only"}},
                "ko",
                "ko",
                key_path="content",
            )
        self.assertEqual(localized["headline"], "")
        self.assertTrue(
            any("Missing localized copy" in message for message in captured.output)
        )
