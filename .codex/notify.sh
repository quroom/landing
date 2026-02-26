#!/usr/bin/env bash
set -euo pipefail

payload=""
if [ ! -t 0 ]; then
  payload="$(cat || true)"
fi

# Best-effort parse of JSON payload; fall back to defaults if keys are absent.
title="Codex"
body="작업이 완료되었습니다."

if [ -n "$payload" ]; then
  parsed_title="$(printf '%s' "$payload" | sed -n 's/.*"title"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
  parsed_body="$(printf '%s' "$payload" | sed -n 's/.*"message"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
  if [ -n "$parsed_title" ]; then
    title="$parsed_title"
  fi
  if [ -n "$parsed_body" ]; then
    body="$parsed_body"
  fi
fi

# Record every invocation so we can verify real end-of-response hooks.
{
  printf '%s | cwd=%s | title=%s\n' "$(date -Iseconds)" "$(pwd)" "$title"
} >> /tmp/codex-notify.log 2>/dev/null || true

if command -v notify-send >/dev/null 2>&1; then
  notify-send -u normal "$title" "$body" || true
fi

if command -v canberra-gtk-play >/dev/null 2>&1; then
  canberra-gtk-play -i complete -d "Codex" || true
fi

# Terminal bell fallback
printf '\a' || true
