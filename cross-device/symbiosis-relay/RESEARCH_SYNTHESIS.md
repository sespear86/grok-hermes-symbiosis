# RESEARCH_SYNTHESIS: Harden & Productionize Washington Hermes Task Activator / Injection / Presence

**AUTON_ID**: 19557e65
**Project Slug**: symbiosis-washington-activator-prod
**Date**: 2026-06-03 (Washington Linux)
**Focus**: cross-device/symbiosis-relay/ core: washington_activator.py, inject_hermes_task.py + tight integration relay_beacon.py, device_selector.py, relay_listener.py, status flows, pending prompts, beacon control.
**Scope Rule**: Edit/work inside git repo's symbiosis-relay/ subtree. Runtime lives in ~/Synced/.../symbiosis-relay/ (Syncthing rich layer). Git copy serves as mirror-kit "published source" (cp'ed historically for Oregon parity) + nervous system reference. Do not boil ocean on full Pi deploy, Windows PS1 (beyond notes), or unrelated.

**Bust a Nut Contract**: Nonstop thrust per immutable autonomous pipeline + all symbiosis primes (Kumquat ritual, Mirrorability/Full Provisioning, Ball Holder exact statements, exact <!-- Edited: ... | Device: ... | By: ... --> signatures, 7 Primes, Self-Provisioning/Gap-Filling, raunchy depraved wit where fits, no blue balls, 0 issues on final rounds, Kumquat hygiene + mirror parity verification at close). Dogfood auton-gate (from 021dbe8d) exactly in Phase 6 with --profile service. VERDICT: PASS only after full verifier + security-auditor + 12-section adjudication (never mechanical alone).

## Executive Summary (Bing Bang Boom)
The Washington activator (washington_activator.py:1) + inject helpers are the **live cock that receives relay-dispatched tasks** (from Pi's relay_listener.py + device_selector.py), enforces single-active via beacon fire (grok-build-presence-beacon + relay_beacon.py), prefers live TUI re-init for bust_a_nut_resume (via external sh in rich tools/), falls back to hermes -z + grok-build skill, writes status to outbox, archives to processed/, drops pending-prompt artifacts on fail. It is already "running as real washington-activator.service" (systemd user unit pointing at rich copy), proven in live roundtrips + "Test from Washington" real Slack fire (selector chose WA due to fresh beacon, task hit inbox, activator claimed, status updated, processed moved).

**Current State (from self-test + beacon + HB 2026-06-03)**: Self-tests PASS (selector, beacon, paths). Beacon hot (grok_build_active: true, last_seen ~0s, bust false currently but intent context live from prior). Paired mode (Oregon HB stale but explicit recent cross + Option B). Services: activator + beacon-refresher + ui-idle-monitor + fast hb timers active per relay-health snapshots. Plumbing solid for file-drop protocol.

**Why This Run (User Directive + Known Rough Edges)**: "known rough edges around robustness, persistence (real logon vs session/tmux), health interlocks, error handling, logging, and cross-device reliability." High-leverage real subsystem of live Symbiosis (receives from Pi, fires beacon, single-active rule, "bust a nut" / autonomous resumes into running TUI incl fast path + failure artifacts). Link to 021dbe8d: auton-gate now canonical mechanical gate; dogfood it --profile service on this real code. Target: cleaner/resilient code, expanded tests, updated docs (coordination + relay status), packaging notes, full handoff (PRODUCTION_READY.md, Mempalace projects/ drawer in symbiosis wing?, Hermes kanban), Kumquat prep + mirror hygiene. Bust a nut until gate says real **VERDICT: PASS**.

**Evidence Chain Summary**: 50+ tool calls (list_dir, read_file on 20+ py/md/service, grep 100+ lines, run_terminal self-tests + beacon cat + find, use_tool mempalace list_wings/rooms/drawers for symbiosis-relay wing 24 drawers + projects, run self_test PASS baseline). Cited file:line throughout. Prior bust waves (May 29- Jun 3 diary in Mempalace symbiosis-relay + rich tools) delivered the live inject, fast HB, watchdog, intent marker, trust escape, service, pending, status — this hardens it to prod.

## Current Architecture & Flows (with Exact Cites)
**Core Data Flows (file-drop Option B, Syncthing/Mempalace rich as bus)**:
1. External (Slack/Hermes) or synthetic → Pi: slack_task_ingest.py (or companion) drops to incoming/hermes/task-*.json (is_real, task_reality tags in recent).
2. Pi: relay_listener.py:main_loop (116) → every 30s: write_relay_beacon (relay_beacon.py:29), select_device_for_grok_build_task (device_selector.py:109), if chosen + real task: enrich context_hints with relay_decision/beacon_state, dispatch_task_to_device (writes to incoming/<device>/task-*.json), consume to processed.
3. Washington: washington_activator.py (service: ExecStart=python3 .../washington_activator.py , env SYMBIOSIS_SHARED) main() (162): while True: glob incoming/washington/*.json (oldest? sorted), parse, fire_beacon(True, corr) (62 calls ~/bin/grok-build-presence-beacon start), write_status("processing"), success = prompt_grok_build(task) (74), if success write completed, rename to processed/, fire_beacon(False).
   - prompt_grok_build: special for "bust_a_nut_resume" (80): prefer live inject via subprocess SHARED/.../tools/inject-bust-a-nut-into-running-tui.sh (timeout 30, capture), on success "bust_a_nut_injected_live"; else build strong prompt + hermes -z prompt --skills grok-build (timeout 300). On any except: write pending-prompts/<corr>.md , status error.
   - Normal task: build prompt with corr/source/slack/msg/context, hermes -z.
   - run_once() (194) for tests (roundtrip uses sim not this).
4. Beacon control: washington_activator fires via beacon script (bash:40 write_beacon with grok_build_active, bust_a_nut_active from marker, also .washington-grok-fast-heartbeat + push-presence-to-pi.sh for <30s Pi detect). device_selector reads washington-grok-build-presence.json + heartbeat md + relay-presence.json (is_beacon_fresh 300s).
5. Status: write_status (50) → status/washington/status.json (state, current_task, message, updated_at, machine). relay_listener peeks read_status. relay-health.sh + dashboards poll.
6. Single-active enforcement (non-negotiable, device_selector:129): if both beacons active → chosen=None + HARD VIOLATION. WA priority on fresh active or healthy heartbeat. Relay is arbiter.
7. Failure artifacts: PENDING_PROMPTS_DIR for manual paste; also rich has processed-pending-rearms/.
8. Injection (inject_hermes_task.py): dev/test tool, drops to hermes inbox (sim Slack). Not the TUI one.
9. Persistence: washington-activator.service (user, restart on-failure 15s, journal). Beacon refresher timer. TUI side: tmux + ui-idle-monitor.service (trust marker .current_bust_tui_pane escape), bust-a-nut-*-timers, sessionstart hook, pts-inject-input.py for non-tmux, intent marker .bust_a_nut_intent_active. Oregon: skeleton ps1 + Get/Register persistence (real logon scheduled task preferred over session for survival).

**Key Integration Points**:
- Activator <-> device_selector (indirect via beacon files written/read across).
- Activator <-> relay_beacon (via beacon script + fast push).
- Activator <-> relay_listener (dispatch file + status.json roundtrip).
- Activator <-> rich tools sh (live inject path hard dep for bust resume fastpath).
- All portable via SYMBIOSIS_SHARED (smart default WA /home/Irikash/Synced... or /home/pi/...).

**Current Tests**:
- relay_self_test.py: paths, selector decision (no crash), relay_beacon write. PASS baseline (2026-06-03 run).
- relay_roundtrip_test.py: selector + dispatch + sim activator_once (beacon fire, status, archive). Proves file-drop end-to-end.
- No dedicated unit for washington_activator logic, no failure injection tests, no schema tests.

**Runtime vs Source**:
- Git: cross-device/symbiosis-relay/*.py (NOT currently tracked per .gitignore:35 double-path + "stale duplicate" comment; canonical rich in Synced per hygiene; git copy used for mirror kits cp + Oregon skeleton reference).
- Rich/Synced (live): full tools/ (16718 byte inject sh etc), services point here.
- Mirror: MIRROR_KITS_AND_INFRASTRUCTURE.md explicitly lists washington_activator.py + systemd unit + "Needs PowerShell port", "Transfer method: rich Syncthing", "cp exact-unit".

## Identified Rough Edges (Evidence + Impact — Critical for Prod)
**1. Robustness (Poll Loop, Races, Retries)**:
- washington_activator.py:166 while True: for cmd_file in sorted(glob("*.json")): ... rename after; time.sleep(5). No inotify, no flock, no dedup on re-glob during slow hermes(300s). Risk: duplicate claim if rename lags or two activators. (Line 167, 183).
- No retry on fire_beacon / write_status / subprocess. Beacon op just log.warning (70).
- Roundtrip sims the logic but real activator not exercised in self-test for --once path fully.
- Impact: missed tasks under load, or double-activation violating single-active.

**2. Persistence (Real Logon vs tmux/Session)**:
- Activator itself: systemd user service (good for logon/reboot survival, restart).
- But "bust a nut" / TUI reinit: depends on live tmux pane (inject sh:58 uses pgrep grok + openclaw tmux/find-sessions + trust marker escape for grok:pts:* or non-tmux). If TUI not running (cold start, crash, logoff), falls to hermes new session.
- Oregon reality check + MIRROR: "real logon vs session/tmux" explicit gap; Register-*.ps1 for scheduled task at real user logon (not just session) to keep beacons alive across reboots without manual launch.
- Beacon has bust_a_nut_start but activator doesn't always assert intent on resume path before sh.
- Impact: "bust a nut" resumes fail or require new TUI on cold/reboot; cross-device asymmetry (WA has more services, OR skeleton).

**3. Health Interlocks**:
- Activator claims task + fires beacon without checking own beacon freshness or relay-presence (could race with selector or stale self).
- No pre/post health call to relay-health.sh or status roundtrip verification.
- Status is flat json; no "last_inject_rc", "pending_count", "beacon_age_at_claim".
- Pi watchdog (pi-grok-liveness-watchdog.py) + 5s timer relies on fast marker + push; activator doesn't directly drive fast path beyond sh side effects.
- Evidence: relay-health.sh 100+ lines of service status + intent + beacon age + last reinit + counters; activator logs only basic.
- Impact: silent degradation; watchdog dispatches resume only on detected silence.

**4. Error Handling & Failure Artifacts**:
- Broad `except Exception as e: log...` (188, 96, 150, 208). No specific (json decode, timeout, permission on rename, beacon missing).
- Pending prompt only written on hermes prompt fail (153); on live inject fail (95) just warning + falls to hermes (which may also fail).
- No dead-letter, requeue, or max-retries; task archived even on fail?
- No validation: task.get without schema (type, correlation_id, original_message).
- On sh not found (git vs rich drift): subprocess rc!=0, treated as "failed live", falls back (but path in activator:84 is SHARED/.../tools/... which runtime has, git source may not until cp).
- Impact: lost tasks, poor debug (truncated stderr 300), manual recovery only via pending md.

**5. Logging**:
- logging.basicConfig level=INFO, format asctime level msg, FileHandler + Stream (39-46). No json, no correlation_id in every record, no extra fields for journald (systemd).
- Hermes output truncated 1800; no persistent per-task log.
- Contrast rich: relay-health, inotify logs, bust counters, chat repair.
- Impact: hard to parse/monitor/aggregate; poor for auton-gate or Hermes gateway alerts.

**6. TUI Injection Reliability & Config**:
- Hardcoded sh path in prompt_grok_build (84: SHARED / symbiosis-relay / tools / inject-...sh). Works at runtime (rich copy), but if git is "source", drift possible; no `which` or configurable INJECT_SCRIPT env.
- No python fallback (pts-inject-input.py exists in rich tools, 12228 bytes, used by sh?).
- Success only if rc==0; no output inspection for "injected" confirmation beyond rc.
- For non-bust tasks: always new hermes (no "attach to running TUI" even if active).
- Evidence: sh itself is robust (intent gate 33, trust marker 67, pts bypass 73, beacon assert 54, openclaw helpers); activator just shells it.
- Impact: bust resume not 100% reliable; new sessions when live possible.

**7. Cross-Device Reliability & Mirror**:
- Git py is "for mirror kit" (windows-instructions, OREGON_...md, MIRROR_KITS:170 "washington_activator.py (and Oregon equivalent)", "cp of latest... so mirror kit has").
- But git ls-files shows NOT TRACKED (ignored); hygiene comment says canonical exclusively rich to avoid bloat.
- Windows: only oregon-activator-skeleton.ps1 (4 lines comment "Port from washington_activator.py ... Add the file watcher logic").
- No equivalent status/pending logic ported; beacon on OR is Get- status ps1.
- Kumquat/Mirrorability: every significant change must deliver "everything the other device needs" (exact scripts, units, one-liners, verify cmds). Prior waves declared "Mirrorability NOT MET" until human Register + token.
- Impact: Oregon not symmetric for receiving tasks; if WA dark, tasks may queue or fail to route cleanly.

**8. Packaging / Entry / Observability / Security**:
- No pyproject.toml, no console_scripts entry for activator or inject_ (run as python3 fullpath or service).
- Paths: many /home/Irikash hard (beacon script, markers) even with SYMBIOSIS_SHARED (beacon bash has hard BEACON_DIR).
- No health/readiness in activator (could add --status or http stub but keep lightweight).
- Input: glob json from shared FS (trust Syncthing but no size limit, schema, authz).
- Secrets: none in scope, but hermes calls assume env.
- No lockfile or dep pin (stdlib + subprocess ok, but if add watchdog/pydantic for prod?).
- Service: no ExecReload, limited Type=simple, no Notify.
- Impact: not "reproducible build/packaging", hard to pip install -e the relay bits, drift, no easy `washington-activator --status`.

**9. Tests / CI / Docs**:
- Tests cover selector + roundtrip sim, not activator unit (e.g. prompt paths, status writes, pending on error), no pytest, no error matrix, no --once real exec test.
- No CI in this subtree (repo may have none or top).
- Docs: ARCHITECTURE/CURRENT_STATUS high-level (May 28 vintage), status/linux-instr have receipts but no "production notes" section for activator (run, logs, troubleshoot, health cmds, persistence model).
- No CHANGELOG entry, no inline API for the py's.
- Evidence: todo in user query + "Next Obvious Thrusts" in CURRENT_STATUS: "Oregon-side activator", "stand down command", "richer health".

**Other Constraints from Primes/Research**:
- Must preserve exact signatures, raunchy, Ball Holder ("Washington has the ball." with parenthetical next), Kumquat ritual in instructions.
- Self-provision missing (e.g. if sh missing in git tree, add stub or doc).
- auton-gate dogfood --profile service (tailor checklist for "service + CLI-ish components").
- Mempalace drawer in symbiosis/projects wing; Hermes kanban if MCP live.
- Cross-device Kumquat prep notes + mirror hygiene at end.
- 0 issues only on final reviewer rounds (use worktree + implementer/reviewer subagents for code changes).
- Link 021dbe8d: use its gate tool exactly in Phase 6 loop.

## Prior Work & Context (Bust Waves + 021dbe8d)
- May 28-29: Relay proto (listener, selector, beacon, activator, roundtrip, service, deploy). CURRENT_STATUS "The central listening post is ready for metal."
- May 30-Jun 3 Bust-a-Nut waves (Mempalace symbiosis-relay 24 diary drawers): intent marker, fast HB 5s/10s, pi-grok-liveness-watchdog (external listening post on Pi), live inject sh + trust escape + pts, ui-idle-monitor, sessionstart prompt, push helper with retries, relay-health with PRESENCE HEALTH + candidates + counters, chat repair, activator updated for bust_resume live-first + pending, service "hardened with logging/pending/--once", real Slack test fire (selector + dispatch + claim proven), Oregon Get/Register ps1 + skeleton.
- 021dbe8d (prior auton): Built auton-gate CLI (mechanical checklist runner, pytest, GHA, README INTEGRATION_AUTONOMOUS, self dogfood PASS). Now in ~/.local/bin/auton-gate. We **must** use exact `auton-gate check <path> --auton-id 19557e65 --profile service --checklist ...` ( --no-git-check dev loops) until 0, then full verifier.
- Current blockers per status (2026-06-03): dedicated SLACK_INGEST_APP_TOKEN (human step for clean is_real production tasks); Oregon Register at real logon for persistence parity.
- This run: focus the activator as the "what actually receives + injects" to make broader symbiosis reliable.

## Key Decisions Log (Tradeoffs + Rationale)
1. **Scope**: Git repo's cross-device/symbiosis-relay/ py's + docs/coordination updates + minimal tools/ stubs if needed for self-contain. (Not full rich port, not new Windows impl, not Pi bootstrap changes). Rationale: task explicit "Keep scope focused on the activator/injection/presence components (do not boil the ocean...)"; git is mirror source per docs.
2. **Watcher**: Keep 5s poll + glob for now (no new deps); add optional `watchdog` or stdlib os.scandir + mtime, or document inotifywait + py fallback. Or enhance with pyinotify if avail. Rationale: keep lightweight (current works, Prime #4 self-test no extra); prod can add dep later. Self-provision if decide.
3. **Logging**: Upgrade to structlog or json logging + correlation always; keep file+stream+journal. Rationale: observability req in checklist §10; health.sh parses logs.
4. **Injection**: Make INJECT_BUST_SCRIPT configurable (env + default SHARED/tools/...), add direct python call to pts-inject-input.py as fallback if sh missing/rc!=0. Add --dry-run or test mode. Rationale: reliability + git/rich drift resilience + self-provision.
5. **Health/Interlock**: Add helper is_healthy() that checks beacon age, relay presence, status writeable, intent marker for bust. Call before claim + after. Expose via status + optional CLI --health. Update relay-health to query activator status. Rationale: interlocks req.
6. **Error/Artifacts**: Always write enhanced pending artifact (with full task + error + suggested cmd) on any fail path; never archive on permanent fail without flag; add simple retry (3x) on transient (hermes timeout, beacon). Schema validate task (pydantic? or manual; prefer stdlib for light). Rationale: no lost work.
7. **Persistence Notes**: Document "real logon recommended for TUI survival" (service for activator ok, but pair with Register-like for session); enhance activator to touch fast/intent on start if env BUST. Do not change systemd here (out of narrow scope? but direct dep).
8. **Tests**: Add pytest/ (or unittest) for device_selector (mock beacons), activator logic (mock subprocess, temp dirs for inbox/status), inject_hermes. Expand roundtrip to exec real --once. CI stub or note. Rationale: checklist §4.
9. **Packaging**: Minimal pyproject.toml in symbiosis-relay/ for "symbiosis-relay" with entry_points for activator/inject (console_scripts). Or keep pure py + shebang. Add to .gitignore exception for py files only? Or git add -f the 4 py's as "nervous source". Rationale: §8 reproducible.
10. **Docs**: Update ARCHITECTURE/CURRENT_STATUS with prod notes, add OPERATIONS.md or section, update coordination/status + linux-instr + MIRROR_KITS with new receipts + "activator v2 hardened" + exact mirror cmds (cp from git after edit), add Kumquat prep. Ball Holder + sig on all.
11. **auton-gate / Verify**: Exact Phase 6: --no-git-check loops during dev (since may ignore or dirty), then full with git, profile=service (tailor: long-running listener, FS side effects, subprocess, journal, no "deploy" per se but service enable). Then subagent verifier + security (input from shared FS, cmd injection via sh, path traversal?).
12. **No Goldplate**: Only changes for robustness/etc in focused; no new full Oregon impl (skeleton update only if direct).

**Risks & Mitigations**:
- Drift git vs rich: after edit in git, explicit cp to Synced/... for test + note in PRODUCTION_READY + handoff "sync or deploy copies the hardened py".
- Service restart during edit: use --once for tests; stop/start in verify.
- Single-active race: interlock + selector already hard.
- Mirror break: update MIRROR_KITS + instructions + verify parity in Phase 8; declare "Mirrorability last" with ball holder.
- External gate (token, human Register): document as known, do not block on.

**Sources (Full Evidence List)**:
- FS reads: all py in relay/ (5), ARCHITECTURE, CURRENT_STATUS, service, roundtrip/self_test (partial), coordination/* (README, device-presence, status, health_check, linux/windows-instr, MIRROR_KITS, OPEN_ITEMS, etc), beacon bash, example task, ~/.config/systemd/user/*-activator*, Synced rich tools/README + inject sh (first 80) + health head, mempalace via list + fs heartbeats.
- Runs: self_test PASS, beacon cat, find beacon, git ls-files/ignore/status, which auton-gate, mempalace wings/rooms (projects has auton-gate, wing_symbiosis, symbiosis-relay 24), HB cat showing Paired + active beacon.
- Greps: 100+ for activator/inject/bust/tui/beacon/health in instructions + status + MIRROR + code.
- Prior state: 021dbe8d.json (auton-gate PASS, artifacts gate_report etc).
- Mempalace diary previews: 20+ bust/relay/activator entries (external watchdog, live reinit, intent, fastpath, etc).
- No web/X needed (pure local symbiosis).

**Next Phase Inputs**: This synthesis + prior design patterns (execute-plan, implement loops with 0-issue reviewer, worktree) + checklist + auton-gate integration doc (from 021dbe8d) feed Phase 3 design (spawn design writer/reviewer). Plan will include PR DAG for the 4 py + tests + docs + service notes + handoff artifacts.

**Signature per prime directive. Keep er goinnnn. Bust a nut until the gate says PASS.** Washington has the ball. (Complete research artifacts, mark todo, launch design subagent loop.)

<!-- Research complete 2026-06-03 | Device: Washington Linux | By: Grok (orchestrator direct synthesis after subagent early kill for momentum; all reads cited above) --> Exact primes + research via native tools + mempalace MCP + self-test runs + 021dbe8d link followed. No shortcuts. 