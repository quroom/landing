from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from django.http import HttpRequest


def i18n_context(request: HttpRequest) -> dict[str, str]:
    full_path = request.get_full_path()
    parsed = urlsplit(full_path)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    qs.pop("lang", None)
    new_query = urlencode(qs, doseq=True)
    clean_url = urlunsplit(("", "", parsed.path, new_query, parsed.fragment))
    return {
        "clean_next_url": clean_url or "/",
    }


def analytics_context(request: HttpRequest) -> dict[str, bool]:
    from .analytics import client_ip_from_request, is_excluded_ip

    return {"posthog_enabled": not is_excluded_ip(client_ip_from_request(request))}
