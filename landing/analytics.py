from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from .models import FunnelEvent


def _extract_utm(request: HttpRequest) -> dict[str, str]:
    source = request.GET.get("utm_source", "")
    medium = request.GET.get("utm_medium", "")
    campaign = request.GET.get("utm_campaign", "")
    term = request.GET.get("utm_term", "")
    content = request.GET.get("utm_content", "")
    return {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
        "utm_term": term,
        "utm_content": content,
    }


def track_event(
    request: HttpRequest,
    event_name: str,
    *,
    page_key: str = "",
    lead_source: str = "",
    metadata: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {}
    payload.update(_extract_utm(request))
    if metadata:
        payload.update(metadata)

    FunnelEvent.objects.create(
        event_name=event_name,
        page_key=page_key,
        lead_source=lead_source,
        metadata=payload,
    )
