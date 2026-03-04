#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-}"
if [[ -z "${BASE_URL}" ]]; then
  echo "BASE_URL is required (example: https://your-app.up.railway.app)" >&2
  exit 1
fi

check_code() {
  local path="$1"
  local expected="$2"
  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" "${BASE_URL}${path}")"
  if [[ "${code}" != "${expected}" ]]; then
    echo "Smoke check failed: ${path} expected ${expected}, got ${code}" >&2
    exit 1
  fi
  echo "OK ${path} -> ${code}"
}

check_not_404() {
  local path="$1"
  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" "${BASE_URL}${path}")"
  if [[ "${code}" == "404" ]]; then
    echo "Smoke check failed: ${path} returned 404" >&2
    exit 1
  fi
  echo "OK ${path} -> ${code}"
}

check_code "/healthz/" "200"
check_not_404 "/admin-dashboard/"
check_not_404 "/contact/submit/"
check_not_404 "/lead-magnet/submit/"

echo "Post-deploy smoke checks passed."
