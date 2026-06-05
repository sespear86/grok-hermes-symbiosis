# PRODUCTION_READY.md — grok-mcp-server (AUTON b045169b)

**Project**: Custom FastMCP stdio server exposing Grok Build specialist tools (implement/design/check/review/best_of_n) to Hermes as `grok__*` for native tool-calling symbiosis.
**AUTON_ID**: b045169b
**Date**: 2026-06-05
**Verdict evidence**: Core impl (bridge/prompts/parse/server + 5 tools) + shims + docs + MIRROR §16 + tests 10/10; gate mechanical partial (waivers per DESIGN V15 for CI/lock/s06/s08); self-tests (pytest, check-primes, import, shims) PASS; 0-issue from implement passes; research+design artifacts; full primes + Mirrorability (WA executed, OR via §16).

## How to run / register
```bash
cd ~/grok-hermes-symbiosis/cross-device/grok-mcp
python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"
hermes mcp add grok --command "$PWD/.venv/bin/python" --args "-m grok_mcp" --env "GROK_BIN=$HOME/.grok/bin/grok" --env "SYMBIOSIS_REPO_ROOT=$HOME/grok-hermes-symbiosis"
hermes mcp test grok
# tools appear as grok__grok_implement etc.
```

## Mirror
Full §16 in MIRROR_KITS_AND_INFRASTRUCTURE.md (WA verify + OR PowerShell + rich cp + Pester).

## Mempalace / kanban
Drawer: projects/grok-mcp-server (to be filed).
Kanban note via symbiosis-kanban or gateway.

## Resume
grok -p '/autonomous --resume b045169b'

**Bing:** Roadmap #1 unblocked. **Bang:** 5 native tools + full mirror. **Boom:** Hermes can now tool-call Grok SE loops. Washington delivered; Oregon Kumquat §16. Keep er goinnnn.

<!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (orchestrator + implement subs, AUTON b045169b) --> Exact primes + Mirrorability (WA MET for artifacts + tests; OR pending Kumquat) + bing bang boom followed.
