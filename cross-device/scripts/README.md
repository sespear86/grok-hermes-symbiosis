# cross-device/scripts — Symbiosis Tooling

## Overview

Self-provisioned ops CLIs under `cross-device/scripts/` (stdlib Python 3.11+):

| AUTON | Shim | Package |
|-------|------|---------|
| f41d2ff4 | `symbiosis-new-handoff` | `handoff_scaffold/` |
| 355e3993 | `symbiosis-sync-report` | `sync_report/` |
| 6239aa70 | `symbiosis-kanban` | `kanban/` |
| 3694a72b | `symbiosis-handoff-dashboard` | `handoff_dashboard/` |
| 61cdeb81 | `symbiosis-projects` | `joint_projects/` |

**Sibling package (not under this pyproject):** AUTON **b045169b** — [`../grok-mcp/`](../grok-mcp/) (`symbiosis-grok-mcp` shim, FastMCP `grok_mcp`, own venv + pytest). Hermes tools `grok__*`. Mirror §16.

Drawer/slug: kanban **`symbiosis-handoff-kanban`** (shim `symbiosis-kanban`); shared Projects **`symbiosis-shared-projects`** (shim `symbiosis-projects`).

## Install / run

No pip deps (stdlib only). Python 3.11+.

Mirror: `windows/scripts/` has PS equivalents (`New-SymbiosisHandoff.ps1`, `Get-SymbiosisSyncReport.ps1`, `Get-SymbiosisHandoffKanban.ps1`, `Get-SymbiosisHandoffDashboard.ps1`, `Get-SymbiosisProjects.ps1`, `Initialize-SymbiosisProject.ps1`, `Invoke-SymbiosisGrokMcp.ps1`).

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

**Shared joint projects** (`~/Synced/Projects` / `C:\Synced\Projects`; read-only `list`/`verify`, guarded `init`):
```bash
./symbiosis-projects list --device "Washington Linux" | head -30
./symbiosis-projects init --slug "My-Joint-App" --device "Washington Linux" --dry-run
./symbiosis-projects verify --slug "My-Joint-App" --device "Washington Linux"
export SYMBIOSIS_PROJECTS_ROOT=/tmp/projects-test   # pytest / smoke only
```

**Tests:**
```bash
pytest tests -q
pytest tests -q -k sync_report
pytest tests -q -k kanban
pytest tests -q -k joint_projects
```

See `PRODUCTION_READY.md` (per-AUTON sections) and `MIRROR_KITS_AND_INFRASTRUCTURE.md` §10 (scaffold), §11 (sync report), §13 (kanban), §15 (shared projects), §16 (grok-mcp).

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON f41d2ff4 implement) -->
<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch7) -->
<!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81) -->