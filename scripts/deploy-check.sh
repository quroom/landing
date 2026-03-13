#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Missing virtualenv python at ${VENV_PYTHON}" >&2
  exit 1
fi

cd "${ROOT_DIR}"
export DEPLOY_STATUS_FILE="${DEPLOY_STATUS_FILE:-/tmp/quroom-deploy-status.json}"
"${VENV_PYTHON}" manage.py check_deploy_ready

LEAF_MIGRATIONS="$("${VENV_PYTHON}" - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "landing.project.settings")
import django
from django.db import connection
from django.db.migrations.loader import MigrationLoader

django.setup()
loader = MigrationLoader(connection, ignore_no_migrations=True)
leaf_names = sorted(name for app, name in loader.graph.leaf_nodes("landing"))
print(" ".join(leaf_names))
PY
)"

if [[ -z "${LEAF_MIGRATIONS}" ]]; then
  echo "No landing leaf migrations found for linting." >&2
  exit 1
fi

# Lint active landing migration heads to guard backwards-compatible deploys.
"${VENV_PYTHON}" manage.py lintmigrations \
  --include-apps landing \
  --include-name ${LEAF_MIGRATIONS} \
  --ignore-initial-migrations \
  --no-cache
