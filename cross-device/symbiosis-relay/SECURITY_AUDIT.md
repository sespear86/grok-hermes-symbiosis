# Security Audit — Washington Activator Hardening (AUTON 19557e65)

| Field | Value |
|-------|-------|
| **AUTON_ID** | `19557e65` |
| **Scope** | Published nervous source: `washington_activator.py`, `activator_core.py`, `task_schema.py`, `inject_hermes_task.py`, `tests/`, `pyproject.toml`, `README.md`, root `.gitignore` exception subtree |
| **References** | `DESIGN.md` (§ security, risks), `RESEARCH_SYNTHESIS.md` (§ security), `gate_report.json` (`s05.03.no_secrets_in_repo` PASS) |
| **Date** | 2026-06-03 |
| **Auditor** | security-auditor subagent |

---

## Summary

Review focused on the **hardening delta**: shared-FS inbox ingestion, schema validation, path construction under `SYMBIOSIS_SHARED`, subprocess boundaries (beacon / inject sh / pts / hermes), logging and status surfaces, and secret hygiene in **tracked** artifacts.

| Severity | Count (in scope) |
|----------|------------------|
| **Critical** | 0 |
| **High** | 0 |
| **Major** | 0 (see accepted trust-model notes below) |
| **Minor** | 8 |

**Mechanical gate:** `s05.03.no_secrets_in_repo` reports zero high-signal leaks in the audited project path; prior s05 finding was relocated out of published py (per orchestrator note — unrelated shell in rich tree).

**Verdict:** **security-auditor PASS 0 crit/high — ready for verifier + full checklist.**

---

## Trust model (accepted architecture — not scored as open defects)

The relay is intentionally **authorizationless at the file layer**: any writer trusted by Syncthing (or local FS ACLs) on `incoming/washington/*.json` can cause the activator to run `hermes` with attacker-controlled `original_message`. Hardening adds **validation and size caps** but does not add cryptographic authz. This matches `DESIGN.md` §5 / checklist §5 “FS trust model” and `RESEARCH_SYNTHESIS.md` (“Input: glob json from shared FS (trust Syncthing…)”). Documented for verifier; not a regression from this auton.

---

## Issues by severity

### Critical

*None.*

### High

*None in tracked hardening code paths.*

### Major

*None requiring code block before verifier.*  
(Inherent **unauthenticated FS inbox → code execution via hermes** is accepted product threat; mitigations are operational: Syncthing device trust, folder ACLs, monitoring — see Recommendations.)

### Minor

| ID | Title | OWASP / theme |
|----|-------|----------------|
| M1 | Slack/user text logged in JSONL | Sensitive data exposure (A09) |
| M2 | Full task JSON in `pending-prompts/*.md` on shared FS | Sensitive data exposure |
| M3 | Inbox JSON read follows symlinks | Path / FS abuse (CWE-61) |
| M4 | `inject_hermes_task.py` no payload size guard | DoS (A04) |
| M5 | `inject_hermes_task.py` bypasses `task_schema` | Consistency / weak input on hermes path |
| M6 | `INJECT_BUST_SCRIPT` / `GROK_BUILD_PRESENCE_BEACON` env override | Misconfiguration → arbitrary execution |
| M7 | Pending “suggested command” embeds prompt fragment in double quotes | Operator mistake / quoting (not remote RCE) |
| M8 | Legacy token-bearing files in same tree (gitignored) | Hygiene adjacent to scope |

---

## Evidence (file:line)

### Input: shared FS inbox + validation (`task_schema`, `activator_core`)

- **Glob + read:** `activator_core.py:338-344` — `COMMAND_INBOX.glob("*.json")`, `read_text()`, then `task_schema.validate_task_from_json_text(text)`.
- **1MB cap:** `task_schema.py:50-51` — `len(text.encode("utf-8")) > MAX_PAYLOAD_BYTES`.
- **Required keys + correlation regex:** `task_schema.py:19-37` — `REQUIRED_KEYS`, `CORR_RE = ^[A-Za-z0-9._-]{3,128}$`.
- **Invalid JSON / schema → failed/:** `activator_core.py:346-354` — rename to `FAILED_DIR`, no hermes.
- **Path base:** `activator_core.py:37-43` — all dirs under `SHARED_BASE / "symbiosis-relay" / ...`; no user-controlled path segments in `Path` joins for inbox roots.
- **Claim/archive:** `activator_core.py:197-222` — rename within `processing/`, `processed/`, `failed/` under inbox; basename preserved (no `..` segment in validated correlation; filename not used as path escape).
- **Gap (M3):** `activator_core.py:343` — `read_text()` on inbox file without `O_NOFOLLOW` / `is_symlink()` check.

### Subprocess: fixed argv, no shell, no user data in inject argv

- **Beacon:** `activator_core.py:134-142` — `cmd = [str(BEACON), "start"|"stop"|"bust_a_nut_start", task_id]`; `subprocess.run(cmd, ...)` — **no `shell=True`** (repo-wide: no `shell=True` in `*.py` under symbiosis-relay).
- **task_id source:** `activator_core.py:345,372` — `correlation` from validated task; regex prevents shell metacharacters in argv.
- **Inject sh:** `activator_core.py:263-264` — `[str(INJECT_BUST_SCRIPT)]` only; script path from env default under `SHARED_BASE/.../tools/` (`46-49`).
- **Pts fallback:** `activator_core.py:277-278` — `["python3", str(INJECT_BUST_PYTHON), "--bust-a-nut"]`; fixed flags.
- **Hermes:** `activator_core.py:311-315` — `["hermes", "-z", prompt, "--skills", "grok-build"]`; prompt built from task fields (`294-307`) but passed as **single argv element**, not interpolated into shell (DESIGN.md:138 — “never pass `original_message` to shell”).
- **DESIGN alignment:** `DESIGN.md:138-139` — subprocess fixed paths; Hermes argv list only.

### Path construction (`SYMBIOSIS_SHARED` + relative)

- **Activator:** `activator_core.py:37` — `Path(os.environ.get("SYMBIOSIS_SHARED", "/home/Irikash/Synced/grok-mempalace-integration"))`.
- **Inject helper:** `inject_hermes_task.py:42-46` — same pattern + Pi fallback if missing.
- **Correlation in filenames (inject):** `inject_hermes_task.py:49,65` — `slack-{int(time.time())}` always matches `CORR_RE`.
- **No `..` in correlation after validation:** `task_schema.py:35-37`.

### Secrets / tokens in tracked files

- **Hardened modules:** `washington_activator.py`, `activator_core.py`, `task_schema.py`, `inject_hermes_task.py`, `tests/test_task_schema.py` — **no** `xoxb-`, `xapp-`, API keys, or passwords in source.
- **Gate:** `gate_report.json:79-90` — `s05.03.no_secrets_in_repo` PASS, `leaks: []`.
- **Out of published allow-list (M8):** `SETUP_NATIVE_SLACK_GATEWAY.md:7-8`, `slack_to_hermes_bridge.py:27` contain live-format Slack tokens; excluded by `.gitignore` `cross-device/symbiosis-relay/*` with only whitelisted paths tracked (`/.gitignore:39-49`). Not in auton published surface; hygiene recommendation remains.

### Logging (secret / PII leakage)

- **Structured log:** `activator_core.py:76-92` — JSON lines; fields are mostly operational (`correlation`, `rc`, truncated stderr).
- **M1:** `activator_core.py:317-318` — `out=out[:1200]` includes **hermes stdout/stderr**, which embeds the full prompt including `original_message` (`300`) and `context_hints` — Slack/message PII on disk at `~/symbiosis-relay/logs/washington_activator.jsonl` (`71`).
- **Beacon stderr slice:** `activator_core.py:146` — `stderr=res.stderr[:200]` — low risk of secrets; operational only.
- **No tokens logged** in activator path.

### Health / status (PII)

- **status.json:** `activator_core.py:120-130` — `state`, `current_task` (correlation id), `message`, `machine`, `version`, optional `beacon_age_seconds_at_claim`, `last_*_rc` — **no** `original_message` field in status writer.
- **Health CLI:** `activator_core.py:154-188`, `washington_activator.py:36-39` — dirs, beacon age, script existence; no user message content.
- **M2:** `activator_core.py:237-238` — pending artifact dumps **full task JSON** (includes `original_message`) to shared `pending-prompts/` — intentional recovery; PII visible to all sync peers.

### `inject_hermes_task.py` (updated)

- **SYMBIOSIS_SHARED:** `inject_hermes_task.py:41-46` — fixed relative segments under shared root.
- **M4/M5:** `inject_hermes_task.py:27,66` — CLI message unbounded; no `validate_task` / 1MB guard before write to `incoming/hermes/`.

### `washington_activator.py` (thin CLI)

- **No subprocess** in thin layer; `washington_activator.py:31-50` delegates to core only.

### Tests / packaging

- `tests/test_task_schema.py` — negative tests for bad correlation; no secrets.
- `pyproject.toml` — empty `dependencies`; entry points only.

---

## OWASP-oriented assessment (hardening scope)

| Category | Assessment |
|----------|------------|
| **Injection (A03)** | **Pass** for activator: no shell; hermes/inject/beacon use argv lists; correlation sanitized. Inject CLI writes JSON only. |
| **Broken access control (A01)** | **Accepted FS trust model** — not introduced by hardening; health interlock reduces unsafe claim when unhealthy (`activator_core.py:356-361`). |
| **Security misconfiguration (A05)** | **Minor (M6)** — env overrides for beacon/inject scripts; systemd operator must control `Environment=`. |
| **Integrity / path (A08)** | **Pass** for path joins; **minor (M3)** symlink read. |
| **Logging / monitoring (A09)** | **Minor (M1, M2)** — message content in logs and pending files. |
| **DoS (A04)** | **Mitigated** on activator read (1MB); **minor (M4)** on inject helper. |

---

## Recommendations (even if minor)

1. **M1:** Redact or hash `original_message` in `_json_log` hermes output; log correlation + rc + length only (or env `ACTIVATOR_LOG_REDACT=1`).
2. **M2:** Document in `OPERATIONS.md` that `pending-prompts/` may contain Slack text; restrict Syncthing peers; optional encrypt-at-rest out of scope.
3. **M3:** Before `read_text()`, reject if `cmd_file.is_symlink()` or open with `O_NOFOLLOW` where available.
4. **M4/M5:** Reuse `task_schema.validate_task` + size check in `inject_hermes_task.py` before write.
5. **M6:** In `OPERATIONS.md`, pin `Environment=` in unit file; avoid user-writable env drop-ins; consider read-only `INJECT_BUST_SCRIPT` path check (`resolve().is_relative_to(SHARED_BASE)`).
6. **M7:** Suggest hermes replay via file reference in pending artifact instead of inline-quoted prompt.
7. **M8:** Rotate tokens in `SETUP_NATIVE_SLACK_GATEWAY.md` / `slack_to_hermes_bridge.py` in rich tree; keep out of git allow-list (already ignored).
8. **Verifier evidence:** Run inbox negative test (bad correlation, >1MB file, malformed JSON) → lands in `failed/` without hermes; confirm journal/jsonl has no new secret patterns.

---

## Files reviewed (full read unless noted)

- `DESIGN.md`, `RESEARCH_SYNTHESIS.md`, `gate_report.json`
- `washington_activator.py`, `activator_core.py`, `task_schema.py`, `inject_hermes_task.py`
- `tests/test_task_schema.py`, `tests/conftest.py`, `tests/test_activator_core.py.incomplete-sub` (skeleton, not in pytest collection)
- `pyproject.toml`, `README.md`, `PRODUCTION_READY.md` (stub)
- Root `.gitignore` symbiosis-relay exception block
- Grep: `subprocess`, `shell=True`, secrets in `*.py` / tracked docs
- Integration spot-check: `relay_listener.py:63-70` (dispatch filename; Washington side validates on consume)

---

**security-auditor PASS 0 crit/high — ready for verifier + full checklist.**

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (security-auditor subagent, AUTON 19557e65) -->