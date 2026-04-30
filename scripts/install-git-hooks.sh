#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v git >/dev/null 2>&1; then
  echo "Missing required command: git" >&2
  exit 1
fi

git -C "${ROOT_DIR}" config core.hooksPath .githooks

echo "Git hooks installed."
echo "  pre-push: ./scripts/verify.sh"
