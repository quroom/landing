from django.test import TestCase

from landing.ax_tool_stack import diagnosis_question_keys
from landing.lead_magnet_sections import (
    normalize_contact_cta_href,
    render_sections_to_text,
    section_contract_signature,
)
from landing.mailers import _build_lead_magnet_user_email
from landing.models import ContactInquiry
from landing.views import _build_lead_magnet_result


class LeadMagnetSectionContractTests(TestCase):
    def _sample_result(self) -> dict:
        keys = diagnosis_question_keys()
        values = [2, 2, 1, 1, 2, 1, 2, 1]
        score_map = {key: values[idx] for idx, key in enumerate(keys)}
        result, _ = _build_lead_magnet_result(score_map)
        return result

    def _perfect_result(self) -> dict:
        keys = diagnosis_question_keys()
        score_map = {key: 2 for key in keys}
        result, _ = _build_lead_magnet_result(score_map)
        return result

    def test_section_contract_signature_is_stable(self) -> None:
        result = self._sample_result()
        signature = section_contract_signature(result["sections"])
        self.assertEqual(
            signature,
            (
                ("summary", "진단 요약"),
                ("weakest_category", "핵심 보완 카테고리"),
                ("one_action", "2주 내 끝낼 작업 1개"),
                ("tools", "주요 추천 툴"),
                (
                    "next_action",
                    "다음 액션/?inquiry_type=ax_diagnosis&lead_context=lead_magnet_diagnosis#contact",
                ),
            ),
        )

    def test_rendered_section_text_snapshot(self) -> None:
        result = self._sample_result()
        self.assertEqual(
            render_sections_to_text(result["sections"]),
            """[진단 요약]
- 점수: 12/16
- 등급: B
- 한 줄 요약: 기본 운영은 가능하지만 반복 업무에서 시간 손실이 큽니다. 2주 동안 핵심 작업 1개 개선을 권장합니다.

[핵심 보완 카테고리]
- 데이터/운영 기반 (B)
  - 데이터는 모이지만 표준화가 약합니다.
  - 1인은 입력 규칙 단순화, 팀은 상태값 통일로 협업 혼선을 줄이세요.

[2주 내 끝낼 작업 1개]
- 작업: 누락/지연 병목 구간 1개를 먼저 특정하기
- 완료 기준: 2주 동안 이 작업 1개를 꼭 완료 기준으로 달성해보세요.
  - 완료 기준 예시: 병목 구간 1개를 지정하고, 시작~종료 단계와 지연 원인 3가지를 문서화.

[주요 추천 툴]
- Trello, Notion, Google Sheets

[다음 액션]
- 생산성 개선 상담 요청 (/?inquiry_type=ax_diagnosis&lead_context=lead_magnet_diagnosis#contact)
- 직접 진행이 어렵다면 상담으로 우선순위부터 함께 정리해드립니다.""",
        )

    def test_email_body_uses_same_section_order(self) -> None:
        result = self._sample_result()
        inquiry = ContactInquiry(
            name="테스트",
            company_name="QuRoom",
            email="test@example.com",
            inquiry_type="lead_magnet_diagnosis",
        )
        _, text_body, _ = _build_lead_magnet_user_email(
            inquiry,
            report_text="dummy",
            result=result,
        )
        headings = [
            "[진단 요약]",
            "[핵심 보완 카테고리]",
            "[2주 내 끝낼 작업 1개]",
            "[주요 추천 툴]",
            "[다음 액션]",
        ]
        positions = [text_body.find(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(
            "(/?inquiry_type=ax_diagnosis&lead_context=lead_magnet_diagnosis#contact)",
            text_body.replace(" ", ""),
        )

    def test_perfect_score_summary_includes_consultation_prompt(self) -> None:
        result = self._perfect_result()
        self.assertEqual(result["score"], result["max_score"])
        self.assertIn("잘 유지하고 있습니다", result["summary"])
        self.assertIn("추가 질의가 있으면 상담을 요청해 주세요", result["summary"])

    def test_contact_cta_normalization_keeps_contact_anchor(self) -> None:
        self.assertEqual(normalize_contact_cta_href("#contact"), "/#contact")
        self.assertEqual(normalize_contact_cta_href("/#contact"), "/#contact")
        self.assertEqual(
            normalize_contact_cta_href("https://example.com/path#contact"),
            "https://example.com/path#contact",
        )
