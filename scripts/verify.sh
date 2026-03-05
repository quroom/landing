#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${ROOT_DIR}/scripts/format-check.sh"
"${ROOT_DIR}/scripts/django-check.sh"
"${ROOT_DIR}/scripts/django-test.sh"

echo "Verification passed: format check + django check + django test"
