from __future__ import annotations

from collections.abc import Mapping


SMTP_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
LOCAL_ONLY_EMAIL_BACKENDS = {
    "django.core.mail.backends.console.EmailBackend",
    "django.core.mail.backends.locmem.EmailBackend",
    "django.core.mail.backends.filebased.EmailBackend",
}


def _get_setting(settings_obj: object | Mapping[str, object], key: str, default: object) -> object:
    if isinstance(settings_obj, Mapping):
        return settings_obj.get(key, default)
    return getattr(settings_obj, key, default)


def collect_runtime_validation_errors(settings_obj: object | Mapping[str, object]) -> list[str]:
    debug = bool(_get_setting(settings_obj, "DEBUG", True))
    if debug:
        return []

    errors: list[str] = []
    secret_key = str(_get_setting(settings_obj, "SECRET_KEY", "")).strip()
    if not secret_key or secret_key == "dev-only-change-me":
        errors.append("DJANGO_SECRET_KEY must be set to a non-default value.")

    allowed_hosts = list(_get_setting(settings_obj, "ALLOWED_HOSTS", []))
    if not allowed_hosts or "*" in allowed_hosts:
        errors.append("DJANGO_ALLOWED_HOSTS must be configured without wildcard '*'.")

    csrf_trusted_origins = list(_get_setting(settings_obj, "CSRF_TRUSTED_ORIGINS", []))
    if not csrf_trusted_origins:
        errors.append("DJANGO_CSRF_TRUSTED_ORIGINS must be configured in production.")

    email_backend = str(_get_setting(settings_obj, "EMAIL_BACKEND", "")).strip()
    if email_backend in LOCAL_ONLY_EMAIL_BACKENDS:
        errors.append(
            "Production cannot use local-only DJANGO_EMAIL_BACKEND "
            "(console/locmem/filebased)."
        )

    if email_backend == SMTP_BACKEND:
        required_smtp_values: Mapping[str, object] = {
            "EMAIL_HOST": _get_setting(settings_obj, "EMAIL_HOST", ""),
            "EMAIL_PORT": _get_setting(settings_obj, "EMAIL_PORT", ""),
            "EMAIL_HOST_USER": _get_setting(settings_obj, "EMAIL_HOST_USER", ""),
            "EMAIL_HOST_PASSWORD": _get_setting(settings_obj, "EMAIL_HOST_PASSWORD", ""),
            "DEFAULT_FROM_EMAIL": _get_setting(settings_obj, "DEFAULT_FROM_EMAIL", ""),
        }
        missing = [key for key, value in required_smtp_values.items() if not value]
        if missing:
            errors.append(f"SMTP backend requires values for: {', '.join(missing)}")

    return errors
