#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APP="${APP:-landing}"
DOKKU_HOST="${DOKKU_HOST:-ubuntu@ssh.quroom.kr}"
REMOTE_BACKUP_ROOT="${REMOTE_BACKUP_ROOT:-~/backups/${APP}/postgres}"
LOCAL_BACKUP_ROOT="${LOCAL_BACKUP_ROOT:-${ROOT_DIR}/backups/prod-db/${APP}}"
BACKUP_BASENAME=""

usage() {
  cat <<'EOF'
Usage: ./scripts/fetch-prod-db-backup.sh [options]

Options:
  --host <user@host>      Dokku SSH host (default: ubuntu@ssh.quroom.kr)
  --app <name>            Dokku app name (default: landing)
  --remote-root <path>    Remote backup directory
  --local-root <path>     Local destination directory
  --file <basename>       Backup basename without extension (default: latest)
  -h, --help              Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      DOKKU_HOST="${2:-}"
      shift 2
      ;;
    --app)
      APP="${2:-}"
      shift 2
      ;;
    --remote-root)
      REMOTE_BACKUP_ROOT="${2:-}"
      shift 2
      ;;
    --local-root)
      LOCAL_BACKUP_ROOT="${2:-}"
      shift 2
      ;;
    --file)
      BACKUP_BASENAME="${2:-}"
      shift 2
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

for cmd in ssh scp; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
done

if [[ -z "${BACKUP_BASENAME}" ]]; then
  BACKUP_BASENAME="$(
    ssh -o BatchMode=yes "${DOKKU_HOST}" \
      "ls -1t ${REMOTE_BACKUP_ROOT}/${APP}-*.dump 2>/dev/null | head -n 1 | xargs -r basename | sed 's/\\.dump\$//'"
  )"
fi

if [[ -z "${BACKUP_BASENAME}" ]]; then
  echo "No backup dump found on remote host." >&2
  exit 1
fi

mkdir -p "${LOCAL_BACKUP_ROOT}"

for suffix in dump json sha256; do
  if ssh -o BatchMode=yes "${DOKKU_HOST}" "test -f ${REMOTE_BACKUP_ROOT}/${BACKUP_BASENAME}.${suffix}"; then
    scp "${DOKKU_HOST}:${REMOTE_BACKUP_ROOT}/${BACKUP_BASENAME}.${suffix}" "${LOCAL_BACKUP_ROOT}/"
  fi
done

echo "Fetched backup:"
echo "  ${LOCAL_BACKUP_ROOT}/${BACKUP_BASENAME}.dump"
