#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLOP_GATE="${ROOT_DIR}/tools/copy-lint/node_modules/.bin/slop-gate"

if [[ ! -x "${SLOP_GATE}" ]]; then
  echo "[copy-check] Missing slop-gate. Run: npm ci --prefix tools/copy-lint" >&2
  exit 1
fi

echo "[copy-check] AI writing-pattern scan"
cd "${ROOT_DIR}"
"${SLOP_GATE}"
