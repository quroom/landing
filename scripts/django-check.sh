#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Error: ${VENV_PYTHON} not found. Create venv first: python3 -m venv .venv" >&2
  exit 1
fi

cd "${ROOT_DIR}"
"${VENV_PYTHON}" manage.py check
