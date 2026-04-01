from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase, override_settings

from landing.deploy_validation import (
    collect_readiness_errors,
    collect_runtime_validation_errors,
)


class DeployValidationTests(SimpleTestCase):
    def test_collect_runtime_validation_errors_returns_empty_in_debug(self) -> None:
        errors = collect_runtime_validation_errors({"DEBUG": True})
        self.assertEqual(errors, [])

    def test_collect_runtime_validation_errors_detects_production_contract(
        self,
    ) -> None:
        errors = collect_runtime_validation_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "dev-only-change-me",
                "ALLOWED_HOSTS": ["*"],
                "CSRF_TRUSTED_ORIGINS": [],
                "EMAIL_BACKEND": "django.core.mail.backends.console.EmailBackend",
            }
        )
        self.assertGreaterEqual(len(errors), 4)
        self.assertTrue(
            any("DJANGO_SECRET_KEY" in message for message in errors),
            errors,
        )

    def test_collect_runtime_validation_errors_requires_smtp_contract(self) -> None:
        errors = collect_runtime_validation_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "secure-key",
                "ALLOWED_HOSTS": ["example.com"],
                "CSRF_TRUSTED_ORIGINS": ["https://example.com"],
                "SITE_BASE_URL": "https://quroom.kr",
                "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
                "EMAIL_HOST": "smtp.example.com",
                "EMAIL_PORT": 587,
                "EMAIL_HOST_USER": "",
                "EMAIL_HOST_PASSWORD": "",
                "DEFAULT_FROM_EMAIL": "",
            }
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("SMTP backend requires values for", errors[0])

    def test_collect_readiness_errors_requires_static_root_in_production(self) -> None:
        errors = collect_readiness_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "secure-key",
                "ALLOWED_HOSTS": ["example.com"],
                "CSRF_TRUSTED_ORIGINS": ["https://example.com"],
                "SITE_BASE_URL": "https://quroom.kr",
                "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
                "EMAIL_HOST": "smtp.example.com",
                "EMAIL_PORT": 587,
                "EMAIL_HOST_USER": "user",
                "EMAIL_HOST_PASSWORD": "pw",
                "DEFAULT_FROM_EMAIL": "help@example.com",
                "STATIC_ROOT": "",
            }
        )
        self.assertIn("STATIC_ROOT must be configured for deploy readiness.", errors)

    def test_collect_readiness_errors_rejects_sqlite_in_production(self) -> None:
        errors = collect_readiness_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "secure-key",
                "ALLOWED_HOSTS": ["example.com"],
                "CSRF_TRUSTED_ORIGINS": ["https://example.com"],
                "SITE_BASE_URL": "https://quroom.kr",
                "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
                "EMAIL_HOST": "smtp.example.com",
                "EMAIL_PORT": 587,
                "EMAIL_HOST_USER": "user",
                "EMAIL_HOST_PASSWORD": "pw",
                "DEFAULT_FROM_EMAIL": "help@example.com",
                "STATIC_ROOT": "/tmp/static",
                "DATABASES": {
                    "default": {
                        "ENGINE": "django.db.backends.sqlite3",
                        "NAME": "/tmp/db.sqlite3",
                    }
                },
            }
        )
        self.assertIn(
            "Production database cannot use sqlite3. "
            "Configure PostgreSQL via DATABASE_URL or PG* variables.",
            errors,
        )

    def test_collect_runtime_validation_errors_requires_quroom_site_base_url(
        self,
    ) -> None:
        errors = collect_runtime_validation_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "secure-key",
                "ALLOWED_HOSTS": ["quroom.kr"],
                "CSRF_TRUSTED_ORIGINS": ["https://quroom.kr"],
                "SITE_BASE_URL": "https://www.quroom.kr",
                "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
                "EMAIL_HOST": "smtp.example.com",
                "EMAIL_PORT": 587,
                "EMAIL_HOST_USER": "user",
                "EMAIL_HOST_PASSWORD": "pw",
                "DEFAULT_FROM_EMAIL": "help@quroom.kr",
            }
        )
        self.assertIn(
            "DJANGO_SITE_BASE_URL must be exactly https://quroom.kr in production.",
            errors,
        )

    def test_collect_runtime_validation_errors_accepts_quroom_site_base_url(
        self,
    ) -> None:
        errors = collect_runtime_validation_errors(
            {
                "DEBUG": False,
                "SECRET_KEY": "secure-key",
                "ALLOWED_HOSTS": ["quroom.kr"],
                "CSRF_TRUSTED_ORIGINS": ["https://quroom.kr"],
                "SITE_BASE_URL": "https://quroom.kr",
                "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
                "EMAIL_HOST": "smtp.example.com",
                "EMAIL_PORT": 587,
                "EMAIL_HOST_USER": "user",
                "EMAIL_HOST_PASSWORD": "pw",
                "DEFAULT_FROM_EMAIL": "help@quroom.kr",
            }
        )
        self.assertEqual(errors, [])


class DeployReadinessCommandTests(TestCase):
    @override_settings(
        DEBUG=True,
        SECRET_KEY="dev-only-change-me",
        ALLOWED_HOSTS=["*"],
        CSRF_TRUSTED_ORIGINS=[],
        EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
    )
    def test_check_deploy_ready_passes_in_default_debug_mode(self) -> None:
        call_command("check_deploy_ready", stdout=StringIO(), stderr=StringIO())

    @override_settings(
        DEBUG=False,
        SECRET_KEY="dev-only-change-me",
        ALLOWED_HOSTS=["*"],
        CSRF_TRUSTED_ORIGINS=[],
        SITE_BASE_URL="http://127.0.0.1:8000",
        EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
    )
    def test_check_deploy_ready_fails_for_invalid_production_settings(self) -> None:
        with self.assertRaises(CommandError):
            call_command("check_deploy_ready", stdout=StringIO(), stderr=StringIO())
