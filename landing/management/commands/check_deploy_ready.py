from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from landing.deploy_validation import collect_runtime_validation_errors


class Command(BaseCommand):
    help = "Validate deployment readiness (runtime config, DB, static contract)."

    def handle(self, *args: object, **options: object) -> None:
        errors = collect_runtime_validation_errors(settings)

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception as exc:
            errors.append(f"Database connectivity check failed: {exc}")

        if not getattr(settings, "STATIC_ROOT", None):
            errors.append("STATIC_ROOT must be configured for deploy readiness.")

        if errors:
            for message in errors:
                self.stderr.write(self.style.ERROR(f"- {message}"))
            raise CommandError("Deployment readiness check failed.")

        self.stdout.write(self.style.SUCCESS("Deployment readiness check passed."))
