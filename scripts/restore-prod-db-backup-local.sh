#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APP="${APP:-landing}"
LOCAL_BACKUP_ROOT="${LOCAL_BACKUP_ROOT:-${ROOT_DIR}/backups/prod-db/${APP}}"
LOCAL_DB_NAME="${LOCAL_DB_NAME:-landing_prod_snapshot}"
BACKUP_FILE=""
SKIP_DROP_CREATE=0

usage() {
  cat <<'EOF'
Usage: ./scripts/restore-prod-db-backup-local.sh [options]

Options:
  --file <path>         Backup dump file path (default: latest in backups/prod-db/<app>)
  --db-name <name>      Local PostgreSQL database name (default: landing_prod_snapshot)
  --local-root <path>   Local backup directory
  --skip-drop-create    Restore into existing database without drop/create
  -h, --help            Show this help message

Notes:
  - Requires local PostgreSQL client tools (`pg_restore`, `createdb`, `dropdb`).
  - Uses current PGHOST/PGPORT/PGUSER/PGPASSWORD environment if set.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file)
      BACKUP_FILE="${2:-}"
      shift 2
      ;;
    --db-name)
      LOCAL_DB_NAME="${2:-}"
      shift 2
      ;;
    --local-root)
      LOCAL_BACKUP_ROOT="${2:-}"
      shift 2
      ;;
    --skip-drop-create)
      SKIP_DROP_CREATE=1
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

for cmd in pg_restore createdb dropdb; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
done

if [[ -z "${BACKUP_FILE}" ]]; then
  BACKUP_FILE="$(ls -1t "${LOCAL_BACKUP_ROOT}/${APP}"-*.dump 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "${BACKUP_FILE}" || ! -f "${BACKUP_FILE}" ]]; then
  echo "Backup file not found. Use --file <path>." >&2
  exit 1
fi

if [[ "${SKIP_DROP_CREATE}" -eq 0 ]]; then
  dropdb --if-exists "${LOCAL_DB_NAME}"
  createdb "${LOCAL_DB_NAME}"
fi

pg_restore \
  --clean \
  --if-exists \
  --no-owner \
  --no-acl \
  --dbname="${LOCAL_DB_NAME}" \
  "${BACKUP_FILE}"

echo "Restore completed:"
echo "  database: ${LOCAL_DB_NAME}"
echo "  source  : ${BACKUP_FILE}"
