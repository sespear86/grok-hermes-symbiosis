#!/usr/bin/env bash
#
# start-handoff-dashboard.sh (AUTON 3694a72b)
# Fire-and-forget localhost handoff kanban dashboard (lock + nohup + optional browser).
#
# Usage:
#   ./start-handoff-dashboard.sh --device "Washington Linux" [--open] [--port 8766] ...

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${SYMBIOSIS_HANDOFF_DASHBOARD_PORT:-8766}"
LOCK_FILE="${SYMBIOSIS_HANDOFF_DASHBOARD_LOCK:-/tmp/symbiosis-handoff-dashboard.lock}"
LOG_FILE="/tmp/symbiosis-handoff-dashboard.log"
URL="http://127.0.0.1:${PORT}"
SHIM="${SCRIPTS_DIR}/symbiosis-handoff-dashboard"

if [[ ! -x "$SHIM" ]]; then
  echo "[symbiosis-handoff-dashboard] shim not found or not executable: $SHIM" >&2
  exit 1
fi

# Detect --port in args for URL (last wins)
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
  if [[ "${args[i]}" == "--port" && $((i + 1)) -lt ${#args[@]} ]]; then
    PORT="${args[$((i + 1))]}"
    URL="http://127.0.0.1:${PORT}"
  fi
done

if [[ -f "$LOCK_FILE" ]]; then
  PID="$(cat "$LOCK_FILE" 2>/dev/null || true)"
  if [[ -n "${PID}" ]] && kill -0 "${PID}" 2>/dev/null; then
    echo "[symbiosis-handoff-dashboard] Already running (PID ${PID}) — ${URL}"
    xdg-open "${URL}" 2>/dev/null || open "${URL}" 2>/dev/null || true
    exit 0
  fi
  rm -f "$LOCK_FILE"
fi

cd "${SCRIPTS_DIR}" || exit 1

nohup python3 "${SHIM}" "$@" >>"${LOG_FILE}" 2>&1 &
SERVER_PID=$!
echo "${SERVER_PID}" >"${LOCK_FILE}"

sleep 1.8

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "${URL}" >/dev/null 2>&1 || true
elif command -v open >/dev/null 2>&1; then
  open "${URL}" || true
else
  echo "[symbiosis-handoff-dashboard] Please open: ${URL}"
fi

echo "[symbiosis-handoff-dashboard] Launched at ${URL} (server PID ${SERVER_PID})"
echo "[symbiosis-handoff-dashboard] Logs: ${LOG_FILE}"
exit 0

# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch3) -->