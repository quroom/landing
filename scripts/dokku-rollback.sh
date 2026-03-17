#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APP="${APP:-landing}"
DOKKU_HOST="${DOKKU_HOST:-ubuntu@43.200.44.34}"
REPO_URL="${REPO_URL:-git@github.com:quroom/landing.git}"
BASE_URL="${BASE_URL:-https://quroom.kr}"
TARGET_SHA=""
SKIP_SMOKE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./scripts/dokku-rollback.sh [options]

Options:
  --target-sha <sha>   Roll back to an explicit git commit SHA.
  --app <name>         Dokku app name (default: landing).
  --host <user@host>   Dokku SSH host (default: ubuntu@43.200.44.34).
  --repo <git-url>     Git repo URL for dokku git:sync.
  --base-url <url>     Base URL for post-deploy smoke (default: https://quroom.kr).
  --skip-smoke         Skip post-deploy smoke checks.
  --dry-run            Print actions without executing rollback.
  -h, --help           Show this help message.

Notes:
  - If --target-sha is omitted, script rolls back one commit from current deployed SHA.
  - After rollback, script verifies deployed SHA and runs ./scripts/post-deploy-smoke.sh.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-sha)
      TARGET_SHA="${2:-}"
      shift 2
      ;;
    --app)
      APP="${2:-}"
      shift 2
      ;;
    --host)
      DOKKU_HOST="${2:-}"
      shift 2
      ;;
    --repo)
      REPO_URL="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --skip-smoke)
      SKIP_SMOKE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

for cmd in git ssh awk; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
done

get_current_sha() {
  ssh -o BatchMode=yes "${DOKKU_HOST}" \
    "dokku git:report ${APP} | awk -F': +' '/Git sha:/ {print \$2}'" \
    | tr -d '\r' | xargs
}

CURRENT_SHA="$(get_current_sha)"
if [[ -z "${CURRENT_SHA}" ]]; then
  echo "Failed to resolve current deployed SHA for app '${APP}'." >&2
  exit 1
fi

if [[ -z "${TARGET_SHA}" ]]; then
  git fetch --quiet origin main
  if ! TARGET_SHA="$(git rev-parse "${CURRENT_SHA}^" 2>/dev/null)"; then
    echo "Failed to resolve previous SHA from current deployed SHA: ${CURRENT_SHA}" >&2
    echo "Use --target-sha <sha> explicitly." >&2
    exit 1
  fi
fi

if ! git cat-file -e "${TARGET_SHA}^{commit}" 2>/dev/null; then
  echo "Target SHA not found in local git history: ${TARGET_SHA}" >&2
  exit 1
fi

if [[ "${TARGET_SHA}" == "${CURRENT_SHA}" ]]; then
  echo "Current SHA and target SHA are identical (${CURRENT_SHA}); nothing to roll back." >&2
  exit 1
fi

echo "Rollback plan:"
echo "  app        : ${APP}"
echo "  host       : ${DOKKU_HOST}"
echo "  repo       : ${REPO_URL}"
echo "  current sha: ${CURRENT_SHA}"
echo "  target sha : ${TARGET_SHA}"
echo "  smoke      : $([[ ${SKIP_SMOKE} -eq 1 ]] && echo 'skip' || echo "run (${BASE_URL})")"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "Dry-run mode enabled; exiting without changes."
  exit 0
fi

ssh -o BatchMode=yes "${DOKKU_HOST}" \
  "dokku git:sync ${APP} ${REPO_URL} ${TARGET_SHA}"

DEPLOYED_SHA="$(get_current_sha)"
if [[ "${DEPLOYED_SHA}" != "${TARGET_SHA}" ]]; then
  echo "Rollback verification failed: deployed SHA is ${DEPLOYED_SHA}, expected ${TARGET_SHA}" >&2
  exit 1
fi

if [[ ${SKIP_SMOKE} -eq 0 ]]; then
  BASE_URL="${BASE_URL}" "${ROOT_DIR}/scripts/post-deploy-smoke.sh"
fi

echo "Rollback completed successfully."
echo "To roll forward back to previous deploy:"
echo "  ./scripts/dokku-rollback.sh --target-sha ${CURRENT_SHA}"
