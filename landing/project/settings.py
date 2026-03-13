import os
from importlib.util import find_spec
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from landing.deploy_validation import collect_runtime_validation_errors

CODE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = CODE_ROOT.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [h for h in os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",") if h]
CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_migration_linter",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "landing.project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [CODE_ROOT / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "landing.project.wsgi.application"
ASGI_APPLICATION = "landing.project.asgi.application"


# Contact form does not require DB persistence. SQLite is kept for Django defaults.
def _first_env(*keys: str) -> str:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return ""


def _database_from_url(database_url: str) -> dict[str, object]:
    parsed = urlparse(database_url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise RuntimeError(
            "Unsupported DATABASE_URL scheme. Use postgres:// or postgresql://."
        )

    db_config: dict[str, object] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": (parsed.path or "").lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or ""),
    }
    extra_options = dict(parse_qsl(parsed.query, keep_blank_values=False))
    if extra_options:
        db_config["OPTIONS"] = extra_options
    return db_config


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": REPO_ROOT / "db.sqlite3",
    }
}

database_url = os.getenv("DATABASE_URL", "").strip()
if database_url:
    DATABASES["default"] = _database_from_url(database_url)
else:
    pg_host = _first_env("PGHOST", "DB_HOST")
    pg_name = _first_env("PGDATABASE", "DB_NAME")
    pg_user = _first_env("PGUSER", "DB_USER")
    pg_password = _first_env("PGPASSWORD", "DB_PASSWORD")
    pg_port = _first_env("PGPORT", "DB_PORT")
    if pg_host and pg_name and pg_user:
        DATABASES["default"] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": pg_name,
            "USER": pg_user,
            "PASSWORD": pg_password,
            "HOST": pg_host,
            "PORT": pg_port or "5432",
        }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko"
LANGUAGES = [
    ("ko", "Korean"),
    ("en", "English"),
]
LOCALE_PATHS = [REPO_ROOT / "locale"]
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    CODE_ROOT / "static",
    REPO_ROOT / "images",
]
STATIC_ROOT = REPO_ROOT / "staticfiles"

if DEBUG:
    staticfiles_storage_backend = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
else:
    if find_spec("whitenoise") is None:
        raise RuntimeError(
            "whitenoise is required when DJANGO_DEBUG=0. "
            "Install requirements and redeploy."
        )
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    staticfiles_storage_backend = "whitenoise.storage.CompressedStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": staticfiles_storage_backend,
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
SITE_BASE_URL = os.getenv("DJANGO_SITE_BASE_URL", "http://127.0.0.1:8000")
ALLOW_REAL_EMAIL_IN_DEBUG = os.getenv("DJANGO_ALLOW_REAL_EMAIL_IN_DEBUG", "0") == "1"


# In debug mode, block real SMTP unless explicitly allowed.
if (
    DEBUG
    and not ALLOW_REAL_EMAIL_IN_DEBUG
    and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend"
):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "0") == "1"
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "20"))
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "help@quroom.kr")
QUROOM_CONTACT_EMAIL = os.getenv("QUROOM_CONTACT_EMAIL", "help@quroom.kr")
GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "")
CONTACT_EMAIL_ASYNC = os.getenv("CONTACT_EMAIL_ASYNC", "1") == "1"
# In debug mode, disable async unless real email is explicitly allowed.
if DEBUG and not ALLOW_REAL_EMAIL_IN_DEBUG:
    CONTACT_EMAIL_ASYNC = False
TESTIMONIAL_PUBLIC_THRESHOLD = int(os.getenv("TESTIMONIAL_PUBLIC_THRESHOLD", "3"))
TESTIMONIAL_INVITE_EXPIRY_DAYS = int(os.getenv("TESTIMONIAL_INVITE_EXPIRY_DAYS", "7"))

_runtime_validation_errors = collect_runtime_validation_errors(globals())
if _runtime_validation_errors:
    error_lines = "\n".join(f"- {message}" for message in _runtime_validation_errors)
    raise RuntimeError(
        f"Production runtime configuration validation failed:\n{error_lines}"
    )
