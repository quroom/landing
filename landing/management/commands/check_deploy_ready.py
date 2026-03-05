from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from landing.deploy_validation import collect_readiness_errors


class Command(BaseCommand):
    help = "Validate deployment readiness (runtime config, DB, static contract)."

    def handle(self, *args: object, **options: object) -> None:
        checks: list[dict[str, object]] = []

        readiness_errors = collect_readiness_errors(settings)
        checks.append(
            {
                "name": "runtime_contract",
                "ok": not readiness_errors,
                "detail": "; ".join(readiness_errors) if readiness_errors else "ok",
            }
        )

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            db_check = {"name": "database", "ok": True, "detail": "ok"}
        except Exception as exc:
            db_check = {
                "name": "database",
                "ok": False,
                "detail": f"Database connectivity check failed: {exc}",
            }
        checks.append(db_check)

        failed_checks = [check for check in checks if not bool(check["ok"])]
        status_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "check_type": "deploy_check",
            "status": "failed" if failed_checks else "passed",
            "items": checks,
        }
        status_file = os.getenv("DEPLOY_STATUS_FILE", "/tmp/quroom-deploy-status.json").strip()
        if status_file:
            history: list[dict[str, object]] = []
            try:
                with open(status_file, encoding="utf-8") as fp:
                    existing = json.load(fp)
                if isinstance(existing, list):
                    history = [item for item in existing if isinstance(item, dict)]
                elif isinstance(existing, dict):
                    history = [existing]
            except (OSError, json.JSONDecodeError):
                history = []

            history = [
                item
                for item in history
                if str(item.get("check_type", "")).strip() != "deploy_check"
            ]
            history.append(status_payload)
            with open(status_file, "w", encoding="utf-8") as fp:
                json.dump(history, fp, ensure_ascii=False, indent=2)

        if failed_checks:
            for check in failed_checks:
                self.stderr.write(
                    self.style.ERROR(f"- [FAIL] {check['name']}: {check['detail']}")
                )
            raise CommandError("Deployment readiness check failed.")

        for check in checks:
            self.stdout.write(self.style.SUCCESS(f"- [OK] {check['name']}: {check['detail']}"))
        self.stdout.write(self.style.SUCCESS("Deployment readiness check passed."))
