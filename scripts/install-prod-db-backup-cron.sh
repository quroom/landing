#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APP="${APP:-landing}"
DOKKU_HOST="${DOKKU_HOST:-ubuntu@ssh.quroom.kr}"
REMOTE_SCRIPT_PATH="${REMOTE_SCRIPT_PATH:-}"
REMOTE_BACKUP_ROOT="${REMOTE_BACKUP_ROOT:-}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
CRON_SCHEDULE="${CRON_SCHEDULE:-15 3 * * *}"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install-prod-db-backup-cron.sh [options]

Options:
  --host <user@host>        Dokku SSH host (default: ubuntu@ssh.quroom.kr)
  --app <name>              Dokku app name (default: landing)
  --schedule "<cron expr>"  Cron schedule (default: 15 3 * * *)
  --backup-root <path>      Remote backup directory (default: $HOME/backups/<app>/postgres)
  --retention-days <days>   Number of days to keep backups (default: 14)
  --remote-script <path>    Remote script path (default: ~/bin/<app>-prod-db-backup.sh)
  --dry-run                 Print actions without remote changes
  -h, --help                Show this help message
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
    --schedule)
      CRON_SCHEDULE="${2:-}"
      shift 2
      ;;
    --backup-root)
      REMOTE_BACKUP_ROOT="${2:-}"
      shift 2
      ;;
    --retention-days)
      RETENTION_DAYS="${2:-}"
      shift 2
      ;;
    --remote-script)
      REMOTE_SCRIPT_PATH="${2:-}"
      shift 2
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

for cmd in ssh scp; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
done

if [[ -z "${REMOTE_SCRIPT_PATH}" ]]; then
  REMOTE_SCRIPT_PATH="/home/ubuntu/bin/${APP}-prod-db-backup.sh"
fi

if [[ -z "${REMOTE_BACKUP_ROOT}" ]]; then
  REMOTE_BACKUP_ROOT="/home/ubuntu/backups/${APP}/postgres"
fi

REMOTE_SCRIPT_DIR="$(dirname "${REMOTE_SCRIPT_PATH}")"
printf -v REMOTE_SCRIPT_DIR_Q '%q' "${REMOTE_SCRIPT_DIR}"
printf -v REMOTE_SCRIPT_PATH_Q '%q' "${REMOTE_SCRIPT_PATH}"
printf -v REMOTE_BACKUP_ROOT_Q '%q' "${REMOTE_BACKUP_ROOT}"

CRON_ENTRY="${CRON_SCHEDULE} APP=${APP} BACKUP_ROOT=${REMOTE_BACKUP_ROOT} RETENTION_DAYS=${RETENTION_DAYS} ${REMOTE_SCRIPT_PATH} >> ${REMOTE_BACKUP_ROOT}/cron.log 2>&1"

echo "Install backup cron:"
echo "  host          : ${DOKKU_HOST}"
echo "  app           : ${APP}"
echo "  schedule      : ${CRON_SCHEDULE}"
echo "  backup root   : ${REMOTE_BACKUP_ROOT}"
echo "  retention days: ${RETENTION_DAYS}"
echo "  remote script : ${REMOTE_SCRIPT_PATH}"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "Dry-run mode enabled; exiting without changes."
  exit 0
fi

ssh -o BatchMode=yes "${DOKKU_HOST}" \
  "mkdir -p ${REMOTE_SCRIPT_DIR_Q} ${REMOTE_BACKUP_ROOT_Q}"
scp "${ROOT_DIR}/scripts/remote-prod-db-backup.sh" "${DOKKU_HOST}:${REMOTE_SCRIPT_PATH}"
ssh -o BatchMode=yes "${DOKKU_HOST}" "chmod 755 ${REMOTE_SCRIPT_PATH_Q}"

ssh -o BatchMode=yes "${DOKKU_HOST}" \
  "(crontab -l 2>/dev/null | grep -Fv ${REMOTE_SCRIPT_PATH_Q} || true; echo '${CRON_ENTRY}') | crontab -"

echo "Cron installed successfully."
echo "To test one-off backup:"
echo "  ssh ${DOKKU_HOST} 'APP=${APP} BACKUP_ROOT=${REMOTE_BACKUP_ROOT} RETENTION_DAYS=${RETENTION_DAYS} ${REMOTE_SCRIPT_PATH}'"
