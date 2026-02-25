from copy import deepcopy

SERVICE_CARDS = [
    {
        "id": "founder-ax-diagnosis",
        "title": "AX 진단 (90분)",
        "summary": "아이디어/운영 이슈를 빠르게 구조화하고 자동화 우선순위를 설계합니다.",
        "items": [
            "현재 업무 흐름/병목 구간 진단",
            "OpenClaw/바이브코딩 적용 후보 도출",
            "2주 실행 백로그와 KPI 기준선 정의",
        ],
        "duration": "90분",
        "price": "15만원 ~ 30만원",
        "deliverable": "AX 실행 진단 리포트 + 우선순위 백로그",
        "audience": "초기 창업팀, 1인기업, 소규모 운영팀",
        "cta_label": "AX 진단 신청",
        "cta_href": "#contact",
        "persona_targets": ["founders"],
    },
    {
        "id": "founder-ax-build",
        "title": "AX 구축 (2주 ~ 4주)",
        "summary": "바이브코딩/OpenClaw/자동화 조합으로 핵심 실행 체계를 구축합니다.",
        "items": [
            "핵심 업무 플로우와 제품 실행 루프 설계/구현",
            "OpenClaw/바이브코딩 기반 반복 작업 자동화 적용",
            "운영 가이드와 인수인계 문서 제공",
        ],
        "duration": "2주 ~ 4주",
        "price": "300만원 ~ 900만원",
        "deliverable": "운영 가능한 AX 실행 체계 + 운영 문서",
        "audience": "실행 체계 고도화가 필요한 창업팀/사업자",
        "cta_label": "AX 구축 상담",
        "cta_href": "#contact",
        "persona_targets": ["founders"],
    },
    {
        "id": "founder-outsourcing-track",
        "title": "외주용역 집중 트랙 (1,000만원+)",
        "summary": "핵심 제품/자동화 구축을 고밀도로 진행하는 전담 외주용역 트랙입니다.",
        "items": [
            "요구사항 정밀 정의 및 주차별 마일스톤 수립",
            "제품/자동화 구현 + 운영 이관까지 일괄 수행",
            "범위 변경 시 영향도(일정/비용) 사전 합의",
        ],
        "duration": "4주 ~ 8주",
        "price": "1,000만원+",
        "deliverable": "운영 가능한 결과물 + 인수인계 문서 + 안정화 지원",
        "audience": "고난도 실행이 필요한 창업팀/사업자",
        "cta_label": "외주용역 상담 신청",
        "cta_href": "#contact",
        "capacity_note": "품질 유지를 위해 한 타임에 한 고객사만 진행합니다.",
        "persona_targets": ["founders"],
    },
    {
        "id": "foreign-dev-network-build",
        "title": "개발사 네트워크 연결 지원",
        "summary": "국내 개발사 네트워크와 연결될 수 있도록 포지셔닝과 소개 흐름을 설계합니다.",
        "items": [
            "개발사/협업 파트너 연결용 프로필 정리",
            "기술 스택/희망 역할 기준 소개 포맷 제공",
            "초기 미팅 연결을 위한 커뮤니케이션 가이드",
        ],
        "duration": "상시 운영",
        "price": "상담 후 결정",
        "deliverable": "네트워크 연결용 프로필 패키지 + 미팅 가이드",
        "audience": "한국 실무 연결이 필요한 외국인 개발자",
        "cta_label": "네트워크 연결 문의",
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
    {
        "id": "foreign-dev-settlement-network",
        "title": "정착 지원 네트워크 연계",
        "summary": "언어, 비자 행정, 주거 정착 관련 실무 네트워크를 연결해 초기 적응을 돕습니다.",
        "items": [
            "한국어 학습/커뮤니케이션 코치 연결",
            "비자/체류 이슈 대응을 위한 행정사 네트워크 연결",
            "주거 탐색/계약 관련 초기 가이드 및 정보 연결",
        ],
        "duration": "요청 시 수시",
        "price": "상담 후 결정",
        "deliverable": "정착 지원 연결 플랜 + 파트너 안내",
        "audience": "한국 생활/업무 적응이 필요한 외국인 개발자",
        "cta_label": "정착 지원 문의",
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
]

SHARED_CONTENT = {
    "site_name": "큐룸(QuRoom)",
    "headline": "창업자의 아이디어를 실행 가능한 제품과 자동화로 연결합니다",
    "subcopy": (
        "큐룸은 창업자/소상공인을 위해 OpenClaw와 바이브코딩 기반 AX 실행 서비스를 제공하고, "
        "아이디어 검증부터 운영 자동화까지 빠르게 연결합니다."
    ),
    "founder_capacity_policy": "외주용역 집중 트랙은 한 타임에 한 고객사만 진행합니다.",
    "hero_support_text": (
        "2018.06 설립 · 총 개발 경력 {career_duration} · 총 7개 프로젝트(법인 5, 외주 2)"
    ),
    "about_title": "큐룸은 실행 가능한 제품을 만듭니다",
    "about_body": [
        "큐룸은 아이디어 검증부터 MVP 개발, 운영 개선까지 실제 시장에서 작동하는 소프트웨어를 만드는 데 집중합니다.",
        "창업자의 실행 속도를 높이는 AX 패키지(진단/구축/용역)로 수익화까지 연결되는 실행 루프를 설계합니다.",
    ],
    "metrics": [
        {
            "label": "총 개발 경력",
            "value_template": "{career_duration}",
            "description": "법인 + 회사 개발 경력 합산",
        },
        {
            "label": "프로젝트 수",
            "value_template": "총 7건",
            "description": "법인 5, 외주 2",
        },
        {
            "label": "재의뢰율",
            "value_template": "100%",
            "description": "기준 프로젝트 내 재의뢰",
        },
        {
            "label": "문의 응답",
            "value_template": "영업일 1~2일",
            "description": "급한 경우 LinkedIn DM",
        },
    ],
    "services": SERVICE_CARDS,
    "service_addons": [
        {
            "title": "비즈니스 메일 구축",
            "summary": "다음 스마트워크 기준으로 도메인 구매 / 연결 / DNS 레코드 설정을 지원합니다.",
            "duration": "2일 ~ 5일",
            "price": "60만원 ~ 150만원",
            "audience": "초기 창업팀, 소상공인, 1인 사업자",
            "note": "메일 계정 발급/초기 발신 안정화까지 포함하며 운영 중 추가 정책 변경은 별도 협의",
        },
        {
            "title": "기업 홈페이지 구축",
            "summary": "신뢰 중심 기업 소개 홈페이지(회사/서비스/포트폴리오/문의) 구축과 배포까지 제공합니다.",
            "duration": "1주 ~ 3주",
            "price": "300만원 ~ 900만원",
            "audience": "신규 법인, 리브랜딩이 필요한 중소기업",
            "note": "콘텐츠 제작/촬영, 유료 플러그인/외부 SaaS 비용은 별도",
        },
    ],
    "evidence_policy": [
        "경력/프로젝트 신뢰 문구는 검증 가능한 사실만 사용합니다.",
        "증빙 링크 타입: LinkedIn, 포트폴리오, GitHub",
        "협력 네트워크는 별도 동의 없으면 범주형 문구(예: 다수 개발사 협업 네트워크)로 표기합니다.",
    ],
    "portfolio": [
        {
            "name": "PromptSpike",
            "period": "2025.04 ~ 현재",
            "summary": "여러 LLM 탭에 한 번에 프롬프트를 전송하고 템플릿으로 재사용하는 브라우저 확장",
            "problem": "멀티 LLM 사용이 보편화되면서 반복 재사용되는 프롬프트 입력 시간이 급격히 증가하는 시장 문제",
            "solution": "한 번 입력으로 다중 탭 동시 전송, 멀티스텝 플로 자동 진행, 긴 프롬프트 분할 전송 지원",
            "result": "반복 입력 시간을 줄이고 프롬프트 운영 효율 개선",
            "tech": "Chrome Extension, JavaScript, LLM Tab Control",
            "image": "portfolio/thumb/2025-promptspike-thumb-v1.jpg",
            "link": "https://chromewebstore.google.com/detail/promptspike-prompt-manage/khokpfkmdgimgfieinhffnhnmncoahpb",
        },
        {
            "name": "WishBox (소망창고) - Alpha",
            "period": "2025.01 ~ 현재",
            "summary": "목표 달성 리워드 기반 서비스 알파 운영",
            "problem": "자기계발/목표관리 시장에서 '설정은 쉽지만 지속 실행은 어려운' 낮은 유지율 문제가 반복되는 구조",
            "solution": "목표 달성 시 리워드 제공, 이메일 수집 및 사용자 피드백 기반 개선 루프 구축",
            "result": "알파 유저 피드백 축적 중, 제품 방향성 검증 단계",
            "tech": "Django, htmx 외 3+",
            "image": "portfolio/thumb/2025-wishbox-thumb-v1.jpg",
            "link": "https://hopxo.com",
        },
        {
            "name": "Obible (PWA 커뮤니티 성경 서비스)",
            "period": "2023.01 ~ 2024.06",
            "summary": "성경 읽기, 그룹 기반 커뮤니티, 댓글/하이라이트를 제공한 PWA 서비스",
            "problem": "신앙 커뮤니티 시장에서 개인 묵상, 소그룹 교제, 일정 운영이 여러 도구로 분산되어 참여 지속성이 떨어지는 문제",
            "solution": "읽기/코멘트/하이라이트 + 그룹 구독/초대 + 그룹 전용 피드로 공동체 기능 통합",
            "result": "온라인 커뮤니티 기반의 지속 읽기 경험 구축",
            "tech": "Docker, Celery 외 13+",
            "image": "portfolio/thumb/2023-obible-thumb-v1.jpg",
            "link": "https://obible.kr",
        },
        {
            "name": "Kids Travel Curating",
            "period": "2022.09 ~ 2022.12",
            "summary": "PSF 검증을 위해 빠른 피벗 중심으로 운영한 여행 큐레이션 서비스",
            "problem": "가족 여행 시장에서 맞춤형 정보 탐색 비용이 높고, 초기 서비스는 검증 전에 개발비가 과투입되기 쉬운 문제",
            "solution": "Nuxt + Google Spreadsheet 기반으로 DB 없이 빠른 배포 사이클을 구축하고 Make/Apify로 반복 수집·정리 흐름 자동화",
            "result": "거의 일 단위 배포로 가설 검증 반복",
            "tech": "Nuxt, Amazon EC2, Nginx, Make, Apify",
            "image": "portfolio/thumb/2022-kidstravel-thumb-v1.jpg",
            "link": "http://43.200.44.34/",
        },
        {
            "name": "미술관 큐레이션 서비스 (ArtTrip)",
            "period": "2022.05 ~ 2022.08",
            "summary": "온라인으로 미술작품을 관람하고 오디오 해설을 들을 수 있는 미술관 큐레이션 서비스",
            "problem": "미술관마다 작품 해설 지원 수준이 다르고 전시를 관통하는 스토리 제공이 부족해 관람 경험이 단절되는 시장 문제",
            "solution": "Django 백엔드와 Vue 프론트엔드 기반으로 작품 정보, 큐레이션 스토리, 오디오 해설을 통합 제공하는 구조 설계",
            "result": "온라인 관람 + 오디오 해설 중심의 큐레이션 서비스 MVP 구축",
            "tech": "Django, Vue",
            "image": "portfolio/thumb/2022-arttrip-thumb-v1.jpg",
            "link": "",
        },
        {
            "name": "Onepaper (부동산 전자계약 서비스)",
            "period": "2020.03 ~ 2022.08",
            "summary": "대면 없이 계약 가능한 온라인 부동산 전자계약 서비스",
            "problem": "부동산 거래 시장에서 법정 양식 준수 요구와 비대면 계약 수요가 동시에 커지며 디지털 전환 마찰이 발생하는 문제",
            "solution": "시장 조사부터 제품 설계/개발/피벗까지 전 과정을 주도",
            "result": "법적 제약을 고려한 전자계약 워크플로우 구축",
            "tech": "Docker, Amazon EC2 외 10+",
            "image": "portfolio/thumb/2020-onepaper-thumb-v1.jpg",
            "link": "https://github.com/quroom/onepaper",
        },
    ],
    "faq": [
        {
            "q": "프로젝트 범위는 어떻게 정하나요?",
            "a": "초기 제안서 기준으로 범위를 확정하고, 추가 요구는 변경관리 절차로 일정/비용 영향을 먼저 공유합니다.",
        },
        {
            "q": "지불 조건은 어떻게 되나요?",
            "a": "착수금/중간금/잔금 3단계 또는 월 단위 청구를 프로젝트별로 협의합니다.",
        },
        {
            "q": "급한 문의는 어떻게 하나요?",
            "a": "기본 채널은 help@quroom.kr이며, 긴급한 경우 LinkedIn DM으로도 문의 가능합니다.",
        },
    ],
    "kpi_keys": {
        "founders": ["founder_consult_submit", "founder_consult_qualified"],
        "foreign_developers": [
            "foreign_linkage_inquiry_submit",
            "foreign_linkage_meeting_booked",
        ],
    },
    "trust_note": "더 상세한 경력/역할 정보는 대표자 LinkedIn에서 확인할 수 있습니다.",
    "links": {
        "linkedin": "https://www.linkedin.com/in/samkimtech",
        "threads": "https://www.threads.com/@godok.eagle/",
    },
    "company": {
        "name": "큐룸(QuRoom)",
        "owner": "김상은",
        "address": "광주광역시 북구 중흥동 338-60, 2층",
        "email": "help@quroom.kr",
        "biz_number": "246-86-01161",
        "mail_order_number": "해당 없음",
    },
}

PERSONA_CONTENT = {
    "founders": {
        "label": "For Founders",
        "title": "창업자/소상공인을 위한 제품화·수익화 실행 파트너",
        "description": "AX 진단, AX 구축, 외주용역 트랙으로 아이디어를 실행 가능한 제품과 수익으로 연결합니다.",
        "primary_cta": {"label": "창업자 상담 신청", "href": "#contact"},
        "secondary_cta": {"label": "제공 서비스 확인", "href": "#services"},
        "service_target": "founders",
        "faq": [
            {
                "q": "범위는 어떻게 확정하나요?",
                "a": "초기 진단에서 우선순위를 정하고, 범위/일정/비용을 합의한 뒤 시작합니다.",
            },
            {
                "q": "비용과 일정은 어떻게 책정되나요?",
                "a": "패키지 단위 기본안(90분/2~4주/외주용역)에서 시작하고 확장 범위는 별도 협의합니다.",
            },
            {
                "q": "변경 요청은 어떻게 처리되나요?",
                "a": "스프린트 단위 변경관리로 일정/비용 영향도를 사전 공유합니다.",
            },
        ],
        "kpi": ["founder_consult_submit", "founder_consult_qualified"],
    },
    "foreign_developers": {
        "label": "For Foreign Developers",
        "title": "외국인 개발자를 위한 국내 개발 네트워크 연결",
        "description": "대기업 실무 경험과 로컬 개발사 네트워크를 바탕으로 국내 협업 기회를 연결합니다.",
        "primary_cta": {"label": "네트워크 연결 문의", "href": "#contact"},
        "secondary_cta": {"label": "제공 서비스 보기", "href": "#services"},
        "service_target": "foreign_developers",
        "credibility_signals": [
            "삼성전자 실무 경험 기반 멘토링",
            "전남대 출신 로컬 맥락 이해와 커뮤니티 연결 경험",
            "다수 개발사 협업 네트워크 기반 실무 연계 지원",
            "공인중개사 자격 기반 생활/정착 맥락 이해",
        ],
        "scope_boundary": "언어/비자/주거 관련 네트워크 연결은 지원하며, 비자·법률 자문을 직접 대행하지는 않습니다.",
        "faq": [
            {
                "q": "연계 프로세스는 어떻게 진행되나요?",
                "a": "역량/희망 직무 확인 후 매칭, 온보딩 가이드, 초기 실무 적응 지원 순서로 진행됩니다.",
            },
            {
                "q": "무엇을 준비해야 하나요?",
                "a": "이력/프로젝트 요약, 희망 직무/기술 스택, 협업 가능한 근무 조건을 준비하면 빠르게 진행됩니다.",
            },
            {
                "q": "지원 범위는 어디까지인가요?",
                "a": "개발사 네트워크 연결, 언어 코치/행정사/주거 정보 연계까지 지원하며, 비자·법률 자문 자체는 전문기관과 연계합니다.",
            },
            {
                "q": "비용은 어떻게 정해지나요?",
                "a": "요청 범위와 연결 난이도에 따라 상담 후 개별 안내합니다.",
            },
        ],
        "kpi": ["foreign_linkage_inquiry_submit", "foreign_linkage_meeting_booked"],
    },
}


def build_page_content(persona: str | None = None) -> dict:
    content = deepcopy(SHARED_CONTENT)
    if persona is None:
        content["services"] = [
            service
            for service in SERVICE_CARDS
            if "founders" in service["persona_targets"]
        ]
        content["faq"] = PERSONA_CONTENT["founders"]["faq"]
        content["kpi"] = PERSONA_CONTENT["founders"]["kpi"]
        return content

    persona_data = PERSONA_CONTENT[persona]
    content["persona"] = persona_data
    content["headline"] = persona_data["title"]
    content["subcopy"] = persona_data["description"]
    content["services"] = [
        service
        for service in SERVICE_CARDS
        if persona_data["service_target"] in service["persona_targets"]
    ]
    content["faq"] = persona_data.get("faq", [])
    content["kpi"] = persona_data.get("kpi", [])
    return content


# Backward compatibility for existing imports
SITE_CONTENT = SHARED_CONTENT

# Date format: YYYY-MM-DD
CAREER_RANGES = [
    {"start": "2012-08-01", "end": "2014-10-31", "label": "삼성전자 S/W 엔지니어"},
    {"start": "2018-06-01", "end": None, "label": "큐룸 개발/운영"},
]
