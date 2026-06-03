# Handoff Package — Clean Oregon Symbiosis Receiver Install Kit (19557e65)

**ID:** 20260603-Oregon-Symbiosis-Receiver-Install-Kit-19557e65
**From:** Washington Linux
**To:** Oregon Windows
**Date:** 2026-06-03
**Status:** Awaiting Oregon Kumquat

## Context
Direct follow-on to the just-completed live test wave on Washington (AUTON 19557e65 hardened Washington-side Hermes task activator / injection / presence).

WA delivered PASS at 60773bd + full live fire receipts (inject + manual drops + --once x2 normal/bust + service restart + PATH self-prov + poll). Everything proven: health interlock before claim, atomic claim via processing/ rename, beacon with active/bust flags, enriched status.json (health_ok + beacon_age_seconds_at_claim + version + last_*_rc + machine), structured JSON logs + correlation on every event, hermes rc enforcement (non-zero = failure + full pending artifact + last_hermes_rc + failed/ archive to avoid silent loss), bust_a_nut_resume live TUI first success (rc=0, marker, presence bust=true), normal hermes fallback + pending, no regressions.

**LIVE_TEST_19557e65_RECEIPTS.md is the verification spec for the Oregon port.**

This handoff delivers the **clean, production-ready, installation-and-implementation-ready packaging** so on Oregon's *next Kumquat* they pull, run a small number of exact commands, and have a fully functional hardened receiver (mirroring activator_core behaviors exactly) integrated with existing bust-a-nut persistence (Register/Get), scheduled tasks, markers, TUI inject paths.

## Task / Request
On your next Kumquat:
1. Pull (git + rich Syncthing).
2. cd C:\Synced\grok-mempalace-integration\symbiosis-relay\windows\oregon-receiver
3. Elevated: powershell -ExecutionPolicy Bypass -File .\Install-OregonSymbiosisReceiver.ps1
4. .\Test-OregonReceiver.ps1  (MUST exit 0 with "PASS — matches LIVE_TEST_19557e65_RECEIPTS.md")
5. Run Get- (extended) + CLIs.
6. Reboot + real logon test (no manual; TUI bust or drop task).
7. Update this RETURN + windows-instructions.md + status.md + MIRROR_KITS + handoff RETURN with your receipts + **Oregon has the ball.** (or hand back).
8. Kumquat back with sigs + Ball Holder.

## Relevant Information / Artifacts
- **Canonical spec:** cross-device/symbiosis-relay/LIVE_TEST_19557e65_RECEIPTS.md (git + rich; exact log lines, status cats, pending examples, commands, verifs).
- **Reports:** FINAL_REPORT_19557e65.md (live test completion + appended resume prompt), PRODUCTION_READY.md (Post-PASS Live Test section), DESIGN.md (health/claim/prompt rules).
- **Source (shared nervous, travels via git+Syncthing):** cross-device/symbiosis-relay/{activator_core.py, washington_activator.py (now with SYMBIOSIS_DEVICE back-compat), pyproject.toml bumped, tests/}.
- **New clean kit (in git + will rich cp):** windows/oregon-receiver/{Install-..., Oregon-Symbiosis-Receiver.ps1 (thin), Test- (the star), README-OREGON-RECEIVER-INSTALL.md}.
- **Updates:** bust-a-nut/{Register-OregonBustANutPersistence.ps1, Get-...} enhanced for receiver task family; oregon-activator-skeleton.ps1 big deprecation note pointing to new kit + "use shared hardened py + launcher for full parity with 19557e65 live test".
- **Handoff self-contained copies:** the 3 ps1 + install guide are copied here.
- Previous: 20260602-2100 handoff (real Slack readiness), f17323b/f2db482/dfaa2d1 commits, rich cps, Mempalace drawer updates.
- Sample task + expected status snippets in this dir (see below) + Test- script.

## What Has Already Been Done (Washington)
- Small back-compat generalization in py (SYMBIOSIS_DEVICE env or --device flag, default "washington"; builds correct inbox/status/beacon paths; "19557e65 + oregon-support" comments; tested on Linux: default unchanged, oregon mode creates right paths + --health/--once work; py_compile + pytest green; "packaging change only").
- Full clean kit written + self-provisioned (Install idempotent elevated + dirs + Register call + scheduled task "Oregon-Symbiosis-Task-Receiver" logon+10s repeat hidden restart; thin launcher wrapper; Test- star that exactly reproduces WA live test outcomes).
- Install guide + deprecation + Register/Get enhancements.
- Handoff package created per HANDOFF_FORMAT (this + RETURN template + scripts).
- Living docs updated (HANDOFF_LOG row, MIRROR_KITS new Oregon receiver section + copy/install/verif cmds, top of windows-instructions new standing order, brief linux note, status entry).
- Git + rich cp ritual + Mempalace + state + check-primes/relay-health equiv.
- All with exact <!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> sigs + Ball Holder + 7 primes + Mirrorability + raunchy + self-prov + no blue balls.
- Linux verification of gen py + Test- logic (will mirror on OR run).

## Success Criteria
- [ ] Kumquat performed, nervous + rich in sync.
- [ ] Install run from elevated PS in oregon-receiver/.
- [ ] .\Test-OregonReceiver.ps1 exits 0 printing "PASS — matches LIVE_TEST_19557e65_RECEIPTS.md" (paste full output).
- [ ] Get- shows receiver task + bust family; --health/--status show enriched oregon data + version.
- [ ] Reboot + real logon test: receiver task runs without manual, beacons hot, TUI bust or dropped task processes (status, presence, archive, logs).
- [ ] First real task or bust test receipts captured.
- [ ] RETURN.md filled + this handoff status Completed + sig + Ball Holder.
- [ ] windows-instructions.md + status.md + MIRROR_KITS updated with OR receipts + exact sig.
- [ ] **Oregon has the ball.** (or hand back with blockers).

## Preferences / Constraints
- Follow HANDOFF_FORMAT exactly (bing bang boom in summaries, Linux Turn? N/A here as cross, Relevant Memory, RETURN template).
- Exact sigs on every touched/created file.
- Mirrorability as mandatory final internal (everything has exact OR install recipe).
- Use the provided Test- / Install / launcher as the mechanical steps — no reinvention.
- Raunchy depraved wit where it fits (in comments, RETURN, updates).

## Handoff Notes
The packaging is **clean**: minimal, focused, production-grade, version/comments referencing 19557e65 + live test date, no cruft. Self-contained (one-liners, full scripts, acceptance that mirrors receipts). Reusable (C:\Synced paths, elevated PS, Task Scheduler).

**Ball Holder:** Oregon has the ball upon their next Kumquat to pull, install via the kit, run Test- to match the WA live test receipts, register via extended Register, reboot-verify, first real/bust test, update docs + RETURN + this handoff with receipts + **Oregon has the ball.** (or hand back).

## Relevant Memory (Mempalace)
- /symbiosis/three-primes.md
- /symbiosis/handoff-conventions.md
- /symbiosis/git-gotchas.md
- /symbiosis/priorities.md (live: cross-device/coordination/OPEN_ITEMS.md)
- /symbiosis/recent-decisions.md
- /symbiosis/usage-pattern.md
- projects/symbiosis-washington-activator-prod drawer (live test wave + this packaging entry)
(See MEMPALACE_INTEGRATION.md, usage-pattern, and the 0010/0130/0200 handoffs for the living pattern.)

## Supporting (embedded for self-containment)
**Sample task JSON (inline in Test- too):**
```json
{
  "type": "grok_build_task",
  "correlation_id": "oregon-test-19557e65",
  "original_message": "Live fire test of 19557e65 hardened core packaging on Oregon (post WA PASS + receipts). Verify health interlock, atomic claim, beacon flags, enriched status, rc enforcement, pending on fail, logs with corr.",
  "priority": "high",
  "source": "test-oregon-receiver",
  "context_hints": { "test": "packaging-19557e65", "mirror": "LIVE_TEST_RECEIPTS" }
}
```

**Expected status snippet (from WA receipts, adapted):**
```json
{
  "state": "error",  // or "bust_a_nut_injected_live" / "completed"
  "current_task": "oregon-test-19557e65",
  "machine": "oregon",
  "version": "0.2.0-auton-19557e65",
  "health_ok": true,
  "beacon_age_seconds_at_claim": 28,
  "last_hermes_rc": 1,
  ...
}
```

**Pending example (fail path, full format per receipts):**
```
# Pending prompt — correlation oregon-test-19557e65

## Error
hermes rc=1

## Suggested command (copy-paste)
hermes -z "..." --skills grok-build

## Task JSON (for context)
{ ... full task ... }
```

See Test-OregonReceiver.ps1 (copied here) for the exact assertions that must pass.

---

**COPY AND PASTE THE BLOCK BELOW TO RESUME AFTER OREGON KUMQUAT + INSTALL (newest prime at end of this handoff):**

```prompt
/autonomous Resume after Oregon Kumquat + 20260603-Oregon-Symbiosis-Receiver-Install-Kit-19557e65 packaging.

Full context from WA live test + this packaging (read these first in order):
- cross-device/symbiosis-relay/LIVE_TEST_19557e65_RECEIPTS.md (the spec — health before claim, atomic, beacon flags, enriched status+version, corr JSON logs, rc enforcement + pending full + failed/ on non-success, bust live TUI rc=0 success, service PATH self-prov, all verifs).
- cross-device/symbiosis-relay/FINAL_REPORT_19557e65.md (live test section + appended resume prompt).
- cross-device/symbiosis-relay/PRODUCTION_READY.md (Post-PASS Live Test).
- cross-device/symbiosis-relay/DESIGN.md (rules).
- The handoff dir 20260603-... (README + copied scripts + RETURN template).
- cross-device/coordination/windows-instructions.md (new top standing order), status.md, MIRROR_KITS (new receiver kit section), linux-instructions (brief note).
- oregon-receiver/ kit + updated Register/Get/skeleton (with deprecation) + install guide.
- ~/.grok/auton-projects/19557e65.json (live_test_wave complete + this packaging).

Oregon has just Kumquat'ed, pulled the packaging, run Install (elevated), Test- (hopefully PASS), Get-, reboot + TUI/bust or real task test.

Your mission (bust a nut, nonstop, no blue balls):
1. Verify the install + Test- output matches receipts (if not, fix gaps self-provision + re-run).
2. Run real or synthetic tasks (drop JSON to incoming\oregon\ or TUI bust), capture full receipts (status cats, logs with corr, presence with bust, pending/processed/failed, journal equiv via Get- or health).
3. Update all docs with Oregon receipts + exact <!-- Edited: YYYY-MM-DD | Device: Windows | By: Grok (19557e65 Oregon packaging + Kumquat verification) --> sigs + Ball Holder.
4. Fill RETURN.md in the handoff (Kumquat performed, install run, Test- PASS output pasted, Get- output, reboot verif, first real task or bust test receipts, updated status + MIRROR + handoff RETURN, **Oregon has the ball.** or hand back, exact sig).
5. Append row to HANDOFF_LOG (mark Completed), top of windows-instructions if needed, status, MIRROR_KITS.
6. Kumquat back (push + rich cp) if needed for WA to see.
7. Prepare next wave (e.g. real Slack through the dual-sided hardened receiver — both sides now have parity; when dedicated ingest token live, route to thrusting side, injector if bust, full end-to-end).

Follow every prime exactly (Kumquat ritual, Mirrorability last internal before output, Ball Holder exact, sigs on every touched, self-provision gaps instantly, raunchy wit, bust a nut no stopping points, newest prompt-creation prime at END of every major output/handoff/report including your RETURN + final summary).

Use todo_write with the phases if multi-step. Subagents/worktree for heavy. Re-verify against receipts on any change.

At absolute end: new perfect copy-pasteable continuation prompt in code block for next (e.g. full dual Slack production, or expand tests, or Pi listener parity, or ...).

Washington had the ball for packaging prep. You (Oregon) have the ball now for execution + verification + hand back.

Bust a nut. Keep er goinnnn with zero natural stopping points until docs updated, RETURN filled, Kumquat hygiene done, next prompt written, and the dual receiver is cocking for real traffic.

Read the receipts + handoff README first. Do it now.
```

**Washington has the ball for packaging prep (complete). Oregon has the ball for the Kumquat + install + Test- to match receipts + report back.**

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> Exact all 7 primes + Mirrorability (handoff + MIRROR + instructions + kit have full zero-guess OR recipe) + bing bang boom + self-provision + raunchy + newest prompt prime at end followed. The one extended machine's receiver just got its cross-device packaging rammed into clean, installable shape. Keep er goinnnn, you packaging-thrusting degenerates.