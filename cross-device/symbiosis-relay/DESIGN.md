# DESIGN: Harden & Productionize Washington Hermes Task Activator / Injection / Presence

| Field | Value |
|-------|-------|
| **AUTON_ID** | `19557e65` |
| **Project Slug** | `symbiosis-washington-activator-prod` |
| **Status** | Design (review-ready) |
| **Date** | 2026-06-03 (Washington Linux) |
| **Canonical Research** | [`RESEARCH_SYNTHESIS.md`](./RESEARCH_SYNTHESIS.md) |
| **Prior Gate Reference** | `021dbe8d` (`auton-gate` mechanical + verifier PASS) |
| **Scope** | `cross-device/symbiosis-relay/` core Python + tests + docs + packaging notes; runtime sync to rich `~/Synced/.../symbiosis-relay/` |

**Ball Holder:** Washington has the ball. (Next: implementer worktrees per PR DAG → mechanical `auton-gate` → verifier/security → Kumquat mirror hygiene.)

---

## Executive Summary

The Washington-side **Symbiosis Relay consumer** is the live organ that **receives** Pi-dispatched tasks, **fires** the Grok Build presence beacon (single-active enforcement), **injects** normal relay work and **`bust_a_nut_resume`** into a running TUI (fast path) or Hermes fallback, and **reports** status + failure artifacts back across the shared file bus. It already runs in production as `washington-activator.service` against the **rich** tree; this design hardens it from “plumbing that mostly works” to **production-ready** with structured logging, health interlocks, explicit error taxonomy, configurable injection, richer `status.json`, expanded tests, mirror-kit hygiene, and a **Phase 6** gate that dogfoods `auton-gate` with **`--profile service`** until the full verifier says **`VERDICT: PASS`** — not a mechanical hand-wave alone.

**Goals (non-negotiable):**

1. **Bust a nut:** implement → review → fix loops until **0 open issues** on final rounds (worktree isolation for code).
2. **0 issues final:** general reviewer + specialists; no “we’ll fix in prod.”
3. **Dogfood `auton-gate` Phase 6 exactly** (from `021dbe8d` / `~/auton-gate/docs/INTEGRATION_AUTONOMOUS.md`) with `--profile service` on this subtree.
4. **Preserve symbiosis primes:** Kumquat ritual, Mirrorability, Ball Holder exact statements, `<!-- Edited: YYYY-MM-DD HH:MM | Device: ... | By: ... -->` on every touched doc, self-provisioning gaps, no secrets in repo.
5. **Do not boil the ocean:** no full Oregon PowerShell port, no Pi bootstrap rewrite, no new paid infra.

---

## Current State / Baseline

### What works today (evidence)

| Capability | Evidence |
|------------|----------|
| File-drop protocol end-to-end | `relay_roundtrip_test.py` simulates selector → inbox → activator behavior; real Slack-style path proven per `linux-instructions.md` + synthesis |
| Selector + single-active | `device_selector.py:129-139` HARD VIOLATION when both beacons active; WA priority `142-151` |
| Relay listener dispatch | `relay_listener.py:64-74` `dispatch_task_to_device`; `116+` main loop + `write_relay_beacon` every ~90s |
| Washington activator loop | `washington_activator.py:162-191` poll 5s, claim, beacon, `prompt_grok_build`, archive, beacon off |
| Bust resume fast path | `washington_activator.py:80-97` shells `inject-bust-a-nut-into-running-tui.sh` under `SHARED_BASE/symbiosis-relay/tools/` |
| Hermes fallback + pending | `washington_activator.py:137-159` `hermes -z` + `pending-prompts/<corr>.md` on failure |
| Self-test baseline | `relay_self_test.py` paths + selector + relay beacon — **PASS** (2026-06-03 per synthesis) |
| Runtime service | `~/.config/systemd/user/washington-activator.service`: `ExecStart=python3 .../Synced/.../washington_activator.py`, `SYMBIOSIS_SHARED` set, journal |
| Paired + beacon hot | Synthesis: `grok_build_active`, fresh `last_seen`, HB Paired mode |

### Git vs rich (mirror nervous system)

- **Live runtime:** `/home/Irikash/Synced/grok-mempalace-integration/symbiosis-relay/` (full `tools/`, inject sh ~16k, services point here).
- **Git mirror-kit copy:** `grok-hermes-symbiosis/cross-device/symbiosis-relay/` — entire tree **ignored** by `.gitignore:35` (“canonical exclusively rich”). Design treats git copy as **published nervous source** after `git add -f` exception (see Key Decisions).

### Known rough edges (from synthesis — must close)

1. Poll loop races / no claim lock (`washington_activator.py:166-183`).
2. No retries on beacon/status/subprocess (`62-71`, broad `except`).
3. No health interlock before claim; flat `status.json` (`50-58`).
4. Archives task even on some failures; weak schema validation.
5. Plaintext logging; no `correlation_id` on every line.
6. Hardcoded inject path (`84-85`); `inject_hermes_task.py` ignores `SYMBIOSIS_SHARED` (`41-43`).
7. `relay_roundtrip_test.py` does **not** exec real `washington_activator.py --once`.
8. No `pyproject.toml`; no dedicated activator unit tests.
9. Docs vintage (`ARCHITECTURE.md` design-phase header); no `OPERATIONS.md`.

---

## Architecture

### System context (unchanged protocol, hardened consumer)

```text
[ Slack / Hermes gateway / inject_hermes_task.py ]
        → incoming/hermes/task-*.json
[ Pi: relay_listener.py ]  (~30s loop)
        → write_relay_beacon (relay_beacon.py:29)
        → device_selector.select_device_for_grok_build_task (109)
        → dispatch → incoming/<device>/task-*.json
[ Washington: washington_activator.py ]  (5s poll → optional claim lock)
        → health interlock (NEW)
        → fire_beacon start (62-66)
        → write_status processing (50-58, enriched NEW)
        → prompt_grok_build (74) — bust live inject | hermes | pending artifact
        → archive OR dead-letter (NEW rules)
        → fire_beacon stop
        → status/washington/status.json  ← relay_listener.read_status (76-84)
```

### Proposed module layout (stdlib-first)

```text
symbiosis-relay/
  washington_activator.py      # thin CLI + loop; imports activator_core
  activator_core.py            # NEW: claim, health, prompt paths, retries, status schema
  task_schema.py               # NEW: validate_task(), TaskValidationError (stdlib)
  inject_hermes_task.py        # hardened CLI + SYMBIOSIS_SHARED
  device_selector.py           # minor: export helpers for tests (beacon age at decision)
  relay_beacon.py              # fix duplicate __main__ (44-49); no behavior change required
  relay_listener.py            # optional: read enriched status fields (backward compatible)
  tests/
    test_task_schema.py
    test_activator_core.py
    test_device_selector.py
    test_inject_hermes_task.py
  pytest.ini                   # self-provision if missing
  pyproject.toml               # minimal package + optional console_scripts
  OPERATIONS.md                # NEW
  DESIGN.md                    # this file
  RESEARCH_SYNTHESIS.md
```

### Resilience additions (conceptual)

| Layer | Mechanism |
|-------|-----------|
| Claim | `fcntl`/`portalocker` optional; **default:** atomic `rename` inbox → `processing/<name>.json` before work |
| Dedup | Skip files in `processing/` and `processed/`; track `last_processed_correlation` in status |
| Retries | Transient: beacon subprocess, status write, hermes timeout — 3 attempts exponential backoff |
| Permanent fail | Write `pending-prompts/<corr>.md` + `failed/<corr>.json` (task snapshot); **do not** move to `processed/` unless `success` or explicit `archive_on_fail=false` override in task |
| Health | `activator_core.check_health()` (or `activator_core.health_check()`) before claim: writable dirs, beacon script exists, self beacon age &lt; 300s (read `device-presence/washington-grok-build-presence.json`), optional `relay-presence.json` stale warning |
| Logging | JSON lines to file + human stream; every log record includes `correlation_id` when known |
| Injection | `INJECT_BUST_SCRIPT`, `INJECT_BUST_PYTHON` env; resolve under `SYMBIOSIS_SHARED`; fallback `pts-inject-input.py` if sh missing |

---

## Detailed Changes

### 1. `washington_activator.py` (+ `activator_core.py`)

| Area | Current (`file:line`) | Change |
|------|----------------------|--------|
| Logging | `39-46` basicConfig | `configure_logging(json=env ACTIVATOR_LOG_JSON)`; journal-friendly prefix; rotate or size cap doc in OPERATIONS |
| `write_status` | `50-58` | Add fields: `last_error`, `last_inject_rc`, `last_hermes_rc`, `pending_prompts_count`, `beacon_age_seconds_at_claim`, `health_ok`, `retry_count`, `version` (package `__version__`) |
| `fire_beacon` | `62-71` | Retry 3x; log rc/stderr; on total fail set status `beacon_failed` and **abort claim** (release processing file) |
| Main loop | `166-191` | Call `process_inbox_once()` from core; atomic claim; `except JSONDecodeError` → `failed/` + status; `except OSError` on rename → retry; never swallow with bare `except` |
| `prompt_grok_build` | `74-159` | Move to core; validate task first; bust path: set intent marker touch (doc-only hook via env `ASSERT_BUST_INTENT=1` calling existing rich script if present); live inject configurable; pending artifact on **any** terminal failure with full task JSON appendix. **Hermes handoff**: treat `result.returncode != 0` as failure (write pending + set `last_hermes_rc`, do not return success / do not archive to processed by default per KD-6). |
| CLI | `213-218` | Add `--health`, `--status`, `--dry-run` (parse task, no hermes), keep `--once` |
| `run_once` | `194-210` | Delegate to core; same semantics for tests |

**Security note for implementer:** subprocess uses **fixed** script paths from env defaults under `SYMBIOSIS_SHARED`; never pass `original_message` to shell. Hermes argv list only.

### 2. `inject_hermes_task.py`

| Area | Current | Change |
|------|---------|--------|
| Shared base | `41-43` hardcoded WA path | `Path(os.environ.get("SYMBIOSIS_SHARED", ...))` same pattern as `device_selector.py:30-33` |
| Task shape | `49-62` | Align required keys with `task_schema.validate_task` (min: `type`, `correlation_id`, `original_message`) |
| CLI | `21-38` | Add `--dry-run`, `--json-out`; exit codes 0/1/2 |
| Tests | none | `tests/test_inject_hermes_task.py` with tmp inbox |

### 3. `device_selector.py` (tight integration)

- Export `beacon_age_seconds(machine) -> float | None` for activator health and status enrichment.
- Optional: include `beacon_age` in decision dict for relay logs (backward compatible keys).
- Unit tests with fixture beacon files in `tests/fixtures/`.

**No change** to single-active rules (`129-139`) unless verifier finds bug.

### 4. `relay_beacon.py`

- Remove duplicate `if __name__ == "__main__"` block (`41-49`); single entry `main()`.
- Activator does not import this; listener unchanged.

### 5. `relay_listener.py` (read-only integration)

- When logging dispatch, optionally `read_status(target)` and warn if `health_ok is False` (new field).
- No dispatch logic change in this project.

### 6. Service & deploy notes (documentation + copy, not necessarily edit unit in git)

**Runtime unit (reference):**

```ini
# ~/.config/systemd/user/washington-activator.service (live)
Environment=SYMBIOSIS_SHARED=/home/Irikash/Synced/grok-mempalace-integration
ExecStart=/usr/bin/python3 .../symbiosis-relay/washington_activator.py
```

**Deploy procedure after code merge:**

1. Edit in git worktree → `git add -f` tracked py/tests/docs.
2. `cp -a` changed files to `~/Synced/.../symbiosis-relay/` (mirror parity).
3. `python3 -m py_compile washington_activator.py activator_core.py`
4. `systemctl --user restart washington-activator.service`
5. Smoke: `python3 washington_activator.py --health`; drop synthetic task or `inject_hermes_task.py` + wait for relay cycle (if Pi live) OR local inbox drop + `--once`.

Document **ExecReload** not required v1; **Restart=on-failure** kept.

### 7. Packaging & git hygiene

- Add `pyproject.toml` (project name `symbiosis-relay`, version `0.2.0`, requires-python `>=3.11`, optional `[project.scripts]` `washington-activator`, `inject-hermes-task`).
- `.gitignore` exception at repo root:

```gitignore
# Nervous-source exception (mirror kit) — keep tree ignored except:
!cross-device/symbiosis-relay/
cross-device/symbiosis-relay/*
!cross-device/symbiosis-relay/*.py
!cross-device/symbiosis-relay/tests/
!cross-device/symbiosis-relay/pytest.ini
!cross-device/symbiosis-relay/pyproject.toml
!cross-device/symbiosis-relay/DESIGN.md
!cross-device/symbiosis-relay/RESEARCH_SYNTHESIS.md
!cross-device/symbiosis-relay/OPERATIONS.md
!cross-device/symbiosis-relay/ARCHITECTURE.md
!cross-device/symbiosis-relay/CURRENT_STATUS.md
```

Alternative: `git add -f` per file without gitignore edit — design accepts either; **implementer picks one** and documents in PRODUCTION_READY.

**Gitignore migration (MANDATORY for publishing the nervous source):**
Current root `.gitignore:35` is blanket `cross-device/symbiosis-relay/`. The negation block above will not un-ignore until the blanket is removed or commented. Implementer must:
1. Edit root `.gitignore`: delete/comment the blanket line for the subtree.
2. Insert the exception block (or rely on `git add -f` + commit the py's).
3. Verify: `git check-ignore -v cross-device/symbiosis-relay/washington_activator.py` must show no match (or explicit "not ignored").
4. Commit the .gitignore change + the focused py's/tests/docs as the "published mirror source".
Document the chosen path (exception vs add -f) + verification command in PRODUCTION_READY + handoff notes. This satisfies Mirrorability (brother can git checkout and have the source without "you had to be there").

---

## Production Readiness Plan

### PR DAG (independent, reviewable units)

Edges: `PR1 → PR2 → PR3`; `PR4` after PR1; `PR5` parallel after PR2; `PR6` after PR1-4; `PR7` last.

| PR | Title | Files (primary) | Review focus |
|----|-------|-----------------|--------------|
| **PR1** | Structured logging + error taxonomy + `activator_core` extraction | `activator_core.py`, `washington_activator.py`, `task_schema.py` | Exception specificity, no secret leakage in logs |
| **PR2** | Health interlocks + enriched `status.json` + `--health`/`--status` | `activator_core.py`, `washington_activator.py`, `device_selector.py` | Race: claim only if healthy |
| **PR3** | Injection reliability + env config + bust intent hook | `activator_core.py`, `inject_hermes_task.py` | Command injection, path traversal on inbox files |
| **PR4** | pytest suite + schema/selector/activator mocks | `tests/*`, `pytest.ini` | Coverage on fail paths |
| **PR5** | Docs: OPERATIONS, ARCHITECTURE, CURRENT_STATUS, coordination | `OPERATIONS.md`, `ARCHITECTURE.md`, `CURRENT_STATUS.md`, `../coordination/*.md` | Signatures, Ball Holder, mirror cmds |
| **PR6** | Packaging + gitignore exception + `pyproject.toml` | `pyproject.toml`, `.gitignore` | Reproducible install |
| **PR7** | Roundtrip + self-test enhancement + gate fixtures | `relay_roundtrip_test.py`, `relay_self_test.py` | Real `--once` subprocess option |

### Ops / Infra / Deploy / Verify tasks (not all separate PRs)

| ID | Task | Owner | Done when |
|----|------|-------|-----------|
| O-1 | Copy hardened py to rich Synced path | Implementer | `diff` clean vs git tagged commit |
| O-2 | Restart `washington-activator.service` | Implementer | `systemctl --user is-active` |
| O-3 | Run `relay_self_test.py` + `relay_roundtrip_test.py` | CI/local | exit 0 |
| O-4 | Run `washington_activator.py --once` on test inbox JSON | Verify | processed + status completed |
| O-5 | Optional: `inject_hermes_task.py "Test from Washington prod hardening"` | Verify | Pi routes if listener live; else WA inbox manual drop |
| O-6 | `journalctl --user -u washington-activator -n 50` | Verify | JSON/correlation visible |
| O-7 | Update MIRROR_KITS / linux-instructions / windows-instructions | PR5 | cp one-liner + Register OR note unchanged |
| O-8 | Kumquat prep note in coordination | PR5 | Oregon verify cmds listed |

### CI (minimal)

If repo has no workflow: add `grok-hermes-symbiosis/.github/workflows/symbiosis-relay.yml` (or document “local only” in gate report with evidence of manual runs). Job: `cd cross-device/symbiosis-relay && python3 -m py_compile *.py && pytest -q`.

---

## Key Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| KD-1 | **Stdlib only** for runtime deps; no `watchdog`/`pydantic` unless self-provision documents optional extra | Prime #4 self-test; Pi/WA parity; OQ default |
| KD-2 | **Poll + atomic claim** (rename to `processing/`) vs inotify | Avoid new dep; fixes duplicate glob race (synthesis #1) |
| KD-3 | **JSON logging** via stdlib `logging` custom formatter | §10 structured events; journal aggregation |
| KD-4 | **`git add -f` or .gitignore exception** for focused py/docs | Nervous mirror source while keeping bloat out |
| KD-5 | **`--profile service`** for auton-gate | §9/§10 MANUAL in gate; verifier supplies deploy/journal evidence |
| KD-6 | **Do not archive failed tasks to `processed/`** by default | Prevents silent loss; pending + failed dir |
| KD-7 | **Extract `activator_core.py`** | Enables unit tests without spawning loop |
| KD-8 | **Rich tools stay in Synced**; git may ship **stub README** in `tools/README.md` pointing to rich | Self-provision path for Oregon mirror |
| KD-9 | **No new Hermes/Slack token work** in this auton | External human blocker documented, not scope |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Git/rich drift | Service runs stale code | PRODUCTION_READY + O-1 cp checklist; version field in status |
| Dual activator / race | Double claim | Atomic processing rename; optional file lock doc |
| Single-active violation during beacon stuck | Pi refuses route | Health checks beacon age; beacon stop in `finally` |
| `hermes` hangs 300s | Blocks loop one task | Timeout + retry; status `processing` with heartbeat timestamp |
| Shared FS malicious JSON | DoS or path tricks | Max file size 1MB; schema; reject `..` in names |
| Mirror break on Oregon | Asymmetric receive | MIRROR docs + skeleton comment update only |
| auton-gate PASS without verifier | False prod | INTEGRATION_AUTONOMOUS 6.5-6.7 mandatory |

---

## Open Questions

| ID | Question | Default if silent |
|----|----------|-------------------|
| OQ-1 | Track py in git via exception vs `git add -f` only? | Implementer chooses; document in PRODUCTION_READY |
| OQ-2 | Add optional `watchdog` extra in pyproject `[project.optional-dependencies]`? | **No** unless implementer proves need |
| OQ-3 | CI workflow in parent repo vs relay-only local verify? | Local verify + gate evidence acceptable for v1 |
| OQ-4 | Invoke `pts-inject-input.py` from Python directly vs only via sh? | Try sh first; Python fallback second |

**Escalate to human:** dedicated `SLACK_INGEST_APP_TOKEN`; Oregon `Register-OregonBustANutPersistence` at real logon — document only.

---

## Validation Gates

### Build

```bash
cd /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay
export SYMBIOSIS_SHARED="${SYMBIOSIS_SHARED:-/home/Irikash/Synced/grok-mempalace-integration}"
python3 -m py_compile washington_activator.py activator_core.py task_schema.py inject_hermes_task.py device_selector.py relay_beacon.py relay_listener.py
# optional if available:
ruff check . || true
```

### Test

```bash
cd /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay
export SYMBIOSIS_SHARED="${SYMBIOSIS_SHARED:-/home/Irikash/Synced/grok-mempalace-integration}"
python3 relay_self_test.py
python3 -m pytest -q tests/
python3 relay_roundtrip_test.py   # after PR7: env USE_REAL_ACTIVATOR=1 runs subprocess --once
```

### auton-gate (Phase 6 — exact)

**Dev loops (gitignored tree / dirty):**

```bash
auton-gate check /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay \
  --auton-id 19557e65 \
  --profile service \
  --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md \
  --no-git-check
```

**Pre-handoff (tracked files committed):**

```bash
auton-gate check /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay \
  --auton-id 19557e65 \
  --profile service \
  --checklist ~/.grok/skills/autonomous/docs/PRODUCTION_CHECKLIST.md
```

Then: **security-auditor** (FS inbox, subprocess, path traversal) → **verifier** re-executes all commands → **`VERDICT: PASS`**.

### 12-section checklist tailoring (`--profile service`)

| Section | Tailoring for this component |
|---------|-------------------------------|
| §1-2 | MANUAL in mechanical gate; verifier uses DESIGN + RESEARCH_SYNTHESIS |
| §3 | py_compile + ruff; 0-issue review loops |
| §4 | pytest + relay_self_test + roundtrip (+ real --once) |
| §5 | FS trust model; no secrets; inject sh path fixed |
| §6 | CI optional with documented local runs |
| §7 | OPERATIONS + coordination updates |
| §8 | pyproject + gitignore exception |
| §9 | **systemd user service**, cp deploy, restart smoke — evidence in PRODUCTION_READY |
| §10 | JSON logs, journalctl, `status.json` + `--health`, relay-health.sh cross-check |
| §11 | git add -f or exception; clear commits |
| §12 | PRODUCTION_READY, Mempalace drawer, Hermes kanban, resume cmd |

---

## Handoff Artifacts Plan

### `PRODUCTION_READY.md` (create at close)

Template sections:

1. **VERDICT** + links to `GATE_REPORT.md`, verifier report, security report
2. **Run local:** venv optional `pip install -e .`; `--health`, `--once`
3. **Run prod:** systemd unit path, `SYMBIOSIS_SHARED`, cp from git commit SHA → rich
4. **Monitor:** `journalctl`, `status.json` fields, `relay-health.sh`, pending-prompts dir
5. **Resume autonomous:** `grok -p '/autonomous --resume 19557e65'`
6. **Mirror / Kumquat:** exact cp one-liner; Oregon verify `python3 washington_activator.py --health` equivalent TBD

### Mempalace drawer spec

- **Wing:** symbiosis (or projects)
- **Room:** `symbiosis-relay` / drawer `washington-activator-prod-19557e65`
- **Content:** AUTON_ID, slug, links to DESIGN, RESEARCH_SYNTHESIS, PRODUCTION_READY, gate hashes, commit SHAs, Ball Holder note, bust-wave diary pointer

### Hermes kanban (if MCP live)

- Lane: Symbiosis / Washington Activator Prod
- Cards: PR1-PR7, O-1–O-8, “Post-Kumquat verify Oregon”

### Coordination updates (exact signatures)

Touch with footer:

- `cross-device/coordination/linux-instructions.md` — prod runbook excerpt
- `cross-device/coordination/status.md` or equivalent living status
- `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md` (master mirror inventory) — cp + version; also touch `cross-device/coordination/linux-instructions.md` and `windows-instructions.md` for receipts
- `CURRENT_STATUS.md`, `ARCHITECTURE.md` in symbiosis-relay

**Ball Holder line (required):**

> Washington has the ball. (Implement PR DAG in worktrees; cp to rich; Phase 6 `auton-gate --profile service`; verifier PASS; then Kumquat mirror verify.)

```html
<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (design-doc-writer subagent, AUTON 19557e65) -->
```

---

## Appendices

### A. File:line change map (implementation checklist)

| File | Lines (current) | Action |
|------|-----------------|--------|
| `washington_activator.py` | 36-46 | Replace logging setup → call `activator_core.configure_logging` |
| `washington_activator.py` | 50-59 | Thin wrapper → `activator_core.write_status` |
| `washington_activator.py` | 62-71 | → `activator_core.fire_beacon` with retries |
| `washington_activator.py` | 74-159 | Move body to `activator_core.prompt_grok_build` |
| `washington_activator.py` | 166-191 | → `activator_core.run_loop` |
| `washington_activator.py` | 194-210 | → `activator_core.run_once` |
| `inject_hermes_task.py` | 40-46 | SYMBIOSIS_SHARED resolution |
| `device_selector.py` | 98-106 | Extract `beacon_age_seconds` helper |
| `relay_beacon.py` | 41-49 | Dedupe `__main__` |
| `relay_roundtrip_test.py` | 90-155 | Add flag to subprocess real activator |

### B. Example enriched `status.json` (target)

```json
{
  "state": "processing",
  "current_task": "slack-1717000000",
  "message": "Received task from Relay",
  "updated_at": "2026-06-03T12:00:00+00:00",
  "machine": "washington",
  "version": "0.2.0",
  "health_ok": true,
  "beacon_age_seconds_at_claim": 4.2,
  "last_inject_rc": null,
  "last_hermes_rc": null,
  "pending_prompts_count": 0,
  "retry_count": 0
}
```

### C. Example pending artifact header

```markdown
# Pending prompt — correlation slack-1717000000
## Error
Hermes timeout after 300s
## Suggested command
hermes -z "$(cat ...)" --skills grok-build
## Task JSON
...
```

### D. Prime alignment (7 primes)

1. **Research** — RESEARCH_SYNTHESIS cited throughout.
2. **Design** — this document; reviewer loop before implement.
3. **Implement** — worktree per PR; Composer/implementer persona.
4. **Self-test** — relay_self_test + pytest + roundtrip.
5. **Verify** — auton-gate + verifier + security.
6. **Handoff** — PRODUCTION_READY + Mempalace + coordination.
7. **Keep er goinnnn** — bust resume path preserved and hardened.

### E. 021dbe8d auton-gate linkage

Mechanical gate cleared `auton-gate` project; **this** auton uses the **installed** CLI (`~/.local/bin/auton-gate` or `pip install -e ~/auton-gate`) per `INTEGRATION_AUTONOMOUS.md` steps 6.1–6.7. Profile **`service`** forces §9/§10 manual adjudication with journal + FS side effects + subprocess evidence.

### F. Commands quick reference

```bash
# Health
python3 washington_activator.py --health

# One-shot (test inbox)
python3 washington_activator.py --once

# Inject Hermes inbox (Pi listener)
python3 inject_hermes_task.py "Test from Washington prod hardening" --priority high

# Service
systemctl --user status washington-activator.service
journalctl --user -u washington-activator -f

# Mirror copy after implement
cp -a /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay/washington_activator.py \
      /home/Irikash/grok-hermes-symbiosis/cross-device/symbiosis-relay/activator_core.py \
      /home/Irikash/Synced/grok-mempalace-integration/symbiosis-relay/
```

---

**Design consensus target:** 0 issues from design reviewer → implement PR1. The relay consumer stops being a hopeful poll loop and becomes a **locked, logged, health-checked** piece of the one extended machine — so when the Pi dispatches work, Washington **busts a nut** reliably, not politely.

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (design-doc-writer subagent, AUTON_ID 19557e65) -->