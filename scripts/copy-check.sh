#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLOP_GATE="${ROOT_DIR}/tools/copy-lint/node_modules/.bin/slop-gate"

if [[ ! -x "${SLOP_GATE}" ]]; then
  echo "[copy-check] Missing slop-gate. Run: npm ci --prefix tools/copy-lint" >&2
  exit 1
fi

echo "[copy-check] 1/2: slop-gate scan (translationese & writing tells)"
cd "${ROOT_DIR}"
"${SLOP_GATE}"

echo ""
echo "[copy-check] 2/2: korean-slop-lint scan (AI clichés & marketing tropes)"
python3 "${ROOT_DIR}/scripts/lint_korean_slop.py"
