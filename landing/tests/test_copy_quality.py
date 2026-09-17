from unittest.mock import patch

from django.test import SimpleTestCase

from landing.content import SHARED_CONTENT, build_gwangju_page_content
from scripts.lint_korean_slop import RULES


class CopyQualityTests(SimpleTestCase):
    def test_quote_uses_current_company_registration(self):
        with patch.dict(SHARED_CONTENT["company"], biz_number="123-45-67890"):
            content = build_gwangju_page_content("outsourcing_checklist")
        self.assertIn(
            "사업자등록번호: 123-45-67890", content["quote_template_markdown"]
        )
        self.assertNotIn("{company_biz_number}", content["quote_template_markdown"])

    def test_linter_catches_reviewed_copy_regressions(self):
        for copy in [
            "일정을 확정합니다",
            "정리 안 돼도 괜찮습니다",
            "정하지 않았어도 괜찮습니다",
            "10년 이상",
            "10년 차",
            "외주 분쟁의 80%",
            "분쟁의 대부분",
            "분쟁의 상당수",
            "완벽한 개발",
            "보완이나 반려 없이 정산",
        ]:
            with self.subTest(copy=copy):
                self.assertTrue(any(rule.pattern.search(copy) for rule in RULES))

    def test_linter_allows_factual_and_collaborative_copy(self):
        for copy in [
            "8년 차 풀스택 개발사",
            "삼성전자 포함 총 개발 경력 10년 5개월",
            "사업 목표와 개발 우선순위를 함께 논의합니다.",
            "완성된 기획서나 기능 명세서가 없어도 좋습니다.",
        ]:
            with self.subTest(copy=copy):
                self.assertFalse(any(rule.pattern.search(copy) for rule in RULES))
