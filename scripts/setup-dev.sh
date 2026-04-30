#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

usage() {
  cat <<'EOF'
Usage: ./scripts/setup-dev.sh

Creates .venv and installs project requirements for local Django development.

Optional environment variables:
  PYTHON_BIN   Python executable to use (default: python3)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Missing required command: ${PYTHON_BIN}" >&2
  exit 1
fi

"${PYTHON_BIN}" -m venv "${ROOT_DIR}/.venv"
"${ROOT_DIR}/.venv/bin/pip" install --upgrade pip
"${ROOT_DIR}/.venv/bin/pip" install -r "${ROOT_DIR}/requirements.txt"
"${ROOT_DIR}/scripts/install-git-hooks.sh"

echo "Local dev environment is ready."
echo "  activate: source ${ROOT_DIR}/.venv/bin/activate"
echo "  run     : ./.venv/bin/python manage.py runserver"
