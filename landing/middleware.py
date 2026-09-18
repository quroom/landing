from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """Consolidate public www URLs without redirecting form POST requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical = urlsplit(settings.SITE_BASE_URL)
        if (
            request.method in {"GET", "HEAD"}
            and canonical.hostname
            and not canonical.hostname.startswith("www.")
            and request.get_host().split(":")[0].lower() == f"www.{canonical.hostname}"
        ):
            return HttpResponsePermanentRedirect(
                f"{canonical.scheme}://{canonical.netloc}{request.get_full_path()}"
            )
        return self.get_response(request)
