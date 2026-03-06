from django.test import SimpleTestCase

from landing.views import _group_preview_reports, _intent_pattern_coverage


class PreviewReportGroupingTests(SimpleTestCase):
    def _preview_item(
        self,
        *,
        title: str,
        score: int = 6,
        max_score: int = 16,
        grade: str = "B",
        coverage_label: str = "정밀 진단 (8문항)",
        execution: str = "담당자·기한·검증 기준을 문서에 남기고 실제로 1회 실행하면 완료입니다.",
        intent_key: str = "document_workflow",
        is_intent_aligned: bool = True,
    ) -> dict:
        return {
            "title": title,
            "score": score,
            "max_score": max_score,
            "grade": grade,
            "coverage_label": coverage_label,
            "cta": {"label": "생산성 개선 상담 요청"},
            "cta_url": "/#contact",
            "one_action": {
                "title": "핵심 업무 1개 문서화",
                "execution": execution,
                "intent_key": intent_key,
            },
            "weakest_insight": {
                "label": "업무 흐름 명확성",
                "grade": "B",
                "grade_visible": True,
                "message_primary": "업무 흐름은 있으나 단계 기준이 아직 느슨합니다.",
                "message_secondary": "시작-처리-완료 기준을 한 페이지로 고정하면 실행 편차를 줄일 수 있습니다.",
                "intent_key": intent_key,
            },
            "alignment": {
                "anchor_intent_key": intent_key,
                "is_intent_aligned": is_intent_aligned,
            },
            "report": "샘플 리포트",
        }

    def test_groups_reports_when_only_title_differs(self) -> None:
        grouped = _group_preview_reports(
            [
                self._preview_item(title="B 등급 · 정밀"),
                self._preview_item(title="B 등급 · 정밀(변형)"),
            ]
        )
        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["scenario_count"], 2)
        self.assertEqual(
            grouped[0]["scenario_titles"],
            ["B 등급 · 정밀", "B 등급 · 정밀(변형)"],
        )

    def test_groups_reports_when_score_and_grade_differ_but_guidance_same(self) -> None:
        grouped = _group_preview_reports(
            [
                self._preview_item(
                    title="A 등급 · 정밀",
                    score=14,
                    max_score=16,
                    grade="A",
                    coverage_label="정밀 진단 (8문항)",
                ),
                self._preview_item(
                    title="C 등급 · 정밀",
                    score=4,
                    max_score=16,
                    grade="C",
                    coverage_label="정밀 진단 (8문항)",
                ),
            ]
        )
        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["scenario_count"], 2)
        self.assertEqual(
            grouped[0]["scenario_titles"],
            ["A 등급 · 정밀", "C 등급 · 정밀"],
        )

    def test_does_not_group_reports_when_intent_alignment_differs(self) -> None:
        first = self._preview_item(title="시나리오 1")
        second = self._preview_item(
            title="시나리오 2", intent_key="identify_bottleneck"
        )
        second["weakest_insight"] = {
            "label": "데이터/운영 기반",
            "grade": "B",
            "grade_visible": True,
            "message_primary": "데이터는 모이지만 기준 통일이 부족합니다.",
            "message_secondary": "필수 입력값과 상태값을 먼저 고정하면 누락/혼선을 줄일 수 있습니다.",
            "intent_key": "identify_bottleneck",
        }
        second["alignment"] = {
            "anchor_intent_key": "identify_bottleneck",
            "is_intent_aligned": True,
        }

        grouped = _group_preview_reports([first, second])

        self.assertEqual(len(grouped), 2)

    def test_does_not_group_reports_when_body_differs(self) -> None:
        grouped = _group_preview_reports(
            [
                self._preview_item(title="B 등급 · 정밀"),
                self._preview_item(
                    title="B 등급 · 정밀(변형)",
                    execution="병목 구간 1개와 지연 원인 3가지를 문서로 정리하면 완료입니다.",
                ),
            ]
        )
        self.assertEqual(len(grouped), 2)

    def test_does_not_group_perfect_preview_with_non_perfect(self) -> None:
        first = self._preview_item(title="16점 만점")
        first["is_perfect_preview"] = True
        second = self._preview_item(title="일반 시나리오")
        second["is_perfect_preview"] = False

        grouped = _group_preview_reports([first, second])

        self.assertEqual(len(grouped), 2)

    def test_grouped_reports_include_representative_intent_metadata(self) -> None:
        grouped = _group_preview_reports(
            [
                self._preview_item(title="시나리오 1", intent_key="document_workflow"),
                self._preview_item(title="시나리오 2", intent_key="document_workflow"),
            ]
        )
        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["representative_intent_key"], "document_workflow")
        self.assertEqual(grouped[0]["intent_keys"], ["document_workflow"])

    def test_intent_pattern_catalog_covers_all_intents(self) -> None:
        coverage = _intent_pattern_coverage()
        self.assertTrue(coverage["is_pattern_count_valid"])
        self.assertTrue(coverage["is_covered"])
        self.assertEqual(coverage["missing_patterns"], [])
        self.assertEqual(coverage["missing_tools"], [])
