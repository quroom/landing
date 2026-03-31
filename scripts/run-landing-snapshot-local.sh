#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT_DIR}/scripts/lib/landing_snapshot_compose.sh"
RUNSERVER_PORT="${RUNSERVER_PORT:-8011}"

usage() {
  cat <<'EOF'
Usage: ./scripts/run-landing-snapshot-local.sh [options]

Options:
  --db-port <port>       Local snapshot Postgres port (default: 55432)
  --port <port>          Exposed app port (default: 8011)
  -h, --help             Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --db-port)
      SNAPSHOT_PGPORT="${2:-}"
      shift 2
      ;;
    --port)
      RUNSERVER_PORT="${2:-}"
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
load_snapshot_env_file

export SNAPSHOT_PGDATABASE SNAPSHOT_PGUSER SNAPSHOT_PGPASSWORD SNAPSHOT_PGPORT
export SNAPSHOT_APP_PORT="${RUNSERVER_PORT}"

landing_snapshot_compose up -d app

until landing_snapshot_compose exec -T app \
  python manage.py showmigrations landing >/dev/null 2>&1; do
  sleep 1
done

echo "Landing snapshot app is ready."
echo "  app url : http://127.0.0.1:${RUNSERVER_PORT}"
echo "  db port : ${SNAPSHOT_PGPORT}"
echo "Useful commands:"
echo "  docker compose --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${COMPOSE_FILE} logs -f app"
echo "  ./scripts/down-landing-snapshot-compose.sh"
