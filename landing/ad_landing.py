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


VARIANTS: dict[str, AdLandingVariant] = {
    "app_general": AdLandingVariant(
        landing_variant="app_general",
        campaign="app_dev",
        ad_group="app_general",
        intent="general",
        headline="앱 아이디어를 실제 제품 범위와 견적으로 정리해드립니다.",
        subcopy="MVP, 외주 개발, 기능 범위 정리, 개발 일정 산정까지 한 번에 검토합니다.",
        primary_cta="앱 개발 범위 상담하기",
        secondary_cta="30분 앱 범위 정리",
        inquiry_type="outsourcing",
    ),
    "app_cost": AdLandingVariant(
        landing_variant="app_cost",
        campaign="app_dev",
        ad_group="app_cost",
        intent="cost",
        headline="앱 개발 비용이 커지기 전에 필요한 범위부터 정리하세요.",
        subcopy="기능 목록, 우선순위, MVP 범위, 예상 일정과 비용 구간을 함께 정리합니다.",
        primary_cta="앱 견적 상담하기",
        secondary_cta="비용 범위 먼저 보기",
        inquiry_type="outsourcing",
    ),
    "app_outsource": AdLandingVariant(
        landing_variant="app_outsource",
        campaign="app_dev",
        ad_group="app_outsource",
        intent="company_outsource",
        headline="맡기기 전에 범위와 완료 기준부터 명확히 잡습니다.",
        subcopy="외주 개발에서 가장 중요한 범위, 일정, 산출물, 운영 이관 기준을 첫 상담에서 정리합니다.",
        primary_cta="외주 개발 상담하기",
        secondary_cta="외주 범위 점검하기",
        inquiry_type="outsourcing",
    ),
    "app_industry": AdLandingVariant(
        landing_variant="app_industry",
        campaign="app_dev",
        ad_group="app_industry",
        intent="industry",
        headline="업종에 맞는 앱 범위와 운영 흐름부터 정리합니다.",
        subcopy="예약, 병원, 쇼핑몰, 커뮤니티, 업무관리 앱처럼 실제 운영 기준이 중요한 기능을 우선순위로 나눕니다.",
        primary_cta="업종형 앱 상담하기",
        secondary_cta="기능 우선순위 정리",
        inquiry_type="outsourcing",
    ),
    "homepage_general": AdLandingVariant(
        landing_variant="homepage_general",
        campaign="homepage",
        ad_group="homepage_general",
        intent="general",
        headline="사업을 설명하고 문의로 이어지는 홈페이지를 구축합니다.",
        subcopy="회사 소개, 서비스 설명, 포트폴리오, 문의 흐름까지 사업 목적에 맞춰 정리합니다.",
        primary_cta="홈페이지 제작 상담하기",
        secondary_cta="홈페이지 범위 정리",
        inquiry_type="infra_setup",
    ),
    "homepage_cost": AdLandingVariant(
        landing_variant="homepage_cost",
        campaign="homepage",
        ad_group="homepage_cost",
        intent="cost",
        headline="홈페이지 제작 비용은 필요한 범위부터 정리해야 줄일 수 있습니다.",
        subcopy="페이지 수, 콘텐츠 준비 상태, 문의 흐름, 운영 방식 기준으로 현실적인 견적 범위를 잡습니다.",
        primary_cta="홈페이지 견적 상담하기",
        secondary_cta="비용 범위 정리",
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
        headline="상품의 장점이 구매 결정으로 이어지도록 상세페이지를 정리합니다.",
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
        subcopy="상품 등록, 결제, 문의, 운영 이관까지 실제 판매에 필요한 범위를 먼저 정리합니다.",
        primary_cta="쇼핑몰 제작 상담하기",
        secondary_cta="판매 흐름 정리",
        inquiry_type="infra_setup",
    ),
    "maintenance": AdLandingVariant(
        landing_variant="maintenance",
        campaign="maintenance",
        ad_group="maintenance",
        intent="maintenance",
        headline="이미 만든 웹·앱의 수정 범위와 우선순위를 정리합니다.",
        subcopy="오류 수정, 리뉴얼, 기능 개선, 운영 이관 기준을 현재 상태에 맞춰 나눕니다.",
        primary_cta="유지보수 상담하기",
        secondary_cta="개선 범위 점검",
        inquiry_type="outsourcing",
    ),
}

CREATIVE_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    ("app_cost", "scope_first"): {
        "headline": "앱 개발 비용은 기능 범위부터 줄여야 현실적으로 잡힙니다.",
        "subcopy": "필수 기능과 나중에 미룰 기능을 나눠 불필요한 개발비가 커지기 전에 1차 범위를 정리합니다.",
        "primary_cta": "앱 비용 범위 상담하기",
        "secondary_cta": "기능 범위 먼저 정리",
    },
    ("app_cost", "mvp_quote"): {
        "headline": "MVP 앱 견적은 처음 만들 기능을 어디까지 줄이느냐에서 결정됩니다.",
        "subcopy": "런칭에 꼭 필요한 기능과 검증 후 붙일 기능을 나눠 현실적인 1차 견적을 잡습니다.",
        "primary_cta": "MVP 견적 상담하기",
        "secondary_cta": "1차 기능 정리",
    },
    ("app_cost_2", "scope_first"): {
        "headline": "앱 개발 비용은 기능 범위부터 줄여야 현실적으로 잡힙니다.",
        "subcopy": "필수 기능과 나중에 미룰 기능을 나눠 불필요한 개발비가 커지기 전에 1차 범위를 정리합니다.",
        "primary_cta": "앱 비용 범위 상담하기",
        "secondary_cta": "기능 범위 먼저 정리",
    },
    ("app_outsource", "outsourcing_risk"): {
        "headline": "앱 외주는 개발 시작 전에 완료 기준부터 맞춰야 합니다.",
        "subcopy": "기능 범위, 일정, 산출물, 운영 이관 기준을 먼저 정리해 외주 리스크를 줄입니다.",
        "primary_cta": "앱 외주 범위 상담하기",
        "secondary_cta": "완료 기준 점검",
    },
    ("homepage_cost", "cost_range"): {
        "headline": "홈페이지 제작 견적은 페이지 수보다 목적과 문의 흐름이 먼저입니다.",
        "subcopy": "필요한 페이지, 콘텐츠 준비 상태, 문의 동선, 운영 방식 기준으로 비용 범위를 현실적으로 잡습니다.",
        "primary_cta": "홈페이지 견적 상담하기",
        "secondary_cta": "필요 페이지 정리",
    },
    ("homepage_general", "first_scope"): {
        "headline": "B2B 홈페이지 제작은 사업 목적과 문의 흐름부터 잡아야 합니다.",
        "subcopy": "기획, 디자인, 개발, 배포까지 한 사람이 이어서 맡아 제작 범위와 운영 기준을 정리합니다.",
        "primary_cta": "홈페이지 제작 상담하기",
        "secondary_cta": "제작 범위 정리",
    },
    ("homepage_general", "local_gwangju"): {
        "headline": "광주권 홈페이지 제작은 지역 사업 이해와 실행 속도가 중요합니다.",
        "subcopy": "광주, 북구, 중흥동 등 가까운 사업 현장을 기준으로 기획부터 디자인, 개발, 배포까지 직접 정리합니다.",
        "primary_cta": "광주 홈페이지 상담하기",
        "secondary_cta": "지역 제작 범위 정리",
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
        "headline": "상세페이지는 고객 질문과 구매 장벽을 먼저 정리해야 합니다.",
        "subcopy": "상품 장점, 고객 우려, 이미지 흐름, 구매 결정을 막는 요소를 페이지 구조로 정리합니다.",
        "primary_cta": "상세페이지 상담하기",
        "secondary_cta": "구매 흐름 점검",
    },
    ("shop_build", "sales_flow"): {
        "headline": "쇼핑몰 제작은 판매 이후 운영 흐름까지 같이 잡아야 합니다.",
        "subcopy": "상품 등록, 결제, 문의, 배송/운영 이관까지 실제 판매에 필요한 범위를 먼저 정리합니다.",
        "primary_cta": "쇼핑몰 제작 상담하기",
        "secondary_cta": "판매 운영 범위 정리",
    },
    ("app_maintenance", "maintenance_scope"): {
        "headline": "앱 유지보수는 오류와 기능 개선의 우선순위부터 나눕니다.",
        "subcopy": "현재 상태를 보고 급한 수정, 릴리즈 안정화, 기능 개선, 리뉴얼 범위를 분리합니다.",
        "primary_cta": "앱 유지보수 상담하기",
        "secondary_cta": "수정 우선순위 정리",
    },
    ("homepage_maintenance", "maintenance_scope"): {
        "headline": "홈페이지 유지보수는 수정 범위와 운영 관리를 먼저 나눠야 합니다.",
        "subcopy": "오류 수정, 콘텐츠 변경, 속도 개선, 운영 관리를 현재 상태 기준으로 분리해 정리합니다.",
        "primary_cta": "홈페이지 유지보수 상담하기",
        "secondary_cta": "수정 범위 점검",
    },
    ("maintenance", "maintenance_scope"): {
        "headline": "웹앱 유지보수는 급한 수정과 나중에 할 일을 먼저 구분합니다.",
        "subcopy": "현재 상태를 보고 오류 수정, 기능 개선, 리뉴얼, 운영 이관 범위를 우선순위로 나눕니다.",
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

    variant_key = GROUP_TO_VARIANT.get(params["group"]) or GROUP_TO_VARIANT.get(
        params["campaign"]
    )
    if not variant_key:
        variant_key = "app_general" if params["campaign"] == "app_dev" else ""
    variant = VARIANTS.get(variant_key or "")
    if not variant:
        return {}
    variant = _apply_creative_override(
        variant, params["group"] or variant.ad_group, params["creative"]
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
    }
