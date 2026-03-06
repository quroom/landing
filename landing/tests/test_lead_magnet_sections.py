from django.test import TestCase

from landing.ax_tool_stack import diagnosis_question_keys
from landing.lead_magnet_sections import (
    normalize_contact_cta_href,
    render_sections_to_text,
    section_contract_signature,
)
from landing.mailers import _build_lead_magnet_user_email
from landing.models import ContactInquiry
from landing.views import _build_lead_magnet_result, _intent_pattern_coverage


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
                ("weakest", "핵심 보완 포인트"),
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
- 진단 유형: 정밀 진단 (8문항)
- 한 줄 요약: 기본 운영은 가능하지만 반복 업무에서 시간 손실이 큽니다. 2주 동안 핵심 작업 1개 개선을 권장합니다.

[핵심 보완 포인트]
- 병목 구간 식별 (B)
  - 누락/지연 구간은 보이지만 원인 기준이 아직 느슨합니다.
  - 병목 구간 1개와 지연 원인 3가지를 먼저 고정해 실행 순서를 명확히 하세요.

[2주 내 끝낼 작업 1개]
- 작업: 누락/지연이 자주 나는 병목 구간 1개를 먼저 특정하기
- 완료 기준: 병목 구간 1개와 지연 원인 3가지를 문서로 정리하면 완료입니다.

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
            "[핵심 보완 포인트]",
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

    def test_detailed_result_uses_eight_question_coverage(self) -> None:
        result = self._sample_result()
        self.assertEqual(result["coverage_mode"], "detailed")
        self.assertEqual(result["coverage_label"], "정밀 진단 (8문항)")
        self.assertEqual(result["max_score"], 16)

    def test_one_action_matches_weakest_anchor_question(self) -> None:
        result = self._sample_result()
        weakest = result["weakest_insight"]
        one_action = result["one_action"]
        self.assertEqual(one_action["question_key"], weakest["anchor_question_key"])
        self.assertEqual(one_action["intent_key"], weakest["intent_key"])

    def test_response_pattern_uses_one_action_intent(self) -> None:
        result = self._sample_result()
        response_pattern = result["response_pattern"]
        self.assertTrue(response_pattern["id"])
        self.assertEqual(
            response_pattern["primary_intent"], result["one_action"]["intent_key"]
        )

    def test_result_contract_includes_intent_alignment_metadata(self) -> None:
        result = self._sample_result()
        alignment = result["intent_alignment"]
        self.assertEqual(
            alignment["anchor_intent_key"],
            result["one_action"]["intent_key"],
        )
        self.assertEqual(
            alignment["anchor_intent_key"],
            result["weakest_insight"]["intent_key"],
        )
        self.assertTrue(alignment["is_intent_aligned"])

    def test_intent_coverage_metadata_is_valid(self) -> None:
        coverage = _intent_pattern_coverage()
        self.assertTrue(coverage["is_pattern_count_valid"])
        self.assertTrue(coverage["is_covered"])

    def test_contact_cta_normalization_keeps_contact_anchor(self) -> None:
        self.assertEqual(normalize_contact_cta_href("#contact"), "/#contact")
        self.assertEqual(normalize_contact_cta_href("/#contact"), "/#contact")
        self.assertEqual(
            normalize_contact_cta_href("https://example.com/path#contact"),
            "https://example.com/path#contact",
        )
