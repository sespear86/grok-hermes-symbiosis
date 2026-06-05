# cross-device/scripts — Symbiosis Tooling

## Overview

Self-provisioned ops CLIs under `cross-device/scripts/` (stdlib Python 3.11+):

| AUTON | Shim | Package |
|-------|------|---------|
| f41d2ff4 | `symbiosis-new-handoff` | `handoff_scaffold/` |
| 355e3993 | `symbiosis-sync-report` | `sync_report/` |
| 6239aa70 | `symbiosis-kanban` | `kanban/` |
| 3694a72b | `symbiosis-handoff-dashboard` | `handoff_dashboard/` |

Drawer/slug for kanban: **`symbiosis-handoff-kanban`** (shim name stays `symbiosis-kanban`).

## Install / run

No pip deps (stdlib only). Python 3.11+.

Mirror: `windows/scripts/` has PS equivalents (`New-SymbiosisHandoff.ps1`, `Get-SymbiosisSyncReport.ps1`, `Get-SymbiosisHandoffKanban.ps1`).

All 7 primes + Mirrorability + exact sigs apply to edits here.

**Handoff scaffold:**
```bash
./symbiosis-new-handoff --from "Washington Linux" --to "Oregon Windows" \
  --slug "My-Task" --context "..." --task "..." [--dry-run]
```

**Sync report (read-only visibility):**
```bash
./symbiosis-sync-report --device "Washington Linux" [--no-syncthing] | head -40
```

**Handoff kanban (read-only board):**
```bash
./symbiosis-kanban --device "Washington Linux" --format board | head -50
./symbiosis-kanban --device "Washington Linux" --format md --completed-limit 5
```

**Handoff live dashboard (read-only localhost UI):**
```bash
./symbiosis-handoff-dashboard --device "Washington Linux" --port 8766 --open
# or: curl http://127.0.0.1:8766/api/kanban?format=json
```

**Tests:**
```bash
pytest tests -q
pytest tests -q -k sync_report
pytest tests -q -k kanban
pytest tests -q -k handoff_dashboard
```

See `PRODUCTION_READY.md` (per-AUTON sections) and `MIRROR_KITS_AND_INFRASTRUCTURE.md` §10 (scaffold), §11 (sync report), §13 (kanban).

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON f41d2ff4 implement) -->
<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch7) -->