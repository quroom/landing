from __future__ import annotations

from dataclasses import dataclass, replace

from django.http import HttpRequest

AD_PARAM_KEYS = ("src", "campaign", "group", "intent", "creative", "kw")


@dataclass(frozen=True)
class AdLandingVariant:
    landing_variant: str
    campaign: str
    ad_group: str
    intent: str
    headline: str
    subcopy: str
    primary_cta: str
    secondary_cta: str
    inquiry_type: str
    eyebrow: str = ""


VARIANTS: dict[str, AdLandingVariant] = {
    "app_general": AdLandingVariant(
        landing_variant="app_general",
        campaign="app_dev",
        ad_group="app_general",
        intent="general",
        headline="앱 아이디어를 실제 구현 가능한 제품 범위와 견적으로 구체화합니다.",
        subcopy="MVP 필수 스펙, 기술 스택, 개발 일정 산정까지 8년 차 개발사가 직접 검토합니다.",
        primary_cta="앱 개발 범위 상담하기",
        secondary_cta="30분 스펙 진단",
        inquiry_type="outsourcing",
    ),
    "app_cost": AdLandingVariant(
        landing_variant="app_cost",
        campaign="app_dev",
        ad_group="app_cost",
        intent="cost",
        headline="앱 개발 비용이 커지기 전에 핵심 기능부터 먼저 압축하세요.",
        subcopy="필수 기능 목록과 2차 백로그를 구분하여 현실적인 일정과 개발 비용을 도출합니다.",
        primary_cta="앱 견적 상담하기",
        secondary_cta="비용 범위 먼저 보기",
        inquiry_type="outsourcing",
    ),
    "app_outsource": AdLandingVariant(
        landing_variant="app_outsource",
        campaign="app_dev",
        ad_group="app_outsource",
        intent="company_outsource",
        headline="외주 개발 착수 전, 개발 범위와 완료 기준부터 명확히 세웁니다.",
        subcopy="외주 개발에서 분쟁이 생기기 쉬운 스펙, 마일스톤 일정, 소스코드 이관 기준을 첫 상담에서 함께 논의합니다.",
        primary_cta="외주 개발 상담하기",
        secondary_cta="외주 범위 점검하기",
        inquiry_type="outsourcing",
    ),
    "app_industry": AdLandingVariant(
        landing_variant="app_industry",
        campaign="app_dev",
        ad_group="app_industry",
        intent="industry",
        headline="업종별 비즈니스 특성에 맞는 앱 스펙과 운영 구조를 설계합니다.",
        subcopy="예약, 병원, 쇼핑몰, 커뮤니티, 업무관리 앱처럼 실제 운영 기준이 중요한 기능을 체계적으로 도출합니다.",
        primary_cta="업종형 앱 상담하기",
        secondary_cta="기능 우선순위 검토",
        inquiry_type="outsourcing",
    ),
    "homepage_general": AdLandingVariant(
        landing_variant="homepage_general",
        campaign="homepage",
        ad_group="homepage_general",
        intent="general",
        headline="사업을 명확히 설명하고 문의로 이어지는 기업 홈페이지를 구축합니다.",
        subcopy="회사 소개, 서비스 핵심 가치, 실적 포트폴리오, 문의 전환 동선을 목적에 맞게 설계합니다.",
        primary_cta="홈페이지 제작 상담하기",
        secondary_cta="제작 스펙 점검",
        inquiry_type="infra_setup",
    ),
    "homepage_cost": AdLandingVariant(
        landing_variant="homepage_cost",
        campaign="homepage",
        ad_group="homepage_cost",
        intent="cost",
        headline="홈페이지 제작 비용은 불필요한 페이지를 덜어내야 절감할 수 있습니다.",
        subcopy="페이지 수, 콘텐츠 준비 상태, 문의 흐름, 운영 방식 기준으로 현실적인 견적 범위를 잡습니다.",
        primary_cta="홈페이지 견적 상담하기",
        secondary_cta="적정 비용 산정",
        inquiry_type="infra_setup",
    ),
    "landing_page": AdLandingVariant(
        landing_variant="landing_page",
        campaign="landing_page",
        ad_group="landing_page",
        intent="conversion",
        headline="광고 유입을 문의로 연결하는 랜딩페이지를 설계합니다.",
        subcopy="검색 의도, CTA, 문의 폼, 전환 추적까지 광고 집행 기준에 맞춰 구성합니다.",
        primary_cta="랜딩페이지 상담하기",
        secondary_cta="전환 흐름 점검",
        inquiry_type="infra_setup",
    ),
    "detail_page": AdLandingVariant(
        landing_variant="detail_page",
        campaign="detail_page",
        ad_group="detail_page",
        intent="detail_page",
        headline="상품의 핵심 강점이 구매 전환으로 이어지도록 상세페이지를 기획합니다.",
        subcopy="상품 구조, 고객 질문, 구매 장벽, 이미지와 문구 흐름을 함께 설계합니다.",
        primary_cta="상세페이지 상담하기",
        secondary_cta="상품 흐름 점검",
        inquiry_type="infra_setup",
    ),
    "shop_build": AdLandingVariant(
        landing_variant="shop_build",
        campaign="shop",
        ad_group="shop_build",
        intent="shop_build",
        headline="판매 흐름과 운영 기준에 맞는 쇼핑몰을 구축합니다.",
        subcopy="상품 등록, PG 결제, 배송/CS, 운영 이관까지 실제 판매에 직결되는 기능부터 먼저 완성합니다.",
        primary_cta="쇼핑몰 제작 상담하기",
        secondary_cta="판매 동선 점검",
        inquiry_type="infra_setup",
    ),
    "maintenance": AdLandingVariant(
        landing_variant="maintenance",
        campaign="maintenance",
        ad_group="maintenance",
        intent="maintenance",
        headline="이미 구축된 웹·앱의 코드 결함과 개선 우선순위를 진단합니다.",
        subcopy="오류 수정, 성능 개선, 기능 추가, 운영 이관 기준을 현재 시스템 상태에 맞춰 단계별로 수립합니다.",
        primary_cta="유지보수 상담하기",
        secondary_cta="개선 범위 점검",
        inquiry_type="outsourcing",
    ),
    "vibe_coding": AdLandingVariant(
        landing_variant="vibe_coding",
        campaign="maintenance",
        ad_group="app_maintenance",
        intent="vibe_sos",
        headline="Codex·Claude로 만든 서비스,\n실서버 배포에서 막히셨나요?",
        subcopy="현재 동작 상태와 배포 오류를 살펴보고 필요한 작업 범위와 진행 가능 여부를 안내합니다. 작업 일정과 비용은 확인 후 협의합니다.",
        primary_cta="기술 진단 신청",
        secondary_cta="해결 사례 및 포트폴리오",
        inquiry_type="vibe_diagnosis",
        eyebrow="바이브코딩 배포 긴급 진단",
    ),
    "gov_token": AdLandingVariant(
        landing_variant="gov_token",
        campaign="app_dev",
        ad_group="app_outsource",
        intent="gov_grant",
        headline="예창패·초창패 AI API 결제,\ne나라도움 정산 반려를 사전에 예방하세요.",
        subcopy="국내 전자세금계산서 정식 발행부터 비교견적서 2부, 과업 검수조서까지 5종 서류 패키지를 완비해 드립니다.",
        primary_cta="e나라도움 정산 5종 샘플 및 상담",
        secondary_cta="정산 지침 가이드 확인",
        inquiry_type="gov_grant",
        eyebrow="정부지원사업 AI 정산 지원",
    ),
}

CREATIVE_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    ("app_cost", "scope_first"): {
        "headline": "앱 개발 비용은 기능 범위부터 줄여야 현실적으로 잡힙니다.",
        "subcopy": "1차 출시 핵심 기능과 차기 개선 항목을 명확히 구분하여 불필요한 개발비가 커지기 전에 현실적인 범위를 함께 논의합니다.",
        "primary_cta": "앱 비용 범위 상담하기",
        "secondary_cta": "기능 스펙 먼저 검토",
    },
    ("app_cost", "mvp_quote"): {
        "headline": "MVP 앱 견적은 처음 만들 기능을 어디까지 줄이느냐에서 결정됩니다.",
        "subcopy": "런칭에 꼭 필요한 핵심 기능과 검증 후 확장할 기능을 체계적으로 구분해 현실적인 1차 견적을 도출합니다.",
        "primary_cta": "MVP 견적 상담하기",
        "secondary_cta": "1차 기능 검토",
    },
    ("app_cost_2", "scope_first"): {
        "headline": "앱 개발 비용은 기능 범위부터 줄여야 현실적으로 잡힙니다.",
        "subcopy": "1차 출시 핵심 기능과 차기 개선 항목을 명확히 구분하여 불필요한 개발비가 커지기 전에 현실적인 범위를 함께 논의합니다.",
        "primary_cta": "앱 비용 범위 상담하기",
        "secondary_cta": "기능 스펙 먼저 검토",
    },
    ("app_outsource", "outsourcing_risk"): {
        "headline": "앱 외주는 개발 시작 전에 완료 기준부터 맞춰야 합니다.",
        "subcopy": "기능 범위, 일정, 산출물, 운영 이관 기준을 사전에 함께 조율해 외주 리스크를 줄입니다.",
        "primary_cta": "앱 외주 범위 상담하기",
        "secondary_cta": "완료 기준 점검",
    },
    ("homepage_cost", "cost_range"): {
        "headline": "홈페이지 제작 견적은 페이지 수보다 목적과 문의 흐름이 먼저입니다.",
        "subcopy": "필요한 페이지, 콘텐츠 준비 상태, 문의 동선, 운영 방식 기준으로 비용 범위를 현실적으로 잡습니다.",
        "primary_cta": "홈페이지 견적 상담하기",
        "secondary_cta": "필요 페이지 검토",
    },
    ("homepage_general", "first_scope"): {
        "headline": "B2B 홈페이지 제작은 사업 목적과 문의 흐름부터 잡아야 합니다.",
        "subcopy": "기획, 개발, 배포까지 대표 엔지니어가 직접 전담하여 구현 범위와 운영 기준을 일관되게 구축합니다.",
        "primary_cta": "홈페이지 제작 상담하기",
        "secondary_cta": "제작 범위 검토",
    },
    ("homepage_general", "local_gwangju"): {
        "headline": "광주권 홈페이지 제작은 지역 사업 이해와 실행 속도가 중요합니다.",
        "subcopy": "광주 현장을 직접 방문하여 대표 엔지니어가 기획부터 개발, 실서버 배포까지 책임지고 완수합니다.",
        "primary_cta": "광주 홈페이지 상담하기",
        "secondary_cta": "광주 제작 스펙 검토",
    },
    ("homepage_outsource", "outsourcing_risk"): {
        "headline": "홈페이지 외주는 디자인보다 운영 이관 기준까지 먼저 봐야 합니다.",
        "subcopy": "디자인, 개발, 콘텐츠 준비, 배포와 수정 기준을 상담에서 분리해 외주 범위를 명확히 합니다.",
        "primary_cta": "홈페이지 외주 상담하기",
        "secondary_cta": "외주 범위 점검",
    },
    ("landing_page", "conversion_flow"): {
        "headline": "랜딩페이지는 예쁘게 만드는 것보다 문의 전환 흐름이 먼저입니다.",
        "subcopy": "검색 의도, 첫 문구, CTA, 문의 폼, 전환 추적까지 광고 집행 기준에 맞춰 설계합니다.",
        "primary_cta": "랜딩페이지 상담하기",
        "secondary_cta": "전환 흐름 점검",
    },
    ("detail_page", "product_flow"): {
        "headline": "상세페이지는 고객 질문과 구매 이탈 요소를 먼저 분석해야 합니다.",
        "subcopy": "상품 강점, 고객 우려, 비주얼 흐름, 결제 동선을 설득력 있는 페이지 구조로 설계합니다.",
        "primary_cta": "상세페이지 상담하기",
        "secondary_cta": "구매 흐름 점검",
    },
    ("shop_build", "sales_flow"): {
        "headline": "쇼핑몰 제작은 판매 이후 운영 흐름까지 같이 잡아야 합니다.",
        "subcopy": "상품 등록, PG 결제, 문의, 운영 이관까지 실제 판매에 필요한 범위를 첫 상담에서 함께 논의합니다.",
        "primary_cta": "쇼핑몰 제작 상담하기",
        "secondary_cta": "판매 운영 범위 검토",
    },
    ("app_maintenance", "maintenance_scope"): {
        "headline": "앱 유지보수는 긴급 장애 대응과 기능 개선의 우선순위부터 분류합니다.",
        "subcopy": "현재 상태를 진단하여 긴급 오류 수정, 릴리즈 안정화, 기능 개선, 리뉴얼 범위를 체계화합니다.",
        "primary_cta": "앱 유지보수 상담하기",
        "secondary_cta": "수정 우선순위 진단",
    },
    ("homepage_maintenance", "maintenance_scope"): {
        "headline": "홈페이지 유지보수는 수정 범위와 운영 관리를 먼저 명확히 구분해야 합니다.",
        "subcopy": "오류 수정, 콘텐츠 변경, 속도 개선, 운영 관리를 현재 사이트 상태 기준으로 명확히 구분합니다.",
        "primary_cta": "홈페이지 유지보수 상담하기",
        "secondary_cta": "수정 범위 점검",
    },
    ("maintenance", "maintenance_scope"): {
        "headline": "웹앱 유지보수는 긴급 결함 조치와 중장기 기능 개선을 먼저 구분합니다.",
        "subcopy": "현재 상태를 진단하여 긴급 오류 수정, 기능 개선, 리뉴얼, 운영 이관 범위를 단계별로 수립합니다.",
        "primary_cta": "웹앱 유지보수 상담하기",
        "secondary_cta": "개선 범위 점검",
    },
}

GROUP_TO_VARIANT = {
    "app_general": "app_general",
    "app_cost": "app_cost",
    "app_cost_2": "app_cost",
    "app_outsource": "app_outsource",
    "app_industry": "app_industry",
    "homepage_general": "homepage_general",
    "homepage_cost": "homepage_cost",
    "homepage_outsource": "homepage_general",
    "landing_page": "landing_page",
    "detail_page": "detail_page",
    "shop_build": "shop_build",
    "app_maintenance": "maintenance",
    "homepage_maintenance": "maintenance",
    "maintenance": "maintenance",
}


def _apply_creative_override(
    variant: AdLandingVariant, ad_group: str, creative: str
) -> AdLandingVariant:
    override = CREATIVE_OVERRIDES.get((ad_group, creative))
    if not override:
        return variant
    return replace(variant, **override)


def _clean_param(value: str, max_length: int = 120) -> str:
    return " ".join(value.strip().split())[:max_length]


def build_ad_landing_context(request: HttpRequest) -> dict:
    params = {
        "src": _clean_param(request.GET.get("src", ""), 40),
        "campaign": _clean_param(request.GET.get("campaign", ""), 80),
        "group": _clean_param(request.GET.get("group", ""), 80),
        "intent": _clean_param(request.GET.get("intent", ""), 80),
        "creative": _clean_param(request.GET.get("creative", ""), 80),
        "kw": _clean_param(request.GET.get("kw", ""), 120),
    }
    if params["src"] != "naver":
        return {}

    intent_to_variant = {
        "vibe_sos": "vibe_coding",
        "gov_grant": "gov_token",
        "token": "gov_token",
    }
    variant_key = (
        intent_to_variant.get(params["intent"])
        or GROUP_TO_VARIANT.get(params["group"])
        or GROUP_TO_VARIANT.get(params["campaign"])
    )
    if not variant_key:
        variant_key = "app_general" if params["campaign"] == "app_dev" else ""
    variant = VARIANTS.get(variant_key or "")
    if not variant:
        return {}
    variant = _apply_creative_override(
        variant, params["group"] or variant.ad_group, params["creative"]
    )

    eyebrow = (
        f"[{params['kw']}] 8년 차 개발사 1:1 진단"
        if params["kw"]
        else (variant.eyebrow or "8년 차 풀스택 개발사 직접 개발")
    )

    return {
        "src": params["src"],
        "campaign": params["campaign"] or variant.campaign,
        "ad_group": params["group"] or variant.ad_group,
        "intent": params["intent"] or variant.intent,
        "creative": params["creative"],
        "keyword": params["kw"],
        "landing_variant": variant.landing_variant,
        "headline": variant.headline,
        "subcopy": variant.subcopy,
        "primary_cta": variant.primary_cta,
        "secondary_cta": variant.secondary_cta,
        "inquiry_type": variant.inquiry_type,
        "eyebrow": eyebrow,
    }
