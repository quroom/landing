#!/usr/bin/env bash
set -euo pipefail

APP="${APP:-landing}"
BACKUP_ROOT="${BACKUP_ROOT:-${HOME}/backups/${APP}/postgres}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP="${TIMESTAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"

usage() {
  cat <<'EOF'
Usage: ./scripts/remote-prod-db-backup.sh

Environment variables:
  APP             Dokku app name (default: landing)
  BACKUP_ROOT     Directory to store dump/json/sha256 files
  RETENTION_DAYS  Delete backup artifacts older than this many days (default: 14)
  TIMESTAMP       Override UTC timestamp suffix (default: now)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-}"

require_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
}

for cmd in sudo docker python3 sha256sum flock stat; do
  require_cmd "${cmd}"
done

mkdir -p "${BACKUP_ROOT}"
LOCK_FILE="${BACKUP_ROOT}/.backup.lock"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
  echo "Another backup is already running: ${LOCK_FILE}" >&2
  exit 1
fi

dokku_config_get() {
  local key="$1"
  sudo -n dokku config:get "${APP}" "${key}" 2>/dev/null || true
}

export_from_database_url() {
  local database_url="$1"
  if [[ -z "${database_url}" ]]; then
    return 1
  fi

  eval "$(
    python3 - "${database_url}" <<'PY'
import shlex
import sys
from urllib.parse import unquote, urlparse

url = sys.argv[1]
parsed = urlparse(url)
database = parsed.path.lstrip("/")
port = str(parsed.port or 5432)

values = {
    "PGHOST": parsed.hostname or "",
    "PGPORT": port,
    "PGDATABASE": unquote(database),
    "PGUSER": unquote(parsed.username or ""),
    "PGPASSWORD": unquote(parsed.password or ""),
}

for key, value in values.items():
    print(f"export {key}={shlex.quote(value)}")
PY
  )"
}

resolve_connection_env() {
  local database_url

  database_url="$(dokku_config_get DATABASE_URL)"
  if [[ -n "${database_url}" ]]; then
    export_from_database_url "${database_url}"
    return 0
  fi

  export PGHOST="${PGHOST:-$(dokku_config_get PGHOST)}"
  export PGPORT="${PGPORT:-$(dokku_config_get PGPORT)}"
  export PGDATABASE="${PGDATABASE:-$(dokku_config_get PGDATABASE)}"
  export PGUSER="${PGUSER:-$(dokku_config_get PGUSER)}"
  export PGPASSWORD="${PGPASSWORD:-$(dokku_config_get PGPASSWORD)}"

  if [[ -z "${PGHOST}" ]]; then
    export PGHOST="${DB_HOST:-$(dokku_config_get DB_HOST)}"
  fi
  if [[ -z "${PGPORT}" ]]; then
    export PGPORT="${DB_PORT:-$(dokku_config_get DB_PORT)}"
  fi
  if [[ -z "${PGDATABASE}" ]]; then
    export PGDATABASE="${DB_NAME:-$(dokku_config_get DB_NAME)}"
  fi
  if [[ -z "${PGUSER}" ]]; then
    export PGUSER="${DB_USER:-$(dokku_config_get DB_USER)}"
  fi
  if [[ -z "${PGPASSWORD}" ]]; then
    export PGPASSWORD="${DB_PASSWORD:-$(dokku_config_get DB_PASSWORD)}"
  fi
}

resolve_connection_env

for required in PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD; do
  if [[ -z "${!required:-}" ]]; then
    echo "Missing required PostgreSQL connection value: ${required}" >&2
    exit 1
  fi
done

if [[ -z "${POSTGRES_CONTAINER}" ]]; then
  if [[ "${PGHOST}" == dokku-postgres-* ]]; then
    POSTGRES_CONTAINER="dokku.postgres.${PGHOST#dokku-postgres-}"
  else
    echo "Unable to derive postgres container name from PGHOST=${PGHOST}. Set POSTGRES_CONTAINER explicitly." >&2
    exit 1
  fi
fi

if ! sudo -n docker ps --format '{{.Names}}' | grep -Fx "${POSTGRES_CONTAINER}" >/dev/null 2>&1; then
  echo "Postgres container not found or not running: ${POSTGRES_CONTAINER}" >&2
  exit 1
fi

TMP_DUMP="${TMP_DIR}/${APP}-${TIMESTAMP}.dump"
TMP_SHA="${TMP_DIR}/${APP}-${TIMESTAMP}.sha256"
TMP_META="${TMP_DIR}/${APP}-${TIMESTAMP}.json"
CONTAINER_DUMP="/tmp/${APP}-${TIMESTAMP}.dump"

sudo -n docker exec \
  -e PGPASSWORD="${PGPASSWORD}" \
  "${POSTGRES_CONTAINER}" \
  pg_dump \
    --format=custom \
    --no-owner \
    --no-acl \
    --host=127.0.0.1 \
    --port="${PGPORT}" \
    --username="${PGUSER}" \
    --dbname="${PGDATABASE}" \
    --file="${CONTAINER_DUMP}"

sudo -n docker cp "${POSTGRES_CONTAINER}:${CONTAINER_DUMP}" "${TMP_DUMP}"
sudo -n docker exec "${POSTGRES_CONTAINER}" rm -f "${CONTAINER_DUMP}"

sha256sum "${TMP_DUMP}" > "${TMP_SHA}"

DUMP_SIZE_BYTES="$(stat -c '%s' "${TMP_DUMP}")"
SHA256_VALUE="$(awk '{print $1}' "${TMP_SHA}")"
CREATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
export APP BACKUP_ROOT RETENTION_DAYS PGHOST PGPORT PGDATABASE PGUSER DUMP_SIZE_BYTES SHA256_VALUE CREATED_AT

python3 - <<'PY' > "${TMP_META}"
import json
import os

payload = {
    "app": os.environ["APP"],
    "created_at": os.environ["CREATED_AT"],
    "backup_root": os.environ["BACKUP_ROOT"],
    "database": {
        "host": os.environ["PGHOST"],
        "port": os.environ["PGPORT"],
        "name": os.environ["PGDATABASE"],
        "user": os.environ["PGUSER"],
    },
    "artifact": {
        "format": "pg_dump_custom",
        "sha256": os.environ["SHA256_VALUE"],
        "size_bytes": int(os.environ["DUMP_SIZE_BYTES"]),
        "retention_days": int(os.environ["RETENTION_DAYS"]),
    },
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
PY

FINAL_DUMP="${BACKUP_ROOT}/${APP}-${TIMESTAMP}.dump"
FINAL_SHA="${BACKUP_ROOT}/${APP}-${TIMESTAMP}.sha256"
FINAL_META="${BACKUP_ROOT}/${APP}-${TIMESTAMP}.json"

mv "${TMP_DUMP}" "${FINAL_DUMP}"
mv "${TMP_SHA}" "${FINAL_SHA}"
mv "${TMP_META}" "${FINAL_META}"

if [[ "${RETENTION_DAYS}" =~ ^[0-9]+$ ]] && [[ "${RETENTION_DAYS}" -gt 0 ]]; then
  find "${BACKUP_ROOT}" -maxdepth 1 -type f \
    \( -name "${APP}-*.dump" -o -name "${APP}-*.sha256" -o -name "${APP}-*.json" \) \
    -mtime +"${RETENTION_DAYS}" -delete
fi

echo "Backup created:"
echo "  dump : ${FINAL_DUMP}"
echo "  sha  : ${FINAL_SHA}"
echo "  meta : ${FINAL_META}"
