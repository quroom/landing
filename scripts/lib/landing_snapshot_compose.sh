#!/usr/bin/env bash

landing_snapshot_defaults() {
  ROOT_DIR="${ROOT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
  COMPOSE_FILE="${COMPOSE_FILE:-${ROOT_DIR}/compose.landing-snapshot.yml}"
  ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env.landing-snapshot}"
  PROJECT_NAME="${PROJECT_NAME:-landing-snapshot}"
  SNAPSHOT_PGDATABASE="${SNAPSHOT_PGDATABASE:-landing_prod_snapshot}"
  SNAPSHOT_PGUSER="${SNAPSHOT_PGUSER:-landing_local}"
  SNAPSHOT_PGPASSWORD="${SNAPSHOT_PGPASSWORD:-}"
  SNAPSHOT_PGPORT="${SNAPSHOT_PGPORT:-55432}"
  SNAPSHOT_APP_PORT="${SNAPSHOT_APP_PORT:-8011}"
}

require_docker_cli() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Missing required command: docker" >&2
    exit 1
  fi
}

docker_cmd() {
  if docker info >/dev/null 2>&1; then
    docker "$@"
    return
  fi
  if sudo -n docker info >/dev/null 2>&1; then
    sudo -n docker "$@"
    return
  fi
  echo "Docker access is unavailable. Ensure docker is installed and usable, or allow passwordless sudo for docker." >&2
  exit 1
}

create_snapshot_env_file() {
  mkdir -p "$(dirname "${ENV_FILE}")"

  local generated_password=""
  if command -v openssl >/dev/null 2>&1; then
    generated_password="$(openssl rand -hex 16)"
  elif [[ -x "${ROOT_DIR}/.venv/bin/python" ]]; then
    generated_password="$(
      "${ROOT_DIR}/.venv/bin/python" -c 'import secrets; print(secrets.token_hex(16))' 2>/dev/null || true
    )"
  fi

  if [[ -z "${generated_password}" ]]; then
    echo "Unable to generate SNAPSHOT_PGPASSWORD automatically." >&2
    exit 1
  fi

  umask 077
  cat > "${ENV_FILE}" <<EOF
SNAPSHOT_PGDATABASE=${SNAPSHOT_PGDATABASE}
SNAPSHOT_PGUSER=${SNAPSHOT_PGUSER}
SNAPSHOT_PGPASSWORD=${generated_password}
SNAPSHOT_PGPORT=${SNAPSHOT_PGPORT}
SNAPSHOT_APP_PORT=${SNAPSHOT_APP_PORT}
EOF
}

ensure_snapshot_env_file() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    create_snapshot_env_file
  fi
}

load_snapshot_env_file() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing snapshot env file: ${ENV_FILE}" >&2
    echo "Run ./scripts/up-landing-snapshot-compose.sh first." >&2
    exit 1
  fi

  set -a
  # shellcheck disable=SC1090
  . "${ENV_FILE}"
  set +a
}

landing_snapshot_compose() {
  docker_cmd compose --env-file "${ENV_FILE}" -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" "$@"
}

landing_snapshot_compose_with_placeholder_env() {
  local temp_env_file
  temp_env_file="$(mktemp)"
  trap 'rm -f "${temp_env_file}"' RETURN
  cat > "${temp_env_file}" <<'EOF'
SNAPSHOT_PGPASSWORD=placeholder
EOF
  docker_cmd compose --env-file "${temp_env_file}" -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" "$@"
}
