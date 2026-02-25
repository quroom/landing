#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${ROOT_DIR}/scripts/django-check.sh"
"${ROOT_DIR}/scripts/django-test.sh"

echo "Verification passed: django check + django test"
