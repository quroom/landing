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
    echo "[format-check] Missing dependency: ${module}" >&2
    echo "Install with: .venv/bin/pip install -r requirements.txt" >&2
    exit 1
  fi
}

require_module "ruff"
require_module "djlint"

run_djlint_check_per_file() {
  mapfile -t template_files < <(rg --files landing/templates -g "*.html" | sort)
  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo "[format-check] No template files found under landing/templates"
    return 0
  fi

  local file
  for file in "${template_files[@]}"; do
    "${VENV_PYTHON}" -m djlint --check "${file}"
  done
}

echo "[format-check] Ruff lint"
"${VENV_PYTHON}" -m ruff check .

echo "[format-check] Ruff format check"
"${VENV_PYTHON}" -m ruff format --check .

echo "[format-check] djLint check (file-by-file)"
run_djlint_check_per_file

echo "Format check passed."
echo "If this fails locally, run: ./scripts/format-apply.sh"
