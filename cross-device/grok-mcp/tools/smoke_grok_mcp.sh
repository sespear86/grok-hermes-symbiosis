#!/usr/bin/env bash
# Smoke: import server + optional live grok -z (GROK_MCP_SMOKE_LIVE=1)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -e ".[dev]"
fi
"$PY" -c "from grok_mcp.server import mcp, run_stdio; assert mcp.name == 'grok'"
"$PY" -m pytest tests -q --tb=no
echo "smoke: package OK"
if [[ "${GROK_MCP_SMOKE_LIVE:-}" == "1" ]]; then
  echo "smoke: live grok -z skipped unless GROK_BIN set and tiny task wired in implement phase"
fi