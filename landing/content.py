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
    "2018.06 설립 · 총 개발 경력 {career_duration} · 자체 제품 9개, 외주 개발 1개": "Founded in 2018.06 · Total development experience {career_duration} · 9 owned products, 1 client project",
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
    "협의": "To be discussed",
    "60만원 ~ 150만원": "KRW 600,000 - 1,500,000",
    "상담 후 결정": "Determined after consultation",
    "2026.09 ~ 현재 (개발 중)": "2026.09 - Present (In Development)",
    "2026.09 ~ 현재": "2026.09 - Present",
    "2026.07 ~ 현재": "2026.07 - Present",
    "2025.04 ~ 현재": "2025.04 - Present",
    "2025.01 ~ 현재": "2025.01 - Present",
    "2026.03 ~ 2026.05": "2026.03 - 2026.05",
    "AI콜봇 NoMiss (getNomiss)": "AI Callbot NoMiss (getNomiss)",
    "광주 도서관 통합검색 (library.quroom.kr)": "Gwangju Library Integrated Search (library.quroom.kr)",
    "단어장앱 (voca.quroom.kr)": "Vocab App (voca.quroom.kr)",
    "손해사정사 문서 자동화 서비스 (R&D)": "Claims Document Automation Service (R&D)",
    "손해사정사를 위한 고객 관리와 문서 초안 생성 기능을 구현한 실험 프로젝트": "An experimental project that implemented customer management and document draft generation for claims adjusters.",
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
    "사업을 이해하고\n앱·웹 개발을 믿고 맡길 수 있는 파트너": "Business-aware app and web development partner\nyou can trust with the work.",
    "앱·웹 서비스의 문제 정의, 범위 정리, 개발, 배포까지 한 사람이 이어서 맡습니다.": "One person carries app and web service work from problem definition and scope alignment to development and deployment.",
    "업무 범위와 우선순위를 먼저 조율하고, 필요한 부분은 직접 맡아 진행합니다.": "We align scope and priorities first, then directly handle the parts that need to move.",
    "업무 범위와 우선순위를 먼저 맞추고, 필요한 실행은 직접 맡아 진행합니다.": "We align scope and priorities first, then directly handle the execution that needs to move.",
    "외주용역 집중 트랙은 한 타임에 한 고객사만 진행합니다.": "The dedicated outsourcing track runs with one client at a time.",
    "외주용역 집중 트랙은 한 번에 한 고객사만 진행합니다.": "The dedicated outsourcing track runs with one client at a time.",
    "요구사항부터 같이 정리합니다.": "We start by aligning requirements together.",
    "제품, 운영, 외주가 따로 움직이면 속도가 바로 떨어집니다.": "When product, operations, and outsourcing move separately, speed drops immediately.",
    "요구사항이 모호하면 일정과 비용이 쉽게 흔들립니다.": "When requirements are unclear, schedule and cost become unstable.",
    "예산과 우선순위에 맞춰 범위를 조율하고, 필요한 실행은 직접 맡아 진행합니다.": "We align scope to budget and priorities, then directly handle the execution that should be delegated.",
    "문의부터 실행까지 진행 방식": "How We Work From Inquiry to Delivery",
    "사전 진단 상담": "Initial Diagnosis Call",
    "현재 상황, 목표, 제약을 함께 정리해 우선순위를 확정합니다.": "We align your current situation, goals, and constraints to set priorities.",
    "실행 범위 설계": "Execution Scope Design",
    "2주~8주 단위 실행 범위, 일정, 산출물 기준을 명확히 합의합니다.": "We align execution scope, timeline, and deliverable criteria for a 2-8 week cycle.",
    "구현 및 점검": "Implementation and Review",
    "주차별 결과를 공유하고 위험 요소를 점검해 일정과 품질을 관리합니다.": "We manage schedule and quality with weekly updates and risk reviews.",
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
    "자체 제품 6, 외주 개발 1": "6 owned products, 1 client project",
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
    "외주용역 집중 트랙": "Dedicated Outsourcing Track",
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
    "바로 맡겨야 할 일과 아직 정리할 일을 구분해, 실제 실행으로 이어지게 돕습니다.": "We help separate what should be delegated now from what still needs alignment, then move it into real execution.",
    "이런 경험과 기준으로 일합니다": "This is the experience and standard I work from.",
    "왜 제가 맡을 수 있는지": "Why I can take this on",
    "삼성전자 포함 총 개발 경력 {career_duration}": "Total development experience {career_duration}, including Samsung Electronics",
    "삼성전자 제품 개발 경험과 자체 제품 운영 경험이 있습니다.": "I have product development experience at Samsung Electronics and direct experience operating owned products.",
    "그래서 예쁜 화면이나 기능 목록만 보지 않고, 우선순위·배포·운영·수정 요청까지 같이 봅니다.": "That means I look beyond screens and feature lists, covering priorities, deployment, operations, and change requests.",
    "자체 제품 기획·개발·운영 경험": "Experience planning, building, and operating owned products",
    "총 7개 프로젝트 경험과 운영 이관 기준 정리": "Experience across 7 projects with clear handover criteria",
    "외주 개발: 미술관 큐레이션 서비스": "Client project: Museum Curation Service",
    "자체 제품과 외주 개발을 구분해 검증 가능한 사례만 제시": "Only verifiable examples, clearly separated between owned products and client work",
    "외주 집중 트랙은 한 타임 1고객만 진행해 집중도를 높입니다": "The dedicated outsourcing track runs one client at a time to keep focus high.",
    "외주 집중 트랙은 한 번에 한 고객사만 진행해 집중도를 높입니다": "The dedicated outsourcing track runs one client at a time to keep focus high.",
    "대표자 경력과 프로젝트 이력은 LinkedIn에서 바로 확인 가능": "The founder's career and project history can be checked directly on LinkedIn.",
    "이런 상황이라면 함께하기 좋습니다": "These are the situations where working together fits well.",
    "범위와 목표가 어느 정도 잡혀 있으면, 첫 대화에서 다음 액션까지 정리하기 쉽습니다.": "If scope and goals are roughly set, it is easier to sort out next actions in the first conversation.",
    "이런 상황이라면 대화가 잘 됩니다": "These are the situations where the conversation tends to go well.",
    "이런 상황이면 첫 상담이 수월합니다": "These are the situations where the first consultation tends to move smoothly.",
    "범위와 목표가 어느 정도 보이면, 첫 대화에서 무엇부터 할지 같이 정리할 수 있습니다.": "If scope and goals are visible enough, we can sort out what to do first in the first conversation.",
    "범위와 목표가 어느 정도 보이면, 첫 대화에서 무엇부터 할지 더 빠르게 정리할 수 있습니다.": "If scope and goals are visible enough, we can sort out what to do first more quickly in the first conversation.",
    "이번 분기 안에 진행해야 할 과제가 있는 경우": "When there is work that needs to move within this quarter",
    "담당자와 의사결정자가 어느 정도 정해져 있는 경우": "When the owner and decision-maker are roughly in place",
    "문의 전에 범위나 우선순위를 한번 같이 정리해보고 싶은 경우": "When you want to sort out scope or priorities before making a full inquiry",
    "기본 연락은 이메일이나 문의 폼으로 부탁드립니다.": "Please use email or the contact form as the primary channel.",
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
    "창업자/소상공인을 위한 제품화·운영 실행 지원": "Productization and operations execution support for founders and small business owners.",
    "문제 정의, 우선순위 정리, 구현, 배포까지 한 흐름으로 봅니다.": "We look at the full flow from problem definition and prioritization to implementation and deployment.",
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
    "자체 제품 6, 외주 1": "6 owned products, 1 client project",
    "현재": "Present",
    "30분": "30 min",
    "무료": "Free",
    "삼성전자 S/W 엔지니어": "Samsung Electronics S/W Engineer",
    "공인중개사 자격 취득": "Licensed Real-Estate Agent",
    "중개업 활동, 자동화로 업무 효율화": "Brokerage operations with automation-driven efficiency",
    "쉐어하우스 창업 및 확장": "Share-house startup and expansion",
    "소셜벤처 창업 및 큐룸 개발/운영": "Social venture founding and QUROOM development/operations",
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
        "title": "외주용역 집중 트랙",
        "summary": "범위가 크고 난도가 높은 과제를 일정 잡고 진행하는 트랙입니다.",
        "items": [
            "첫 주에 범위·일정·완료 기준 고정",
            "주차별 마일스톤으로 진행 상황 공유",
            "운영 이관과 초기 이슈 점검 범위를 별도 합의",
        ],
        "duration": "협의",
        "price": "협의",
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
            "ko": "커리어 전략",
            "en": "Career Strategy",
        },
        "summary": {
            "ko": "한국에서 어떤 방향으로 시작할지, 지금 단계에서 무엇부터 준비할지 함께 정리합니다.",
            "en": "Clarify where to start and what to prepare first for working in Korea.",
        },
        "items": [
            {
                "ko": "현재 준비 상태와 목표 방향 점검",
                "en": "Review your current readiness and direction",
            },
            {
                "ko": "우선순위가 선명한 다음 액션 정리",
                "en": "Set the next action with practical priority",
            },
            {
                "ko": "한국 취업·연결을 위한 시작 가이드",
                "en": "Start guidance for entering work opportunities and networks in Korea",
            },
        ],
        "duration": "상시 운영",
        "price": "상담 후 결정",
        "deliverable": {
            "ko": "현재 단계 요약 + 다음 액션 가이드",
            "en": "Current-stage summary + next-step guidance",
        },
        "audience": {
            "ko": "한국에서 일하거나 기회를 넓히고 싶은 외국인 인재",
            "en": "International talent who want a clearer starting point for working in Korea",
        },
        "cta_label": {"ko": "문의하기", "en": "Send Inquiry"},
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
    {
        "id": "foreign-dev-profile-readiness",
        "title": {
            "ko": "이력서 · 포트폴리오 준비",
            "en": "Resume / Portfolio Readiness",
        },
        "summary": {
            "ko": "이력서, LinkedIn, GitHub, 포트폴리오를 매칭 검토에 맞게 정리합니다.",
            "en": "Sharpen your resume, LinkedIn, GitHub, and portfolio for matching review.",
        },
        "items": [
            {
                "ko": "이력서와 LinkedIn 핵심 정보 정리",
                "en": "Tighten your resume and LinkedIn essentials",
            },
            {
                "ko": "GitHub·포트폴리오 링크 구조 점검",
                "en": "Review GitHub and portfolio link structure",
            },
            {
                "ko": "소개 메시지와 프로필 문장 다듬기",
                "en": "Refine intro copy and profile messaging",
            },
        ],
        "duration": "상시 운영",
        "price": "상담 후 결정",
        "deliverable": {
            "ko": "프로필 체크리스트 + 개선 가이드",
            "en": "Profile checklist + improvement guidance",
        },
        "audience": {
            "ko": "특히 외국인 소프트웨어 엔지니어로서 한국 취업 준비를 구체화하려는 분",
            "en": "Especially for foreign software engineers preparing for practical review",
        },
        "cta_label": {"ko": "프로필 작성하기", "en": "Open Profile Form"},
        "cta_href": "#matching-profile",
        "persona_targets": ["foreign_developers"],
    },
    {
        "id": "foreign-dev-settlement-network",
        "title": {
            "ko": "한국 적응 가이드",
            "en": "Korea Guidance",
        },
        "summary": {
            "ko": "한국 생활과 일 적응에 필요한 언어, 행정, 주거 관련 실무 가이드를 연결합니다.",
            "en": "Connect practical guidance for language, administration, and settling into work and life in Korea.",
        },
        "items": [
            {
                "ko": "한국어 학습·커뮤니케이션 가이드 안내",
                "en": "Connect Korean learning and communication guidance",
            },
            {
                "ko": "비자·체류 이슈를 위한 전문 파트너 연결",
                "en": "Connect licensed partners for visa and stay issues",
            },
            {
                "ko": "주거 탐색과 생활 적응을 위한 초기 정보 연결",
                "en": "Connect early guidance for housing search and life setup",
            },
        ],
        "duration": "요청 시 수시",
        "price": "상담 후 결정",
        "deliverable": {
            "ko": "적응 가이드 + 파트너 안내",
            "en": "Korea guidance plan + partner referrals",
        },
        "audience": {
            "ko": "한국에서 일하고 적응하는 데 실무 가이드가 필요한 외국인 인재",
            "en": "International talent who need practical guidance for working in Korea",
        },
        "cta_label": {"ko": "가이드 문의하기", "en": "Ask About Korea Guidance"},
        "cta_href": "#contact",
        "persona_targets": ["foreign_developers"],
    },
]

SHARED_CONTENT = {
    "site_name": "큐룸 (QUROOM)",
    "seo_title": {
        "ko": "큐룸 (QUROOM) | 웹·앱 외주 개발 & 린 MVP 개발사",
        "en": "QUROOM | Web & App Development Partner & Lean MVP Builder",
    },
    "seo_description": {
        "ko": "큐룸(QUROOM)은 8년 차 삼성전자 출신 1인 풀스택 개발사입니다. 웹·앱 외주 개발, 린 MVP 구현, 실서버 배포 및 운영 이관까지 대표가 직접 책임집니다.",
        "en": "QUROOM is an 8-year full-stack software development studio led by a former Samsung engineer, taking direct responsibility from MVP build to deployment.",
    },
    "hero_eyebrow": {
        "ko": "웹·앱 개발부터 기술 상담까지",
        "en": "From web and app development to technical consultation",
    },
    "headline": {
        "ko": "개발 전체를 맡기셔도,\n막힌 부분만 맡기셔도 됩니다.",
        "en": "Bring me the whole build,\nor just the part where you are stuck.",
    },
    "subcopy": {
        "ko": "기획부터 개발, 배포, 운영까지 직접 해왔습니다. 전 과정을 맡기셔도 되고, 막힌 부분만 편하게 물어보셔도 됩니다. 30분 커피챗은 무료입니다.",
        "en": "I have handled planning, development, deployment, and operations firsthand. You can bring me the whole project or just the part where you are stuck. The 30-minute coffee chat is free.",
    },
    "hero_primary_cta": {"ko": "무료 커피챗 신청", "en": "Book a Free Chat"},
    "hero_secondary_cta": {"ko": "수행 사례 보기", "en": "View Client Work"},
    "response_note": {
        "ko": "아직 무엇을 맡길지 정하지 않았어도 괜찮습니다. 대표가 직접 보고 영업일 1~2일 안에 답합니다.",
        "en": "It is fine if you have not decided what to delegate yet. The founder replies within 1-2 business days.",
    },
    "career_proof_prefix": {
        "ko": "삼성전자 포함",
        "en": "Including Samsung",
    },
    "proof_items": [
        {
            "label": {"ko": "개발 경력", "en": "Experience"},
            "value": {"ko": "{career_duration}", "en": "{career_duration}"},
        },
        {
            "label": {"ko": "수행 방식", "en": "Delivery"},
            "value": {"ko": "대표 1인 직접 수행", "en": "Founder-led directly"},
        },
        {
            "label": {"ko": "프로젝트 기간", "en": "Project length"},
            "value": {"ko": "협의", "en": "To be discussed"},
        },
        {
            "label": {"ko": "예산", "en": "Budget"},
            "value": {"ko": "협의", "en": "To be discussed"},
        },
        {
            "label": {"ko": "동시 진행", "en": "Capacity"},
            "value": {"ko": "한 고객사", "en": "One client at a time"},
        },
    ],
    "services_label": {"ko": "서비스", "en": "Services"},
    "services_title": {
        "ko": "필요한 기능부터 정하고\n직접 개발합니다.",
        "en": "Define what needs to be built,\nthen build it directly.",
    },
    "services_intro": {
        "ko": "무엇을 만들지 완전히 정리되지 않아도 괜찮습니다. 첫 상담에서 꼭 필요한 기능과 나중에 해도 될 기능부터 나눕니다.",
        "en": "You do not need a finished specification. In the first consultation, we separate what needs to be built now from what can wait.",
    },
    "outsourcing_services": [
        {
            "title": {"ko": "신규 웹·앱 MVP", "en": "New Web or App MVP"},
            "description": {
                "ko": "아이디어를 화면 흐름과 기능 목록으로 정리하고, 먼저 만들 범위를 정합니다.",
                "en": "Turn your idea into screen flows and a feature list, then decide what to build first.",
            },
        },
        {
            "title": {"ko": "사내 업무 도구", "en": "Internal Work Tools"},
            "description": {
                "ko": "엑셀이나 여러 서비스에 흩어진 업무를 한곳에서 처리할 수 있게 만듭니다.",
                "en": "Bring work scattered across spreadsheets and other services into one place.",
            },
        },
        {
            "title": {"ko": "기존 서비스 개선", "en": "Existing Product Improvement"},
            "description": {
                "ko": "오류, 느린 화면, 반복 문의를 확인하고 불편이 큰 문제부터 고칩니다.",
                "en": "Review errors, slow screens, and repeated support requests, then fix the biggest problems first.",
            },
        },
    ],
    "deliverables_title": {"ko": "프로젝트에 포함되는 것", "en": "What Is Included"},
    "deliverables": [
        {
            "ko": "요구사항·제외 범위·완료 기준",
            "en": "Requirements, exclusions, and completion criteria",
        },
        {"ko": "반응형 웹 또는 앱 화면", "en": "Responsive web or app interface"},
        {"ko": "백엔드·API·관리자 기능", "en": "Backend, API, and admin capabilities"},
        {"ko": "테스트와 운영 환경 배포", "en": "Testing and production deployment"},
        {
            "ko": "운영 이관 문서와 점검 항목",
            "en": "Operational handover guide and checks",
        },
    ],
    "deliverables_note": {
        "ko": "디자인이나 외부 서비스 연동이 필요하면 첫 상담에서 함께 확인합니다.",
        "en": "If you need design work or external service integrations, we will cover them in the first consultation.",
    },
    "engagements": [
        {
            "title": {"ko": "30분 커피챗", "en": "30-minute Coffee Chat"},
            "description": {
                "ko": "막힌 부분만 이야기해도 괜찮습니다",
                "en": "Start with the part where you are stuck",
            },
            "terms": {"ko": "30분 · 무료", "en": "30 min · Free"},
            "cta": {"ko": "무료 커피챗 신청", "en": "Book a Free Chat"},
            "inquiry_type": "coffee_chat",
        },
        {
            "title": {"ko": "15분 코드·배포 진단", "en": "15-minute Code & Deploy Diagnosis"},
            "description": {
                "ko": "Cursor·Claude 생성 코드 배포 및 결제 연동 에러 긴급 점검",
                "en": "Emergency review for AI-generated code, deployment, and payment webhook errors",
            },
            "terms": {"ko": "15분 · 무료", "en": "15 min · Free"},
            "cta": {"ko": "15분 진단 신청", "en": "Request Diagnosis"},
            "inquiry_type": "vibe_diagnosis",
        },
        {
            "title": {"ko": "외주 WBS 사전 검수", "en": "Outsourcing WBS Scope Review"},
            "description": {
                "ko": "계약 전 WBS 5대 제외범위 명시 및 추가금 분쟁 예방 검수",
                "en": "Pre-contract WBS out-of-scope review to prevent fee disputes",
            },
            "terms": {"ko": "무료 검수", "en": "Free Review"},
            "cta": {"ko": "WBS 검수 신청", "en": "Request WBS Review"},
            "inquiry_type": "wbs_review",
        },
        {
            "title": {"ko": "외주 프로젝트", "en": "Development Project"},
            "description": {
                "ko": "기획, 개발, 배포 중 필요한 부분만 맡길 수 있습니다",
                "en": "Choose the parts you need: planning, development, or deployment",
            },
            "terms": {
                "ko": "기간·예산 협의",
                "en": "Timeline and budget to be discussed",
            },
            "cta": {"ko": "프로젝트 상담", "en": "Discuss a Project"},
            "inquiry_type": "outsourcing",
        },
    ],
    "founder_capacity_policy": "외주용역 집중 트랙은 한 번에 한 고객사만 진행합니다.",
    "hero_support_text": (
        "2018.06 설립 · 총 개발 경력 {career_duration} · 자체 제품 9개, 외주 개발 1개"
    ),
    "about_title": "왜 제가 맡을 수 있는지",
    "about_body": [
        "삼성전자 제품 개발 경험과 자체 제품 운영 경험이 있습니다.",
        "그래서 예쁜 화면이나 기능 목록만 보지 않고, 우선순위·배포·운영·수정 요청까지 같이 봅니다.",
    ],
    "client_work_label": {"ko": "외주 수행 사례", "en": "Client Work"},
    "client_work_note": {
        "ko": "고객사 요청에 따라 역할, 기간, 결과만 공개합니다.",
        "en": "At the client's request, only the role, timeline, and outcome are public.",
    },
    "client_work_intro": {
        "ko": "작품 정보와 오디오 해설을 한곳에서 볼 수 있게 만든 프로젝트입니다.",
        "en": "This project brings artwork information and audio guides together in one place.",
    },
    "products_label": {"ko": "직접 만든 제품", "en": "Owned Products"},
    "products_title": {
        "ko": "직접 만들고 운영한\n자체 제품 9개",
        "en": "Nine products I built\nand operated myself.",
    },
    "products_intro": {
        "ko": "직접 출시하고 운영하면서 고객 요청, 장애, 서버 비용을 다뤘습니다. 그래서 납품으로 끝내지 않고 배포 뒤 운영까지 생각합니다.",
        "en": "I have handled customer requests, incidents, and server costs after launching my own products. That is why I plan for operations after delivery.",
    },
    "execution_process_label": {"ko": "진행 방식", "en": "Process"},
    "execution_process_title": {
        "ko": "매주 결과물을 보여드리고\n다음 할 일을 정합니다.",
        "en": "Review working software each week\nand decide what comes next.",
    },
    "execution_process": [
        {
            "period": {"ko": "1주차", "en": "Week 1"},
            "title": {"ko": "목표와 범위 확정", "en": "Confirm Goals and Scope"},
            "description": {
                "ko": "만들 기능과 만들지 않을 기능, 일정, 완료 조건을 함께 적습니다.",
                "en": "Write down what will and will not be built, the schedule, and what counts as done.",
            },
        },
        {
            "period": {"ko": "2~7주차", "en": "Weeks 2-7"},
            "title": {"ko": "구현과 주간 검토", "en": "Build and Review Weekly"},
            "description": {
                "ko": "실행 가능한 화면과 기능을 보여드리고 다음 주 우선순위를 정합니다.",
                "en": "Review usable screens and features, then set priorities for the following week.",
            },
        },
        {
            "period": {"ko": "마지막 주", "en": "Final Week"},
            "title": {"ko": "배포와 운영 이관", "en": "Deploy and Hand Over"},
            "description": {
                "ko": "서비스를 배포하고 직접 운영할 수 있도록 점검 방법과 수정할 곳을 알려드립니다.",
                "en": "Deploy the service and show your team how to check it and where to make changes.",
            },
        },
    ],
    "profile_label": {"ko": "대표 소개", "en": "Founder"},
    "profile_title": {
        "ko": "개발자이면서\n사업 운영자입니다.",
        "en": "A software engineer\nand business operator.",
    },
    "profile_lead": {
        "ko": "삼성전자에서 소프트웨어를 개발했고, 이후 8년 차 개발사 큐룸(QUROOM)을 설립하여 직접 운영해왔습니다. 개발뿐 아니라 고객 응대, 비용, 현장 운영도 직접 해봤습니다.",
        "en": "I developed software at Samsung Electronics, then founded and operated the 8-year software studio QUROOM. I have handled customers, costs, and day-to-day operations as well as development.",
    },
    "profile_body": {
        "ko": "개발 전에는 누가 쓰고 누가 운영할지부터 묻습니다. 배포 후 직접 관리할 수 있는 방법도 함께 남겨드립니다.",
        "en": "Before development, I ask who will use and operate the product. I also leave your team with a practical way to manage it after launch.",
    },
    "profile_link_label": {
        "ko": "LinkedIn에서 상세 경력 확인",
        "en": "View Full Experience on LinkedIn",
    },
    "faq_label": {"ko": "자주 묻는 질문", "en": "FAQ"},
    "faq_title": {
        "ko": "상담 전에 자주 묻는 내용입니다.",
        "en": "Common Questions Before a Consultation",
    },
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
            "description": "자체 제품 6, 외주 1",
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
    "services_section_subtitle": "바로 맡겨야 할 일과 아직 정리할 일을 구분해, 실제 실행으로 이어지게 돕습니다.",
    "fit_section_title": "이런 상황이라면 함께하기 좋습니다",
    "fit_section_intro": "범위와 목표가 어느 정도 잡혀 있으면, 첫 대화에서 다음 액션까지 정리하기 쉽습니다.",
    "hero_trust_title": "이런 경험과 기준으로 일합니다",
    "hero_trust_points": [
        "삼성전자 포함 총 개발 경력 {career_duration}",
        "총 7개 프로젝트 경험과 운영 이관 기준 정리",
        "외주 집중 트랙은 한 번에 한 고객사만 진행해 집중도를 높입니다",
        "대표자 경력과 프로젝트 이력은 LinkedIn에서 바로 확인 가능",
    ],
    "contact_label": {"ko": "편하게 문의하세요", "en": "Start a Conversation"},
    "contact_title": {
        "ko": "지금 고민 중인 내용을\n보내주세요.",
        "en": "Tell me what you are\nworking through.",
    },
    "contact_intro": {
        "ko": "전체 개발, 일부 기능 구현, 기술 검토 중 어떤 문의든 가능합니다.",
        "en": "You can ask about a full build, one feature, or a technical review.",
    },
    "contact_response": {
        "ko": "대표가 직접 확인하고 영업일 1~2일 내 답변드립니다.",
        "en": "The founder replies within 1-2 business days.",
    },
    "contact_points": [
        "이번 분기 안에 진행해야 할 과제가 있는 경우",
        "담당자와 의사결정자가 어느 정도 정해져 있는 경우",
        "문의 전에 범위나 우선순위를 한번 같이 정리해보고 싶은 경우",
        "기본 연락은 이메일이나 문의 폼으로 부탁드립니다.",
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
            "name": "AI콜봇 NoMiss (getNomiss)",
            "type_label": "자체 제품",
            "period": "2026.09 ~ 현재 (개발 중)",
            "summary": "1인 미용실·출장설비를 위한 30초 AI 음성 응대 및 모바일 접수 카드 솔루션 (지난주 착수, 현재 개발 중)",
            "problem": "1인 매장 및 현장 작업자가 시술·작업 중 전화를 받지 못해 고객이 타 매장으로 이탈하는 문제",
            "solution": "통신사 착신전환 연동 30초 AI 음성 응대, 더블 부킹 방지 일정 가드레일 접수, 통화 종료 즉시 모바일 증상 사진 접수 링크(SMS/알림톡) 자동 발송",
            "result": "지난주 개발 착수 후 핵심 음성 대화 파이프라인 및 백엔드 프로토타입 구축 진행 중",
            "tech": "FastAPI, Twilio, OpenAI Realtime API, WebSocket, Next.js",
            "image": "portfolio/thumb/2026-nomiss-thumb-v1.jpg",
            "link": "",
            "is_in_development": True,
        },
        {
            "name": "단어장앱 (voca.quroom.kr)",
            "type_label": "자체 제품",
            "period": "2026.09 ~ 현재",
            "summary": "SM-2 간격 반복 알고리즘 기반의 오프라인 우선(Offline-First) 단어 암기 웹앱 (voca.quroom.kr)",
            "problem": "통신 단절 환경(비행기, 이동 중)에서 앱이 멈추거나, 단어 카드 전환 시 발음 음성 딜레이로 학습 흐름이 끊기는 문제",
            "solution": "Next.js + Capacitor 기반 하이브리드 모바일 앱, IndexedDB(Dexie.js) 로컬 우선 저장 및 Web Audio API 사전 디코딩 최적화, SM-2 간격 반복 알고리즘 직접 구현",
            "result": "2주 전 개발 착수 후 voca.quroom.kr 배포 완료 및 오프라인 0ms 즉각 반응 학습 지원",
            "tech": "Next.js, TypeScript, IndexedDB, Web Audio API, Capacitor",
            "image": "portfolio/thumb/2025-son-vocab-thumb-v1.jpg",
            "link": "https://voca.quroom.kr",
            "is_in_development": False,
        },
        {
            "name": "광주 도서관 통합검색 (library.quroom.kr)",
            "type_label": "자체 제품",
            "period": "2026.07 ~ 현재",
            "summary": "광주광역시 전역 공공도서관 실시간 대출 상태 및 소장 도서 통합 검색 포털 (library.quroom.kr)",
            "problem": "도서관마다 분산된 전산 시스템으로 소장 도서 위치 및 실시간 대출 가능 여부를 확인하기 어려운 높은 탐색 비용",
            "solution": "공공데이터포털 OpenAPI 대량 수집 파이프라인(Celery+Redis), PostgreSQL FTS(tsvector/GIN) 기반 고속 검색 및 카카오 알림톡 반납 일정 알림 연동",
            "result": "2달 전 개발 착수 후 library.quroom.kr 배포 완료 및 분산 도서관 실시간 소장·대출 데이터 일괄 조회 제공",
            "tech": "Next.js, Django, PostgreSQL, Celery, Redis, pg_trgm",
            "image": "portfolio/thumb/2025-library-portal-thumb-v1.jpg",
            "link": "https://library.quroom.kr",
            "is_in_development": False,
        },
        {
            "name": "WishBox (소망창고) - Alpha",
            "type_label": "자체 제품",
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
            "name": "손해사정사 문서 자동화 서비스 (R&D)",
            "type_label": "자체 제품",
            "period": "2026.03 ~ 2026.05",
            "summary": "손해사정사를 위한 고객 관리와 문서 초안 생성 기능을 구현한 실험 프로젝트",
            "problem": "반복되는 고객 정보 관리와 손해사정 문서 초안 작성에 시간이 많이 드는 문제",
            "solution": "고객 CRM과 문서 초안 생성 기능을 구현해 실제 업무 적용 가능성을 확인",
            "result": "기능 구현 후 유료 사용 의사가 불확실해 2026년 5월 개발 종료",
            "tech": "Django, LLM",
            "image": "portfolio/thumb/2026-autodocx-thumb-v1.png",
            "link": "",
        },
        {
            "name": "PromptSpike",
            "type_label": "자체 제품",
            "period": "2025.04 ~ 2025.09",
            "summary": "여러 LLM 탭에 한 번에 프롬프트를 전송하고 템플릿으로 재사용하는 브라우저 확장",
            "problem": "멀티 LLM 사용이 보편화되면서 반복 재사용되는 프롬프트 입력 시간이 급격히 증가하는 시장 문제",
            "solution": "한 번 입력으로 다중 탭 동시 전송, 멀티스텝 플로 자동 진행, 긴 프롬프트 분할 전송 지원",
            "result": "반복 입력 시간을 줄이고 프롬프트 운영 효율 개선",
            "tech": "Chrome Extension, JavaScript, LLM Tab Control",
            "image": "portfolio/thumb/2025-promptspike-thumb-v1.jpg",
            "link": "https://chromewebstore.google.com/detail/promptspike-prompt-manage/khokpfkmdgimgfieinhffnhnmncoahpb",
        },
        {
            "name": "Obible (PWA 커뮤니티 성경 서비스)",
            "type_label": "자체 제품",
            "period": "2023.01 ~ 2024.06",
            "summary": "성경 읽기, 그룹 기반 커뮤니티, 댓글/하이라이트를 제공한 PWA 서비스",
            "problem": "신앙 커뮤니티 시장에서 개인 묵상, 소그룹 교제, 일정 운영이 여러 도구로 분산되어 참여 지속성이 떨어지는 문제",
            "solution": "읽기/코멘트/하이라이트 + 그룹 구독/초대 + 그룹 전용 피드로 공동체 기능 통합",
            "result": "온라인 커뮤니티 기반의 지속 읽기 경험 구축",
            "tech": "Docker, Celery 외 13+",
            "image": "portfolio/thumb/2023-obible-thumb-v1.jpg",
            "link": "https://github.com/quroom/obible/",
        },
        {
            "name": "Kids Travel Curating",
            "type_label": "자체 제품",
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
            "type_label": "외주 개발",
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
            "type_label": "자체 제품",
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
            "q": {
                "ko": "프로젝트 범위는 어떻게 정하나요?",
                "en": "How is the project scope defined?",
            },
            "a": {
                "ko": "첫 주에 만들 기능과 만들지 않을 기능을 적고 완료 조건을 정합니다. 새 요청이 생기면 일정과 비용이 얼마나 달라지는지 먼저 알려드립니다.",
                "en": "In the first week, we list what will and will not be built and agree on what counts as done. For new requests, I explain the schedule and cost changes first.",
            },
        },
        {
            "q": {
                "ko": "지불 조건은 어떻게 되나요?",
                "en": "What are the payment terms?",
            },
            "a": {
                "ko": "보통 착수금, 중간금, 잔금으로 나누거나 매월 청구합니다. 프로젝트 규모에 맞춰 상담할 때 정합니다.",
                "en": "Payment is usually split into a deposit, an interim payment, and a final payment, or billed monthly. We decide during the consultation based on the project size.",
            },
        },
        {
            "q": {
                "ko": "배포 후 유지보수도 가능한가요?",
                "en": "Is maintenance available after launch?",
            },
            "a": {
                "ko": "네. 직접 운영할 수 있도록 점검 방법과 수정할 곳을 문서로 드립니다. 이후 유지보수가 필요하면 기간과 범위를 따로 정합니다.",
                "en": "Yes. I provide a guide showing how to check the service and where to make changes. If you need ongoing maintenance, we agree on the timeline and scope separately.",
            },
        },
        {
            "q": {
                "ko": "어떤 프로젝트와 잘 맞나요?",
                "en": "Which projects are a good fit?",
            },
            "a": {
                "ko": "만들거나 고칠 대상이 있고, 진행 중 결정을 내려줄 담당자가 있으면 좋습니다. 아이디어만 있어도 커피챗에서 어디부터 확인할지 함께 이야기할 수 있습니다.",
                "en": "It helps to have something specific to build or improve and someone who can make decisions during the project. If you only have an idea, we can still use the coffee chat to decide what to check first.",
            },
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
        "name": "큐룸 (QUROOM)",
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
        "title": "창업자/소상공인을 위한 제품화·운영 실행 지원",
        "description": "문제 정의, 우선순위 정리, 구현, 배포까지 한 흐름으로 봅니다.",
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
        "meta_title": {
            "ko": "글로벌 인재 지원 | 큐룸",
            "en": "International Talent Support | QuRoom",
        },
        "label": {
            "ko": "글로벌 인재 지원",
            "en": "For International Talent",
        },
        "title": {
            "ko": "한국에서 일하려는 외국인 인재를 위한 실무 지원",
            "en": "Work in Korea with practical support",
        },
        "description": {
            "ko": "커리어 방향 정리, 이력서·포트폴리오 점검, 한국 생활·업무 적응 가이드까지 지금 단계에 맞는 다음 행동을 함께 정리합니다.",
            "en": "Career direction, resume or portfolio readiness, and Korea guidance to help you take the next realistic step.",
        },
        "focus_note": {
            "ko": "현재는 외국인 소프트웨어 엔지니어 지원에 가장 강합니다.",
            "en": "Currently strongest for foreign software engineers.",
        },
        "hero_support_buckets": [
            {"ko": "커리어 전략", "en": "Career strategy"},
            {"ko": "이력서 · 포트폴리오", "en": "Resume / portfolio"},
            {"ko": "한국 적응 가이드", "en": "Korea guidance"},
        ],
        "boundary_note": {
            "ko": "취업 보장이나 비자·법률 자문 대행은 하지 않으며, 필요한 경우 전문 파트너와 연결합니다.",
            "en": "We provide practical guidance and introductions, but not guaranteed placement or direct visa/legal representation.",
        },
        "regional_support_note": {
            "ko": "광주/전남은 오프라인 네트워킹과 대면 안내를 우선할 수 있고, 다른 지역은 온라인 중심으로 지원합니다.",
            "en": "Based in Gwangju. Gwangju/Jeonnam support can include in-person networking, while other regions are primarily supported online.",
        },
        "primary_cta": {
            "label": {"ko": "문의하기", "en": "Send Inquiry"},
            "href": "#contact",
        },
        "secondary_cta": {
            "label": {"ko": "지원 내용 보기", "en": "See Support Areas"},
            "href": "#services",
        },
        "nav_cta": {
            "ko": "문의하기",
            "en": "Inquire",
        },
        "menu_label": {
            "ko": "메뉴",
            "en": "Menu",
        },
        "nav_home_label": {
            "ko": "홈",
            "en": "Home",
        },
        "nav_services_label": {
            "ko": "제공 서비스",
            "en": "Support Areas",
        },
        "nav_credibility_label": {
            "ko": "신뢰 근거",
            "en": "Track Record",
        },
        "nav_faq_label": {
            "ko": "FAQ",
            "en": "FAQ",
        },
        "nav_contact_label": {
            "ko": "문의",
            "en": "Contact",
        },
        "service_section_title": {
            "ko": "어떤 지원을 받을 수 있나요",
            "en": "What Support You Can Get",
        },
        "recommended_audience_label": {
            "ko": "권장 고객",
            "en": "Recommended for",
        },
        "duration_label": {
            "ko": "예상 기간",
            "en": "Timeline",
        },
        "price_label": {
            "ko": "비용",
            "en": "Price",
        },
        "deliverable_label": {
            "ko": "예상 결과물",
            "en": "What you get",
        },
        "profile_section_title": {
            "ko": "대표자 프로필과 경력",
            "en": "Founder Profile and Track Record",
        },
        "profile_section_intro": {
            "ko": "명함이나 QR로 처음 들어온 분도 바로 신뢰를 확인할 수 있도록 대표자의 주요 경력 흐름과 실무 배경을 먼저 보여줍니다.",
            "en": "If you arrived from a business card or QR, you can quickly review the founder's practical background and career track record here.",
        },
        "profile_link_title": {
            "ko": "대표자 LinkedIn",
            "en": "Founder LinkedIn",
        },
        "profile_link_label": {
            "ko": "LinkedIn 바로 보기",
            "en": "Open LinkedIn",
        },
        "profile_link_note": {
            "ko": "회사 공식 계정이 아닌 대표자 개인 계정입니다.",
            "en": "This is the founder's personal LinkedIn profile, not a company account.",
        },
        "career_timeline_title": {
            "ko": "주요 커리어",
            "en": "Career Timeline",
        },
        "career_timeline_note": {
            "ko": "대표자의 주요 경력 흐름을 간단히 확인할 수 있습니다.",
            "en": "A quick view of the founder's major career history.",
        },
        "credibility_title": {
            "ko": "신뢰 근거",
            "en": "Why QuRoom",
        },
        "scope_boundary_label": {
            "ko": "지원 범위 안내",
            "en": "Support boundary",
        },
        "present_label": {
            "ko": "현재",
            "en": "Present",
        },
        "faq_title": {
            "ko": "시작 전에 많이 묻는 질문",
            "en": "Questions Before You Start",
        },
        "contact_title": {
            "ko": "문의하기",
            "en": "Start with an Inquiry",
        },
        "contact_intro": {
            "ko": "현재 상황과 방향을 짧게 남겨주시면, 지금 단계에 맞는 다음 단계를 안내드립니다. 외국인 소프트웨어 엔지니어라면 Step 2까지 이어서 프로필 검토를 받을 수 있습니다.",
            "en": "Share your current situation briefly and we will guide the next realistic step. If you are a foreign software engineer, you can continue to Step 2 for profile review.",
        },
        "quick_intake_title": {
            "ko": "1단계. 간단 문의",
            "en": "Step 1. Simple Inquiry",
        },
        "quick_intake_hint": {
            "ko": "이름, 이메일, 현재 역할이나 방향 정도만 적어주시면 됩니다.",
            "en": "Name, email, and your current focus are enough to start.",
        },
        "next_actions_summary": {
            "ko": "선택 사항: 프로필 더 자세히 남기기",
            "en": "Optional: Continue with Your Profile",
        },
        "matching_profile_title": {
            "ko": "2단계. 프로필 상세 작성",
            "en": "Step 2. Matching Profile",
        },
        "matching_profile_hint": {
            "ko": "이력서/CV, 링크, 비자 상태, 근무 조건",
            "en": "CV/profile links, visa status, and work preferences",
        },
        "matching_profile_note": {
            "ko": "외국인 소프트웨어 엔지니어이거나 해당 진로를 준비 중이라면 여기까지 작성해 주시면 검토에 도움이 됩니다.",
            "en": "If you are a foreign software engineer or preparing for that path, Step 2 helps us review your profile more concretely.",
        },
        "community_note": {
            "ko": "다른 분야이거나 아직 탐색 단계라면 1단계만 제출해도 충분합니다. 커뮤니티 대기열 신청은 1단계와 2단계 모두에서 가능합니다.",
            "en": "If you are from another field or still exploring, Step 1 is enough to start. Community waitlist opt-in is available in both Step 1 and Step 2.",
        },
        "one_action_note": {
            "ko": "아직 정리가 덜 됐다면 1단계만 남겨도 충분합니다.",
            "en": "If you are not ready yet, Step 1 alone is enough to start.",
        },
        "service_target": "foreign_developers",
        "credibility_signals": [
            {
                "ko": "삼성전자 실무 경험 기반 멘토링",
                "en": "Mentoring grounded in Samsung Electronics practical experience",
            },
            {
                "ko": "전남대 기반 오프라인 네트워킹과 광주/전남 로컬 맥락 이해",
                "en": "Offline networking rooted in Chonnam National University and local context in Gwangju/Jeonnam",
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
            "ko": "한국에서 일하기 위한 커리어 전략, 프로필 준비, 적응 가이드는 지원하지만 취업 보장이나 비자·법률 자문 대행은 하지 않습니다.",
            "en": "We support career strategy, profile readiness, and Korea guidance for working in Korea, but do not guarantee placement or provide visa/legal representation.",
        },
        "faq": [
            {
                "q": {
                    "ko": "어떻게 시작하면 되나요?",
                    "en": "How do I get started?",
                },
                "a": {
                    "ko": "1단계에서 현재 상황을 짧게 남겨주시면, 지금 단계에 맞는 다음 단계를 안내합니다. 외국인 소프트웨어 엔지니어라면 2단계 프로필 작성까지 이어서 검토할 수 있습니다.",
                    "en": "Start with Step 1 and share your current situation briefly. We then guide the next step that fits you, and foreign software engineers can continue into Step 2 for profile review.",
                },
            },
            {
                "q": {
                    "ko": "개발자가 아니어도 문의할 수 있나요?",
                    "en": "Can I inquire even if I am not a developer?",
                },
                "a": {
                    "ko": "네. 현재는 외국인 소프트웨어 엔지니어 지원에 가장 강하지만, 다른 분야의 외국인 인재도 1단계 문의로 시작할 수 있습니다.",
                    "en": "Yes. Our strongest support today is for foreign software engineers, but international talent from other fields can also start through Step 1.",
                },
            },
            {
                "q": {
                    "ko": "처음에는 무엇을 준비하면 되나요?",
                    "en": "What should I prepare first?",
                },
                "a": {
                    "ko": "처음에는 현재 역할이나 방향 정도만 알려주면 됩니다. 외국인 소프트웨어 엔지니어로 더 자세한 검토를 원할 경우 2단계에서 이력서, 링크, 기술 스택 정보를 보완하면 됩니다.",
                    "en": "To start, just share your current focus or role. If you want deeper review as a foreign software engineer, you can add your resume, links, and tech stack in Step 2.",
                },
            },
            {
                "q": {
                    "ko": "취업이나 비자 문제까지 직접 해결해 주나요?",
                    "en": "Do you directly handle job placement or visa issues?",
                },
                "a": {
                    "ko": "아닙니다. 취업 보장이나 비자·법률 자문 대행은 하지 않으며, 커리어 전략과 프로필 준비, 실무 가이드, 필요한 경우 전문 파트너 연결을 지원합니다.",
                    "en": "No. We do not guarantee placement or directly handle visa or legal issues. We focus on career strategy, profile readiness, practical guidance, and partner referrals when needed.",
                },
            },
            {
                "q": {
                    "ko": "광주만 지원하나요?",
                    "en": "Do you only support Gwangju?",
                },
                "a": {
                    "ko": "아닙니다. 광주/전남은 오프라인 네트워킹과 대면 안내를 우선할 수 있고, 다른 지역은 온라인 중심으로 지원합니다.",
                    "en": "No. Gwangju/Jeonnam can include in-person networking support, while other regions are primarily supported online.",
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
    content["client_projects"] = [
        item for item in content["portfolio"] if item["type_label"] == "외주 개발"
    ]
    content["owned_products"] = [
        item for item in content["portfolio"] if item["type_label"] == "자체 제품"
    ]
    if persona is None:
        content["services"] = [
            service
            for service in SERVICE_CARDS
            if "founders" in service["persona_targets"]
        ]
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


GWANGJU_COMMON_TRUST = {
    "title": "왜 제가 맡을 수 있는지",
    "body": "삼성전자에서 제품 개발을 경험했고, 이후 여러 자체 제품을 기획부터 개발, 배포, 운영까지 직접 해봤습니다. 그래서 화면 제작만 보지 않고 기능 우선순위, 배포, 운영, 수정 요청까지 같이 봅니다. 외주 프로젝트는 미술관 큐레이션 서비스처럼 실제 고객 요구사항을 받아 구현한 경험을 기준으로 설명합니다.",
    "points": [
        "삼성전자 포함 총 개발 경력 {career_duration}",
        "2018.06 설립",
        "자체 제품 기획·개발·운영 경험",
        "외주 개발: 미술관 큐레이션 서비스",
        "한 번에 한 고객사만 진행하는 집중 트랙 운영",
    ],
}

GWANGJU_PAGE_CONTENT = {
    "gwangju": {
        "meta_title": "광주 홈페이지 제작 · 웹개발 · 앱개발 | 큐룸 (QUROOM)",
        "meta_description": "광주광역시 8년 차 1인 풀스택 개발사 큐룸(QUROOM). 반응형 홈페이지, 웹개발, 앱개발 요구사항 정리부터 배포까지 대표가 직접 책임집니다.",
        "meta_keywords": "광주 홈페이지 제작, 광주 웹개발, 광주 앱개발, 광주 개발 외주, 광주 개발 파트너",
        "hero_label": "광주 개발 상담",
        "hero_title": "광주 홈페이지 제작·웹개발·앱개발, 요구사항부터 같이 정리합니다",
        "hero_summary": "페이지 구성, 기능 목록, 준비된 자료를 먼저 확인하고 기획 정리부터 개발, 배포까지 한 사람이 이어서 맡습니다.",
        "hero_badges": [
            "광주 기반 상담",
            "범위·일정·운영 기준 합의",
            "대표자가 직접 진행",
        ],
        "hero_checkpoints": [
            "지금 필요한 것이 홈페이지인지, 기능 개발인지 먼저 구분",
            "이번 분기 안에 진행할 범위와 미뤄도 되는 범위 정리",
            "예상 기간/비용/운영 이관 기준까지 첫 상담에서 확인",
        ],
        "hero_stats": [
            {"label": "상담 범위", "value": "홈페이지 · 웹 · 앱"},
            {"label": "진행 방식", "value": "직접 설계/개발"},
        ],
        "primary_cta_label": "상담 문의하기",
        "secondary_cta_label": "외주 전 체크리스트 보기",
        "secondary_cta_href": "/outsourcing-checklist/",
        "outcome_title": "무엇을 먼저 할지 정리합니다",
        "outcome_intro": "단순 견적부터 던지지 않고, 지금 단계에서 바로 맡겨야 할 일과 아직 정리할 일을 구분합니다.",
        "outcome_items": [
            {
                "title": "무엇을 만들지 구분",
                "description": "홈페이지, 웹서비스, 앱/PWA 중 지금 필요한 형태를 현실적으로 나눕니다.",
            },
            {
                "title": "범위와 예산 기준",
                "description": "처음 만들 기능과 나중에 해도 되는 기능을 나눠 견적 기준을 먼저 정리합니다.",
            },
            {
                "title": "운영 이후까지 고려",
                "description": "배포 후 수정, 계정, 소스코드, 운영 문서 기준까지 함께 확인합니다.",
            },
        ],
        "fit_title": "이런 경우에 적합합니다",
        "fit_items": [
            "회사 소개 홈페이지가 필요하지만 무엇부터 만들지 정리가 안 된 경우",
            "MVP를 빠르게 만들고 실제 사용자 반응을 확인해야 하는 경우",
            "앱이 필요한지 웹앱으로 먼저 검증할지 판단이 필요한 경우",
            "기능 요청이 늘어나 견적 기준을 먼저 잡아야 하는 경우",
        ],
        "services_title": "광주 전용 상세 안내",
        "service_links": [
            {
                "title": "광주 홈페이지 제작",
                "summary": "신뢰가 보이고 문의로 이어지는 회사 소개형 홈페이지",
                "url_name": "landing:gwangju_homepage",
            },
            {
                "title": "광주 웹개발",
                "summary": "MVP, 신청·예약·관리 기능까지 포함한 웹서비스 개발",
                "url_name": "landing:gwangju_web_development",
            },
            {
                "title": "광주 앱개발",
                "summary": "앱·웹앱·PWA 중 현실적인 방식으로 시작하는 제품 개발",
                "url_name": "landing:gwangju_app_development",
            },
        ],
        "process_title": "진행 방식",
        "process_steps": [
            {
                "title": "요구사항 정리",
                "description": "목표, 제약, 일정, 예산을 먼저 맞추고 우선순위를 확정합니다.",
            },
            {
                "title": "실행 범위 확정",
                "description": "2주~8주 단위로 실행 가능한 범위와 결과물을 합의합니다.",
            },
            {
                "title": "구현 및 점검",
                "description": "주차별 결과 공유와 리스크 점검으로 일정/품질을 관리합니다.",
            },
            {
                "title": "배포 및 이관",
                "description": "운영에 필요한 가이드까지 전달해 이후 확장이 가능하게 마무리합니다.",
            },
        ],
        "timeline_cost_title": "예상 기간/비용 범위",
        "timeline_cost_items": [
            "홈페이지 제작: 1주~3주 / 100만원~500만원",
            "웹개발: 2주~8주 / 300만원~1,000만원+",
            "앱/웹앱/PWA: 2주~8주 / 범위별 협의",
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "광주에서만 진행하나요?",
                "a": "광주 기반으로 진행하지만, 다른 지역도 온라인 중심으로 협업 가능합니다.",
            },
            {
                "q": "홈페이지 제작과 웹개발은 어떻게 다른가요?",
                "a": "홈페이지 제작은 신뢰 중심 소개 구조에 가깝고, 웹개발은 기능 구현과 운영 흐름까지 포함합니다.",
            },
            {
                "q": "문의 전에 준비해야 할 것이 있나요?",
                "a": "현재 상황, 원하는 일정, 대략 예산 범위만 정리해 주셔도 첫 상담이 가능합니다.",
            },
        ],
        "portfolio_names": [
            "AI콜봇 NoMiss (getNomiss)",
            "단어장앱 (voca.quroom.kr)",
            "광주 도서관 통합검색 (library.quroom.kr)",
            "손해사정사 문서 자동화 서비스 (R&D)",
            "PromptSpike",
            "WishBox (소망창고) - Alpha",
            "Obible (PWA 커뮤니티 성경 서비스)",
            "Kids Travel Curating",
            "Onepaper (부동산 전자계약 서비스)",
            "미술관 큐레이션 서비스 (ArtTrip)",
        ],
        "cta_title": "광주 프로젝트 문의하기",
        "cta_description": "현재 상황과 목표를 짧게 남겨주시면, 먼저 정리해야 할 범위와 다음 액션을 제안합니다.",
        "cta_button_label": "문의 보내기",
        "contact_anchor": "contact",
        "recommended_inquiry_type": "gwangju_scope",
    },
    "gwangju_homepage": {
        "meta_title": "광주 홈페이지 제작 | 회사·서비스 소개와 문의 전환 | 큐룸 (QUROOM)",
        "meta_description": "광주 기업·회사 소개 홈페이지 제작. 방문자 문의 전환 구조를 큐룸(QUROOM) 8년 차 개발사가 직접 기획·구축합니다.",
        "meta_keywords": "광주 홈페이지 제작, 광주 기업 홈페이지, 광주 회사 홈페이지, 광주 소개 사이트 제작",
        "hero_label": "광주 홈페이지 제작",
        "hero_title": "광주 홈페이지 제작, 신뢰 중심 기업 소개 홈페이지를 작고 명확하게 구축합니다",
        "hero_summary": "회사/서비스/포트폴리오/문의 구조를 먼저 정리하고, 방문자가 이해하기 쉬운 흐름으로 만듭니다.",
        "hero_badges": ["회사 소개", "서비스/포트폴리오", "문의 전환 동선"],
        "hero_checkpoints": [
            "첫 화면에서 무엇을 하는 회사인지 바로 보이게 정리",
            "서비스/포트폴리오/문의 동선을 한 흐름으로 연결",
            "기본 검색 노출과 공유 메타데이터까지 함께 반영",
        ],
        "hero_stats": [
            {"label": "예상 기간", "value": "1주 ~ 3주"},
            {"label": "예상 비용", "value": "100만 ~ 500만원"},
        ],
        "primary_cta_label": "홈페이지 제작 상담하기",
        "secondary_cta_label": "외주 전 체크리스트 보기",
        "secondary_cta_href": "/outsourcing-checklist/",
        "outcome_title": "홈페이지에서 먼저 정리할 것",
        "outcome_intro": "방문자가 회사를 이해하고, 신뢰하고, 문의할 수 있는 최소 구조를 먼저 잡습니다.",
        "outcome_items": [
            {
                "title": "대표 메시지",
                "description": "누구에게 어떤 문제를 해결해주는지 첫 화면에서 선명하게 보여줍니다.",
            },
            {
                "title": "신뢰 근거",
                "description": "이력, 사례, 진행 방식, 사업자 정보를 검증 가능한 문구로 정리합니다.",
            },
            {
                "title": "문의 흐름",
                "description": "서비스 소개부터 문의 폼까지 끊기지 않도록 CTA와 섹션 순서를 설계합니다.",
            },
        ],
        "fit_title": "이런 경우에 적합합니다",
        "fit_items": [
            "회사 소개가 약해 첫 신뢰 형성이 어려운 경우",
            "기존 사이트가 오래되어 최신 정보 반영이 어려운 경우",
            "포트폴리오/서비스 소개 구조가 정리되지 않은 경우",
            "문의 동선이 약해 상담 전환이 낮은 경우",
        ],
        "scope_title": "제공 범위",
        "scope_items": [
            "회사 소개형 홈페이지 구조 설계",
            "서비스 소개/포트폴리오 페이지 정리",
            "문의 폼과 기본 전환 동선 구성",
            "기본 메타데이터/검색 노출 구조 적용",
            "배포 및 운영 기본 가이드 전달",
        ],
        "process_title": "진행 방식",
        "process_steps": [
            {
                "title": "요구사항 정리",
                "description": "핵심 메시지, 타깃 고객, 필요한 페이지를 먼저 정리합니다.",
            },
            {
                "title": "구조 합의",
                "description": "화면 흐름과 카피 방향을 합의한 뒤 제작 범위를 고정합니다.",
            },
            {
                "title": "제작/수정",
                "description": "우선순위 기준으로 구현하고 핵심 문구와 동선을 점검합니다.",
            },
            {
                "title": "배포",
                "description": "실서비스 반영과 기본 운영 기준을 전달합니다.",
            },
        ],
        "timeline_cost_title": "예상 기간/비용 범위",
        "timeline_cost_items": [
            "예상 기간: 1주 ~ 3주",
            "예상 비용: 100만원 ~ 500만원",
            "정확한 일정/비용은 페이지 수와 콘텐츠 준비 상태에 따라 조정됩니다.",
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "회사 소개 홈페이지는 어느 정도 기간이 걸리나요?",
                "a": "일반적으로 1주~3주 내에서 진행하며, 페이지 수와 수정 횟수에 따라 달라집니다.",
            },
            {
                "q": "문구나 이미지 정리가 안 되어 있어도 진행 가능한가요?",
                "a": "가능합니다. 우선 현재 자료로 구조를 잡고 필요한 보완 목록을 함께 정리합니다.",
            },
            {
                "q": "제작 후 수정은 어떻게 하나요?",
                "a": "배포 후 운영 기준과 수정 포인트를 전달해 내부에서도 관리할 수 있게 구성합니다.",
            },
        ],
        "portfolio_names": [
            "AI콜봇 NoMiss (getNomiss)",
            "단어장앱 (voca.quroom.kr)",
            "광주 도서관 통합검색 (library.quroom.kr)",
            "손해사정사 문서 자동화 서비스 (R&D)",
            "PromptSpike",
            "WishBox (소망창고) - Alpha",
            "Kids Travel Curating",
            "Onepaper (부동산 전자계약 서비스)",
            "미술관 큐레이션 서비스 (ArtTrip)",
        ],
        "cta_title": "홈페이지 제작 문의하기",
        "cta_description": "현재 자료가 충분하지 않아도 괜찮습니다. 먼저 필요한 페이지와 우선순위부터 함께 정리합니다.",
        "cta_button_label": "문의 보내기",
        "contact_anchor": "contact",
        "recommended_inquiry_type": "gwangju_homepage",
    },
    "gwangju_web_development": {
        "meta_title": "광주 웹개발 외주 | MVP·웹서비스·운영도구 구축 | 큐룸 (QUROOM)",
        "meta_description": "광주 웹개발 외주 파트너 큐룸(QUROOM). 린 MVP, 사내 관리자 도구, 업무 시스템을 8년 차 풀스택 엔지니어가 직접 만듭니다.",
        "meta_keywords": "광주 웹개발, 광주 MVP 개발, 광주 웹서비스 개발, 광주 관리자 페이지 개발",
        "hero_label": "광주 웹개발",
        "hero_title": "광주 웹개발, MVP와 운영 도구를 실제 업무 흐름에 맞게 구축합니다",
        "hero_summary": "단순 화면 구현보다 사용자가 실제로 쓰고, 운영자가 이어받을 수 있는 기능 범위를 먼저 정합니다.",
        "hero_badges": ["MVP", "관리자 화면", "운영 도구"],
        "hero_checkpoints": [
            "사용자 화면과 관리자 화면을 함께 보고 범위 결정",
            "데이터 입력/조회/알림 등 실제 운영 흐름까지 점검",
            "2주~8주 안에 만들 핵심 기능부터 우선순위화",
        ],
        "hero_stats": [
            {"label": "예상 기간", "value": "2주 ~ 8주"},
            {"label": "예상 비용", "value": "300만원+"},
        ],
        "primary_cta_label": "웹개발 상담하기",
        "secondary_cta_label": "광주 홈페이지 제작 보기",
        "secondary_cta_href": "/gwangju-homepage/",
        "outcome_title": "웹개발 전에 먼저 확정하는 기준",
        "outcome_intro": "기능 목록만 늘리지 않고, 실제 사용과 운영에 필요한 최소 단위를 먼저 고정합니다.",
        "outcome_items": [
            {
                "title": "핵심 사용자 행동",
                "description": "가입, 신청, 예약, 결제, 관리 등 검증해야 할 행동을 먼저 좁힙니다.",
            },
            {
                "title": "운영자 업무",
                "description": "관리자가 매일 봐야 하는 데이터와 처리 흐름을 기능 범위에 반영합니다.",
            },
            {
                "title": "배포와 이관",
                "description": "서비스 반영 후 확인해야 할 계정, 환경변수, 운영 문서 기준을 남깁니다.",
            },
        ],
        "fit_title": "이런 경우에 적합합니다",
        "fit_items": [
            "빠르게 MVP를 만들어 사용자 반응을 봐야 하는 경우",
            "신청·예약·관리 기능이 필요한 경우",
            "내부 운영용 웹도구가 필요한 경우",
            "데이터 흐름까지 함께 설계해야 하는 경우",
        ],
        "scope_title": "제공 범위",
        "scope_items": [
            "요구사항/우선순위 정리",
            "핵심 기능 개발 및 관리자 화면 구성",
            "배포 파이프라인과 운영 기본 구조 점검",
            "운영 이관용 핵심 가이드 제공",
        ],
        "process_title": "진행 방식",
        "process_steps": [
            {
                "title": "문제 정의",
                "description": "무엇을 자동화/제품화해야 하는지 기준을 먼저 정합니다.",
            },
            {
                "title": "범위 확정",
                "description": "2주~8주 안에 완료 가능한 기능 범위로 스코프를 고정합니다.",
            },
            {
                "title": "개발/검증",
                "description": "핵심 기능부터 순차 개발하고 주차별 검증을 진행합니다.",
            },
            {
                "title": "배포/이관",
                "description": "운영 관점에서 필요한 체크포인트를 정리해 인계합니다.",
            },
        ],
        "timeline_cost_title": "예상 기간/비용 범위",
        "timeline_cost_items": [
            "예상 기간: 2주 ~ 8주",
            "예상 비용: 300만원 ~ 1,000만원+",
            "정확한 일정/비용은 기능 난이도와 연동 범위 기준으로 확정합니다.",
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "MVP와 정식 서비스 개발은 어떻게 구분하나요?",
                "a": "MVP는 검증에 필요한 핵심 기능 위주로, 정식 서비스는 운영 확장 기준까지 포함해 설계합니다.",
            },
            {
                "q": "관리자 페이지도 같이 만들 수 있나요?",
                "a": "가능합니다. 운영자가 실제로 사용하는 핵심 관리 기능을 우선 반영합니다.",
            },
            {
                "q": "기능이 많지 않아도 웹개발이 필요한가요?",
                "a": "반복 운영을 줄이거나 데이터 관리가 필요하면 소규모 기능도 충분히 개발 가치가 있습니다.",
            },
        ],
        "portfolio_names": [
            "AI콜봇 NoMiss (getNomiss)",
            "단어장앱 (voca.quroom.kr)",
            "광주 도서관 통합검색 (library.quroom.kr)",
            "손해사정사 문서 자동화 서비스 (R&D)",
            "PromptSpike",
            "WishBox (소망창고) - Alpha",
            "Obible (PWA 커뮤니티 성경 서비스)",
            "Kids Travel Curating",
            "Onepaper (부동산 전자계약 서비스)",
            "미술관 큐레이션 서비스 (ArtTrip)",
        ],
        "cta_title": "웹개발 상담받기",
        "cta_description": "MVP, 관리자 화면, 운영 도구 중 무엇부터 만들지 함께 정리합니다.",
        "cta_button_label": "문의 보내기",
        "contact_anchor": "contact",
        "recommended_inquiry_type": "gwangju_web",
    },
    "gwangju_app_development": {
        "meta_title": "광주 앱개발 외주 | 웹앱·PWA·크로스플랫폼 기획과 구축 | 큐룸 (QUROOM)",
        "meta_description": "광주 모바일 앱·웹앱·PWA 개발 외주 파트너 큐룸(QUROOM). 사업 단계와 예산에 맞춘 최적의 개발 방식을 8년 차 개발사가 직접 제안하고 구축합니다.",
        "meta_keywords": "광주 앱개발, 광주 모바일 앱, 광주 PWA 개발, 광주 웹앱 개발",
        "hero_label": "광주 앱개발",
        "hero_title": "광주 앱개발, 앱·웹앱·PWA 중 현실적인 시작점을 같이 정합니다",
        "hero_summary": "처음부터 큰 비용으로 앱을 만드는 대신, 사용자 문제와 예산에 맞는 검증 범위부터 정합니다.",
        "hero_badges": ["앱/웹앱 판단", "PWA MVP", "초기 검증"],
        "hero_checkpoints": [
            "앱스토어 앱이 꼭 필요한 상황인지 먼저 판단",
            "웹앱/PWA로 빠르게 검증 가능한 범위와 한계 정리",
            "초기 사용자 반응을 확인할 MVP 기준 합의",
        ],
        "hero_stats": [
            {"label": "예상 기간", "value": "2주 ~ 8주"},
            {"label": "추천 시작", "value": "MVP/PWA"},
        ],
        "primary_cta_label": "앱개발 방향 상담하기",
        "secondary_cta_label": "광주 웹개발 보기",
        "secondary_cta_href": "/gwangju-web-development/",
        "outcome_title": "앱개발 전에 먼저 줄이는 리스크",
        "outcome_intro": "앱이라는 형태보다 사용자 문제 검증과 운영 가능성을 먼저 봅니다.",
        "outcome_items": [
            {
                "title": "앱 필요성 판단",
                "description": "푸시, 카메라, 위치 등 앱 고유 기능이 필요한지 먼저 확인합니다.",
            },
            {
                "title": "초기 출시 방식",
                "description": "웹앱/PWA/MVP 중 예산과 속도에 맞는 시작점을 제안합니다.",
            },
            {
                "title": "확장 기준",
                "description": "초기 사용 데이터를 본 뒤 네이티브 앱 확장이 필요한지 판단합니다.",
            },
        ],
        "fit_title": "이런 경우에 적합합니다",
        "fit_items": [
            "앱 아이디어를 먼저 검증하고 싶은 경우",
            "모바일 중심 서비스가 필요한 경우",
            "커뮤니티/구독/콘텐츠형 서비스 구조가 필요한 경우",
            "앱과 웹앱 중 어떤 방식이 맞는지 판단이 필요한 경우",
        ],
        "scope_title": "제공 범위",
        "scope_items": [
            "기획/기능 우선순위 정리",
            "MVP 설계 및 구현",
            "웹앱/PWA 중심의 현실적인 초기 출시 구조 제안",
            "백엔드/운영 구조 연결",
        ],
        "process_title": "진행 방식",
        "process_steps": [
            {
                "title": "필요성 판단",
                "description": "앱이 정말 필요한지, 웹앱/PWA로 먼저 검증 가능한지 판단합니다.",
            },
            {
                "title": "MVP 범위 확정",
                "description": "핵심 사용자 행동을 검증할 최소 기능으로 범위를 좁힙니다.",
            },
            {
                "title": "구축/출시",
                "description": "빠르게 출시 가능한 형태로 구현하고 초기 운영 루프를 만듭니다.",
            },
            {
                "title": "확장 판단",
                "description": "실사용 데이터를 기반으로 다음 확장 단계를 결정합니다.",
            },
        ],
        "timeline_cost_title": "예상 기간/비용 범위",
        "timeline_cost_items": [
            "예상 기간: 2주 ~ 8주",
            "예상 비용: 범위별 협의",
            "앱/웹앱/PWA 선택과 기능 우선순위에 따라 비용이 달라집니다.",
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "앱이 꼭 필요한지 아직 모르는데 문의해도 되나요?",
                "a": "가능합니다. 앱 필요성과 웹앱/PWA 대안을 먼저 비교해 현실적인 시작점을 정합니다.",
            },
            {
                "q": "앱 대신 웹앱이나 PWA로 시작할 수 있나요?",
                "a": "네. 초기 검증 단계에서는 웹앱/PWA가 비용·속도 측면에서 유리한 경우가 많습니다.",
            },
            {
                "q": "처음부터 전체 기능을 다 만들어야 하나요?",
                "a": "아닙니다. 핵심 기능부터 우선 출시하고 사용자 반응을 보며 확장하는 방식을 권장합니다.",
            },
        ],
        "portfolio_names": [
            "단어장앱 (voca.quroom.kr)",
            "AI콜봇 NoMiss (getNomiss)",
            "광주 도서관 통합검색 (library.quroom.kr)",
            "Obible (PWA 커뮤니티 성경 서비스)",
            "WishBox (소망창고) - Alpha",
            "Kids Travel Curating",
            "PromptSpike",
            "미술관 큐레이션 서비스 (ArtTrip)",
        ],
        "cta_title": "앱개발 문의하기",
        "cta_description": "앱, 웹앱, PWA 중 지금 단계에 맞는 시작점을 함께 판단합니다.",
        "cta_button_label": "문의 보내기",
        "contact_anchor": "contact",
        "recommended_inquiry_type": "gwangju_app",
    },
    "outsourcing_checklist": {
        "meta_title": "홈페이지·웹개발 외주 맡기기 전 체크리스트 7가지 | 큐룸 (QUROOM)",
        "meta_description": "홈페이지나 웹개발 외주를 맡기기 전에 범위, 일정, 비용, 유지관리, 소유권에서 꼭 확인해야 할 7가지 항목을 8년 차 개발사 큐룸(QUROOM)이 정리했습니다.",
        "meta_keywords": "홈페이지 외주 체크리스트, 웹개발 외주 체크리스트, 외주 계약 전 확인사항, 개발 외주 분쟁 방지",
        "hero_label": "외주 전 필수 확인",
        "hero_title": "홈페이지·웹개발 외주 맡기기 전 확인하는 체크리스트 7가지",
        "hero_summary": "외주를 맡길 때 추가금 분쟁과 개발 지연을 막으려면 범위, 일정, 산출물, 소유권 기준이 사전에 명시되어야 합니다. 계약서에 서명하기 전 반드시 검토할 7개 항목입니다.",
        "hero_badges": ["추가금 분쟁 방지", "검수 기준 합의", "소유권 100% 이관"],
        "hero_checkpoints": [
            "원하는 화면보다 '실제 작동해야 하는 기능 목록'이 적혀 있는가",
            "개발사가 '안 해주는 범위(5대 제외범위)'가 사전에 명시되어 있는가",
            "배포 후 소스코드와 인프라 계정 소유권이 클라이언트에게 귀속되는가",
        ],
        "hero_stats": [
            {"label": "검토 기준", "value": "7개 핵심 항목"},
            {"label": "적용 대상", "value": "홈페이지 · 웹 · 앱 외주"},
        ],
        "primary_cta_label": "체크리스트 기반 외주 상담",
        "secondary_cta_label": "WBS 5대 제외범위 보기",
        "secondary_cta_href": "#wbs-rules",
        "timeline_cost_title": "체크리스트 활용 시 기대 효과",
        "timeline_cost_items": [
            "불명확한 요구사항으로 인한 개발 중간 일정 지연 방지",
            "기획 변경에 따른 일방적 추가 개발비 청구 분쟁 차단",
            "배포 완료 후 코드 미인계 및 유지보수 단절 리스크 예방",
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "외주 경험이 없어도 체크리스트만으로 점검할 수 있나요?",
                "a": "가능합니다. 최소한의 기준을 먼저 확인해도 실패 확률을 크게 줄일 수 있습니다.",
            },
            {
                "q": "견적이 너무 낮으면 무조건 위험한가요?",
                "a": "무조건은 아니지만, 범위/품질/인수인계 기준이 빠졌을 가능성이 높아 세부 항목 확인이 필요합니다.",
            },
            {
                "q": "체크리스트 검토 후 바로 상담 가능한가요?",
                "a": "가능합니다. 현재 준비 상태 기준으로 우선순위를 함께 정리할 수 있습니다.",
            },
        ],
        "portfolio_names": [
            "미술관 큐레이션 서비스 (ArtTrip)",
            "AI콜봇 NoMiss (getNomiss)",
            "단어장앱 (voca.quroom.kr)",
            "광주 도서관 통합검색 (library.quroom.kr)",
            "손해사정사 문서 자동화 서비스 (R&D)",
            "PromptSpike",
            "Obible (PWA 커뮤니티 성경 서비스)",
            "Onepaper (부동산 전자계약 서비스)",
        ],
        "outcome_title": "외주 실패를 줄이는 핵심 기준",
        "outcome_intro": "가격만 비교하면 놓치기 쉬운 범위, 소유권, 운영 이관 리스크를 먼저 분리합니다.",
        "outcome_items": [
            {
                "title": "범위 변경 기준",
                "description": "추가 요청이 생길 때 일정과 비용이 어떻게 바뀌는지 확인합니다.",
            },
            {
                "title": "소유권과 접근권한",
                "description": "도메인, 서버, 저장소, 관리자 계정의 소유 주체를 분명히 합니다.",
            },
            {
                "title": "운영 이관",
                "description": "수정 방법, 배포 방법, 장애 대응 기준이 문서로 남는지 확인합니다.",
            },
        ],
        "checklist_title": "사전 점검 체크리스트",
        "checklist_items": [
            {
                "title": "요구사항이 문서로 정리되어 있는가",
                "description": "기능/페이지/우선순위를 문서로 확정해야 일정과 비용 변동을 줄일 수 있습니다.",
            },
            {
                "title": "범위 밖 요청 처리 방식이 계약에 포함되어 있는가",
                "description": "추가 요청 시 일정·비용이 어떻게 변하는지 사전에 합의해야 분쟁을 줄일 수 있습니다.",
            },
            {
                "title": "일정 점검 방식과 보고 주기가 정해져 있는가",
                "description": "주간 단위 공유 구조가 없으면 지연을 늦게 발견하게 됩니다.",
            },
            {
                "title": "비용 산정 기준이 기능 단위로 설명되어 있는가",
                "description": "총액만 제시된 견적보다 기능별 근거가 있는 견적이 리스크가 낮습니다.",
            },
            {
                "title": "도메인/배포/소스코드 소유권이 명확한가",
                "description": "계정/저장소/서버 접근 권한과 소유 주체를 계약 전에 반드시 확인해야 합니다.",
            },
            {
                "title": "수정 요청 프로세스가 있는가",
                "description": "수정 접수-반영-확인 절차가 없으면 운영 단계에서 비용이 급증하기 쉽습니다.",
            },
            {
                "title": "운영 이관 문서 제공 범위가 정의되어 있는가",
                "description": "인수인계 문서가 없으면 프로젝트 종료 이후 유지 운영이 불가능해질 수 있습니다.",
            },
        ],
        "faq_title": "자주 묻는 질문",
        "faq": [
            {
                "q": "외주 경험이 없어도 체크리스트만으로 점검할 수 있나요?",
                "a": "가능합니다. 최소한의 기준을 먼저 확인해도 실패 확률을 크게 줄일 수 있습니다.",
            },
            {
                "q": "견적이 너무 낮으면 무조건 위험한가요?",
                "a": "무조건은 아니지만, 범위/품질/인수인계 기준이 빠졌을 가능성이 높아 세부 항목 확인이 필요합니다.",
            },
            {
                "q": "체크리스트 검토 후 바로 상담 가능한가요?",
                "a": "가능합니다. 현재 준비 상태 기준으로 우선순위를 함께 정리할 수 있습니다.",
            },
        ],
        "portfolio_names": [
            "미술관 큐레이션 서비스 (ArtTrip)",
            "손해사정사 문서 자동화 서비스 (R&D)",
            "PromptSpike",
            "Obible (PWA 커뮤니티 성경 서비스)",
            "Onepaper (부동산 전자계약 서비스)",
        ],
        "cta_title": "외주 진행 전 범위 점검이 필요하다면",
        "cta_description": "현재 상황을 남겨주시면 어떤 항목부터 정리해야 할지 우선순위를 제안합니다.",
        "cta_button_label": "문의 보내기",
        "contact_anchor": "contact",
        "recommended_inquiry_type": "outsourcing_check",
        "wbs_rules_title": "계약 전 필수 명시: WBS 5대 제외범위 (5 Out-of-Scope Rules)",
        "wbs_rules_summary": "외주 계약 및 용역 진행 시 발생하는 분쟁의 대부분은 '당연히 해주는 줄 알았다'는 모호함에서 출발합니다. 계약서 별첨 과업지시서에 아래 5대 제외범위를 사전 명시하면 추가금 분쟁을 사전에 방지할 수 있습니다.",
        "wbs_rules": [
            {
                "article": "제1조 (기능 범위)",
                "title": "P0 확정 요구사항 외 기획 변경 및 신규 기능 추가",
                "rule": "본 계약의 과업 범위는 WBS 명세서 상의 P0(출시 필수) 기능으로 한정합니다.",
                "exclusions": [
                    "개발 진행 중 신규 화면 추가, 기존 확정된 비즈니스 로직 변경, 신규 사용자 권한 추가",
                    "WBS P0에 명시되지 않은 부가 기능(SNS 공유, 다크모드, 다국어 지원 등)",
                ],
                "procedure": "P0 외 요구사항 발생 시 P1/P2(백로그)로 분리하여 2차 스프린트로 이관하거나, 별도 추가 공수(M/D) 견적을 상호 합의 후 진행합니다.",
            },
            {
                "article": "제2조 (외부 의존성)",
                "title": "서드파티 서비스 심사 지연 및 외부 플랫폼 장애",
                "rule": "개발사는 API 연동 코드 작성을 책임지며, 외부 기관의 심사 승인 및 장애는 납기 지연 사유에서 제외됩니다.",
                "exclusions": [
                    "PG사(포트원, 토스페이먼츠 등) 가맹점 가입 심사, 통신판매업 신고, 보증보험 발급 지연",
                    "카카오 알림톡 템플릿 검수 반려, 공공데이터 OpenAPI 인증키 발급 지연, SMS 발신번호 사전등록",
                    "서드파티 플랫폼의 자체 서버 다운 또는 사후 API 사양 변경",
                ],
                "procedure": "API 연동 검증은 Mock/테스트 환경 승인을 기준으로 과업 완료를 판정합니다.",
            },
            {
                "article": "제3조 (스토어 심사)",
                "title": "애플/구글 앱스토어 비즈니스 모델 심사 리젝 대응 기준",
                "rule": "앱 빌드 및 스토어 제출 규격 준수는 개발사 책임이나, 사업 모델 및 콘텐츠 사유의 리젝은 제외됩니다.",
                "exclusions": [
                    "코드 결함이 아닌 비즈니스 모델(수수료, 디지털 상품 IAP 미적용), 저작권, 개인정보처리방침 문구 미비로 인한 리젝",
                    "앱스토어 검수 가이드라인 사후 변경으로 인한 UI/UX 전면 수정",
                ],
                "procedure": "기술적 버그로 인한 1차 리젝은 무상 수정 제출하며, 사업 정책상 리젝은 가이드라인에 맞게 요구사항을 조정합니다.",
            },
            {
                "article": "제4조 (품질 보증)",
                "title": "하자보수(무상 3개월)와 기능 개선(유상)의 경계",
                "rule": "무상 하자보수 기간은 검수 완료일로부터 3개월로 정의합니다.",
                "exclusions": [
                    "버튼 위치 변경, 폰트/색상 변경, 통계 집계 조건 변경 등 명세와 무관한 사용성 개선",
                    "클라이언트가 임의로 서버 환경설정(Nginx, DB 등)을 변경하거나 타사 개발자가 코드를 수정한 경우",
                ],
                "procedure": "WBS P0 명세서에 정의된 기능이 명세대로 작동하지 않는 코드 버그는 무상 수정하며, 사용성 개선은 유상 별도 산정합니다.",
            },
            {
                "article": "제5조 (인프라 및 운영)",
                "title": "월간 클라우드 실비 및 운영 대행 분리",
                "rule": "개발 용역비는 소프트웨어 구축 공수에 대한 비용이며, 인프라 운영 실비는 포함되지 않습니다.",
                "exclusions": [
                    "도메인 구입비, 유료 SSL 발급비, 클라우드 VPS(AWS, Cloudtype, Dokku) 월 서버 비용",
                    "DB 용량 증설, AI 토큰 사용료(OpenAI/Claude API 청구 비용), 대용량 트래픽 CDN 비용",
                    "납품 완료 후 일상적인 데이터 백업 확인, 콘텐츠 등록, 사용자 CS 응대",
                ],
                "procedure": "인프라 실비는 발주사 명의 카드로 직접 결제 등록하며 개발사는 환경 설정 및 배포를 완료합니다.",
            },
        ],
        "quote_template_title": "[실전 양식] 린 MVP 과업지시서(WBS) 및 표준 견적서 서식",
        "quote_template_intro": "8년 차 풀스택 엔지니어가 실제 사용하는 린 MVP 6대 모듈 WBS와 국세청 전자세금계산서 표준 견적서 양식입니다. 아래 버튼으로 마크다운을 복사해 즉시 계약 별첨 자료로 활용하세요.",
        "quote_template_markdown": """# [프로젝트명] 린 MVP 외주 구축 과업지시서 (WBS)

## 1. 기본 개요
- 발주사 (클라이언트): (주)OOO (대표자: OOO)
- 개발사: 큐룸 (대표자: 김상은, 8년 차 풀스택 개발사)
- 개발 기간: 202X년 X월 X일 ~ 202X년 X월 X일 (총 X주)
- 납품 목표: 웹/앱 MVP 출시 및 실제 결제/문의 접수 기능 정상 작동

## 2. P0 (핵심 기능 명세서 - 출시 필수)
| 모듈 | 화면/기능명 | 세부 요구사항 | 기술 스택 | 공수(M/D) |
| :--- | :--- | :--- | :--- | :---: |
| 인증 | 회원가입/로그인 | 카카오 1초 간편 로그인 + 휴대폰 본인인증 | OAuth 2.0 | 2.0 |
| 메인 | 서비스 대시보드 | 실시간 신청 목록 조회 및 상태 필터링 (FTS) | PostgreSQL | 3.0 |
| 신청 | 모바일 증상 접수 | 반응형 모바일 웹 폼, 사진 업로드(WebP 압축) | Next.js/S3 | 2.5 |
| 결제 | 주문 및 결제 연동 | 포트원 V2 REST API + 웹훅 HMAC 서명 검증 | PortOne V2 | 2.5 |
| 알림 | 카카오 알림톡 발송 | 신청 완료 및 결제 확인 알림톡 자동 발송 | 비즈톡 API | 1.5 |
| 배포 | 실서버 인프라 구축 | Docker Nginx 리버스 프록시 + Let's Encrypt SSL | VPS / Dokku | 1.5 |
| **합계** | **총 6개 모듈** | **P0 핵심 기능 런칭 완비** | **풀스택** | **13.0 M/D** |

## 3. P1/P2 (제외 및 2차 백로그 항목)
- ❌ 네이버/구글/애플 다중 소셜 로그인 (카카오 단일 우선)
- ❌ 관리자 다크모드 및 엑셀 다운로드 커스텀 스타일
- ❌ 실시간 1:1 채팅 (카카오 채널톡 링크 버튼으로 대체)

## 4. 검수 및 인수인계 기준
1. 스테이징 서버에서 P0 기능 6개 모듈 단위 테스트 시연 성공.
2. Git 저장소 전체 소스코드 Push 및 README.md 환경설정 가이드 제공.
3. 실서버 배포 완료 및 HTTPS 정상 통신 확인 후 '과업 완료 검수조서' 날인.

---

# 표 준 견 적 서 (Quotation)

- 공급자: 큐룸 (QUROOM) / 사업자등록번호: 729-16-01048
- 대표자: 김상은 (8년 차 풀스택 엔지니어) / 사업장: 광주광역시 북구
- 수신처: (주)OOOOOO 대표 귀하
- 견적일자: 202X년 X월 X일 (유효기간: 발행일로부터 14일)

### 1. 견적 요약
- 용역명: [프로젝트명] 린 MVP 웹/앱 풀스택 구축 용역
- 결제 조건: 계약금 40% (착수 시) / 잔금 60% (과업 완료 및 검수 시)

### 2. 세부 산출 내역
| 항목 | 규격 및 내용 | 수량 | 단위 | 금액(원) |
| :--- | :--- | :---: | :---: | :---: |
| 린 MVP 풀스택 개발 | WBS P0 6개 모듈 설계, 프론트/백엔드 구현 | 13 | M/D | 협의 |
| 결제/외부 API 연동 | 포트원 V2 결제 웹훅 멱등성 및 알림톡 연동 | 1 | 식 | 포함 |
| 프로덕션 서버 배포 | Docker Nginx 리버스 프록시, SSL, 무중단 배포 | 1 | 식 | 포함 |
| 인수인계 및 운영 문서 | 아키텍처 다이어그램, 환경변수 가이드, 검수조서 | 1 | 식 | 포함 |
| **부가가치세 (VAT)** | 10% (국세청 전자세금계산서 정식 발행) | | | 별도 |

### 3. 특약 사항
1. 본 견적은 [WBS 5대 제외범위]를 준수하며, 명시되지 않은 기능 추가는 상호 협의 후 별도 산정합니다.
2. 검수 완료 후 3개월간 코드 오류에 대한 무상 하자보수를 보증합니다.""",
        "enaradaum_package_title": "[실무 가이드] 정부지원사업(예창패·초창패·AI바우처) e나라도움 5종 서류 패키지",
        "enaradaum_package_intro": "예창패, 초창패, 청창사, AI 바우처 협약 기업이 IT 외주비 및 AI 토큰 사용료를 e나라도움 회계 검수에서 보완이나 반려 없이 정산할 수 있도록 완비된 5종 서류 패키지입니다.",
        "enaradaum_docs": [
            {
                "num": "1",
                "name": "전자세금계산서",
                "who": "개발사 발행",
                "point": "국세청 승인번호(24자리) 정상 발급, 사업계획서 상 외주용역비 비목 일치, 협약 기간 내 발행",
            },
            {
                "num": "2",
                "name": "비교견적서 2부",
                "who": "주관기업+개발사",
                "point": "당사(큐룸) 견적서 1부 + 타사 비교견적서 1부로 단가 및 공수 타당성 객관화",
            },
            {
                "num": "3",
                "name": "표준 과업지시서 & WBS",
                "who": "개발사 제공",
                "point": "단순 총액 표기가 아닌 단위 기능별 M/D 공수 및 주간 일정표, 산출물 정의 명시",
            },
            {
                "num": "4",
                "name": "과업 완료 검수조서",
                "who": "주관기업+개발사 날인",
                "point": "기능별 단위테스트 결과표, 실서버 캡처본, 발주사 대표자 서명 및 개발사 대표자 직인",
            },
            {
                "num": "5",
                "name": "기업 증빙 서류 2종",
                "who": "개발사 제공",
                "point": "공급기업 국세청 사업자등록증 사본 + 세금계산서 명의와 일치하는 기업 통장 사본",
            },
        ],
        "inspection_template_title": "[실전 서식] 과업 완료 검수조서 (표준 서식)",
        "inspection_template_markdown": """# 과 업 완 료 검 수 조 서 (Acceptance Report)

## 1. 사업 개요
- 사 업 명: 202X년도 [예비창업패키지 / 초기창업패키지 / AI바우처] 지원사업
- 과 제 명: [프로젝트명] 린 MVP 웹/앱 풀스택 구축 용역
- 발 주 처 (주관기업): (주)OOOO (대표자: OOO)
- 수 급 인 (개발사): 큐룸 (대표자: 김상은, 8년 차 풀스택 개발사)
- 계약 기간: 202X. 00. 00 ~ 202X. 00. 00
- 검수 일자: 202X. 00. 00

---

## 2. 과업 완료 및 단위 테스트 검수 내역
| 모듈 | 요구 기능 | 검수 기준 및 시연 결과 | 판정 |
| :---: | :--- | :--- | :---: |
| 01 | 회원가입/인증 | 카카오 OAuth 2.0 간편 로그인 및 토큰 세션 유지 정상 | 합격 |
| 02 | 서비스 신청/접수 | 반응형 모바일 웹 사진 업로드 및 DB 정상 저장 | 합격 |
| 03 | 결제 모듈 연동 | 포트원 V2 카드 결제 승인 및 HMAC 웹훅 결제 검증 | 합격 |
| 04 | 알림 발송 파이프라인 | 결제 완료 시 카카오 알림톡 실시간 수신 확인 | 합격 |
| 05 | 프로덕션 배포 | Docker Nginx 리버스 프록시 통신 및 HTTPS 인증서 적용 | 합격 |

## 3. 최종 산출물 납품 목록
1. 전체 소스코드 Git 저장소 이관 및 커밋 로그 완비.
2. 시스템 아키텍처 다이어그램 및 환경변수(`.env`) 세팅 가이드 문서 1부.
3. 실서버 가동 URL (`https://app.yourcompany.com`) 및 관리자 계정.

## 4. 검수 결과
위 과업지시서 및 WBS 계약 내용에 명시된 개발 용역이 정상적으로 완료되었으며, 
단위 테스트 및 실서버 배포 상태를 최종 확인하고 본 검수조서를 발행합니다.

202X년  00월  00일

- 주관기업 (발주처): (주)OOOO 대표자  O O O  (인)
- 공급기업 (개발사): 큐룸 (QUROOM) 대표자  김 상 은  (인)""",
        "ai_token_section": {
            "title": "AI 토큰(OpenAI / Claude API) 원화 전자세금계산서 정산 안내",
            "problem": "해외 신용카드 USD 결제는 부가세 누락 및 개인 계정 토큰 혼용 의혹으로 e나라도움 회계 감사 지적 1위 항목입니다.",
            "solution_title": "큐룸의 기업 전용 AI 토큰 정산 대행 (LiteLLM Proxy)",
            "solutions": [
                "국세청 전자세금계산서 정식 발행: 원화(KRW) 기준 부가세 10% 포함 정식 발행",
                "사내 전용 프록시 구축: LiteLLM 기반 사내 엔드포인트 제공",
                "감사 로그(Audit Trail) CSV 제공: 일시, 사용자, 모델명, 입출력 토큰 수, 사업 비즈니스 태그 기재 (원문 마스킹으로 사생활 보호)",
            ],
        },
    },
}


def _filter_portfolio_items(names: list[str]) -> list[dict]:
    if not names:
        return []
    name_set = set(names)
    return [item for item in SHARED_CONTENT["portfolio"] if item["name"] in name_set]


def build_gwangju_page_content(page_key: str) -> dict:
    page_content = deepcopy(GWANGJU_PAGE_CONTENT[page_key])
    page_content["trust"] = deepcopy(GWANGJU_COMMON_TRUST)
    page_content["links"] = deepcopy(SHARED_CONTENT["links"])
    page_content["company"] = deepcopy(SHARED_CONTENT["company"])
    page_content["metrics"] = deepcopy(SHARED_CONTENT["metrics"])
    page_content["founder_capacity_policy"] = SHARED_CONTENT["founder_capacity_policy"]
    page_content["portfolio"] = _filter_portfolio_items(
        page_content.get("portfolio_names", [])
    )
    return page_content


VIBE_CODING_CHECKLIST = [
    {
        "category": "보안 및 환경변수",
        "icon": "🔐",
        "items": [
            ".env 저장소 격리: .env, .env.local 파일이 .gitignore에 등록되어 GitHub에 커밋되지 않았는가",
            "클라이언트 키 노출 통제: NEXT_PUBLIC_ 또는 VITE_ 접두사에 DB 비번, 결제 시크릿 키가 없는가",
            "하드코딩 API Key 제거: 코드 내부에 sk-ant- 또는 sk- 형태의 토큰 문자열이 잔존하지 않는가",
        ],
    },
    {
        "category": "인프라 & 네트워크",
        "icon": "🌐",
        "items": [
            "포트 바인딩 확인: 백엔드 앱 포트(3000/8000) 바인딩 및 Nginx 리버스 프록시 80/443 포워딩",
            "Let's Encrypt SSL 자동 갱신: HTTPS 인증서 설치 및 certbot renew 자동 갱신 크론잡 구성",
            "CORS 도메인 명시: 와일드카드(*) 대신 실제 프로덕션 프론트엔드 도메인만 화이트리스트 허용",
        ],
    },
    {
        "category": "데이터베이스 & 세션",
        "icon": "🗄️",
        "items": [
            "마이그레이션 이력 관리: alembic / prisma migrate 등 버전 관리 파일이 순차적으로 유지되는가",
            "커넥션 풀링(Connection Pooling): 서버리스/컨테이너 환경 PgBouncer 또는 Supabase Pooler 설정",
            "외래키(FK) 무결성 및 인덱스: 결제 및 주문 테이블에 사용자 ID 외래키와 기본 조회 인덱스 확인",
        ],
    },
    {
        "category": "결제 및 웹훅 멱등성",
        "icon": "💳",
        "items": [
            "결제 금액 위변조 검증: 브라우저 금액 대신 서버에서 PG사 REST API로 실제 승인 금액 대조",
            "웹훅 HMAC 서명 검증: 외부 결제 완료 웹훅 수신 시 시크릿 헤더 서명 검증",
            "멱등성(Idempotency) 보장: 중복 웹훅 도달 시에도 결제 및 주문이 1회만 처리되도록 트랜잭션 보장",
        ],
    },
]

