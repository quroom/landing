#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Missing virtualenv python at ${VENV_PYTHON}" >&2
  exit 1
fi

cd "${ROOT_DIR}"

require_module() {
  local module="$1"
  if ! "${VENV_PYTHON}" -c "import ${module}" >/dev/null 2>&1; then
    echo "[format-apply] Missing dependency: ${module}" >&2
    echo "Install with: .venv/bin/pip install -r requirements.txt" >&2
    exit 1
  fi
}

require_module "ruff"
require_module "djlint"

echo "[format-apply] Ruff lint fix"
"${VENV_PYTHON}" -m ruff check --fix .

echo "[format-apply] Ruff format"
"${VENV_PYTHON}" -m ruff format .

echo "[format-apply] djLint reformat"
"${VENV_PYTHON}" -m djlint --reformat landing/templates

echo "Format apply completed."
