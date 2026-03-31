#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT_DIR}/scripts/lib/landing_snapshot_compose.sh"
APP="${APP:-landing}"
LOCAL_BACKUP_ROOT="${LOCAL_BACKUP_ROOT:-${ROOT_DIR}/backups/prod-db/${APP}}"
BACKUP_FILE=""
FETCH_LATEST=0
FRESH=0

usage() {
  cat <<'EOF'
Usage: ./scripts/up-landing-snapshot-compose.sh [options]

Options:
  --fetch-latest        Fetch latest landing backup before restore
  --file <path>         Restore a specific dump file
  --fresh               Recreate compose stack and volume before restore
  --port <port>         Local postgres port (default: 55432)
  -h, --help            Show this help message

Examples:
  ./scripts/up-landing-snapshot-compose.sh --fetch-latest
  ./scripts/up-landing-snapshot-compose.sh --file backups/prod-db/landing/landing-20260331T052611Z.dump
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fetch-latest)
      FETCH_LATEST=1
      shift
      ;;
    --file)
      BACKUP_FILE="${2:-}"
      shift 2
      ;;
    --fresh)
      FRESH=1
      shift
      ;;
    --port)
      SNAPSHOT_PGPORT="${2:-}"
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

landing_snapshot_defaults
require_docker_cli
ensure_snapshot_env_file
load_snapshot_env_file

if [[ "${FETCH_LATEST}" -eq 1 ]]; then
  APP="${APP}" "${ROOT_DIR}/scripts/fetch-prod-db-backup.sh"
fi

if [[ -z "${BACKUP_FILE}" ]]; then
  BACKUP_FILE="$(ls -1t "${LOCAL_BACKUP_ROOT}/${APP}"-*.dump 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "${BACKUP_FILE}" || ! -f "${BACKUP_FILE}" ]]; then
  echo "Backup file not found. Use --fetch-latest or --file <path>." >&2
  exit 1
fi

export SNAPSHOT_PGDATABASE SNAPSHOT_PGUSER SNAPSHOT_PGPASSWORD SNAPSHOT_PGPORT

if [[ "${FRESH}" -eq 1 ]]; then
  landing_snapshot_compose down -v --remove-orphans
fi

landing_snapshot_compose up -d db

until landing_snapshot_compose exec -T db \
  pg_isready -U "${SNAPSHOT_PGUSER}" -d "${SNAPSHOT_PGDATABASE}" >/dev/null 2>&1; do
  sleep 1
done

landing_snapshot_compose exec -T db \
  pg_restore \
  -U "${SNAPSHOT_PGUSER}" \
  -d "${SNAPSHOT_PGDATABASE}" \
  --clean \
  --if-exists \
  --no-owner \
  --no-acl \
  "/backups/$(basename "${BACKUP_FILE}")"

landing_snapshot_compose exec -T db \
  psql -U "${SNAPSHOT_PGUSER}" -d "${SNAPSHOT_PGDATABASE}" -At \
  -c "select current_database(), current_user;"

echo "Landing snapshot DB is ready."
echo "  backup : ${BACKUP_FILE}"
echo "  port   : ${SNAPSHOT_PGPORT}"
echo "Next:"
echo "  ./scripts/run-landing-snapshot-local.sh"
