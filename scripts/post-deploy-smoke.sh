#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-}"
if [[ -z "${BASE_URL}" ]]; then
  echo "BASE_URL is required (example: https://your-app.example.com)" >&2
  exit 1
fi
DEPLOY_STATUS_FILE="${DEPLOY_STATUS_FILE:-/tmp/quroom-deploy-status.json}"

TMP_RESULT_FILE="$(mktemp)"
FAILED_COUNT=0

record_result() {
  local path="$1"
  local expected="$2"
  local actual="$3"
  local ok="$4"
  printf "%s\t%s\t%s\t%s\n" "${path}" "${expected}" "${actual}" "${ok}" >> "${TMP_RESULT_FILE}"
}

check_code() {
  local path="$1"
  local expected="$2"
  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" "${BASE_URL}${path}")"
  if [[ "${code}" != "${expected}" ]]; then
    FAILED_COUNT=$((FAILED_COUNT + 1))
    record_result "${path}" "${expected}" "${code}" "false"
    echo "Smoke check failed: ${path} expected ${expected}, got ${code}" >&2
    return
  fi
  record_result "${path}" "${expected}" "${code}" "true"
  echo "OK ${path} -> ${code}"
}

write_status_file() {
  local status_file="$1"
  local final_status="$2"

  python3 - "${status_file}" "${final_status}" "${TMP_RESULT_FILE}" <<'PY'
import json
import sys
from datetime import datetime, timezone

status_file = sys.argv[1]
final_status = sys.argv[2]
result_file = sys.argv[3]

items = []
failed_items = []
with open(result_file, encoding="utf-8") as fp:
    for raw in fp:
        path, expected, actual, ok = raw.strip().split("\t")
        item = {
            "path": path,
            "expected": expected,
            "actual": actual,
            "ok": ok == "true",
        }
        items.append(item)
        if not item["ok"]:
            failed_items.append(path)

payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "check_type": "smoke_check",
    "status": final_status,
    "items": items,
    "failed_items": failed_items,
}

history = []
try:
    with open(status_file, encoding="utf-8") as fp:
        existing = json.load(fp)
    if isinstance(existing, list):
        history = [item for item in existing if isinstance(item, dict)]
    elif isinstance(existing, dict):
        history = [existing]
except (OSError, json.JSONDecodeError):
    history = []

history = [item for item in history if str(item.get("check_type", "")).strip() != "smoke_check"]
history.append(payload)

with open(status_file, "w", encoding="utf-8") as fp:
    json.dump(history, fp, ensure_ascii=False, indent=2)
PY
}

check_code "/healthz/" "200"
check_code "/healthz/live/" "200"
check_code "/healthz/ready/" "200"
check_code "/admin-dashboard/" "302"
check_code "/admin-operation-links/" "302"
check_code "/contact/submit/" "405"
check_code "/lead-magnet/submit/" "405"
check_code "/robots.txt" "200"
check_code "/sitemap.xml" "200"

FINAL_STATUS="passed"
if [[ "${FAILED_COUNT}" -gt 0 ]]; then
  FINAL_STATUS="failed"
fi

write_status_file "${DEPLOY_STATUS_FILE}" "${FINAL_STATUS}"

rm -f "${TMP_RESULT_FILE}"

if [[ "${FINAL_STATUS}" == "failed" ]]; then
  echo "Post-deploy smoke checks failed (${FAILED_COUNT} failure(s))." >&2
  exit 1
fi

echo "Post-deploy smoke checks passed."
