from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


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
            return urlunsplit(
                (parsed.scheme, parsed.netloc, path, parsed.query, "contact")
            )
    return value


def attach_diagnosis_contact_context(href: str, context: dict | None = None) -> str:
    normalized_href = normalize_contact_cta_href(href)
    if not context:
        return normalized_href

    inquiry_type = (context.get("inquiry_type") or "").strip()
    lead_context = (context.get("lead_context") or "").strip()
    if not inquiry_type and not lead_context:
        return normalized_href

    parsed = urlsplit(normalized_href)
    if parsed.fragment != "contact":
        return normalized_href

    merged = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if inquiry_type:
        merged["inquiry_type"] = inquiry_type
    if lead_context:
        merged["lead_context"] = lead_context
    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urlencode(merged), parsed.fragment)
    )


def build_lead_magnet_section_ast(payload: dict) -> list[dict]:
    grade = payload.get("grade", "B")
    weakest = payload.get("weakest_insight") or payload.get("weakest_category_insight")
    category_insights = payload.get("category_insights") or payload.get("insights") or []
    if not weakest:
        weakest_key = payload.get("weakest_axis_key")
        weakest = next(
            (item for item in category_insights if item.get("key") == weakest_key),
            category_insights[0] if category_insights else None,
        )

    one_action = payload.get("one_action") or {}
    cta = payload.get("cta") or {}
    normalized_cta_href = attach_diagnosis_contact_context(
        cta.get("href", "#contact"),
        payload.get("contact_context"),
    )
    primary_tools = [
        item.strip()
        for item in (one_action.get("tools") or "").split(",")
        if item.strip()
    ]
    profile_tools = payload.get("profile_tools") or []
    merged_tools: list[str] = []
    for item in primary_tools + profile_tools:
        if item and item not in merged_tools:
            merged_tools.append(item)

    return [
        {
            "id": "summary",
            "heading": "진단 요약",
            "rows": [
                f"점수: {payload.get('score', 0)}/{payload.get('max_score', 0)}",
                f"등급: {grade}",
                (
                    f"진단 유형: {payload.get('coverage_label', '')}"
                    if payload.get("coverage_label")
                    else ""
                ),
                f"한 줄 요약: {payload.get('summary', '')}",
            ],
        },
        {
            "id": "weakest",
            "heading": "핵심 보완 포인트",
            "weakest_insight": weakest,
            "all_insights": category_insights,
        },
        {
            "id": "one_action",
            "heading": "2주 내 끝낼 작업 1개",
            "rows": [
                f"작업: {one_action.get('title', '-')}",
                f"완료 기준: {one_action.get('execution', '-')}",
            ],
        },
        {
            "id": "tools",
            "heading": "주요 추천 툴",
            "rows": [
                (
                    ", ".join(merged_tools[:3])
                    if merged_tools
                    else "Make, Google Sheets, Notion"
                )
            ],
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
                if not row:
                    continue
                lines.append(f"- {row}")
        elif section_id in {"weakest", "weakest_category"}:
            weakest = section.get("weakest_insight") or section.get("weakest_category")
            if weakest:
                grade_label = (
                    f" ({weakest.get('grade')})" if weakest.get("grade_visible") else ""
                )
                lines.append(f"- {weakest.get('label', '-')}{grade_label}")
                lines.append(f"  - {weakest.get('message_primary', '')}")
                lines.append(f"  - {weakest.get('message_secondary', '')}")
            else:
                lines.append(
                    "- 핵심 보완 항목을 추출하지 못했습니다. 상담으로 확인해 주세요."
                )

            if include_all_categories:
                lines.append("- 다른 진단 포인트(전체)")
                for category in section.get("all_insights") or section.get("all_categories") or []:
                    grade_label = (
                        f" ({category.get('grade')})"
                        if category.get("grade_visible")
                        else ""
                    )
                    lines.append(f"  - {category.get('label', '-')}{grade_label}")
                    lines.append(f"    - {category.get('message_primary', '')}")
                    lines.append(f"    - {category.get('message_secondary', '')}")
        elif section_id == "next_action":
            cta = section.get("cta") or {}
            lines.append(
                f"- {cta.get('label', '상담 문의하기')} ({cta.get('href', '/#contact')})"
            )
            if cta.get("note"):
                lines.append(f"- {cta.get('note')}")

        lines.append("")

    return "\n".join(lines).strip()
