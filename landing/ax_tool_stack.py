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

QUESTION_SUPPORT_SCOPE = {
    "q1": "direct",
    "q2": "direct",
    "q3": "direct",
    "q4": "direct",
    "q5": "direct",
    "q6": "direct",
    "q7": "direct",
    "q8": "direct",
}

DIAGNOSIS_AXES = {
    "workflow_clarity": {
        "label": "업무 흐름 명확성",
        "description": "업무 흐름, 병목, 역할이 명확히 정리되어 있는지 확인합니다.",
        "questions": ["q1", "q2"],
    },
    "data_operation_base": {
        "label": "데이터/운영 기반",
        "description": "데이터가 한 곳에서 표준화되고 운영에 활용되는지 확인합니다.",
        "questions": ["q3", "q4"],
    },
    "automation_design": {
        "label": "자동화 적합도",
        "description": "규칙형 업무를 자동화로 전환할 준비 상태를 확인합니다.",
        "questions": ["q5", "q6"],
    },
    "execution_system": {
        "label": "실행 체계",
        "description": "2주 안에 실행 가능한 운영 루틴과 책임 구조를 점검합니다.",
        "questions": ["q7", "q8"],
    },
}

DIAGNOSIS_QUESTIONS = {
    "q1": "현재 주요 업무(리드관리/고객응대/콘텐츠운영/내부협업)를 명확히 구분해 운영하고 있다",
    "q2": "반복되는 복붙/수작업이 어디서 발생하는지 최근 2주 기준으로 파악했다",
    "q3": "누락/지연이 자주 발생하는 병목 구간(응대, 승인, 전달)을 특정해두었다",
    "q4": "고객/리드/진행상태 데이터를 하나의 시트 또는 도구에서 관리한다",
    "q5": "규칙형 업무(분류/알림/리마인드/집계)를 자동화 후보로 정리해두었다",
    "q6": "자동화가 필요한 업무를 우선순위(효과 대비 노력) 기준으로 정렬해두었다",
    "q7": "2주 안에 실험할 수 있는 담당자/시간/검증 기준이 잡혀 있다",
    "q8": "실행 후 점검 루틴(주간 리뷰/체크리스트/개선 로그)이 정해져 있다",
}


def diagnosis_question_keys() -> list[str]:
    return list(DIAGNOSIS_QUESTIONS.keys())
