from django.test import TestCase

from landing.ax_tool_stack import diagnosis_question_keys
from landing.lead_magnet_sections import (
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

    def test_section_contract_signature_is_stable(self) -> None:
        result = self._sample_result()
        signature = section_contract_signature(result["sections"])
        self.assertEqual(
            signature,
            (
                ("summary", "진단 요약"),
                ("weakest_category", "핵심 보완 카테고리"),
                ("one_action", "2주 실행 우선 1개"),
                ("tools", "주요 추천 툴"),
                ("next_action", "다음 액션/#contact"),
            ),
        )

    def test_rendered_section_text_snapshot(self) -> None:
        result = self._sample_result()
        self.assertEqual(
            render_sections_to_text(result["sections"]),
            """[진단 요약]
- 점수: 12/16
- 등급: B
- 한 줄 요약: 핵심 실행은 가능하지만 반복 운영 손실이 누적되는 단계입니다. 1인/팀 모두 2주 집중 개선이 효과적입니다.

[핵심 보완 카테고리]
- 데이터/운영 기반 (B)
  - 데이터는 모이지만 표준화가 약합니다.
  - 1인은 입력 규칙 단순화, 팀은 상태값 통일로 협업 혼선을 줄이세요.

[2주 실행 우선 1개]
- 과제: 누락/지연이 자주 발생하는 병목 구간(응대, 승인, 전달)을 특정해두었다
- 추천 툴: Trello, Notion
- 수행 기준: 2주 동안 이 항목 1개만 완료 기준으로 실행하세요.

[주요 추천 툴]
- Trello, Notion, Google Sheets

[다음 액션]
- 자동화 실행 구축 상담 요청 (/#contact)
- 2~4주 실행체계 구축 상담으로 연결합니다.""",
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
            "[2주 실행 우선 1개]",
            "[주요 추천 툴]",
            "[다음 액션]",
        ]
        positions = [text_body.find(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("( /#contact)".replace(" ", ""), text_body.replace(" ", ""))
