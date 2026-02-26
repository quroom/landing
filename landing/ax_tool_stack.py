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

DIAGNOSIS_QUESTIONS = {
    "q1": "지난 2주 동안 3회 이상 반복된 업무를 목록화하고 시작/종료 지점을 정의했다",
    "q2": "반복 업무를 규칙형(자동화 가능)과 판단형(AI 보조)으로 구분해두었다",
    "q3": "고객/리드/진행상태 데이터를 Google Sheets 등 한 곳에서 관리한다",
    "q4": "하루 30분 이상 소요되거나 복붙/누락이 발생하는 자동화 후보를 식별해두었다",
    "q5": "문서/메일/콘텐츠 생성 업무를 GPT/Claude 템플릿으로 표준화했다",
    "q6": "요약/리서치 흐름에 NotebookLM/Perplexity를 연결해 의사결정 속도를 높이고 있다",
    "q7": "운영 표준 작업 문서(응대/배포/장애 대응)와 2주 점검 루틴이 문서화되어 있다",
    "q8": "2주 내 시험 구현 가능성, 매출 연결성, 내부 구축(Django)과 외부 도구 도입 기준을 가지고 있다",
}

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
