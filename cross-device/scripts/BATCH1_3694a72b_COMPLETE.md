# BATCH1+2 — AUTON 3694a72b (symbiosis-handoff-live-dashboard)

**Date:** 2026-06-04  
**Device:** Washington Linux  
**Worktree:** `/tmp/wt-3694a72b-dashboard` (branch `auton-3694a72b-dashboard`)

## Delivered

- `handoff_dashboard/` package: `__init__.py`, `paths.py`, `collectors.py`, `server.py`, `cli.py`, `static/{index.html,style.css,app.js}`
- Shim: `symbiosis-handoff-dashboard`
- Tests: `tests/test_handoff_dashboard.py` (25 cases), `tests/fixtures/expected_dashboard_api.json` (generated golden)
- Packaging: `pyproject.toml` (`handoff_dashboard` on pythonpath, v0.2.1), `README.md` row + examples

## Self-verification (PASS)

```bash
cd /tmp/wt-3694a72b-dashboard/cross-device/scripts
pytest tests -q -k handoff_dashboard          # 25 passed
pytest tests -q                               # 93 passed (full tree)
ruff check handoff_dashboard                  # All checks passed
./symbiosis-handoff-dashboard --device "Washington Linux" \
  --repo-root /tmp/wt-3694a72b-dashboard --check-only --no-presence  # exit 0
# Server dogfood (port 9876):
curl -sS http://127.0.0.1:9876/healthz
curl -sS 'http://127.0.0.1:9876/api/kanban?format=json' | python3 -c \
  'import sys,json; d=json.load(sys.stdin); assert d["schema_version"]==1'
```

## Notes

- Reuses `kanban.collect_board` / `kanban.render` (no duplicated column logic).
- Default bind `127.0.0.1`; `0.0.0.0` refused without `--allow-lan`.
- Default port **8766**; no `shell=True` in package sources.

**Core package + tests + shim basics done in worktree. Next: reviewer or batch3 launcher polish + PS. Washington has the ball.**

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->