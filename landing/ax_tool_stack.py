USED_TOOLS = {
    "automation_workflow": [
        "Make",
        "n8n",
        "Google Apps Script",
        "OpenClaw",
        "Telegram",
        "Discord",
    ],
    "knowledge_docs": [
        "Notion",
        "Obsidian",
        "Google Sheets",
        "NotebookLM",
    ],
    "ai_llm": [
        "OpenAI GPT / Codex",
        "Anthropic Claude / Claude Code",
        "Google Gemini",
        "Perplexity AI",
        "OpenClaw",
    ],
    "dev_stack": [
        "Django",
        "HTMX",
        "Alpine.js",
        "Tailwind",
        "daisyUI",
        "PostgreSQL",
        "Lightsail",
        "Ec2",
    ],
    "project_management": [
        "Trello",
    ],
    "ops_marketing": [
        "GA4",
        "Paddle",
        "PortOne",
    ],
}

POSSIBLE_TOOLS = [
    "GitHub",
    "Supabase",
    "Zapier",
    "n8n",
    "Slack",
    "Figma",
    "Canva",
]

DIAGNOSIS_AXES = {
    "workflow_clarity": {
        "label": "업무 흐름 명확성",
        "description": "반복 업무 흐름이 명확한지 점검합니다.",
        "questions": ["q1", "q2"],
    },
    "data_operation_base": {
        "label": "데이터/운영 기반",
        "description": "운영 데이터가 같은 기준으로 관리되는지 점검합니다.",
        "questions": ["q3", "q4"],
    },
    "automation_design": {
        "label": "자동화 적합도",
        "description": "자동화 후보와 우선순위가 준비됐는지 점검합니다.",
        "questions": ["q5", "q6"],
    },
    "execution_system": {
        "label": "실행 체계",
        "description": "2주 실행과 점검 루틴이 작동하는지 점검합니다.",
        "questions": ["q7", "q8"],
    },
}

DIAGNOSIS_QUESTION_META = {
    "q1": {
        "order": 1,
        "axis": "workflow_clarity",
        "required": True,
        "intent_key": "find_repetitive_work",
        "impact_weight": 1.5,
        "question": "최근 2주 동안 반복 수작업이 어디서 발생하는지 파악해두었다",
    },
    "q2": {
        "order": 2,
        "axis": "workflow_clarity",
        "required": True,
        "intent_key": "document_workflow",
        "impact_weight": 1.0,
        "question": "최근 2주 동안 그 반복 업무의 시작-처리-완료 흐름을 문서로 정리해두었다",
    },
    "q3": {
        "order": 3,
        "axis": "data_operation_base",
        "required": True,
        "intent_key": "identify_bottleneck",
        "impact_weight": 1.3,
        "question": "최근 2주 동안 누락·지연이 자주 나는 구간(응대/승인/전달)을 특정해두었다",
    },
    "q4": {
        "order": 4,
        "axis": "data_operation_base",
        "required": True,
        "intent_key": "unify_operational_data",
        "impact_weight": 1.15,
        "question": "최근 2주 동안 고객/리드/진행상태 데이터를 같은 기준으로 한곳에서 관리해왔다",
    },
    "q5": {
        "order": 5,
        "axis": "automation_design",
        "required": True,
        "intent_key": "pick_automation_candidate",
        "impact_weight": 1.25,
        "question": "최근 2주 동안 자동화 후보 업무를 1개 이상 선정해두었다",
    },
    "q6": {
        "order": 6,
        "axis": "automation_design",
        "required": True,
        "intent_key": "prioritize_automation",
        "impact_weight": 1.3,
        "question": "최근 2주 동안 자동화 후보를 효과 대비 노력 기준으로 우선순위화해두었다",
    },
    "q7": {
        "order": 7,
        "axis": "execution_system",
        "required": True,
        "intent_key": "set_owner_and_goal",
        "impact_weight": 1.1,
        "question": "최근 2주 실행을 위한 담당자·일정·완료기준을 정해두었다",
    },
    "q8": {
        "order": 8,
        "axis": "execution_system",
        "required": True,
        "intent_key": "run_review_loop",
        "impact_weight": 1.2,
        "question": "최근 2주 실행 결과를 점검하는 주간 리뷰/체크리스트 루틴을 운영하고 있다",
    },
}

DIAGNOSIS_QUESTIONS = {
    key: meta["question"] for key, meta in DIAGNOSIS_QUESTION_META.items()
}

QUESTION_SUPPORT_SCOPE = {key: "direct" for key in DIAGNOSIS_QUESTION_META}


def diagnosis_question_keys() -> list[str]:
    return sorted(
        DIAGNOSIS_QUESTION_META.keys(),
        key=lambda item: int(DIAGNOSIS_QUESTION_META[item]["order"]),
    )


def core_question_keys() -> list[str]:
    return [
        key
        for key in diagnosis_question_keys()
        if DIAGNOSIS_QUESTION_META[key]["required"]
    ]


def optional_question_keys() -> list[str]:
    return [
        key
        for key in diagnosis_question_keys()
        if not DIAGNOSIS_QUESTION_META[key]["required"]
    ]
