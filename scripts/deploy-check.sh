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
