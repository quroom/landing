import logging
from copy import deepcopy

SUPPORTED_LOCALES = ("ko", "en")
SUPPORTED_LOCALE_SET = set(SUPPORTED_LOCALES)
SAFE_LOCALE = "ko"

logger = logging.getLogger(__name__)

EN_TRANSLATIONS = {
    "큐룸(QuRoom)": "QuRoom",
    "김상은": "Sang-eun Kim",
    "광주광역시 북구 중흥동 338-60, 2층": "2F, 338-60 Jungheung-dong, Buk-gu, Gwangju, South Korea",
    "해당 없음": "N/A",
    "2018.06 설립 · 총 개발 경력 {career_duration} · 총 7개 프로젝트(법인 5, 외주 2)": "Founded in 2018.06 · Total development experience {career_duration} · 7 projects total (5 corporate, 2 outsourced)",
    "90분": "90 min",
    "2주 ~ 4주": "2-4 weeks",
    "4주 ~ 8주": "4-8 weeks",
    "2일 ~ 5일": "2-5 days",
    "1주 ~ 3주": "1-3 weeks",
    "상시 운영": "Always available",
    "요청 시 수시": "On request",
    "15만원 ~ 30만원": "KRW 150,000 - 300,000",
    "300만원 ~ 900만원": "KRW 3,000,000 - 9,000,000",
    "1,000만원+": "KRW 10,000,000+",
    "60만원 ~ 150만원": "KRW 600,000 - 1,500,000",
    "상담 후 결정": "Determined after consultation",
    "2025.04 ~ 현재": "2025.04 - Present",
    "2025.01 ~ 현재": "2025.01 - Present",
    "WishBox (소망창고) - Alpha": "WishBox - Alpha",
    "Obible (PWA 커뮤니티 성경 서비스)": "Obible (PWA Community Bible Service)",
    "미술관 큐레이션 서비스 (ArtTrip)": "Museum Curation Service (ArtTrip)",
    "Onepaper (부동산 전자계약 서비스)": "Onepaper (Real Estate e-Contract Service)",
    "Django, htmx 외 3+": "Django, htmx, and 3+ others",
    "Docker, Celery 외 13+": "Docker, Celery, and 13+ others",
    "Docker, Amazon EC2 외 10+": "Docker, Amazon EC2, and 10+ others",
    "신앙 커뮤니티 시장에서 개인 묵상, 소그룹 교제, 일정 운영이 여러 도구로 분산되어 참여 지속성이 떨어지는 문제": "In the faith community market, personal devotion, small-group interaction, and schedule operations were fragmented across tools, reducing sustained participation.",
    "읽기/코멘트/하이라이트 + 그룹 구독/초대 + 그룹 전용 피드로 공동체 기능 통합": "Integrated community features through reading/comments/highlights plus group subscription/invite and a group-only feed.",
    "가족 여행 시장에서 맞춤형 정보 탐색 비용이 높고, 초기 서비스는 검증 전에 개발비가 과투입되기 쉬운 문제": "In the family travel market, customized information discovery costs were high, and early services were prone to over-investing in development before validation.",
    "Nuxt + Google Spreadsheet 기반으로 DB 없이 빠른 배포 사이클을 구축하고 Make/Apify로 반복 수집·정리 흐름 자동화": "Built a fast deployment cycle without a DB using Nuxt + Google Spreadsheet, and automated repeated collection/organization workflows with Make/Apify.",
    "미술관마다 작품 해설 지원 수준이 다르고 전시를 관통하는 스토리 제공이 부족해 관람 경험이 단절되는 시장 문제": "A market issue where artwork commentary support varied by museum and cross-exhibition storytelling was limited, causing fragmented viewing experiences.",
    "Django 백엔드와 Vue 프론트엔드 기반으로 작품 정보, 큐레이션 스토리, 오디오 해설을 통합 제공하는 구조 설계": "Designed an architecture that integrates artwork information, curation stories, and audio guides with a Django backend and Vue frontend.",
    "부동산 거래 시장에서 법정 양식 준수 요구와 비대면 계약 수요가 동시에 커지며 디지털 전환 마찰이 발생하는 문제": "In the real estate market, compliance requirements for statutory forms and demand for non-face-to-face contracts grew simultaneously, creating digital transformation friction.",
    "사업을 이해하고\n믿고 맡길 수 있는 파트너": "Understands the business\nand is a partner you can trust with the work.",
    "업무 범위와 우선순위를 먼저 조율하고, 필요한 부분은 직접 맡아 진행합니다.": "We align scope and priorities first, then directly handle the parts that need to move.",
    "외주용역 집중 트랙은 한 타임에 한 고객사만 진행합니다.": "The dedicated outsourcing track runs with one client at a time.",
    "막힌 실행부터 같이 정리합니다": "We start by sorting out what is blocked in execution.",
    "제품, 운영, 외주가 따로 움직이면 속도가 바로 떨어집니다.": "When product, operations, and outsourcing move separately, speed drops immediately.",
    "지금 어디가 막혀 있는지 보고, 실제로 굴러가게 정리합니다.": "We look at what is blocked now and organize it so it can actually run.",
    "문의부터 실행까지 진행 방식": "How We Work From Inquiry to Delivery",
    "사전 진단 상담": "Initial Diagnosis Call",
    "현재 상황, 목표, 제약을 함께 정리해 우선순위를 확정합니다.": "We align your current situation, goals, and constraints to set priorities.",
    "실행 범위 설계": "Execution Scope Design",
    "2주~8주 단위 실행 범위, 일정, 산출물 기준을 명확히 합의합니다.": "We align execution scope, timeline, and deliverable criteria for a 2-8 week cycle.",
    "구현 및 점검": "Implementation and Review",
    "주차별 결과 공유와 리스크 점검을 통해 일정/품질을 안정적으로 관리합니다.": "We manage schedule and quality through weekly updates and risk reviews.",
    "운영 이관 및 다음 단계": "Handover and Next Step",
    "운영 가이드 전달 후 다음 자동화 과제까지 이어지는 실행 루프를 제안합니다.": "After handover guidance, we propose the next automation loop to sustain momentum.",
    "이런 팀과 잘 맞습니다": "Good Fit",
    "아직 맞지 않을 수 있습니다": "Not a Fit Yet",
    "실행해야 할 과제는 명확한데 내부 리소스가 부족한 팀": "Teams with clear execution goals but limited internal resources",
    "아이디어 검증 이후 실제 제품/운영 자동화로 빠르게 넘어가려는 팀": "Teams moving quickly from validation to real product and operations automation",
    "짧은 주기로 가설 검증과 개선 반복을 원하는 팀": "Teams that want short cycles of hypothesis testing and improvement",
    "요구사항이 아직 정리되지 않아 우선순위 합의가 어려운 상태": "Cases where requirements are not yet organized enough to align priorities",
    "내부 의사결정 구조가 불명확해 담당자/기한 확정이 어려운 상태": "Cases where internal decision-making is unclear and ownership/timelines cannot be fixed",
    "단기 성과보다 장기 연구 성격이 강해 즉시 실행이 어려운 과제": "Projects that are primarily long-term research and not ready for immediate execution",
    "총 개발 경력": "Total Development Experience",
    "법인 + 회사 개발 경력 합산": "Combined corporate and company development experience",
    "프로젝트 수": "Number of Projects",
    "총 7건": "Total 7",
    "법인 5, 외주 2": "5 corporate, 2 outsourced",
    "재의뢰율": "Re-engagement Rate",
    "기준 프로젝트 내 재의뢰": "Re-engagement within reference projects",
    "문의 응답": "Response Time",
    "영업일 1~2일": "1-2 business days",
    "이메일 기준 안내": "Email-first contact",
    "무엇을 먼저 할지, 무엇은 미뤄도 될지 90분 안에 정리합니다.": "In 90 minutes, we clarify what to do first and what can wait.",
    "자동화 실행 진단 (90분)": "Automation Execution Diagnosis (90 min)",
    "90분 안에 지금 막힌 지점을 잡고, 바로 실행할 자동화 1순위를 정합니다.": "In 90 minutes, we pinpoint current bottlenecks and define the top automation priority to execute next.",
    "현재 흐름에서 시간·비용이 새는 구간 1~2개를 특정": "Identify 1-2 points where time and cost are leaking in the current flow",
    "자동화 효과가 큰 후보를 우선순위로 정리": "Prioritize high-impact automation candidates",
    "2주 안에 시도 가능한 작업 목록과 완료 기준 확정": "Define a 2-week executable task list and completion criteria",
    "진단 요약 문서 + 2주 실행 후보 리스트": "Diagnosis summary document + 2-week execution candidate list",
    "초기 창업팀, 1인기업, 소규모 운영팀": "Early-stage founder teams, solo businesses, small operations teams",
    "자동화 실행 진단 신청": "Request Automation Diagnosis",
    "자동화 실행 구축 (2주 ~ 4주)": "Automation Execution Build (2-4 weeks)",
    "반복 업무와 운영 흐름을 실제로 돌아가게 정리합니다.": "We organize repetitive work and operations so they actually run.",
    "핵심 업무 플로우를 실제 운영 기준에 맞게 설계": "Design core workflows based on real operational criteria",
    "반복 작업 자동화 적용 및 실패 케이스 점검": "Apply automation to repetitive tasks and review failure cases",
    "팀이 바로 이어받을 수 있는 운영 가이드 제공": "Provide operational guides your team can immediately take over",
    "운영 가능한 자동화 구성 + 자동화 운영 가이드 문서": "Operable automation setup + automation operation guide document",
    "실행 체계 고도화가 필요한 창업팀/사업자": "Founders/business owners needing advanced execution systems",
    "자동화 실행 구축 상담": "Request Automation Build Consultation",
    "외주용역 집중 트랙 (1,000만원+)": "Dedicated Outsourcing Track (KRW 10M+)",
    "범위가 크고 난도가 높은 과제를 일정 잡고 진행하는 트랙입니다.": "A track for larger, higher-complexity work run on a defined schedule.",
    "첫 주에 범위·일정·완료 기준 고정": "Lock scope, timeline, and completion criteria in week 1",
    "주차별 마일스톤으로 진행 상황 공유": "Share progress through weekly milestones",
    "운영 이관과 초기 이슈 점검 범위를 별도 합의": "Agree separately on handover and initial issue review scope",
    "구축 결과물 + 운영 이관 문서 (후속 지원 범위 별도 합의)": "Build deliverables + operations handover document (follow-up support scope separately agreed)",
    "진단 예약하기": "Book Diagnosis",
    "구축 상담받기": "Request Build Consultation",
    "집중 트랙 문의하기": "Request Dedicated Track Consultation",
    "고난도 실행이 필요한 창업팀/사업자": "Founders/business owners needing high-complexity execution",
    "외주용역 상담 신청": "Request Outsourcing Consultation",
    "품질 때문에 한 타임에 한 고객사만 진행합니다.": "We handle one client at a time to keep focus.",
    "제품화·운영 실행 파트": "Productization and Operations Execution",
    "만드는 일, 운영하는 일, 맡길 일이 실제로 굴러가도록 돕는 서비스입니다.": "Services that help what you build, operate, and delegate actually keep moving.",
    "이런 경험과 기준으로 일합니다": "This is the experience and standard I work from.",
    "삼성전자 포함 총 개발 경력 {career_duration}": "Total development experience {career_duration}, including Samsung Electronics",
    "총 7개 프로젝트 경험과 운영 이관 기준 정리": "Experience across 7 projects with explicit handover criteria",
    "외주 집중 트랙은 한 타임 1고객만 진행해 집중도를 높입니다": "The dedicated outsourcing track runs one client at a time to keep focus high.",
    "대표자 경력과 프로젝트 이력은 LinkedIn에서 바로 확인 가능": "The founder's career and project history can be checked directly on LinkedIn.",
    "이런 상황이라면 함께하기 좋습니다": "These are the situations where working together fits well.",
    "범위와 목표가 어느 정도 잡혀 있으면, 첫 대화에서 다음 액션까지 정리하기 쉽습니다.": "If scope and goals are roughly set, it is easier to sort out next actions in the first conversation.",
    "이런 상황이라면 대화가 잘 됩니다": "These are the situations where the conversation tends to go well.",
    "범위와 목표가 어느 정도 보이면, 첫 대화에서 무엇부터 할지 같이 정리할 수 있습니다.": "If scope and goals are visible enough, we can sort out what to do first in the first conversation.",
    "이번 분기 안에 진행해야 할 과제가 있는 경우": "When there is work that needs to move within this quarter",
    "담당자와 의사결정자가 어느 정도 정해져 있는 경우": "When the owner and decision-maker are roughly in place",
    "문의 전에 범위나 우선순위를 한번 같이 정리해보고 싶은 경우": "When you want to sort out scope or priorities before making a full inquiry",
    "기본 연락은 이메일로 받습니다.": "Email is the default contact channel.",
    "담당자와 의사결정자가 정해져 있어 범위 합의가 가능한 팀": "Teams with a clear owner and decision-maker who can align scope",
    "추가로 도와드릴 수 있는 것": "Additional Founder Infrastructure Support",
    "메인 실행 과제 외에 창업 초기에 자주 필요한 운영 인프라를 빠르게 정리합니다.": "Beyond the main execution work, we can quickly set up common operating infrastructure founders need early on.",
    "비즈니스 메일 구축": "Business Email Setup",
    "다음 스마트워크 기준으로 도메인 구매 / 연결 / DNS 레코드 설정을 지원합니다.": "Support domain purchase/connection and DNS records based on Daum Smartwork standards.",
    "초기 창업팀, 소상공인, 1인 사업자": "Early-stage teams, small merchants, solo founders",
    "메일 계정 발급/초기 발신 안정화까지 포함하며 운영 중 추가 정책 변경은 별도 협의": "Includes account issuance and initial sender stabilization; additional policy changes are discussed separately.",
    "기업 홈페이지 구축": "Corporate Website Build",
    "신뢰 중심 기업 소개 홈페이지(회사/서비스/포트폴리오/문의) 구축과 배포까지 제공합니다.": "Provide build and deployment of trust-oriented corporate websites (company/service/portfolio/contact).",
    "신규 법인, 리브랜딩이 필요한 중소기업": "New corporations and SMEs needing rebranding",
    "콘텐츠 제작/촬영, 유료 플러그인/외부 SaaS 비용은 별도": "Content creation/shooting and paid plugins/external SaaS costs are separate.",
    "더 상세한 경력/역할 정보는 대표자 LinkedIn에서 확인할 수 있습니다.": "More detailed career/role information is available on the founder's LinkedIn.",
    "PromptSpike": "PromptSpike",
    "여러 LLM 탭에 한 번에 프롬프트를 전송하고 템플릿으로 재사용하는 브라우저 확장": "A browser extension that sends prompts to multiple LLM tabs at once and reuses them as templates.",
    "멀티 LLM 사용이 보편화되면서 반복 재사용되는 프롬프트 입력 시간이 급격히 증가하는 시장 문제": "As multi-LLM usage became common, repetitive prompt entry time increased sharply.",
    "한 번 입력으로 다중 탭 동시 전송, 멀티스텝 플로 자동 진행, 긴 프롬프트 분할 전송 지원": "Supports one-input multi-tab sending, automatic multi-step flows, and long prompt chunking.",
    "반복 입력 시간을 줄이고 프롬프트 운영 효율 개선": "Reduced repetitive input time and improved prompt operation efficiency.",
    "목표 달성 리워드 기반 서비스 알파 운영": "Operating an alpha service based on goal-achievement rewards.",
    "자기계발/목표관리 시장에서 '설정은 쉽지만 지속 실행은 어려운' 낮은 유지율 문제가 반복되는 구조": "In self-development/goal management, low retention repeats because setup is easy but sustained execution is hard.",
    "목표 달성 시 리워드 제공, 이메일 수집 및 사용자 피드백 기반 개선 루프 구축": "Provides rewards on goal completion and builds feedback loops via email collection and user input.",
    "알파 유저 피드백 축적 중, 제품 방향성 검증 단계": "Accumulating alpha-user feedback, currently validating product direction.",
    "성경 읽기, 그룹 기반 커뮤니티, 댓글/하이라이트를 제공한 PWA 서비스": "A PWA service offering Bible reading, group community, comments, and highlights.",
    "온라인 커뮤니티 기반의 지속 읽기 경험 구축": "Built sustained reading experiences through online community.",
    "PSF 검증을 위해 빠른 피벗 중심으로 운영한 여행 큐레이션 서비스": "A travel curation service operated with rapid pivots for PSF validation.",
    "거의 일 단위 배포로 가설 검증 반복": "Repeated hypothesis validation with near-daily deployments.",
    "온라인으로 미술작품을 관람하고 오디오 해설을 들을 수 있는 미술관 큐레이션 서비스": "A museum curation service for online artwork viewing with audio guides.",
    "온라인 관람 + 오디오 해설 중심의 큐레이션 서비스 최소 기능 제품 구축": "Built an MVP curation service centered on online viewing + audio guides.",
    "대면 없이 계약 가능한 온라인 부동산 전자계약 서비스": "An online real-estate e-contract service enabling non-face-to-face contracts.",
    "시장 조사부터 제품 설계/개발/피벗까지 전 과정을 주도": "Led the full cycle from market research to design/development/pivots.",
    "법적 제약을 고려한 전자계약 워크플로우 구축": "Built e-contract workflows considering legal constraints.",
    "프로젝트 범위는 어떻게 정하나요?": "How do you define project scope?",
    "초기 제안서 기준으로 범위를 확정하고, 추가 요구는 변경관리 절차로 일정/비용 영향을 먼저 공유합니다.": "We fix scope based on the initial proposal, and for additional requests we first share schedule/cost impacts via change management.",
    "지불 조건은 어떻게 되나요?": "What are the payment terms?",
    "착수금/중간금/잔금 3단계 또는 월 단위 청구를 프로젝트별로 협의합니다.": "We agree per project on either 3-stage payments or monthly billing.",
    "문의는 어떻게 진행되나요?": "How should I reach out?",
    "기본 채널은 help@quroom.kr 이메일입니다.": "The default contact channel is help@quroom.kr email.",
    "30분 무료 커피챗": "30-min Free Coffee Chat",
    "지금 뭐가 막혀 있는지 가볍게 이야기해보는 첫 대화입니다.": "A lightweight first conversation about what feels blocked right now.",
    "지금 가장 막힌 지점부터 정리": "Start by sorting out the most blocked point",
    "자동화나 구축이 필요한 구간을 가볍게 점검": "Quickly review where automation or a build may be needed",
    "정식 상담까지 갈 일인지 같이 판단": "Decide together whether it should move into a formal consultation",
    "대화 후 다음 액션 1~2개 정리": "1-2 next actions after the conversation",
    "가볍게 방향을 점검해보고 싶은 창업자/소규모 팀": "Founders and small teams who want a light directional check-in",
    "커피챗 신청하기": "Book Coffee Chat",
    "범위는 어떻게 확정하나요?": "How is scope finalized?",
    "초기 진단에서 우선순위를 정하고, 범위/일정/비용을 합의한 뒤 시작합니다.": "We set priorities in initial diagnosis, then start after agreeing scope/schedule/cost.",
    "비용과 일정은 어떻게 책정되나요?": "How are cost and schedule determined?",
    "패키지 단위 기본안(90분/2~4주/외주용역)에서 시작하고 확장 범위는 별도 협의합니다.": "We start from package baselines (90 min / 2-4 weeks / outsourcing); expanded scope is discussed separately.",
    "변경 요청은 어떻게 처리되나요?": "How are change requests handled?",
    "스프린트 단위 변경관리로 일정/비용 영향도를 사전 공유합니다.": "We pre-share schedule/cost impacts via sprint-based change management.",
    "경력/프로젝트 신뢰 문구는 검증 가능한 사실만 사용합니다.": "Trust copy on career/projects uses only verifiable facts.",
    "증빙 링크 타입: LinkedIn, 포트폴리오, GitHub": "Evidence link types: LinkedIn, Portfolio, GitHub",
    "협력 네트워크는 별도 동의 없으면 범주형 문구(예: 다수 개발사 협업 네트워크)로 표기합니다.": "Collaboration networks are written as category-level descriptions unless explicit consent is given.",
    "2018.06 설립 · 총 개발 경력": "Founded 2018.06 · Total development experience",
    "총 7개 프로젝트(법인 5, 외주 2)": "Total 7 projects (5 corporate, 2 outsourced)",
    "현재": "Present",
    "30분": "30 min",
    "무료": "Free",
    "삼성전자 S/W 엔지니어": "Samsung Electronics S/W Engineer",
    "공인중개사 자격 취득": "Licensed Real-Estate Agent",
    "중개업 활동, 자동화로 업무 효율화": "Brokerage operations with automation-driven efficiency",
    "쉐어하우스 창업 및 확장": "Share-house startup and expansion",
    "소셜벤처 창업 및 큐룸 개발/운영": "Social venture founding and QuRoom development/operations",
}

SERVICE_CARDS = [
    {
        "id": "founder-ax-coffee-chat",
        "title": "30분 무료 커피챗",
        "summary": "지금 뭐가 막혀 있는지 가볍게 이야기해보는 첫 대화입니다.",
        "items": [
            "지금 가장 막힌 지점부터 정리",
            "자동화나 구축이 필요한 구간을 가볍게 점검",
            "정식 상담까지 갈 일인지 같이 판단",
        ],
        "duration": "30분",
        "price": "무료",
        "deliverable": "대화 후 다음 액션 1~2개 정리",
        "audience": "가볍게 방향을 점검해보고 싶은 창업자/소규모 팀",
        "cta_label": "커피챗 신청하기",
        "cta_href": "#contact",
        "persona_targets": ["founders"],
    },
    {
        "id": "founder-ax-diagnosis",
        "title": "자동화 실행 진단 (90분)",
        "summary": "무엇을 먼저 할지, 무엇은 미뤄도 될지 90분 안에 정리합니다.",
        "items": [
            "현재 흐름에서 시간·비용이 새는 구간 1~2개 확인",
            "자동화 효과가 큰 후보 우선순위 정리",
            "2주 안에 해볼 작업과 완료 기준 정리",
        ],
        "duration": "90분",
        "price": "15만원 ~ 30만원",
        "deliverable": "진단 요약 문서 + 2주 실행 후보 리스트",
        "audience": "초기 창업팀, 1인기업, 소규모 운영팀",
        "cta_label": "진단 예약하기",
        "cta_href": "#contact",
        "persona_targets": ["founders"],
    },
    {
        "id": "founder-ax-build",
        "title": "자동화 실행 구축 (2주 ~ 4주)",
        "summary": "반복 업무와 운영 흐름을 실제로 돌아가게 정리합니다.",
        "items": [
            "핵심 업무 흐름을 운영 기준에 맞게 정리",
            "반복 작업 자동화 적용과 실패 구간 점검",
            "팀이 이어받을 수 있게 운영 가이드 정리",
        ],
        "duration": "2주 ~ 4주",
        "price": "300만원 ~ 900만원",
        "deliverable": "운영 가능한 자동화 구성 + 자동화 운영 가이드 문서",
        "audience": "실행 체계 고도화가 필요한 창업팀/사업자",
        "cta_label": "구축 상담받기",
        "cta_href": "#contact",
        "persona_targets": ["founders"],
    },
    {
        "id": "founder-outsourcing-track",
        "title": "외주용역 집중 트랙 (1,000만원+)",
        "summary": "범위가 크고 난도가 높은 과제를 일정 잡고 진행하는 트랙입니다.",
        "items": [
            "첫 주에 범위·일정·완료 기준 고정",
            "주차별 마일스톤으로 진행 상황 공유",
            "운영 이관과 초기 이슈 점검 범위를 별도 합의",
        ],
        "duration": "4주 ~ 8주",
        "price": "1,000만원+",
        "deliverable": "구축 결과물 + 운영 이관 문서 (후속 지원 범위 별도 합의)",
        "audience": "고난도 실행이 필요한 창업팀/사업자",
        "cta_label": "집중 트랙 문의하기",
        "cta_href": "#contact",
        "capacity_note": "품질 때문에 한 타임에 한 고객사만 진행합니다.",
        "persona_targets": ["founders"],
    },
    {
        "id": "foreign-dev-network-build",
        "title": {
            "ko": "취업 전략 및 매칭 준비 지원",
            "en": "Job Strategy and Matching Readiness Support",
        },
        "summary": {
            "ko": "지원 전략, 포지셔닝, 소개 준비도를 함께 정리해 실제 매칭 가능성을 높입니다.",
            "en": "We help shape your strategy, positioning, and introduction readiness to improve matching potential.",
        },
        "items": [
            {
                "ko": "개발사/협업 파트너 연결용 프로필 정리",
                "en": "Profile preparation tailored for developer and partner matching",
            },
            {
                "ko": "기술 스택/희망 역할 기준 소개 포맷 제공",
                "en": "Introduction format based on your tech stack and preferred role",
            },
            {
                "ko": "초기 미팅 연결을 위한 커뮤니케이션 가이드",
                "en": "Communication guide for initial meetings and introductions",
            },
        ],
        "duration": "상시 운영",
        "price": "상담 후 결정",
        "deliverable": {
            "ko": "매칭 준비 프로필 패키지 + 미팅 가이드",
            "en": "Matching-ready profile package + meeting guide",
        },
        "audience": {
            "ko": "한국 실무 연결이 필요한 외국인 개발자",
            "en": "Foreign developers seeking practical collaboration in Korea",
        },
        "cta_label": {"ko": "전략 상담 시작", "en": "Start Strategy Intake"},
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
    {
        "id": "foreign-dev-settlement-network",
        "title": {
            "ko": "지역 적응 및 정착 가이드",
            "en": "Regional Adaptation and Settlement Guidance",
        },
        "summary": {
            "ko": "한국어, 비자 행정, 주거 정보 등 초기 적응에 필요한 실무 가이드를 연결합니다.",
            "en": "We connect practical guidance for Korean learning, visa administration, and housing adaptation.",
        },
        "items": [
            {
                "ko": "한국어 학습/커뮤니케이션 코치 연결",
                "en": "Connection to Korean language and communication coaches",
            },
            {
                "ko": "비자/체류 이슈 대응을 위한 행정사 네트워크 연결",
                "en": "Connection to licensed administrative networks for visa and stay issues",
            },
            {
                "ko": "주거 탐색/계약 관련 초기 가이드 및 정보 연결",
                "en": "Initial guidance and partner links for housing search and contracts",
            },
        ],
        "duration": "요청 시 수시",
        "price": "상담 후 결정",
        "deliverable": {
            "ko": "정착 가이드 플랜 + 파트너 안내",
            "en": "Settlement guidance plan + partner guidance",
        },
        "audience": {
            "ko": "한국 생활/업무 적응이 필요한 외국인 개발자",
            "en": "Foreign developers adapting to work and life in Korea",
        },
        "cta_label": {"ko": "적응 가이드 받기", "en": "Get Adaptation Guidance"},
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
]

SHARED_CONTENT = {
    "site_name": "큐룸(QuRoom)",
    "headline": "사업을 이해하고\n믿고 맡길 수 있는 파트너",
    "subcopy": "업무 범위와 우선순위를 먼저 조율하고, 필요한 부분은 직접 맡아 진행합니다.",
    "founder_capacity_policy": "외주용역 집중 트랙은 한 타임에 한 고객사만 진행합니다.",
    "hero_support_text": (
        "2018.06 설립 · 총 개발 경력 {career_duration} · 총 7개 프로젝트(법인 5, 외주 2)"
    ),
    "about_title": "막힌 실행부터 같이 정리합니다",
    "about_body": [
        "제품, 운영, 외주가 따로 움직이면 속도가 바로 떨어집니다.",
        "지금 어디가 막혀 있는지 보고, 실제로 굴러가게 정리합니다.",
    ],
    "execution_process_title": "문의부터 실행까지 진행 방식",
    "execution_process": [
        {
            "title": "사전 진단 상담",
            "description": "현재 상황, 목표, 제약을 함께 정리해 우선순위를 확정합니다.",
        },
        {
            "title": "실행 범위 설계",
            "description": "2주~8주 단위 실행 범위, 일정, 산출물 기준을 명확히 합의합니다.",
        },
        {
            "title": "구현 및 점검",
            "description": "주차별 결과 공유와 리스크 점검을 통해 일정/품질을 안정적으로 관리합니다.",
        },
        {
            "title": "운영 이관 및 다음 단계",
            "description": "운영 가이드 전달 후 다음 자동화 과제까지 이어지는 실행 루프를 제안합니다.",
        },
    ],
    "engagement_fit": {
        "good_fit_title": "이런 팀과 잘 맞습니다",
        "good_fit": [
            "실행해야 할 과제는 명확한데 내부 리소스가 부족한 팀",
            "아이디어 검증 이후 실제 제품/운영 자동화로 빠르게 넘어가려는 팀",
            "짧은 주기로 가설 검증과 개선 반복을 원하는 팀",
        ],
        "not_fit_title": "아직 맞지 않을 수 있습니다",
        "not_fit": [
            "요구사항이 아직 정리되지 않아 우선순위 합의가 어려운 상태",
            "내부 의사결정 구조가 불명확해 담당자/기한 확정이 어려운 상태",
            "단기 성과보다 장기 연구 성격이 강해 즉시 실행이 어려운 과제",
        ],
    },
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
            "description": "이메일 기준 안내",
        },
    ],
    "services_section_title": "제품화·운영 실행 파트",
    "services_section_subtitle": "만드는 일, 운영하는 일, 맡길 일이 실제로 굴러가도록 돕는 서비스입니다.",
    "fit_section_title": "이런 상황이라면 함께하기 좋습니다",
    "fit_section_intro": "범위와 목표가 어느 정도 잡혀 있으면, 첫 대화에서 다음 액션까지 정리하기 쉽습니다.",
    "hero_trust_title": "이런 경험과 기준으로 일합니다",
    "hero_trust_points": [
        "삼성전자 포함 총 개발 경력 {career_duration}",
        "총 7개 프로젝트 경험과 운영 이관 기준 정리",
        "외주 집중 트랙은 한 타임 1고객만 진행해 집중도를 높입니다",
        "대표자 경력과 프로젝트 이력은 LinkedIn에서 바로 확인 가능",
    ],
    "contact_title": "이런 상황이라면 대화가 잘 됩니다",
    "contact_intro": "범위와 목표가 어느 정도 보이면, 첫 대화에서 무엇부터 할지 같이 정리할 수 있습니다.",
    "contact_points": [
        "이번 분기 안에 진행해야 할 과제가 있는 경우",
        "담당자와 의사결정자가 어느 정도 정해져 있는 경우",
        "문의 전에 범위나 우선순위를 한번 같이 정리해보고 싶은 경우",
        "기본 연락은 이메일로 받습니다.",
    ],
    "addon_section_title": "추가로 도와드릴 수 있는 것",
    "addon_section_subtitle": "메인 실행 과제 외에 창업 초기에 자주 필요한 운영 인프라를 빠르게 정리합니다.",
    "services": SERVICE_CARDS,
    "service_addons": [
        {
            "title": "비즈니스 메일 구축",
            "summary": "다음 스마트워크 기준으로 도메인 구매 / 연결 / DNS 레코드 설정을 지원합니다.",
            "duration": "1일",
            "price": "10만원 ~ 20만원",
            "audience": "초기 창업팀, 소상공인, 1인 사업자",
            "note": "메일 계정 발급/초기 발신 안정화까지 포함하며 운영 중 추가 정책 변경은 별도 협의",
        },
        {
            "title": "기업 홈페이지 구축",
            "summary": "신뢰 중심 기업 소개 홈페이지(회사/서비스/포트폴리오/문의) 구축과 배포까지 제공합니다.",
            "duration": "1주 ~ 3주",
            "price": "100만원 ~ 500만원",
            "audience": "신규 법인, 리브랜딩이 필요한 중소기업",
            "note": "콘텐츠 제작/촬영, 유료 플러그인/외부 SaaS 비용은 별도",
        },
    ],
    "handover_template": {
        "title": "운영 이관 문서 템플릿",
        "summary": "단일 템플릿으로 유지하되, 카드별 앵커 목차로 빠르게 찾아볼 수 있게 구성합니다.",
        "toc": [
            {"id": "handover-diagnosis", "label": "카드1: 자동화 실행 진단"},
            {"id": "handover-build", "label": "카드2: 자동화 실행 구축"},
            {"id": "handover-outsourcing", "label": "카드3: 외주용역 집중 트랙"},
        ],
        "sections": [
            {
                "id": "handover-diagnosis",
                "title": "카드1: 자동화 실행 진단 (90분)",
                "deliverable": "진단 요약 문서 + 2주 실행 후보 리스트",
                "items": [
                    "핵심 병목/리스크 요약",
                    "우선순위 후보 작업 목록(작업명/목적/난이도/선행조건)",
                    "2주 내 시도 가능한 실행 후보 제안",
                ],
            },
            {
                "id": "handover-build",
                "title": "카드2: 자동화 실행 구축 (2주 ~ 4주)",
                "deliverable": "운영 가능한 자동화 구성 + 자동화 운영 가이드 문서",
                "items": [
                    "자동화 흐름 개요",
                    "실행/중지 방법",
                    "기본 장애 점검 포인트",
                    "수정 지점(변수/연동 포인트)",
                ],
            },
            {
                "id": "handover-outsourcing",
                "title": "카드3: 외주용역 집중 트랙 (4주 ~ 8주)",
                "deliverable": "구축 결과물 + 운영 이관 문서 (후속 지원 범위 별도 합의)",
                "items": [
                    "구성 개요: 개발 스택, PaaS/인프라, 연동 구조",
                    "배포/실행: 배포 절차, 서버 재시작 방법, 기본 롤백 절차",
                    "환경설정: 필수 환경변수 목록(값 제외), 비밀정보 관리 위치",
                    "운영 점검: 로그 위치, 1차 장애 점검 순서, 자주 발생 이슈 대응",
                    "지원 채널: 플랫폼 고객센터/지원 경로, 내부 에스컬레이션 경로",
                ],
            },
        ],
    },
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
            "result": "온라인 관람 + 오디오 해설 중심의 큐레이션 서비스 최소 기능 제품 구축",
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
            "q": "문의는 어떻게 진행되나요?",
            "a": "기본 채널은 help@quroom.kr 이메일입니다.",
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
        "description": "자동화 실행 진단, 자동화 실행 구축, 외주용역 트랙으로 아이디어를 실행 가능한 제품과 수익으로 연결합니다.",
        "primary_cta": {"label": "창업자 상담 신청", "href": "#contact"},
        "secondary_cta": {"label": "제공 서비스 확인", "href": "#services"},
        "service_target": "founders",
        "faq": [
            {
                "q": "범위는 어떻게 확정하나요?",
                "a": "초기 진단에서 우선순위를 정하고, 범위/일정/비용을 합의한 뒤 시작합니다.",
            },
            {
                "q": "커피챗에서는 무엇을 이야기하나요?",
                "a": "자동화, 제품화, 사업 실행에 대해 현재 막힌 지점을 가볍게 점검하고 다음 액션을 정리합니다.",
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
        "title": {
            "ko": "외국인 개발자를 위한 한국 취업 전략 파트너",
            "en": "Get a Korea Job Strategy Tailored to Your Stage",
        },
        "description": {
            "ko": "처음에는 간단히 시작하고, 준비가 되면 매칭 프로필을 완성해 연결 가능성을 높입니다.",
            "en": "Start simple, move at your pace, and grow into a matching-ready profile.",
        },
        "regional_support_note": {
            "ko": "광주/전남은 로컬 맥락을 살린 대면 지원을 우선하고, 다른 지역은 온라인 매칭과 원격 가이드를 기본으로 지원합니다.",
            "en": "Based in Gwangju. In-person support is prioritized for Gwangju/Jeonnam, while other regions are supported through online matching and remote guidance.",
        },
        "primary_cta": {
            "label": {"ko": "취업 전략 받기", "en": "Get My Job Search Strategy"},
            "href": "#quick-intake",
        },
        "secondary_cta": {
            "label": {"ko": "제공 서비스 보기", "en": "View Services"},
            "href": "#services",
        },
        "service_target": "foreign_developers",
        "credibility_signals": [
            {
                "ko": "삼성전자 실무 경험 기반 멘토링",
                "en": "Mentoring grounded in Samsung Electronics practical experience",
            },
            {
                "ko": "전남대 출신 로컬 맥락 이해와 커뮤니티 연결 경험",
                "en": "Local context understanding and community linkage experience in Gwangju/Jeonnam",
            },
            {
                "ko": "다수 개발사 협업 네트워크 기반 실무 연계 지원",
                "en": "Practical linkage support through multi-company collaboration networks",
            },
            {
                "ko": "공인중개사 자격 기반 생활/정착 맥락 이해",
                "en": "Settlement context understanding backed by licensed real-estate experience",
            },
        ],
        "scope_boundary": {
            "ko": "언어/비자/주거 관련 네트워크 연결은 지원하며, 비자·법률 자문을 직접 대행하지는 않습니다.",
            "en": "We support language/visa/housing network connections, but do not directly provide visa or legal representation.",
        },
        "faq": [
            {
                "q": {
                    "ko": "연계 프로세스는 어떻게 진행되나요?",
                    "en": "How does the matching process work?",
                },
                "a": {
                    "ko": "역량/희망 직무 확인 후 매칭, 온보딩 가이드, 초기 실무 적응 지원 순서로 진행됩니다.",
                    "en": "We proceed through profile review, matching, onboarding guidance, and early-stage practical adaptation support.",
                },
            },
            {
                "q": {
                    "ko": "무엇을 준비해야 하나요?",
                    "en": "What should I prepare?",
                },
                "a": {
                    "ko": "이력/프로젝트 요약, 희망 직무/기술 스택, 협업 가능한 근무 조건을 준비하면 빠르게 진행됩니다.",
                    "en": "Prepare your profile/project summary, preferred role and stack, and collaboration constraints to accelerate matching.",
                },
            },
            {
                "q": {
                    "ko": "지원 범위는 어디까지인가요?",
                    "en": "What is included in your support scope?",
                },
                "a": {
                    "ko": "개발사 네트워크 연결, 언어 코치/행정사/주거 정보 연계까지 지원하며, 비자·법률 자문 자체는 전문기관과 연계합니다.",
                    "en": "We support developer network matching plus language/administrative/housing connections, while visa and legal advisory are handled through specialized partners.",
                },
            },
            {
                "q": {
                    "ko": "비용은 어떻게 정해지나요?",
                    "en": "How is pricing determined?",
                },
                "a": {
                    "ko": "요청 범위와 연결 난이도에 따라 상담 후 개별 안내합니다.",
                    "en": "Pricing is provided after consultation based on requested scope and matching complexity.",
                },
            },
            {
                "q": {
                    "ko": "광주만 지원하나요?",
                    "en": "Do you only support Gwangju?",
                },
                "a": {
                    "ko": "광주/전남은 로컬 맥락을 살린 대면 지원을 우선할 수 있고, 다른 지역은 온라인 매칭과 원격 가이드를 기본으로 진행합니다.",
                    "en": "Gwangju/Jeonnam candidates can be supported with local in-person context when needed, while other regions are supported online first.",
                },
            },
        ],
        "kpi": ["foreign_linkage_inquiry_submit", "foreign_linkage_meeting_booked"],
    },
}


def _normalize_locale(locale: str | None) -> str:
    if locale in SUPPORTED_LOCALE_SET:
        return str(locale)
    return SAFE_LOCALE


def _is_locale_dict(value: object) -> bool:
    return (
        isinstance(value, dict)
        and bool(value)
        and set(value).issubset(SUPPORTED_LOCALE_SET)
    )


def _resolve_locale_value(
    value: dict[str, object],
    locale: str,
    page_default_locale: str,
    *,
    key_path: str,
) -> object:
    fallback_chain: list[str] = []
    for candidate in (locale, page_default_locale, SAFE_LOCALE):
        if candidate not in fallback_chain:
            fallback_chain.append(candidate)
    for candidate in fallback_chain:
        if candidate in value:
            return value[candidate]
    logger.warning(
        "Missing localized copy for key '%s' (requested=%s, page_default=%s)",
        key_path,
        locale,
        page_default_locale,
    )
    return ""


def _localize_value(
    value: object,
    locale: str,
    page_default_locale: str,
    *,
    key_path: str,
) -> object:
    if _is_locale_dict(value):
        return _resolve_locale_value(
            value, locale, page_default_locale, key_path=key_path
        )
    if isinstance(value, dict):
        return {
            key: _localize_value(
                item,
                locale,
                page_default_locale,
                key_path=f"{key_path}.{key}",
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [
            _localize_value(
                item,
                locale,
                page_default_locale,
                key_path=f"{key_path}[{index}]",
            )
            for index, item in enumerate(value)
        ]
    if isinstance(value, str) and locale == "en":
        return EN_TRANSLATIONS.get(value, value)
    return value


def build_page_content(
    persona: str | None = None,
    *,
    locale: str = SAFE_LOCALE,
    page_default_locale: str = SAFE_LOCALE,
) -> dict:
    resolved_locale = _normalize_locale(locale)
    resolved_page_default = _normalize_locale(page_default_locale)
    content = deepcopy(SHARED_CONTENT)
    if persona is None:
        content["services"] = [
            service
            for service in SERVICE_CARDS
            if "founders" in service["persona_targets"]
        ]
        content["faq"] = PERSONA_CONTENT["founders"]["faq"]
        content["kpi"] = PERSONA_CONTENT["founders"]["kpi"]
        return _localize_value(
            content, resolved_locale, resolved_page_default, key_path="content"
        )

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
    return _localize_value(
        content, resolved_locale, resolved_page_default, key_path="content"
    )


def build_career_ranges(
    *, locale: str = SAFE_LOCALE, page_default_locale: str = SAFE_LOCALE
) -> list[dict]:
    resolved_locale = _normalize_locale(locale)
    resolved_page_default = _normalize_locale(page_default_locale)
    return _localize_value(
        deepcopy(CAREER_RANGES),
        resolved_locale,
        resolved_page_default,
        key_path="career_ranges",
    )


# Backward compatibility for existing imports
SITE_CONTENT = SHARED_CONTENT

# Date format: YYYY-MM-DD
# Timeline label rule: "연도(또는 기간) + 핵심 행동/성과" 형식을 유지한다.
CAREER_RANGES = [
    {
        "start": "2012-08-01",
        "end": "2014-10-31",
        "label": "삼성전자 S/W 엔지니어",
        "count_for_career": True,
    },
    {
        "start": "2015-01-01",
        "end": "2015-12-31",
        "label": "공인중개사 자격 취득",
        "count_for_career": False,
    },
    {
        "start": "2016-01-01",
        "end": "2016-12-31",
        "label": "중개업 활동, 자동화로 업무 효율화",
        "count_for_career": False,
    },
    {
        "start": "2017-01-01",
        "end": "2017-12-31",
        "label": "쉐어하우스 창업 및 확장",
        "count_for_career": False,
    },
    {
        "start": "2018-06-01",
        "end": None,
        "label": "소셜벤처 창업 및 큐룸 개발/운영",
        "count_for_career": True,
    },
]
