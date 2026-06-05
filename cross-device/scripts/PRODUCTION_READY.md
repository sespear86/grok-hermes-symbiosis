# PRODUCTION_READY — symbiosis-handoff-scaffold

**AUTON_ID:** `f41d2ff4`  
**Subtree:** `cross-device/scripts/`  
**Profile:** `cli` (stdlib Python 3.11+, no network in unit tests)

## Status

| Gate | Evidence |
|------|----------|
| V1 pytest | `pytest tests -q` → 14 passed (Washington 2026-06-04) |
| V2 FORMAT drift | `test_render.test_format_drift_against_live_repo` |
| V3 Path confinement | `test_validate.test_path_confinement_rejects_escape` |
| V4 dry-run | CLI `--dry-run` writes nothing |
| V5 smoke | `./symbiosis-new-handoff ... --dry-run` OK |
| V6 legacy validate | Pre-scaffold handoffs may fail new strict section list (expected); new packages pass |
| V7 auton-gate | Run: `auton-gate check ~/grok-hermes-symbiosis/cross-device/scripts --auton-id f41d2ff4 --profile cli` |
| V8 PS/WA parity | `New-SymbiosisHandoff.ps1` maps flags → same Python CLI |
| V9 CI | N/A — pure stdlib CLI subtree; evidence = pytest + Pester + local auton-gate (s06/s08 lockfile waivers per DESIGN) |

## Mirror declaration

**Washington + Oregon parity:** Same flags and behavior via PS wrapper + shared Python shim. **Mirrorability: MET** (see `MIRROR_KITS_AND_INFRASTRUCTURE.md` §10).

## Rich deploy

```bash
cp -a ~/grok-hermes-symbiosis/cross-device/scripts ~/Synced/grok-mempalace-integration/symbiosis-relay/
```

## Mempalace

Drawer: `projects/symbiosis-handoff-scaffold` (wing `projects`, room `symbiosis-handoff-scaffold`).

---

**Bing:** Manual handoff tax was brutal post-19557e65.  
**Bang:** This subtree makes FORMAT + LOG + Mempalace mechanical.  
**Boom:** Next handoff opens with one command; dogfood closes the loop.

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON f41d2ff4 implement) -->

---

# PRODUCTION_READY — symbiosis-sync-report-emitter

**AUTON_ID:** `355e3993`  
**Subtree:** `cross-device/scripts/` (package `sync_report/`)  
**Profile:** `cli` (stdlib Python 3.11+, mocked subprocess in unit tests)

## Status

| Gate | Evidence |
|------|----------|
| V1 pytest | `pytest tests -q -k sync_report` → 24 passed (Washington 2026-06-04, post review fixes) |
| V2 auton-gate | `auton-gate check ~/grok-hermes-symbiosis/cross-device/scripts --auton-id 355e3993 --profile cli --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` |
| V3 MIRROR §11 | WA/OR verify blocks in `MIRROR_KITS_AND_INFRASTRUCTURE.md` §11 |
| V4 smoke | `./symbiosis-sync-report --device "Washington Linux" --no-syncthing \| head -40` — typical &lt;2s WA |
| V5 check-primes | `~/grok-hermes-symbiosis/Mempalace/scripts/check-primes.sh` exit 0 at verify |
| V6 Mempalace drawer | `projects/symbiosis-sync-report-emitter` (wing `projects`) — batch 8 |
| V7 OPEN_ITEMS / SKILL | #1 Done; Forward Vision sync line struck (docs matrix 2026-06-04) |
| V8 PS/WA parity | `Get-SymbiosisSyncReport.ps1` + Pester (batch 4); normalized sample compare |
| V9 JSON schema | `tests/test_sync_report.py::test_render_json_schema_keys` + golden `fixtures/expected_report.md` |
| V10 `--no-syncthing` | Always succeeds; `syncthing.available=false` |
| V11 no `shell=True` | `test_no_shell_true_in_sync_report_sources` |
| V12 Verifier | `VERIFIER_GATE_REPORT.md` **PASS** + Mirror **MET** (batch 7) |
| V14 CI GH Actions | **N/A** — stdlib CLI; evidence = pytest + Pester + auton-gate (s06/s08 waivers per f41d2ff4) |
| V15 Implement reviewer | 0 critical/high after fix round (see `/tmp/grok-auton-355e3993/REVIEW_impl_core.md`) |
| V16 ruff | `ruff check sync_report` clean at gate |

## Dual-package pytest

```bash
cd ~/grok-hermes-symbiosis/cross-device/scripts
pytest tests -q                    # handoff_scaffold + sync_report
pytest tests -q -k sync_report     # emitter only
```

## Syncthing (WA smoke — fill after `syncthing cli help`)

v1 runtime uses **`SYMBIOSIS_SYNCTHING_FOLDERS`** only (comma-separated, max 5). Example placeholder until smoke documents real IDs:

```bash
export SYMBIOSIS_SYNCTHING_FOLDERS="symbiosis-repo,grok-mempalace-integration,mempalace"
# Per-folder: syncthing cli show folder <id>  (3s timeout in collector)
```

Oregon: set the same env or pass `--no-syncthing` when the CLI is absent.

## Mirror declaration

**Washington + Oregon parity:** Same flags via PS wrapper + shared Python shim. **Mirrorability: MET** when batch 4 PS + Pester land (see `MIRROR_KITS_AND_INFRASTRUCTURE.md` §11).

## Rich deploy

```bash
cp -a ~/grok-hermes-symbiosis/cross-device/scripts ~/Synced/grok-mempalace-integration/symbiosis-relay/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisSyncReport.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisSyncReport.Tests.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
```

## Mempalace

Drawer: `projects/symbiosis-sync-report-emitter` (batch 8).

---

**Bing:** Spelunking git + Syncthing + LOG separately was the visibility tax.  
**Bang:** One read-only report for Kumquat, handoffs, and paste.  
**Boom:** Dogfood §2.3a on the next Paired handoff wave.

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 355e3993 sync-report-emitter docs matrix) -->

---

# PRODUCTION_READY — symbiosis-handoff-kanban

**AUTON_ID:** `6239aa70`  
**Subtree:** `cross-device/scripts/` (package `kanban/`)  
**Profile:** `cli` (stdlib Python 3.11+, mocked paths in unit tests)

## Status

| Gate | Evidence |
|------|----------|
| V1 pytest all | `pytest tests -q` → scaffold + sync_report + kanban green (Washington 2026-06-04) |
| V1b pytest kanban | `pytest tests -q -k kanban` → kanban unit + golden tests |
| V2 auton-gate | `auton-gate check ~/grok-hermes-symbiosis/cross-device/scripts --auton-id 6239aa70 --profile cli --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md` |
| V3 MIRROR §13 | WA/OR verify blocks in `MIRROR_KITS_AND_INFRASTRUCTURE.md` §13 |
| V4 smoke | `./symbiosis-kanban --device "Washington Linux" --format board \| head -50` |
| V5 check-primes | `~/bin/check-primes.sh` exit 0 at Batch 8 verify (also Batch 7) |
| V6 Mempalace drawer | `projects/symbiosis-handoff-kanban` — **3 drawers filed (Batch 8, 2026-06-04)** |
| V7 OPEN_ITEMS / SKILL | #4 Done; Forward Vision kanban struck (Batch 7) |
| V8 PS/WA parity | `Get-SymbiosisHandoffKanban.ps1` + Pester (batch 4) |
| V9 JSON schema | `tests/test_kanban.py::test_kanban_json_schema_keys` + fixtures `expected_kanban.md` / `expected_kanban_board.txt` |
| V10 no shell | `test_no_shell_true_in_kanban_sources` |
| V11 Verifier | `VERIFIER_GATE_REPORT.md` **PASS** (Phase 6) |
| V12 security-auditor | 0 critical/high on `kanban/` + shims (Phase 6) |
| V13 Mirrorability | **MET** — MIRROR §13 + PRODUCTION_READY + OR verify block |
| V14 CI GH Actions | **N/A** — stdlib CLI; evidence = pytest + Pester + auton-gate (s06/s08 waivers per siblings) |
| V15 Hermes kanban | Phase 9: `hermes_delegation.kanban` in `6239aa70.json` |
| V16 ruff | `ruff check kanban` clean |

## Dual/triple-package pytest

```bash
cd ~/grok-hermes-symbiosis/cross-device/scripts
pytest tests -q
pytest tests -q -k kanban
```

## Mirror declaration

**Washington + Oregon parity:** Same flags via PS wrapper + shared Python shim. **Mirrorability: MET** (see `MIRROR_KITS_AND_INFRASTRUCTURE.md` §13).

## Rich deploy

```bash
cp -a ~/grok-hermes-symbiosis/cross-device/scripts ~/Synced/grok-mempalace-integration/symbiosis-relay/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisHandoffKanban.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisHandoffKanban.Tests.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
```

## Mempalace

Drawer: `projects/symbiosis-handoff-kanban` (Batch 8).

---

**Bing:** LOG tables and handoff folders were a two-screen foreplay tease.  
**Bang:** One CLI boards the whole `handoffs/` nerve center for Paired ops.  
**Boom:** Dogfood §2.3b on the next Kumquat when workload clarity matters.

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch8) -->

---

# PRODUCTION_READY — symbiosis-shared-projects

**AUTON_ID:** `61cdeb81`  
**Subtree:** `cross-device/scripts/` (package `joint_projects/`)  
**Profile:** `cli` (stdlib Python 3.11+, no network in unit tests)

## Status (gates — PR6 evidence 2026-06-05)

| Gate | Evidence |
|------|----------|
| V1 pytest joint_projects | **27 passed** (`pytest tests -q -k joint_projects`) |
| V2 pytest all | **82 passed** (`pytest tests -q`) |
| V3 auton-gate | **MECHANICAL_PASS** exit 0 — `auton-gate check ~/grok-hermes-symbiosis/cross-device/scripts --auton-id 61cdeb81 --profile cli`; `GATE_REPORT.md` + `gate_report.json` |
| V4 MIRROR §15 | WA/OR verify blocks in `MIRROR_KITS_AND_INFRASTRUCTURE.md` §15 |
| V5 smoke | `~/bin/symbiosis-projects list --device "Washington Linux"` (dogfood PR6); `init --dry-run`; tmp-root init+verify in pytest |
| V6 check-primes | `~/bin/check-primes.sh` → exit 0 (2026-06-05) |
| V7 Mempalace drawer | `projects/symbiosis-shared-projects` (s12.02 auton-gate PASS) |
| V8 OPEN_ITEMS / SKILL | #5 Done; Forward Vision struck when shipped |
| V9 PS/OR parity | **Pending on branch tip** — PS scripts on PR2 stack; WA Python + shim **PASS**; OR Pester after rich cp |
| V10 path confinement | `test_assert_under_projects_root_rejects_escape` (+ init escape in pytest) |
| V11 no shell | `test_no_shell_true_in_joint_projects_sources` |
| V12 list coord policy | `test_list_succeeds_without_repo_coord_warnings`; `test_list_strict_coord_exit2_invalid_repo` |
| V13 Verifier | `VERIFIER_GATE_REPORT.md` **VERDICT: PASS** (61cdeb81 section, PR6) |
| V14 security-auditor | Manual: 0 crit/high — no secrets, no shell in package, path guards, read-only list |
| V15 Mirrorability | **MET** (WA); OR §15 smoke recipe when PS merged |
| V16 ruff | `ruff check .` clean (PR6 gate fix: unused import in tests) |
| V17 CI / lockfiles | **N/A** — auton-gate s06.01 + s08.01 FAIL non-strict, waived (sibling pattern) |

## Mirror declaration

**Washington + Oregon parity:** Same list/init/verify contract via PS wrappers + shared Python shim. **Mirrorability: MET** when OR runs §15 verify (Python 3.11+). Empty `C:\Synced\Projects` → honest empty list.

## Rich deploy

```bash
cp -a ~/grok-hermes-symbiosis/cross-device/scripts ~/Synced/grok-mempalace-integration/symbiosis-relay/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisProjects.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Initialize-SymbiosisProject.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
cp -a ~/grok-hermes-symbiosis/windows/scripts/Get-SymbiosisProjects.Tests.ps1 ~/Synced/grok-mempalace-integration/symbiosis-relay/windows/scripts/
ln -sf ~/grok-hermes-symbiosis/cross-device/scripts/symbiosis-projects ~/bin/symbiosis-projects
```

## Mempalace

Drawer: `projects/symbiosis-shared-projects` (PR5).

## Waivers

s06/s08 lockfile + monorepo CI **N/A** (3694a72b / f41d2ff4 / 6239aa70 pattern).

---

**Bing:** Handoffs had a gym; joint product work had no locker room under `Synced/Projects`.  
**Bang:** `symbiosis-projects` lists, inits, and verifies joint trees without touching `HANDOFF_LOG.md`.  
**Boom:** Dogfood PLAYBOOK §2.3d on the next Paired joint build; Oregon mirrors MIRROR §15.

<!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR6 gates) -->
# PRODUCTION_READY — bidirectional-memory-sync (AUTON 7eb7d1b7)

**AUTON_ID:** `7eb7d1b7`  
**Subtree:** `cross-device/scripts/memory_sync/` ( + shim `symbiosis-memory-sync`, Mempalace helper in ../Mempalace/scripts/)  
**Profile:** `cli`

## Status (bootstrap + early execute)
- Skeleton + core modules (paths, bundle, redact, merge, collectors/grok+hermes+coordination, palace_io + venv helper for real mempalace, render, cli, shim) land.
- pyproject updated (pythonpath + desc).
- 3 unit tests + full subtree 124/124 green.
- Smoke: `python -m memory_sync.cli bundle --agent grok --device "Washington Linux" --dry-run` + shim exec.
- Mempalace drawer `projects/bidirectional-memory-sync` filed via MCP.
- DESIGN: 4-round writer/reviewer loop → **0 open issues** (VERDICT ready for implement per DESIGN_REVIEW.md).
- RESEARCH + DESIGN artifacts in auton-projects/7eb7d1b7/ + workspace auton-artifacts/.

## Next (B1-B10 per DESIGN)
B1 paths/bundle/redact + hygiene; B2 collectors; B3 palace+cli+shim; B4 tests; ... B10 gate + PRODUCTION + MIRROR §17 + rich + PS + coord hygiene + OPEN_ITEMS struck.

## Mirror (draft §17)
WA: pytest -q -k memory; python -m memory_sync.cli ... ; auton-gate ... --auton-id 7eb7d1b7 --profile cli
OR: Get-SymbiosisMemorySync.ps1 + Pester; same commands via shim.
Rich: cp -a .../memory_sync ... ; cp helper; ln -sf shim ~/bin/

## Mempalace
Drawer: `projects/bidirectional-memory-sync` (plus diary on gate).

**Bing:** One-way was the memory cockring; now the bidirectional bridge.  
**Bang:** Grok todos + Hermes excerpts + shared palace without paste.  
**Boom:** README 191 Done + full mirror. Washington thrusting.

<!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 7eb7d1b7 bootstrap + design gate) --> Exact primes + Mirror as last + bing bang boom followed.
