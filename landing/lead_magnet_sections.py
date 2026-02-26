from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit


def normalize_contact_cta_href(href: str) -> str:
    value = (href or "").strip()
    if not value:
        return "/#contact"
    if value == "#contact" or value == "/#contact":
        return "/#contact"
    if value.startswith("http://") or value.startswith("https://"):
        parsed = urlsplit(value)
        if parsed.fragment == "contact":
            path = parsed.path or "/"
            return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, "contact"))
    return value


def build_lead_magnet_section_ast(payload: dict) -> list[dict]:
    grade = payload.get("grade", "B")
    weakest = payload.get("weakest_category_insight")
    category_insights = payload.get("category_insights") or []
    if not weakest:
        weakest_key = payload.get("weakest_axis_key")
        weakest = next(
            (item for item in category_insights if item.get("key") == weakest_key),
            category_insights[0] if category_insights else None,
        )

    one_action = payload.get("one_action") or {}
    cta = payload.get("cta") or {}
    normalized_cta_href = normalize_contact_cta_href(cta.get("href", "#contact"))
    profile_tools = payload.get("profile_tools") or []

    return [
        {
            "id": "summary",
            "heading": "진단 요약",
            "rows": [
                f"점수: {payload.get('score', 0)}/{payload.get('max_score', 0)}",
                f"등급: {grade}",
                f"한 줄 요약: {payload.get('summary', '')}",
            ],
        },
        {
            "id": "weakest_category",
            "heading": "핵심 보완 카테고리",
            "weakest_category": weakest,
            "all_categories": category_insights,
        },
        {
            "id": "one_action",
            "heading": "2주 실행 우선 1개",
            "rows": [
                f"과제: {one_action.get('title', '-')}",
                f"추천 툴: {one_action.get('tools', '-')}",
                f"수행 기준: {one_action.get('execution', '-')}",
            ],
        },
        {
            "id": "tools",
            "heading": "주요 추천 툴",
            "rows": [", ".join(profile_tools) if profile_tools else "Make, Google Sheets, Notion"],
        },
        {
            "id": "next_action",
            "heading": "다음 액션",
            "cta": {
                "label": cta.get("label", "상담 문의하기"),
                "href": normalized_cta_href,
                "note": cta.get("note", ""),
            },
        },
    ]


def section_contract_signature(sections: list[dict]) -> tuple[tuple[str, str], ...]:
    signature: list[tuple[str, str]] = []
    for section in sections:
        cta_href = ""
        if section.get("id") == "next_action":
            cta_href = (section.get("cta") or {}).get("href", "")
        signature.append((section.get("id", ""), section.get("heading", "") + cta_href))
    return tuple(signature)


def render_sections_to_text(
    sections: list[dict], *, include_all_categories: bool = False
) -> str:
    lines: list[str] = []
    for section in sections:
        lines.append(f"[{section.get('heading', '')}]")
        section_id = section.get("id")

        if section_id in {"summary", "one_action", "tools"}:
            for row in section.get("rows", []):
                lines.append(f"- {row}")
        elif section_id == "weakest_category":
            weakest = section.get("weakest_category")
            if weakest:
                grade_label = (
                    f" ({weakest.get('grade')})" if weakest.get("grade_visible") else ""
                )
                lines.append(f"- {weakest.get('label', '-')}{grade_label}")
                lines.append(f"  - {weakest.get('message_primary', '')}")
                lines.append(f"  - {weakest.get('message_secondary', '')}")
            else:
                lines.append("- 핵심 보완 항목을 추출하지 못했습니다. 상담으로 확인해 주세요.")

            if include_all_categories:
                lines.append("- 다른 진단 항목(전체)")
                for category in section.get("all_categories") or []:
                    grade_label = (
                        f" ({category.get('grade')})" if category.get("grade_visible") else ""
                    )
                    lines.append(f"  - {category.get('label', '-')}{grade_label}")
                    lines.append(f"    - {category.get('message_primary', '')}")
                    lines.append(f"    - {category.get('message_secondary', '')}")
        elif section_id == "next_action":
            cta = section.get("cta") or {}
            lines.append(f"- {cta.get('label', '상담 문의하기')} ({cta.get('href', '/#contact')})")
            if cta.get("note"):
                lines.append(f"- {cta.get('note')}")

        lines.append("")

    return "\n".join(lines).strip()
