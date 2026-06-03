# Design Document Review: Harden Washington Hermes Task Activator (19557e65)

## Round 2 (2026-06-03)

**Reviewer:** design-doc-reviewer subagent  
**Artifact:** [`DESIGN.md`](./DESIGN.md) (amended after round 1)  
**Cross-check:** `washington_activator.py`, `inject_hermes_task.py`, `device_selector.py`, `relay_beacon.py`, `relay_listener.py`, root `.gitignore:35`, `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md`, `RESEARCH_SYNTHESIS.md`, `~/auton-gate/docs/INTEGRATION_AUTONOMOUS.md`, live `washington-activator.service`

---

### Summary

**VERDICT: APPROVED FOR IMPLEMENT — 0 issues (round 2).**

All **four round-1 major** findings are **resolved** in the amended design. No new **critical** or **major** issues were introduced. **Five round-1 minor** items remain (documented below); none block implementation if implementers follow PR DAG + §7 gitignore migration + line 134 Hermes contract.

---

### Round-1 major — resolution verification

| # | Issue | Status | Evidence in amended `DESIGN.md` |
|---|--------|--------|----------------------------------|
| 1 | Wrong MIRROR_KITS path | **Fixed** | Line 390: `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md` (file exists at that path) |
| 2 | `.gitignore` migration omitted | **Fixed** | Lines 209–215: mandatory steps 1–4 + `git check-ignore -v` + PRODUCTION_READY note |
| 3 | `activator_health.check()` naming | **Fixed** | Line 118: `activator_core.check_health()` (or `health_check()`) |
| 4 | Hermes `returncode` ignored | **Fixed** | Line 134: explicit failure on `result.returncode != 0`, pending + `last_hermes_rc`, KD-6 no archive |

---

### Baseline & feasibility (re-confirmed)

| Claim | Still accurate |
|-------|----------------|
| Poll loop `166–191`, archive even on failed prompt today | Yes (`washington_activator.py`) |
| Inject sh `84–85`; git `tools/` lacks inject script | Yes |
| `inject_hermes_task.py` `41–43` no `SYMBIOSIS_SHARED` | Yes |
| Single-active `129–139`, WA `142–151` | Yes |
| `relay_listener` ~30s, beacon ~90s | Yes |
| Roundtrip sim, not real `--once` | Yes |
| `relay_beacon` duplicate `__main__` | Yes |
| Service → rich `washington_activator.py` + env | Yes |
| `.gitignore` blanket ignore line 35 | Yes (migration doc now matches reality) |
| Phase 6 `auton-gate` commands + checklist path | Yes |

---

### Remaining minor (non-blocking; may fix during implement/docs)

**Issue R2-M1 (was #5):** Appendix F mirror `cp` still lists only `washington_activator.py` + `activator_core.py`. PR1–PR7 touch more files — use O-1 “diff clean vs tagged commit” or expand F to match PR file lists.

**Issue R2-M2 (was #6):** `processing/` and `failed/` used in resilience table but not in “Proposed module layout” or explicit startup `mkdir` — add in PR1/PR2 acceptance or `activator_core` init.

**Issue R2-M3 (was #7):** `BEACON = ~/bin/grok-build-presence-beacon` hardcoded in current code; design health checks “script exists” but no `GROK_BUILD_PRESENCE_BEACON` env — optional OPERATIONS note.

**Issue R2-M4 (was #8):** Claim row still mentions `portalocker` while KD-1 is stdlib-only — implementer should treat v1 as **rename-only** (align with KD-2; no new dep).

**Issue R2-M5 (was #9):** Shared-FS partial JSON during Syncthing drop not in Risks — optional PR1 guard (mtime stable / size cap already cited).

**Issue R2-M6 (new nit):** Handoff line 390 references `windows-instructions.md` without `cross-device/coordination/` prefix (linux path is fully qualified) — fix path in PR5 for consistency.

**Issue R2-M7 (new nit):** Health API allows two names (`check_health` vs `health_check`) — PR2 should pick **one** symbol and export it.

---

### Primes / Phase 6 / Mirrorability (round 2)

| Item | OK |
|------|-----|
| Ball Holder + next steps | Present |
| Phase 6 exact cmds + verifier/security chain | Present |
| Gitignore migration + Mirrorability prose | Present (§7) |
| Kumquat / O-7 / MIRROR at correct path | Present |
| Bust path + KD-6 archive rules | Strengthened (Hermes rc) |
| Security: fixed inject paths, no shell on `original_message` | Present |

---

### Round 1 archive (for history)

Round 1 verdict was **NOT APPROVED** (4 major, 5 minor). This file supersedes round 1 for gating; majors are closed above.

---

**Washington has the ball.** (Next: spawn implementers per PR DAG in isolated worktrees — **PR1** first → PR2 → PR3; PR4 after PR1; PR5/PR6/PR7 per edges; O-1 cp to rich after each merge wave; Phase 6 `auton-gate --profile service` with `--no-git-check` in dev until tracked; full verifier + security → `VERDICT: PASS`.)

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (design-doc-reviewer subagent, AUTON_ID 19557e65, round 2) -->