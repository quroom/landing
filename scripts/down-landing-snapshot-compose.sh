#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT_DIR}/scripts/lib/landing_snapshot_compose.sh"
REMOVE_VOLUME=0

usage() {
  cat <<'EOF'
Usage: ./scripts/down-landing-snapshot-compose.sh [options]

Options:
  --remove-volume    Remove the snapshot volume as well
  -h, --help         Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remove-volume)
      REMOVE_VOLUME=1
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

landing_snapshot_defaults
require_docker_cli

if [[ "${REMOVE_VOLUME}" -eq 1 ]]; then
  if [[ -f "${ENV_FILE}" ]]; then
    landing_snapshot_compose down -v --remove-orphans
  else
    landing_snapshot_compose_with_placeholder_env down -v --remove-orphans
  fi
else
  if [[ -f "${ENV_FILE}" ]]; then
    landing_snapshot_compose down --remove-orphans
  else
    landing_snapshot_compose_with_placeholder_env down --remove-orphans
  fi
fi
