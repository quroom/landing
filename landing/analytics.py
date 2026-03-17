from __future__ import annotations

from ipaddress import ip_address, ip_network
from typing import Any

from django.conf import settings
from django.db import DatabaseError
from django.http import HttpRequest

from .models import AnalyticsExcludedIP, FunnelEvent

DEFAULT_CLOUDFLARE_PROXY_CIDRS: tuple[str, ...] = (
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
    "2400:cb00::/32",
    "2606:4700::/32",
    "2803:f800::/32",
    "2405:b500::/32",
    "2405:8100::/32",
    "2a06:98c0::/29",
    "2c0f:f248::/32",
)
CLOUDFLARE_PROXY_NETWORKS = tuple(
    ip_network(cidr) for cidr in DEFAULT_CLOUDFLARE_PROXY_CIDRS
)


def _normalize_ip(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    if raw.startswith("[") and "]" in raw:
        raw = raw[1 : raw.index("]")]
    if raw.count(":") == 1 and raw.rsplit(":", 1)[1].isdigit():
        raw = raw.rsplit(":", 1)[0]
    try:
        return str(ip_address(raw))
    except ValueError:
        return ""


def _first_forwarded_ip(request: HttpRequest) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    for hop in forwarded_for.split(","):
        candidate = _normalize_ip(hop)
        if candidate:
            return candidate
    return ""


def _should_trust_cf_connecting_ip(source_ip: str) -> bool:
    source = _normalize_ip(source_ip)
    if not source:
        return False
    try:
        source_obj = ip_address(source)
    except ValueError:
        return False
    return any(source_obj in network for network in CLOUDFLARE_PROXY_NETWORKS)


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


def client_ip_from_request(request: HttpRequest) -> str:
    source_ip = _first_forwarded_ip(request) or _normalize_ip(
        request.META.get("REMOTE_ADDR", "")
    )
    cf_connecting_ip = _normalize_ip(request.META.get("HTTP_CF_CONNECTING_IP", ""))
    if cf_connecting_ip and _should_trust_cf_connecting_ip(source_ip):
        return cf_connecting_ip
    return source_ip


def _is_excluded_ip(client_ip: str) -> bool:
    excluded_ips = getattr(settings, "ANALYTICS_EXCLUDED_IPS", [])
    if not client_ip or not excluded_ips:
        return _is_excluded_ip_from_db(client_ip)
    if client_ip in set(excluded_ips):
        return True
    return _is_excluded_ip_from_db(client_ip)


def _is_excluded_ip_from_db(client_ip: str) -> bool:
    if not client_ip:
        return False
    try:
        return AnalyticsExcludedIP.objects.filter(
            ip_address=client_ip,
            is_active=True,
        ).exists()
    except DatabaseError:
        # During migration bootstrap, exclude check should fail-open.
        return False


def track_event(
    request: HttpRequest,
    event_name: str,
    *,
    page_key: str = "",
    lead_source: str = "",
    metadata: dict[str, Any] | None = None,
) -> None:
    client_ip = client_ip_from_request(request)
    if _is_excluded_ip(client_ip):
        return

    payload: dict[str, Any] = {}
    payload.update(_extract_utm(request))
    if metadata:
        payload.update(metadata)

    FunnelEvent.objects.create(
        event_name=event_name,
        page_key=page_key,
        lead_source=lead_source,
        client_ip=client_ip or None,
        metadata=payload,
    )
