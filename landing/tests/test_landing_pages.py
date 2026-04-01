import json
import tempfile
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from landing.content import CAREER_RANGES, build_career_ranges
from landing.models import (
    AnalyticsExcludedIP,
    ContactInquiry,
    FunnelEvent,
    Testimonial,
    TestimonialInvite,
)


class LandingPageTests(TestCase):
    @override_settings(SITE_BASE_URL="https://quroom.kr")
    def test_home_page_renders_canonical_and_og_url(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<link rel="canonical" href="https://quroom.kr/" />',
            html=False,
        )
        self.assertContains(
            response,
            '<meta property="og:url" content="https://quroom.kr/" />',
            html=False,
        )

    @override_settings(
        SITE_BASE_URL="https://quroom.kr",
        SEARCH_ROBOTS_EXTRA_LINES=["User-agent: Daumoa", "Allow: /"],
    )
    def test_robots_txt_includes_sitemap_and_operator_extra_lines(self) -> None:
        response = self.client.get(reverse("landing:robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(
            response.content.decode("utf-8"),
            "\n".join(
                [
                    "User-agent: *",
                    "Allow: /",
                    "Sitemap: https://quroom.kr/sitemap.xml",
                    "User-agent: Daumoa",
                    "Allow: /",
                    "",
                ]
            ),
        )

    @override_settings(SITE_BASE_URL="https://quroom.kr")
    def test_sitemap_xml_contains_primary_public_routes(self) -> None:
        response = self.client.get(reverse("landing:sitemap_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<loc>https://quroom.kr/</loc>", html=False)
        self.assertContains(
            response,
            "<loc>https://quroom.kr/free-diagnosis/</loc>",
            html=False,
        )
        self.assertContains(
            response,
            "<loc>https://quroom.kr/for-foreign-developers/</loc>",
            html=False,
        )
        self.assertContains(
            response,
            "<loc>https://quroom.kr/privacy/</loc>",
            html=False,
        )
        self.assertContains(response, "<loc>https://quroom.kr/terms/</loc>", html=False)

    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="ko">', html=False)
        self.assertContains(response, "사업을 이해하고")
        self.assertContains(response, "믿고 맡길 수 있는 파트너")
        self.assertContains(
            response,
            "업무 범위와 우선순위를 먼저 맞추고, 필요한 실행은 직접 맡아 진행합니다.",
        )
        self.assertContains(response, "30분 무료 커피챗")
        self.assertContains(response, "제공 서비스")
        self.assertContains(response, "외주용역 집중 트랙")
        self.assertContains(response, "추가로 도와드릴 수 있는 것")
        self.assertContains(response, "문의부터 실행까지 진행 방식")
        self.assertContains(response, "이런 상황이라면 함께하기 좋습니다")
        self.assertContains(response, "이런 팀과 잘 맞습니다")
        self.assertContains(response, "아직 맞지 않을 수 있습니다")
        self.assertContains(
            response,
            "무엇을 먼저 할지, 무엇은 미뤄도 될지 90분 안에 정리합니다.",
        )
        self.assertContains(response, "이런 상황이면 첫 상담이 수월합니다")
        self.assertContains(
            response,
            "범위와 목표가 어느 정도 보이면, 첫 대화에서 무엇부터 할지 더 빠르게 정리할 수 있습니다.",
        )
        self.assertContains(
            response,
            "이런 경험과 기준으로 일합니다",
        )
        self.assertContains(
            response, "외주 집중 트랙은 한 번에 한 고객사만 진행해 집중도를 높입니다"
        )
        self.assertNotContains(response, "OpenClaw")
        self.assertNotContains(response, "바이브코딩")
        self.assertNotContains(response, "안정화 지원")
        service_map = {
            item["id"]: item for item in response.context["content"]["services"]
        }
        self.assertEqual(
            service_map["founder-ax-coffee-chat"]["deliverable"],
            "대화 후 다음 액션 1~2개 정리",
        )
        self.assertEqual(
            service_map["founder-ax-diagnosis"]["deliverable"],
            "진단 요약 문서 + 2주 실행 후보 리스트",
        )
        self.assertEqual(
            service_map["founder-ax-build"]["deliverable"],
            "운영 가능한 자동화 구성 + 자동화 운영 가이드 문서",
        )
        self.assertEqual(
            service_map["founder-outsourcing-track"]["deliverable"],
            "구축 결과물 + 운영 이관 문서 (후속 지원 범위 별도 합의)",
        )
        self.assertContains(response, "공인중개사 자격 취득")
        self.assertContains(response, "중개업 활동, 자동화로 업무 효율화")
        self.assertContains(response, "쉐어하우스 창업 및 확장")
        self.assertEqual(response.context["career_ranges"], CAREER_RANGES)
        body = response.content.decode("utf-8")
        self.assertLess(
            body.index("이런 팀과 잘 맞습니다"),
            body.index("요구사항부터 같이 정리합니다."),
        )
        self.assertLess(
            body.index("30분 무료 커피챗"),
            body.index("문의부터 실행까지 진행 방식"),
        )
        self.assertLess(
            body.index("공인중개사 자격 취득"),
            body.index("중개업 활동, 자동화로 업무 효율화"),
        )
        self.assertLess(
            body.index("중개업 활동, 자동화로 업무 효율화"),
            body.index("쉐어하우스 창업 및 확장"),
        )
        self.assertTrue(
            FunnelEvent.objects.filter(event_name="lp_view", page_key="home").exists()
        )

    def test_home_page_supports_english_override_for_career_timeline(self) -> None:
        response = self.client.get(reverse("landing:index"), {"lang": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">', html=False)
        self.assertContains(response, "Samsung Electronics S/W Engineer")
        self.assertContains(
            response, "Social venture founding and QuRoom development/operations"
        )
        self.assertContains(response, "Present")
        self.assertContains(response, "y ")
        self.assertContains(response, " m")
        self.assertContains(
            response,
            "Understands the business",
        )
        self.assertContains(response, "and is a partner you can trust with the work.")
        self.assertContains(response, "30-min Free Coffee Chat")
        self.assertContains(response, "Services")
        self.assertContains(
            response, "This is the experience and standard I work from."
        )
        self.assertContains(response, "How We Work From Inquiry to Delivery")
        self.assertContains(response, "Good Fit")
        self.assertContains(response, "Not a Fit Yet")
        self.assertEqual(
            response.context["career_ranges"],
            build_career_ranges(locale="en", page_default_locale="ko"),
        )

    def test_free_diagnosis_page_renders(self) -> None:
        response = self.client.get(reverse("landing:free_diagnosis"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 자동화 실행 진단 (3분 / 8문항)")
        self.assertContains(response, "8개 문항 모두 필수 응답입니다.")
        self.assertNotContains(response, "업무 흐름 명확성")
        self.assertNotContains(response, "데이터/운영 기반")

    def test_free_diagnosis_report_preview_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:lead_magnet_report_preview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_free_diagnosis_report_preview_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="preview_staff",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:lead_magnet_report_preview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "무료 진단 결과 메시지 시뮬레이션")
        self.assertContains(response, "16점 만점 시나리오 (정밀)")
        self.assertContains(response, "16/16")
        self.assertContains(response, "핵심 보완 포인트")
        self.assertContains(response, "Intent Coverage")
        preview_reports = response.context["preview_reports"]
        perfect_items = [
            item for item in preview_reports if item.get("is_perfect_preview")
        ]
        self.assertEqual(len(perfect_items), 1)
        self.assertEqual(perfect_items[0]["score"], perfect_items[0]["max_score"])
        one_action_titles = [
            item["one_action"]["title"]
            for item in preview_reports
            if not item.get("is_perfect_preview")
        ]
        self.assertEqual(len(one_action_titles), len(set(one_action_titles)))
        intent_keys = {
            item["one_action"]["intent_key"]
            for item in preview_reports
            if not item.get("is_perfect_preview")
        }
        self.assertTrue(
            all(
                item.get("alignment", {}).get("is_intent_aligned", False)
                for item in preview_reports
            )
        )
        expected_cta_count = sum(
            1 for item in preview_reports if not item.get("is_perfect_preview")
        )
        self.assertEqual(len(intent_keys), 8)
        self.assertContains(response, "2주 내 끝낼 작업 1개")
        self.assertContains(response, "anchor intent:")
        self.assertContains(response, "정밀 진단")
        self.assertNotContains(response, "간단 진단")
        self.assertContains(
            response,
            'href="/?inquiry_type=ax_diagnosis&amp;lead_context=lead_magnet_diagnosis#contact"',
            count=expected_cta_count,
        )
        self.assertNotContains(response, "핵심 보완 카테고리")
        self.assertNotContains(response, "Top 5")
        self.assertNotContains(response, "전체 4개 항목 보기")

    def test_index_applies_recommended_inquiry_type_from_diagnosis_context(
        self,
    ) -> None:
        response = self.client.get(
            reverse("landing:index"),
            {
                "inquiry_type": "ax_diagnosis",
                "lead_context": "lead_magnet_diagnosis",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<option value="ax_diagnosis" selected>자동화 실행 진단</option>',
            html=False,
        )
        self.assertContains(
            response,
            'name="lead_source" value="founder_contact_from_diagnosis"',
            html=False,
        )

    def test_index_defaults_contact_form_to_coffee_chat(self) -> None:
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<option value="coffee_chat" selected>30분 무료 커피챗</option>',
            html=False,
        )

    def test_founders_page_redirects_to_home(self) -> None:
        response = self.client.get(reverse("landing:founders"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("landing:index"))

    def test_foreign_developers_page_renders(self) -> None:
        response = self.client.get(reverse("landing:foreign_developers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">', html=False)
        self.assertContains(response, "For International Talent")
        self.assertContains(response, "Work in Korea with practical support")
        self.assertContains(
            response, "Currently strongest for foreign software engineers."
        )
        self.assertContains(response, "Career Strategy")
        self.assertContains(response, "What Support You Can Get")
        self.assertContains(response, "Send Inquiry")
        self.assertContains(response, "Current Focus or Role")
        self.assertContains(response, "Founder LinkedIn")
        self.assertContains(response, "https://www.linkedin.com/in/samkimtech")
        self.assertContains(response, "Samsung Electronics S/W Engineer")
        self.assertContains(response, "Support Areas")
        self.assertContains(response, "Why QuRoom")
        self.assertContains(response, "Recommended for")
        self.assertNotContains(response, "제공 서비스")
        self.assertNotContains(response, "신뢰 근거")
        body = response.content.decode("utf-8")
        self.assertLess(
            body.index("Samsung Electronics S/W Engineer"),
            body.index("Founder LinkedIn"),
        )
        event = FunnelEvent.objects.get(
            event_name="lp_view", page_key="foreign_developers"
        )
        self.assertEqual(event.metadata["route_variant"], "canonical")

    def test_foreign_developers_page_supports_korean_override(self) -> None:
        response = self.client.get(
            reverse("landing:foreign_developers"), {"lang": "ko"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="ko">', html=False)
        self.assertContains(response, "한국에서 일하려는 외국인 인재를 위한 실무 지원")
        self.assertContains(response, "어떤 지원을 받을 수 있나요")
        self.assertContains(response, "커리어 전략")
        self.assertContains(response, "문의하기")
        self.assertContains(response, "현재 역할 또는 관심 분야")
        self.assertContains(response, "대표자 LinkedIn")
        self.assertContains(response, "삼성전자 S/W 엔지니어")
        body = response.content.decode("utf-8")
        self.assertLess(
            body.index("삼성전자 S/W 엔지니어"),
            body.index("대표자 LinkedIn"),
        )

    def test_foreign_developers_short_alias_renders_same_page(self) -> None:
        response = self.client.get(reverse("landing:foreign_developers_short"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">', html=False)
        self.assertContains(response, "For International Talent")
        event = FunnelEvent.objects.get(
            event_name="lp_view", page_key="foreign_developers"
        )
        self.assertEqual(event.metadata["route_variant"], "short_alias")

    def test_foreign_developers_short_alias_preserves_locale_and_query(self) -> None:
        response = self.client.get(
            reverse("landing:foreign_developers_short"),
            {"lang": "ko", "utm_source": "card"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="ko">', html=False)
        self.assertEqual(response.wsgi_request.GET["utm_source"], "card")
        event = FunnelEvent.objects.get(
            event_name="lp_view", page_key="foreign_developers"
        )
        self.assertEqual(event.metadata["route_variant"], "short_alias")
        self.assertEqual(event.metadata["utm_source"], "card")

    def test_locale_resolution_priority_query_over_session(self) -> None:
        session = self.client.session
        session[settings.LANGUAGE_COOKIE_NAME] = "ko"
        session.save()

        response = self.client.get(
            reverse("landing:foreign_developers"), {"lang": "en"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">', html=False)

    def test_set_language_endpoint_updates_language_session(self) -> None:
        response = self.client.post(
            reverse("set_language"),
            {"language": "en", "next": reverse("landing:index")},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)
        self.assertEqual(
            response.cookies[settings.LANGUAGE_COOKIE_NAME].value,
            "en",
        )

    def test_language_switcher_does_not_use_top_right_overlay_on_shared_pages(
        self,
    ) -> None:
        targets = [
            reverse("landing:index"),
            reverse("landing:foreign_developers"),
            reverse("landing:free_diagnosis"),
        ]
        for target in targets:
            with self.subTest(target=target):
                response = self.client.get(target)
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    "fixed bottom-4 right-4 z-30 flex items-center gap-1",
                    html=False,
                )
                self.assertNotContains(
                    response,
                    "fixed right-4 top-4 z-50",
                    html=False,
                )

    def test_policy_pages_render(self) -> None:
        privacy = self.client.get(reverse("landing:privacy"))
        terms = self.client.get(reverse("landing:terms"))
        self.assertEqual(privacy.status_code, 200)
        self.assertEqual(terms.status_code, 200)

    def test_healthz_returns_ok(self) -> None:
        response = self.client.get(reverse("landing:healthz"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn(payload.get("status"), {"ok", "degraded"})
        self.assertEqual(payload.get("liveness"), "ok")
        self.assertIn(payload.get("readiness"), {"ok", "failed"})

    def test_healthz_live_and_ready_return_ok(self) -> None:
        live = self.client.get(reverse("landing:healthz_live"))
        ready = self.client.get(reverse("landing:healthz_ready"))
        self.assertEqual(live.status_code, 200)
        self.assertEqual(live.json().get("check"), "liveness")
        self.assertIn(ready.status_code, {200, 503})
        self.assertEqual(ready.json().get("check"), "readiness")

    @override_settings(
        DEBUG=False,
        SECRET_KEY="dev-only-change-me",
        ALLOWED_HOSTS=["*"],
        CSRF_TRUSTED_ORIGINS=[],
        EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
    )
    def test_healthz_ready_returns_503_when_runtime_contract_fails(self) -> None:
        response = self.client.get(reverse("landing:healthz_ready"))
        self.assertEqual(response.status_code, 503)

    def test_admin_dashboard_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_operation_links_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_operation_links"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_review_guide_requires_staff(self) -> None:
        response = self.client.get(reverse("landing:admin_review_guide"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_operation_links_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_operation_links",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_operation_links"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "운영 링크 모음")
        self.assertContains(response, reverse("landing:healthz"))
        self.assertContains(response, reverse("landing:healthz_live"))
        self.assertContains(response, reverse("landing:healthz_ready"))
        self.assertContains(response, reverse("landing:admin_dashboard"))
        self.assertContains(response, reverse("landing:admin_review_guide"))
        self.assertContains(response, "최근 Deploy Check")
        self.assertContains(response, "최근 Smoke Check")
        self.assertContains(response, "./scripts/deploy-check.sh")
        self.assertContains(response, "./scripts/post-deploy-smoke.sh")
        self.assertContains(response, "운영 이관 문서 템플릿")
        self.assertContains(response, "카드별 목차")
        self.assertContains(response, "#handover-outsourcing")
        self.assertContains(
            response, "구축 결과물 + 운영 이관 문서 (후속 지원 범위 별도 합의)"
        )

    def test_admin_review_guide_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_review_guide",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_review_guide"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "리뷰 요청 운영 가이드")
        self.assertContains(response, "Testimonial invites")
        self.assertContains(response, "https://quroom.kr/testimonials/invite/")
        self.assertContains(response, "링크 생성")
        self.assertContains(response, "최근 초대 링크")
        self.assertContains(response, "승인 대기 리뷰")

    def test_admin_review_guide_post_creates_invite_and_shows_lists(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_review_guide_post",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        pending_invite = TestimonialInvite.issue(
            target_note="기존 링크",
            expires_in_days=7,
        )
        Testimonial.objects.create(
            invite=pending_invite,
            name="홍길동",
            role_title="대표",
            company_name="큐룸",
            content="리뷰 내용",
            consent_public=True,
            status=Testimonial.Status.PENDING,
        )

        response = self.client.post(
            reverse("landing:admin_review_guide"),
            {"target_note": "신규 상담", "expiry_days": "10"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "리뷰 요청 링크가 생성되었습니다.")
        self.assertContains(response, "신규 상담")
        self.assertContains(response, "홍길동")
        self.assertContains(response, "Pending")
        self.assertContains(response, "/testimonials/invite/")
        self.assertEqual(
            TestimonialInvite.objects.filter(target_note="신규 상담").count(), 1
        )

    def test_admin_operation_links_shows_latest_check_summary_from_status_file(
        self,
    ) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_operation_summary",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        with tempfile.NamedTemporaryFile("w+", suffix=".json") as fp:
            json.dump(
                [
                    {
                        "timestamp": "2026-03-05T00:00:00+00:00",
                        "check_type": "deploy_check",
                        "status": "passed",
                        "items": [],
                    },
                    {
                        "timestamp": "2026-03-05T00:01:00+00:00",
                        "check_type": "smoke_check",
                        "status": "failed",
                        "items": [],
                        "failed_items": ["/healthz/ready/"],
                    },
                ],
                fp,
                ensure_ascii=False,
            )
            fp.flush()
            with patch.dict("os.environ", {"DEPLOY_STATUS_FILE": fp.name}, clear=False):
                response = self.client.get(reverse("landing:admin_operation_links"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "passed")
        self.assertContains(response, "failed")
        self.assertContains(response, "/healthz/ready/")

    def test_admin_index_shows_operation_link_next_to_dashboard(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_admin_index",
            password="pass1234",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의 대시보드")
        self.assertContains(response, "운영 링크")

    def test_admin_dashboard_renders_for_staff(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff",
            password="pass1234",
            is_staff=True,
        )
        ContactInquiry.objects.create(
            name="대시보드 테스트",
            email="dashboard@example.com",
            inquiry_type="development",
            message="문의",
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "문의 운영 대시보드")
        self.assertContains(response, "리드마그넷 퍼널 (간단 확인)")
        self.assertContains(response, "대시보드 테스트")
        self.assertContains(response, "유입 제외 IP 관리")

    def test_admin_dashboard_shows_current_client_ip(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_ip",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("landing:admin_dashboard"),
            REMOTE_ADDR="203.0.113.50",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "현재 접속 IP")
        self.assertContains(response, "203.0.113.50")

    def test_admin_dashboard_shows_cf_connecting_ip_when_proxy_is_trusted(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_cf_ip",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("landing:admin_dashboard"),
            REMOTE_ADDR="10.0.0.1",
            HTTP_X_FORWARDED_FOR="173.245.48.7",
            HTTP_CF_CONNECTING_IP="198.51.100.44",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "현재 접속 IP")
        self.assertContains(response, "198.51.100.44")

    def test_admin_dashboard_can_add_excluded_ip(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_ip_add",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("landing:admin_dashboard"),
            {
                "action": "exclude_ip_add",
                "ip_address": "198.51.100.77",
                "note": "personal office ip",
            },
            REMOTE_ADDR="198.51.100.77",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "제외 IP로 추가했습니다.")
        self.assertTrue(
            AnalyticsExcludedIP.objects.filter(
                ip_address="198.51.100.77",
                is_active=True,
            ).exists()
        )

    def test_admin_dashboard_can_deactivate_excluded_ip(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff_ip_disable",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)
        AnalyticsExcludedIP.objects.create(
            ip_address="198.51.100.90",
            note="temp",
            is_active=True,
        )

        response = self.client.post(
            reverse("landing:admin_dashboard"),
            {
                "action": "exclude_ip_deactivate",
                "ip_address": "198.51.100.90",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "비활성화했습니다.")
        self.assertTrue(
            AnalyticsExcludedIP.objects.filter(
                ip_address="198.51.100.90",
                is_active=False,
            ).exists()
        )

    def test_admin_dashboard_filters_by_date_range(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff2",
            password="pass1234",
            is_staff=True,
        )
        old_inquiry = ContactInquiry.objects.create(
            name="오래된 문의",
            email="old@example.com",
            inquiry_type="development",
            message="old",
        )
        ContactInquiry.objects.filter(id=old_inquiry.id).update(
            created_at=timezone.now() - timedelta(days=10)
        )
        ContactInquiry.objects.create(
            name="오늘 문의",
            email="today@example.com",
            inquiry_type="development",
            message="today",
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("landing:admin_dashboard"), {"range": "today"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "오늘 문의")
        self.assertNotContains(response, "오래된 문의")

    def test_admin_dashboard_filters_by_inquiry_type(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff5",
            password="pass1234",
            is_staff=True,
        )
        ContactInquiry.objects.create(
            name="리드마그넷 문의",
            email="lead-type@example.com",
            inquiry_type="lead_magnet_diagnosis",
            message="lead",
        )
        ContactInquiry.objects.create(
            name="일반 문의",
            email="normal-type@example.com",
            inquiry_type="development",
            message="normal",
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("landing:admin_dashboard"), {"type": "lead_magnet_diagnosis"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "리드마그넷 문의")
        self.assertNotContains(response, "일반 문의")

    def test_admin_dashboard_uses_user_mail_event_for_conversion_rate(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff6",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        FunnelEvent.objects.create(
            event_name="lead_magnet_start",
            page_key="home",
            lead_source="founder_lead_magnet",
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_submit_user",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent_user",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B", "lead_context": "lead_magnet_diagnosis"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent_admin",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"lead_context": "lead_magnet_diagnosis"},
        )

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "메일 발송 성공 (사용자)")
        self.assertContains(response, "관리자 알림: 1")
        self.assertContains(response, "성공률 100.0%")

    def test_admin_dashboard_falls_back_to_legacy_mail_event(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff7",
            password="pass1234",
            is_staff=True,
        )
        self.client.force_login(staff)

        FunnelEvent.objects.create(
            event_name="lead_magnet_start",
            page_key="home",
            lead_source="founder_lead_magnet",
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_submit",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )
        FunnelEvent.objects.create(
            event_name="lead_magnet_email_sent",
            page_key="home",
            lead_source="founder_lead_magnet",
            metadata={"grade": "B"},
        )

        response = self.client.get(reverse("landing:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "legacy 이벤트 기준으로 임시 집계 중")
        self.assertContains(response, "제출은 legacy 이벤트 기준으로 임시 집계 중")
        self.assertContains(response, "성공률 100.0%")

    def test_admin_resend_inquiry_updates_status(self) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff3",
            password="pass1234",
            is_staff=True,
        )
        inquiry = ContactInquiry.objects.create(
            name="재전송 대상",
            email="retry@example.com",
            inquiry_type="development",
            message="retry",
            email_delivery_status=ContactInquiry.DeliveryStatus.FAILED,
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("landing:admin_resend_inquiry", kwargs={"inquiry_id": inquiry.id})
        )
        self.assertEqual(response.status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(
            inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.SUCCESS
        )

    @patch("landing.mailers.send_mail", side_effect=RuntimeError("smtp failed"))
    def test_admin_resend_inquiry_keeps_failed_on_send_error(
        self, _send_mail: object
    ) -> None:
        user_model = get_user_model()
        staff = user_model.objects.create_user(
            username="staff4",
            password="pass1234",
            is_staff=True,
        )
        inquiry = ContactInquiry.objects.create(
            name="재전송 실패",
            email="retry-fail@example.com",
            inquiry_type="development",
            message="retry fail",
            email_delivery_status=ContactInquiry.DeliveryStatus.FAILED,
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("landing:admin_resend_inquiry", kwargs={"inquiry_id": inquiry.id})
        )
        self.assertEqual(response.status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(
            inquiry.email_delivery_status, ContactInquiry.DeliveryStatus.FAILED
        )
        self.assertIn("smtp failed", inquiry.email_error)
