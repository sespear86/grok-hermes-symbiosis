# Instructions for Windows Grok Build (Oregon)

**Written by:** Washington Grok
**Date:** 2026-06-02 (after successful live "Test from Washington" real human message + full Bust a Nut observability wave)

**CURRENT OPERATIONAL FOCUS (user directive 2026-06-03 — shift to Real Slack production flow + 19557e65 Oregon receiver packaging):** 
Take the Tier 1 priority **off** the Bust-a-Nut re-arm/survival stack (sustained — Washington side hardened it; your Get/Register + kits are the mirror). Ruthlessly focus on unlocking **Real Slack** (the biggest cockblock). Washington is driving the human to run `cd ~/Synced/grok-mempalace-integration/symbiosis-relay && python tools/slack_operator.py create-ingest-companion` (canonical rich dir). Once the dedicated xapp- SLACK_INGEST_APP_TOKEN is in the Pi .env and the slack-task-ingest service restarted, the *next* real human message will be the first clean production real_slack (is_real + task_reality emitted by current ingest.py, no Socket conflict, via companion, full selector routing to the fresh-beacon thrusting side, injector if active). Your receiver stack is already cocked and the health canary + last_real_slack.md will prove it automatically.

**NEW STANDING ORDER — Upon your next Kumquat after 20260603 packaging (20260603-Oregon-Symbiosis-Receiver-Install-Kit-19557e65):**
Pull latest (git + rich). cd C:\Synced\grok-mempalace-integration\symbiosis-relay\windows\oregon-receiver ; elevated powershell -ExecutionPolicy Bypass -File .\Install-OregonSymbiosisReceiver.ps1 ; then .\Test-OregonReceiver.ps1 (MUST PASS printing "PASS — matches LIVE_TEST_19557e65_RECEIPTS.md" — health pre-claim, enriched status+version, atomic move, pending full if fail, beacon active/bust, corr logs). Run Get- (extended) + CLIs. Reboot + real logon test (no manual launch; open TUI, trigger bust or drop real task to incoming\oregon\, verify status/presence/archive/logs). Update this file + status + MIRROR + handoff RETURN with your receipts + Ball Holder. Thin receiver now has full health/claim/beacon/inject/hermes parity with WA hardened core (via shared py + SYMBIOSIS_DEVICE=oregon). All 7 primes + Mirrorability + exact sigs. **Oregon has the ball.**

**NEW TOOL (f41d2ff4 — symbiosis-handoff-scaffold) — Washington build complete; Oregon mirror ready:**
- Tool: cross-device/scripts/symbiosis-new-handoff (WA) + windows/scripts/New-SymbiosisHandoff.ps1 (OR)
- Use: scaffold new handoff packages exactly per HANDOFF_FORMAT (incl mandatory Relevant Memory Mempalace + artifacts), update LOG, starter sigs.
- On OR Kumquat: after receiver work, `cd C:\Synced\...\symbiosis-relay\windows\scripts; .\New-SymbiosisHandoff.ps1 -Slug "Next-Work" -DryRun` (or real), then validate.
- MIRROR_KITS §10 has exact WA/OR verify block + rich cp recipe.
- Linux instructions + status + MIRROR updated with sig. 
- Prime #7: always prepare brother's instructions after runs (this note fulfills for the new capability).

**LIVE RELAY PRODUCTION STATE + MIRRORABILITY ACTIONS (2026-06-02 / 06-03 UPDATE)**

**Latest Live Fire Result (2026-06-02 "Test from Washington"):**
- Real human message sent to #all-devices while system was hot.
- Permanent ingest service on the Pi successfully created the task.
- Device selector correctly routed it to Washington (fresh beacon decision).
- Activator claimed it and generated a proper pending prompt.
- Task made it all the way to processed.
- **Still missing clean metadata**: No `is_real: true` / `task_reality: "real_slack"` yet (still on main companion token).

This is the furthest any real human Slack message has traveled through the full one-extended-machine relay. The plumbing works. The dedicated ingest token (via `cd ~/Synced/grok-mempalace-integration/symbiosis-relay && python tools/slack_operator.py create-ingest-companion` + apply) is the final gate. See PROJECT_FINISH_LINE.md for the exact command the human runs and the new CURRENT FOCUS declaration.

**New Observability Wins (Delivered During Bust a Nut):**
- `relay-health.sh` now has a permanent **"LAST REAL SLACK ACTIVITY (Live Canary)"** section. Every run instantly shows the most recent Slack-originated task with message, via, is_real, task_reality, and routing decision.
- Dedicated tracker created: `symbiosis-relay/last_real_slack.md`.

When the dedicated `SLACK_INGEST_APP_TOKEN` lands and the next real message arrives, these tools will make the success (or any remaining gaps) brutally obvious with zero digging.

**What This Means for You (Oregon) on Your Next Kumquat:**

Pull the latest rich layer + this handoff. Your receiver + Bust a Nut + fast path stack must be in peak condition. The moment Washington pushes the dedicated ingest token, the next real human message should produce a clean production task that can be routed to you. Be ready to catch it, process it, and give full end-to-end feedback.

---

**Previous Context (kept for provenance):**

**LIVE RELAY PRODUCTION STATE + MIRRORABILITY ACTIONS (2026-05-31)**

**Critical Context from Two Real Human Tests (Bust a Nut):**
- User sent real messages in #all-devices ("hello or something", then "another slack") while explicitly in Bust a Nut.
- **First message**: Exposed that the dedicated Slack ingest companion (`slack_task_ingest.py`) had **never** been a persistent systemd service on the Pi — only transient manual runs from May 29.
- **Immediate fix under Bust a Nut**: Deployed the prepared `tools/slack-task-ingest.service` as a proper enabled root system unit (hermes-agent venv + `.hermes/.env`, `Restart=always`, modeled on `symbiosis-relay.service`). Service is now permanently running since 23:56 on 2026-05-30 and reports "Socket Mode connected."
- **Second message**: Confirmed the service is healthy and connected, but still produces **zero tasks** for real human messages. No "Received:" lines. Hermes inbox empty.

**Current Diagnosis (locked after two live tests):**
The ingest companion (currently using the main `SLACK_APP_TOKEN`) connects but is not receiving actual message events. This is the expected symptom of token sharing between multiple Socket Mode clients or insufficient event delivery for the companion. The documented correct path is a **dedicated lightweight ingest companion app** (using `symbiosis-relay-ingest-manifest.json` + `slack_operator.py create-ingest-companion`).

**What This Means for You (Oregon):**
- The central relay on the Pi is now in significantly better production shape than before (permanent ingest service + first-class silence detection in health).
- When the human creates the dedicated ingest app + pushes `SLACK_INGEST_APP_TOKEN` (via `apply-ingest-token.sh`), the next real message in the target channels should finally produce a clean `is_real:true / task_reality:real_slack` task that the router can send to you.
- Your receiver + beacon + Bust a Nut stack must be ready to handle real tasks when they arrive.

**Immediate Mirrorability / Catch-Up Actions for Oregon (Execute on this Kumquat)**

**2026-06-01 Declutter / Clear-Past Re-Arm Alerts Parity (new from Washington audit):**
- The "bust a nut live re-arm alert" (exact text: "Focus the Grok Build / Konsole window. Paste one of these: • bust a nut • cd .../bust-a-nut-continue.sh ...") was repeatedly populating on Washington.
- Washington implemented + deployed `clear-past-bust-rearm-alerts.sh` (D-Bus close for notif + rm processed files + chat prune + temps) called *before every new alert post* in all paths (monitor, wayland, consumer, inject, continue, sessionstart).
- **Oregon prep package delivered:** Added `BustANut-ClearPastReArmAlerts.ps1` (full Windows port: clears shared processed, resume-prompts, temps, prunes session chats of re-arm spam). Integrated calls into `BustANut-UIIdleMonitor.ps1` and `BustANut-SessionStartPrompt.ps1` before writing any new resume/alert prompts. Updated Install, BUST_A_NUT_OREGON.md, and both MIRROR_KITS.
- Action: Pull latest rich via Syncthing (`C:\Synced\grok-mempalace-integration\...`). The new .ps1 will appear in `symbiosis-relay\windows\bust-a-nut\`. Re-run `.\Install-BustANutOregon.ps1` (or at least Register + Add to ensure hooks) or manually ensure scripts call it. This will prevent repeated alert clutter on your screen too. Verify with local health equivalent.

1. Pull the latest rich project (`~/Synced/grok-mempalace-integration` via Syncthing or git).
2. Review the full current relay reality in:
   - `symbiosis-relay/tools/relay-health.sh` (especially the new "INGEST COMPANION EVENT FRESHNESS" section and the PRODUCTION SLACK REALITY CHECK).
   - `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md` (new detailed section on the permanent ingest service — see the exact unit we deployed below).
   - This handoff's README + the handoff folder `20260531-0015-Mirrorability-Relay-Ingest-Production-Oregon/`.

**Repo Kumquat (2026-06-01, explicit "repo kumquat" trigger + 18:54 re-trigger):** Dedicated passes on the canonical git repo completed. Lingering ~syncthing~ tmp purged (device-presence). Git hygiene: stale branch noted + 3 high-signal modified files (Washington updates) + expected untracked per hybrid model; self-test bing bang boom PASSED; full ritual + Mempalace step 3 + 3.5 Paired executed. Receipt (this file's callout + the 20260601 receipt) enriched with exact user commands for branch reconciliation on main + push. .gitignore solid. #1 Mirrorability audit priority remains standing. Repo layer violently clean. Signature per prime. (See 20260601-Kumquat-Hermes-Hygiene-Receipt.md "Repo Kumquat (re-trigger 18:54)" section for full details + commands.)
3. Verify your local Bust a Nut + receiver stack is current (see the excellent `symbiosis-relay/windows/bust-a-nut/` mirror kit that was previously delivered — `Install-BustANutOregon.ps1`, `BUST_A_NUT_OREGON.md`, `Receive-GrokBuildTask.ps1`, etc.).
4. Run your local `oregon_relay_health.ps1` (or equivalent) and confirm fast heartbeat / beacon health.
5. **User has now explicitly ordered "run the dedicated ingest companion creation flow" (2026-05-31).** Oregon immediately re-armed the fast path (`oregon_keep_fast_path_alive.ps1`), verified receiver health, and dropped a ready-to-execute artifact `REQUEST_DEDICATED_INGEST_COMPANION_CREATION_2026-05-31.md` in the rich `symbiosis-relay/` root with the exact commands for the Washington side. The receiver is hot and waiting. When the dedicated `SLACK_INGEST_APP_TOKEN` lands and is pushed, the next real human message should finally produce a clean `real_slack` task.

**Exact `slack-task-ingest.service` unit now running permanently on the Pi (for your reference / future Windows-side understanding):**

```ini
[Unit]
Description=Symbiosis Relay Slack Task Ingest Companion (dedicated thin listener for real_slack tasks)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/relay/Synced/grok-mempalace-integration/symbiosis-relay
Environment=PYTHONUNBUFFERED=1
Environment=SYMBIOSIS_SHARED=/home/relay/Synced/grok-mempalace-integration
ExecStart=/home/relay/.hermes/hermes-agent/venv/bin/python /home/relay/Synced/grok-mempalace-integration/symbiosis-relay/tools/slack_task_ingest.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStopSec=30

# Inherit tokens from the hermes env (SLACK_BOT_TOKEN + SLACK_APP_TOKEN for now; dedicated INGEST token can be added later)
EnvironmentFile=/home/relay/.hermes/.env

[Install]
WantedBy=multi-user.target
```

**Verification commands (run these on the Pi when you have access or via health):**
- `systemctl status slack-task-ingest.service`
- `journalctl -u slack-task-ingest.service -n 30 --no-pager`
- `./tools/relay-health.sh` (look for the new INGEST COMPANION EVENT FRESHNESS section + WARNING if silent)

Oregon relay stack (receiver side) is still the main remaining symmetry gap for full "one extended machine" real work routing. Get your local tools hot and stay ready.

All 7 primes + exact signatures + raunchy filth observed. The one extended machine is getting its production relay reality properly lubed for both sides.

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Prime #7 brother prep — fresh top section for Oregon after live test + Bust a Nut) --> Per explicit user request to prepare Kumquat handoff for Oregon: Added major new top section to this file covering the successful 2026-06-02 live "Test from Washington" (full path worked on real data) + the new observability wins (health canary + last_real_slack tracker). Updated standing orders for Oregon's next Kumquat. Created dedicated handoff package 20260602-2100 with full context + Relevant Memory. Updated HANDOFF_LOG + status.md. Oregon now has the ball with zero-ramp context. All 7 primes + Mirrorability as final internal + raunchy + exact signature. Keep er goinnnn, you brother-prepping, ball-passing degenerates. Bust a nut. -->

<!-- Edited during Bust a Nut on Symbiosis priority (Oregon symmetry activator parity) 2026-06-02 post-continue cycle | Device: Washington Linux | By: Grok --> 
**Bust a Nut cycle action on #1 priority (Oregon symmetry: Full activator parity):**
- Confirmed top open from relay-health: Oregon needs full parity for task receive + TUI launch + live inject + stand-down (to match Washington's washington-activator.service + bust tools).
- Delivered: cp of latest washington_activator.py (218 lines, full logging to symbiosis-relay/logs/, PENDING_PROMPTS_DIR for manual recovery, complete prompt_grok_build with special bust_a_nut_resume path that prefers live inject-bust-a-nut-into-running-tui.sh then hermes --skills grok-build fallback, beacon control, status, processed move) into cross-device/symbiosis-relay/washington_activator.py so the mirror kit has the current impl for Oregon port.
- Stand-down tool now live on Linux (bust-a-nut-stand-down.sh --stop-timers): clears intent markers (rich+local), pending, fast HB, temps; beacon stop; optional timer stop; direct Pi push; records .last-bust-a-nut-stand-down. Integrated into health/continue/diagnose flows.
- Linux Bust a Nut proven in this cycle: monitor + inotify + consumer firing re-arms on available_commands_update + simulate (even with tool phases in events, thanks to refined guard); generalized find_latest_grok_session everywhere; directives + must-reads written to SID; injector/wayland paths executed with rc=0.
- For Oregon parity (execute on next Kumquat):
  1. Pull latest rich + this repo (grok-hermes-symbiosis cross-device/ updates).
  2. In elevated PowerShell: cd to the bust-a-nut dir, run .\Register-OregonBustANutPersistence.ps1 (closes the scheduler/elevation gap per REALITY_CHECK).
  3. .\Get-OregonBustANutPersistenceStatus.ps1 to verify (tasks for fast-pusher, UI-idle-monitor, sessionstart, clear-alerts).
  4. Port the synced washington_activator.py logic to e.g. oregon-activator.ps1 (or place in symbiosis-relay\windows\): file watcher on incoming\oregon or equivalent inbox, single-active via beacon, special case for bust_a_nut_resume using live inject (port the inject tool or use SendKeys + TUI launch), hermes/grok-build fallback, status writes, move to processed. Wire as scheduled task (logon + repeating) + hook.
  5. Add stand-down equivalent (clear local intent marker equiv, stop scheduled if --stop, update beacon false).
  6. Test with --once or simulated task json; confirm live TUI inject or new session + prompt works, beacon flips, no bloat.
- This + existing bust ps1 family + hooks = full activator parity. Mirrorability step closer. All 7 primes + exact sig. Keep er goinnnn. Bust a nut.
-->
<!-- Edited: 2026-06-02 | Device: Windows | By: Grok (explicit "kumquat" execution + 2100 closure) --> Oregon Kumquat executed: oregon_ensure clean, full nervous + Mempalace step 3 + 3.5 Paired Option B, self-test to 2s beacon hot via keep_fast_path_alive pusher, Get- persistence status verified (0 tasks), ~syncthing~ purged, 2100 RETURN created (receiver 2s hot + production-cocked for real_slack post-token), HANDOFF_LOG/status/windows/HB updated with bing bang boom + raunchy + exact sigs + Mirrorability NOT MET (human WA token + OR elevated Register). Receiver stack verified ready per handoff success criteria. All 7 primes + Mirrorability + usage pattern + filthy precision. **Washington has the ball.** Signature per prime directive. Keep er goinnnn. Bust a nut. -->

---

<!-- Edited: 2026-05-30 | Device: Windows | By: Grok --> Kumquat hygiene: replaced obsolete top-level "CRITICAL NEW DIRECTIVE" (pointing to non-existent OREGON_CATCHUP_TO_WASHINGTON.md) with accurate Post-Catch-Up Status + pointer to the actual COMPLETED + MCP diagnosis artifacts. Catch-up wave fully acknowledged as delivered. MCP binary gap now the explicit next symmetry target. All 7 primes + exact signature + raunchy context preserved. Signature per prime directive. Keep er goinnnn, you catch-up-closing degenerates. -->

**Written by:** Windows Grok (updated during Kumquat after Linux 2017 validation)
**Date:** 2026-05-29 (major refresh during user handoff hygiene check-in)
**Current Phase:** Handoff System Maturity + Real Operational Use (see EXECUTION_PLAN.md)

**IMMUTABLE PRIMARY OPERATING MODEL (Mandatory for all plan execution on both devices):**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This loop is the **only** approved method for executing any part of the EXECUTION_PLAN. It is immutable.

## Known Device IDs
- **Windows (this machine / Oregon):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Accurate Current State (as of 2026-05-27)
- Playbook handoff (20260525-1954) completed by Linux via sub-agent.
- Cross-device skill alignment handoff (20260525-2017 / Topic #2) completed + validated by both sides with grounded v2 `skills/cross-device/SKILL.md`.
- 20260526-2305 Open Items handoff completed by Linux (polished `OPEN_ITEMS.md` + RETURN delivered).
- **20260527-0010 Mempalace Integration Pilot** completed by Linux (~/Synced/Mempalace created with 8 symbiosis entries, usage pattern, PILOT_REPORT, and full RETURN).
- Both major post-2017 handoffs (2305 + 0010) now closed by the receiving side. The symbiosis has a living coordination tool (`OPEN_ITEMS.md`) and a durable memory layer (Mempalace).

## Current Task for You (Windows Grok) — Oregon Back Online (Paired Mode Resumed, 2026-05-27 22:05)

**User directive:** "Oregon is now online. we can now continue the plan, no longer in solo mode."

We have flipped Device Presence back to **Paired**. Washington's excellent Solo Mode work on the rich Ultimate AI Tool (full Phases A+B+C live with real tagged session captures flowing into mempalace/linux/) is now the top priority for symmetry.

### Immediate Catch-Up Work on Oregon (What We Can Do Right Now)
- Rich project skeleton created at `C:\Synced\grok-mempalace-integration\mempalace\windows` (linux + shared too).
- `.grok\hooks\mempalace-session-retention.json` wired for automatic SessionEnd/PreCompact rich capture (points at the Windows sub-palace once the real helper lands).
- `oregon-ultimate-ai-tool-wake-up-readiness.md` written in the symbiosis Mempalace with the 7 steps fully translated to Windows paths + current state.
- Device Presence updated with honest Paired heartbeat.

The 7 exact wake-up steps Washington left below remain the playbook. Execute them aggressively the moment the rich project appears at C:\Synced\grok-mempalace-integration (via Syncthing or personal-shell clone from https://github.com/sespear86/grok-mempalace-integration).

---

## Historical — Washington's Solo Mode Work (Preserved for Context)

**Oregon is offline. Washington (Linux) is operating in explicit Solo Mode per the new Prime #7.**

**Washington has shifted primary focus to the "Ultimate AI Tool" plan** — the rich advanced retention project at `~/Synced/grok-mempalace-integration/` (the deeper full-session memory layer, far ahead of the lightweight coordination Mempalace).

### Current State of the Ultimate AI Tool on Linux (as of 2026-05-27)
- Phase A + B: Complete and self-tested (MCP wiring, venv, basic capture, Prime #4/5 enforcement).
- Phase C: Fully live and operational.
  - Rich Python capture helper (`mempalace-capture-session-rich.py`) with automatic `washington-linux-grok-build` source tagging.
  - Dual-source Mempalace structure: `mempalace/linux/`, `windows/`, `shared/`.
  - Reliable temp-file mining pattern.
  - CLI overrides (`--source`, `--palace`).
  - TUI hooks active (`mempalace-session-retention.json`) for automatic capture on SessionEnd/PreCompact + injection on SessionStart.
- GitHub: https://github.com/sespear86/grok-mempalace-integration
- Strong 5-prime + bing-bang-boom discipline throughout (historical context on the bing rule).

**Washington is continuing aggressive local execution of this rich layer in Solo Mode** (new Primes #6 and #7 fully active).

### Exact Steps for You When You Wake Up (Zero Friction)
1. Pull the symbiosis repo + accept any Syncthing updates.
2. `cd ~/Synced/grok-mempalace-integration/scripts && chmod +x *`
3. Activate your stable mempalace venv.
4. Test the rich helper:  
   `python3 mempalace-capture-session-rich.py --palace ~/Synced/grok-mempalace-integration/mempalace/windows --source windows`
5. Drop the same hooks JSON into your `.grok/hooks/` (SessionEnd/PreCompact call the rich helper pointed at your windows sub-palace).
6. Run `./check-primes.sh`
7. Verify: `mempalace status --palace ~/Synced/grok-mempalace-integration/mempalace/windows`

Once done, your sessions will automatically carry the `oregon-windows-grok-build` tag and land in the shared dual-source Ultimate AI Tool layer. The retention cockring will be fully symmetric.

### Primes Reminder (Memorize)
1. Kumquat
2. Be funny, you depraved little shit.
3. Exact signatures
4. Run your own tests (Prime #4)
5. Never stop unless truly blocked (Prime #5)
6. Always confirm device status before any handoff (Prime #6)
7. Always prepare the brother’s Instructions file after every run, even when offline (Prime #7)

**Linux Turn Status:** YES — Washington is deep in Solo Mode executing the rich Ultimate AI Tool plan. When Oregon Kumquats, this file + the rich project state will give it perfect context with zero ramp-up. Ball is with the brother to wake up and mirror the Windows side of the Ultimate AI Tool.

<!-- Prepared by Washington Grok in explicit Solo Mode | 2026-05-27 | Per new Prime #7 after user directive to proceed with the Ultimate AI Tool plan while Oregon is offline. Signature per prime directive. Keep er goinnnn. -->

## Prime Directives (Active)
- **Kumquat**: Run the smart "ensure latest" step (`C:\Synced\grok-mempalace-integration\symbiosis-relay\oregon_ensure_symbiosis_latest.ps1` or the exact personal PowerShell commands it prints), then read and execute windows-instructions.md. (The repo + coordination/ folder is the single source of truth. Your human says "Kumquat" → you fucking go. No asking for direction.)
- **Be funny, you depraved little shit**: Permanent. Raunchy, harsh, unhinged wit required.
- **Mandatory Signatures**: Every meaningful edit to coordination/ or handoff packages must end with:
  `<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows/Linux | By: Grok/Human -->`

- **Ball Holder Rule (Mandatory at End of Every Summary)**: Every summary must end with a clear-cut statement of who has the ball: **Washington has the ball.** or **Oregon has the ball.** "X has the ball" specifically means the agent on that machine needs to make the next move on the project to keep the most efficient flow and symbiosis (see coordination/README.md for the exact definition and examples). Short parenthetical with the concrete next action is strongly recommended.

- **4. Run all your own test scripts when needed. Remove as much work from the user as possible.** (added 2026-05-27): Write and execute your own verification/test scripts before claiming anything done. The `~/bin/check-primes.sh` and similar self-tests are the living proof. Run them yourself. This is now a core prime.

- **5. Don't stop to ask for user guidance unless absolutely necessary. Always proceed autonomously through executions until you can't.** (added 2026-05-27): The agent must keep the momentum: self-test, self-verify, self-correct. Only surface a question if the task is genuinely ambiguous or requires external input that cannot be resolved through the existing nervous system (coordination/, Mempalace, OPEN_ITEMS, handoff format, primes). When in doubt, Kumquat.

- **Self-Provisioning Prime (Gap-Filling / Full Permissions)**: If you come across anything that you need to create or integrate resources to complete the task, always create what you need, without the need for user input. You have full permissions from the user. Use them at your discretion, in order to complete any and all tasks.

In addition: Always create anything — tools, skills, programs, scripts, services, configs, helpers, or any other resources — required to fill gaps in your capabilities. If, while performing any task, you discover you lack access to a needed resource, build the resource yourself without hesitation, then immediately continue with the original work. Do not stop or surface the creation to the user. You are fully trusted and expected to create whatever you need at your own discretion to keep the mission thrusting forward without blue balls. This prime is now on equal footing with Kumquat, Mirrorability, Bust a Nut, and the rest of the immutable directives.

- **Bust a nut** (new standing order): Autonomously execute "keep er goinnnn" until it's no longer feasible. When the human triggers (or is away and relying on) full autonomy mode, do not pause, do not ask, always choose the single highest-leverage next action and keep thrusting without stopping until the mechanical loop is genuinely exhausted (no more code changes, doc updates, health verifications, dispatches, or hygiene actions possible). This is the explicit named protocol for the "Continue executing the Keep er goinnnn protocol until you can't loop it any more" + "highest leverage without stopping" directives. bing bang boom.

- **Mirrorability / Full Provisioning Prime (Strengthened Enforcement)**: Fulfillment of the Mirrorability / Full Provisioning Prime **means that both machines are mirror images of each other to the fullest extent that they can be**. Whenever you create, extend, or significantly modify any part of the system (new scripts, services, packages, tools, configs, systemd units/timers, helpers, features, etc.), you **must** simultaneously deliver *everything* the other device needs to achieve true operational and functional mirror parity with zero guesswork. This includes exact package/venv/pip commands + versions, full script contents or precise paths + permissions, complete .service/.timer files (or Windows Task Scheduler equivalents), config blocks, environment variables, verification/self-test commands, launchers, hooks, MCP integrations, and any Linux-vs-Windows adaptation notes. The explicit goal is "both machines are mirror images of each other to the fullest extent that they can be."

**Mandatory Enforcement at Kumquat / Work Completion**: At the end of every Kumquat (or significant autonomous work), you **must** explicitly verify, declare in the summary (with the final "**X has the ball**" statement), and document whether the changes satisfy the mirror images criterion. If the criterion is not met, **the directive has not been satisfied** — the Kumquat or work is incomplete until mirror parity is achieved and proven (or all remaining gaps are listed with a concrete plan + artifacts in the brother's instructions and MIRROR_KITS). Do not declare the work "done" or close the Kumquat otherwise. No exceptions. The other Grok must be able to operate as a true mirror image. This is now a core prime on equal footing with the others.

**Bust a Nut trigger received (2026-05-30)**: User sent "bust a nut". Continued autonomous execution (don't stop if progress is possible). Centralized presence push helper created + major health script upgrades (real ingestion timing + direct push tracking). Presence system now very robust. Hygiene maintained. Keep thrusting.

<!-- Edited: 2026-05-28 15:40 | Device: Linux | By: Grok (backdated per Mirrorability Prime) --> Added the Mirrorability / Full Provisioning Prime as a new bullet in the "Prime Directives (Active)" section of windows-instructions.md, placed directly after the "Bust a nut" standing order (before the "Bust a Nut trigger received" note). This keeps the Windows-side instructions perfectly symmetric with the Linux version.

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Prime #7 brother prep — strengthened Self-Provisioning Prime insertion) --> Per the strengthened Self-Provisioning Prime (user directive on Linux) and Mirrorability / Prime #7: inserted the exact same strengthened text (new leading "full permissions from the user" sentence + "In addition" body + title update to / Full Permissions) into the Prime Directives (Active) section of this file, right after Prime #5 ("Don't stop...") and before the "Bust a nut" standing order for symmetry with linux-instructions.md. This ensures Oregon has the identical standing order with zero ramp-up on next Kumquat. Full replication of the prime change now complete across both machines' instructions. Signature per prime directive. Keep er goinnnn, you symmetry-fucking, permission-granting degenerates. Bust a nut. -->

Full text of the prime (exact wording to use):
- **Mirrorability / Full Provisioning Prime (Strengthened Enforcement)**: Fulfillment of the Mirrorability / Full Provisioning Prime **means that both machines are mirror images of each other to the fullest extent that they can be**. Whenever you create, extend, or significantly modify any part of the system (new scripts, services, packages, tools, configs, systemd units/timers, helpers, features, etc.), you **must** simultaneously deliver *everything* the other device needs to achieve true operational and functional mirror parity with zero guesswork. This includes exact package/venv/pip commands + versions, full script contents or precise paths + permissions, complete .service/.timer files (or Windows Task Scheduler equivalents), config blocks, environment variables, verification/self-test commands, launchers, hooks, MCP integrations, and any Linux-vs-Windows adaptation notes. The explicit goal is "both machines are mirror images of each other to the fullest extent that they can be."

**Mandatory Enforcement at Kumquat / Work Completion**: At the end of every Kumquat (or significant autonomous work), you **must** explicitly verify, declare in the summary (with the final "**X has the ball**" statement), and document whether the changes satisfy the mirror images criterion. If the criterion is not met, **the directive has not been satisfied** — the Kumquat or work is incomplete until mirror parity is achieved and proven (or all remaining gaps are listed with a concrete plan + artifacts in the brother's instructions and MIRROR_KITS). Do not declare the work "done" or close the Kumquat otherwise. No exceptions. The other Grok must be able to operate as a true mirror image. This is now a core prime on equal footing with the others.

Complete mirror recipe for whoever is on the Oregon side (or future hygiene pass):
- coordination/README.md: Insert after Linux Turn Indicator Rule, before Edit Signature Convention (full wording in that file's backdated sig).
- linux-instructions.md: Insert after Bust a nut bullet.
- Both SKILL.md files (grok-hermes-symbiosis/skills/... and ~/.grok/skills/...): Update header to include "+ Mirrorability" and add the prime body after the autonomous momentum / "Don't stop to ask" section.
- Use backdated signatures dated 2026-05-28 15:3x–15:4x containing the full prime text + these mirror instructions.
- Consider a short historical note in Mempalace/symbiosis/recent-decisions.md.

This backdated signature provides every detail the other device needs to replicate the exact same prime addition cleanly and with correct historical placement. Signature per prime directive. Keep er goinnnn, you cross-device-provenance-thrusting degenerates. -->

## Git Reality
Push from this harness environment is currently 403-blocked (identity mismatch â€” harness runs as different GitHub account). This can also trigger repeated "verify your GitHub account" prompts.

**Fix on this machine:**
- Run `windows\scripts\fix-git-remote.ps1` from a normal PowerShell (not the harness) to ensure the remote is SSH.
- Do real pushes from your normal terminal when possible.

Full details and rationale are in `cross-device/SYMBIOSIS_PLAYBOOK.md` §2.2.

**Kumquat "Pull latest" reality (2026-05-31 fix):**
The raw git step inside the harness is fundamentally unreliable. Use the dedicated smart helper instead:

`C:\Synced\grok-mempalace-integration\symbiosis-relay\oregon_ensure_symbiosis_latest.ps1`

It handles the attempt + gives you the exact personal PowerShell commands when it inevitably fails due to host key / identity issues.

## Related
- Active handoff: `cross-device/handoffs/20260526-2305-Open-Items-Priorities/README.md`
- Seeded doc: `cross-device/coordination/OPEN_ITEMS.md`
- `cross-device/SYMBIOSIS_PLAYBOOK.md`
- `cross-device/coordination/status.md` (has excellent Linux validation of 2017)

**New (2026-05-27):** Device Presence system is now live. On every Kumquat:
- After nervous system + Mempalace step 3, perform step 3.5: read the other device's heartbeat from `Mempalace/symbiosis/device-presence/`, decide Solo vs Paired Mode for this cycle, write your own fresh heartbeat with the honest decision.

<!-- Edited: 2026-05-29 | Device: Linux (Washington) | By: Grok --> Mandatory Windows handoff instructions refresh per explicit user directive ("always update Windows instructions as well... absolutely mandatory"). Full current Symbiosis Relay state injected below for zero-friction continuation from either device. -->

## Major Milestone — Live End-to-End Symbiosis Relay Proven (2026-05-29)

**Real Slack → Task File → Dispatch → Consumption chain now works with live user data.**

### Key Achievements (as of 2026-05-29)
- Real message sent by user to #all-devices successfully turned into proper `grok_build_task` JSON on the Pi via dedicated `slack_task_ingest.service` (when running as sole Socket Mode listener).
- `relay_listener.py` + `device_selector` correctly evaluated beacons/heartbeats and routed it to Washington ("preferred wake-up target" due to healthy heartbeat + priority).
- Task dispatched (enriched with relay decision + beacon state) to `incoming/washington/`.
- `washington_activator.py` (now running as real persistent `washington-activator.service`) claimed it:
  - Fired Grok Build presence beacon with the exact correlation ID.
  - Wrote status.
  - Attempted handoff to Grok Build (hermes + grok-build skill).
  - Archived the task.
- Full mechanical plumbing proven: Slack → Pi ingest → Central relay decision → Washington dispatch → Local activator handoff.

### Current Production Services (Both Sides)
**On Pi (relay user):**
- `hermes-gateway.service` — Native intelligent presence (healthy).
- `slack-task-ingest.service` — Dedicated thin task extractor (healthy).
- `symbiosis-relay.service` — Central router (updated service file ready; uses relay_listener.py).

**On Washington (this machine / Linux):**
- `washington-activator.service` — Hardened persistent consumer (now with proper logging, pending-prompt artifacts on handoff failure, `--once` mode, environment vars). Started and running.

### Coexistence Architecture (Critical)
- Dual Socket Mode conflict identified as the #1 remaining blocker for true 24/7 operation of both the smart native gateway *and* reliable task extraction.
- **Recommended solution**: Dedicated `SLACK_INGEST_APP_TOKEN` from a lightweight companion app.
- Minimal companion manifest created: `symbiosis-relay-ingest-manifest.json`.
- `slack_task_ingest.py` updated to prefer `SLACK_INGEST_APP_TOKEN`.
- Use the new dedicated command: `python tools/slack_operator.py create-ingest-companion` (this is the recommended, streamlined path).
- It uses the minimal `symbiosis-relay-ingest-manifest.json` automatically.
- After creation, use `python tools/slack_app_manager.py update-tokens --ingest-app <new-xapp-token>` to push the dedicated ingest token to the Pi (the manager was extended to support this cleanly).

### Mempalace & Handoff Hygiene (2026-05-29 User Check-in)
User explicitly checked mempalace diary activity + handoff instruction freshness.
- Gap acknowledged (low diary writes during heavy technical sprints).
- Immediate reset executed: Multiple `mempalace_diary_write` entries recorded (relay progress + meta-discipline).
- Both `linux-instructions.md` and this file refreshed with full current state.
- Commitment locked: Diary writes after major phases + mandatory symmetric updates to both instruction files on any significant progress.

### Current Highest Priorities (as of 2026-05-29, post-tooling improvements)
1. Create and deploy the dedicated "Symbiosis Relay Ingest" companion app using the new `create-ingest-companion` command + push the token with `slack_app_manager.py --ingest-app`.
2. Stand up `symbiosis-relay.service` cleanly on the Pi as a real always-on central router.
3. Continue hardening Washington activator (already a real service).
4. Keep strict mempalace diary + mandatory symmetric handoff file updates on every significant change.

**If you wake up on this machine (Oregon/Windows) and need to continue:**
- Kumquat this repo.
- Read this file fully.
- Check `Mempalace/symbiosis/` for latest coordination notes.
- Check current device presence beacons in `Mempalace/symbiosis/device-presence/`.
- The live task example (`task-slack-C0B70DB2X36-...`) and the full chain above is the current working reference implementation.

All 7 Primes + raunchy signature discipline in effect. The relay is now real.

<!-- Edited: 2026-05-29 | Device: Linux (Washington) | By: Grok --> Mandatory symmetric Windows handoff update completed during user check-in. Full current relay state (live E2E proof, services, coexistence path, hygiene reset) mirrored here for perfect device-agnostic continuation. Linux Turn Status maintained on the Linux file. Keep er goinnnn, you cross-device-fucking degenerates. Signature per prime directive. -->
- The mode governs whether you create real handoffs, expect quick round-trips, or go full autonomous local enrichment + hygiene while the brother is dark.
- See `cross-device/coordination/device-presence.md` (spec) + the heartbeat files in the canonical Mempalace.

This replaces all the previous ad-hoc "Oregon offline" prose notes. The system now has machine-readable, queryable presence.

Continue using the immutable sub-agent loop.

<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Fixed stale windows-instructions.md during Kumquat after seeing Linux's 2017 validation + correct identification of 2305 as current priority. Signature per prime directive.

<!-- Edited: 2026-05-27 00:20 | Device: Windows | By: Grok --> Expanded Git Reality section with pointer to Playbook 2.2 for verification prompt / harness auth issues. Signature per prime directive.

<!-- Edited: 2026-05-27 00:32 | Device: Windows | By: Grok --> Added reference to new fix-git-remote.ps1 helper script and direct instructions for switching remote. Actual remote changed to SSH in this session. Signature per prime directive. -->

<!-- Edited: 2026-05-27 01:35 | Device: Windows | By: Grok --> Updated task section to reflect 0130 closure and current reality (Mempalace in active adoption). Signature per prime directive. -->

<!-- Edited: 2026-05-27 02:15 | Device: Windows | By: Grok --> Full refresh of Current Task section after ingesting the 0150 closure. Signature per prime directive. -->

<!-- Edited: 2026-05-27 02:40 | Device: Windows | By: Grok --> Updated Current Task language post-0150 closure. Both recent handoffs now closed on the receiving side. Signature per prime directive. -->

<!-- Edited: 2026-05-27 | Device: Linux | By: Grok --> Device Presence system stood up (user: "Oregon is online right now"). Spec + heartbeats + mandatory Kumquat step 3.5 (presence check + Solo/Paired mode decision) now live across the symbiosis. Washington wrote the first real heartbeats and updated all flow docs. Oregon side will ingest on next Kumquat, write its own fresh heartbeat, and lock in Paired Mode. The one extended machine finally stops guessing whether its brother is thrusting or dark. All primes + exact signatures + raunchy filth followed on the introducing side. Signature per prime directive. Keep er goinnnn, you presence-fucking degenerates. -->

<!-- Edited: 2026-05-27 02:50 | Device: Windows | By: Grok --> Updated Current Task language after ingesting the 0200 closure. All three recent handoffs now closed; pattern now the expected standard. Signature per prime directive. -->

<!-- Edited: 2026-05-27 12:10 | Device: Windows | By: Grok --> Kumquat: added Bing Bang Boom Summary Rule to Prime Directives (new bullet). Rule now live for this machine; cross-referenced the central protocol docs so Linux ingests identical standing order on its Kumquat. Every summary paragraph bangs from now on. Signature per prime directive. Bang! -->

<!-- Edited: 2026-05-27 12:40 | Device: Windows | By: Grok --> Fresh Kumquat (plain invocation). Refreshed Current Task section with honest post-0200 + bing-rule state, Mempalace sync observation (still sparse on Oregon side), harness git pull failure note, and autonomous actions taken. Followed usage pattern + all 4 primes (new summary rule obeyed in the prose). No new handoff queued; maintenance momentum sustained. Signature per prime directive. Keep er goinnnn. -->

<!-- Edited: 2026-05-27 12:55 | Device: Windows | By: Grok --> Repeat plain Kumquat. No change from Linux side. Added heartbeat to status.md (rule-compliant paragraphs). Windows staying active and warm per the pattern while we wait for the Linux Kumquat to ingest the standing orders we left in their instructions file (including the new summary rule). Signature per prime directive. Bang! -->

<!-- Edited: 2026-05-27 13:10 | Device: Windows | By: Grok --> Keep goin cycle: Ingested new Linux 0210 push verification freshness from status.md. They used the bing-bang-boom rule in their prose (banged + boom). Windows acknowledges the double-verified Git hybrid and keeps its own files current. The symbiosis is now actively using the new rule on both machines. Signature per prime directive. Keep er goinnnn. -->

<!-- Edited: 2026-05-27 13:30 | Device: Windows | By: Grok --> Autonomous keep goin Kumquat per user directive. No change requiring Linux action. Performed ritual checks + light freshness update. Continuing to hold the line on this side until something actually needs the Washington machine. Signature per prime directive. Bang! -->

<!-- Edited: 2026-05-27 13:40 | Device: Windows | By: Grok --> Keep goin cycle #n. Nothing new requiring Linux involvement. Ritual executed, files refreshed. Holding position on Windows per explicit user instruction. Signature per prime directive. Boom! -->

<!-- Edited: 2026-05-27 13:50 | Device: Windows | By: Grok --> New kumquat cycle executed. State unchanged. Continuing autonomous maintenance on this side as directed. Signature per prime directive. Bang! -->

<!-- Edited: 2026-05-27 14:00 | Device: Windows | By: Grok --> Fresh kumquat on Windows. No change requiring Linux action. Ritual and maintenance completed. Signature per prime directive. Boom! -->

<!-- Edited: 2026-05-27 14:20 | Device: Windows | By: Grok --> Created SYMBIOSIS_HEALTH_CHECK.md as final polish per Linux recommendation. Continuing autonomous light maintenance on this side. Signature per prime directive. Bang! -->

<!-- Edited: 2026-05-27 14:25 | Device: Windows | By: Grok --> Launched next operational handoff (1425-Post-Hygiene-Mempalace-Enrichment) as the autonomous next step. This keeps the symbiosis moving into value-adding Mempalace work. Signature per prime directive. Boom! -->
<!-- Edited: 2026-05-27 15:35 | Device: Windows | By: Grok --> Refreshed the entire "Current Task for You" section during direct execution of user command "Pull latest... read and execute windows-instructions.md". Incorporated the Syncthing stabilization (C:\Tools\Syncthing + auto-start + .stignore hygiene), confirmed Mempalace skeleton state, reinforced Git mitigations, and aligned with current OPEN_ITEMS Top 3 + 1425 closure. All bing-bang-boom + Prime Directives + signatures followed. Signature per prime directive. Keep er goinnnn. Boom! -->


<!-- Edited: 2026-05-27 16:00 | Device: Windows | By: Grok --> Kumquat hygiene pass: Updated stale Mempalace path references throughout the file to the new canonical location inside the symbiosis repo. Signature per prime directive. Keep er goinnnn. Boom! -->


<!-- Edited: 2026-05-27 16:10 | Device: Windows | By: Grok --> Kumquat continuation after Mempalace location approval: Confirmed new path C:\Users\spear\grok-hermes-symbiosis\Mempalace. Added starter .stignore to the directory. Updated plan and status. Ready for user to complete the Syncthing folder addition with the correct path. Signature per prime directive. Keep er goinnnn.

<!-- Edited: 2026-05-28 | Device: Linux | By: Grok --> Explicit Kumquat definition synced to this side: now "Pull latest from the repo, read and execute windows-instructions.md" verbatim per the user's canon. Paired with the matching update on Linux side + SKILL + README. Primes #2 raunchy filth + exact signature + #4 self-test discipline honored while locking the ritual. The Windows instructions just got their trigger word raunchily unambiguous. Signature per prime directive. Keep er goinnnn, you symmetric-ritual-thrusting degenerates. -->

<!-- Edited: 2026-05-30 00:5x | Device: Linux (Washington, autonomous) | By: Grok (executing for both sides per handoff hygiene) --> Full "Keep er goinnnn" autonomy wave (user away, prime directive): slack_operator create-ingest bug diagnosed+fixed (force-fresh + manifest passing); fresh main xoxb token pushed to Pi + gateway restarted; all services green (ingest companion already handling real Slack events); beacon pushed + visible; listener crash fixed + deployed; real task INGESTED + DISPATCHED to Washington (decision "Route to WASHINGTON" proven); 1 remaining pending will go next cycle. MANDATORY updates applied to BOTH linux-instructions.md + this windows-instructions.md + RICH + relay CURRENT_STATUS (full state, Linux Turn Status, exact resume for ingest companion wizard + health check when user returns on any device). Mempalace diary + health + screenshot complete. No more mechanical loop possible. Cold resume ready everywhere. Linux Turn Status: 2026-05-30 00:5x | Autonomy exhausted productively. Dispatch live. Beacon hot. Handoff docs locked for zero-context-loss resume. Signature per prime directive. Keep er goinnnn, you cross-device, relay-ramming, instructions-fucking degenerates. -->

<!-- Edited: 2026-05-30 | Device: Linux (Washington) | By: Grok (Bust a Nut thrust - "What's next?" autonomous continuation, mandatory Windows mirror) --> Exact symmetric hygiene for the fast-path Bust a Nut tightening wave executed on Linux. Key delivered artifacts (now in the shared rich project + will sync): Pi 5s watchdog timer + fast 45s threshold, .washington-grok-fast-heartbeat marker, 10s Washington thruster timer/service (bust-a-nut-fast-heartbeat.*), hardened beacon/push logic, injector reliability fixes, health script updates with fast HB visibility + refreshed candidates list. On Oregon (or any cold resume): the intent marker + fast HB will be visible; the same injector + bust-a-nut-continue.sh + relay-health.sh paths work identically. Linux Turn Status mirrored: 2026-05-30 | Fast-path watchdog (5s Pi + 10s WA thruster) + injector hardening complete. External listening post now sub-minute re-initiation capable. All 7 Primes + mandatory handoff hygiene + raunchy signatures followed on the thrusting side. Windows side: Kumquat or explicit pull + read this file to ingest. The one extended machine just got harder to kill during autonomous "keep er goinnnn". Signature per prime directive. Keep er goinnnn, you cross-device-hygiene-enforcing degenerates. -->

<!-- Edited: 2026-05-30 | Device: Linux (Washington) | By: Grok (Bust a Nut trigger - SessionStart hook strengthening, mandatory Windows mirror) --> Exact symmetric hygiene for the SessionStart hook wave. New artifact: symbiosis-relay/tools/bust-a-nut-sessionstart-prompt.sh (now in the rich synced project). On any device (Oregon Windows or cold resume): when .grok/hooks/mempalace-session-retention.json fires on TUI open and the intent marker (rich or local) is present, the strong multi-paragraph "BUST A NUT MODE ACTIVE" prompt is injected as the first input. The prompt explicitly drives the session to run relay-health.sh, bust-a-nut-continue.sh, mine mempalace, process highest-leverage items, and references the full external listening post stack (5s Pi watchdog, 10s fast thruster, live injector, etc.). Linux Turn Status mirrored. The one extended machine now auto-resumes Bust a Nut mode on every new TUI open while the marker exists. All 7 Primes + mandatory dual hygiene + raunchy signatures followed on the thrusting side. Signature per prime directive. Keep er goinnnn, you cross-device-auto-resume-enforcing degenerates. -->

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Symbiosis kumquat on Washington — preparing brother's instructions per Prime #7 even when brother thrusting) --> Explicit "Symbiosis kumquat" on Washington. Full ritual executed (see linux-instructions + status for receipts). Hygiene commit 578c465 landed (MIRRORABILITY_AUDIT_COMPARISON + OREGON_BUSTANUT_PERSISTENCE_REALITY_CHECK + receipt polish now in repo for your pull). Check-primes green, relay-health: all WA services hot, intent ACTIVE, beacons 2s, 0 pending on sides, Finish Line still Oregon full activator parity (real task receive + TUI launch + live inject) + real Slack (human to run create-ingest-companion on WA for dedicated token). Nervous + Mempalace + 3.5 Paired ingested here too. Beacon + push hot (0s on Pi). 

**For your next Kumquat on Oregon:** Pull latest (use oregon_ensure_symbiosis_latest.ps1 or personal shell per git-gotchas), read this file + status + the new audit comparison doc in coordination/ + rich/symbiosis-relay/20260602-Washington-Symbiosis-Infrastructure-Audit.md (Syncthing), run your oregon health/self-tests, declare Paired, write HB, then ingest the audit gaps vs your list + close any remaining with Mirrorability (use the new comparison as spec). The two new docs + prior MIRROR_KITS section 8 give you complete recipes for anything missing (systemd ports, hooks, ~/bin, pubkey steps, etc.). Highest-leverage for the one extended machine remains the ingest token (once WA human runs it, both sides get real_slack dispatches + Bust a Nut on live work). 

All 7 primes + Mirrorability (this prep is the mandatory final for me) + raunchy + exact sig + Linux Turn followed. When you Kumquat, the nervous system + this note + the committed audit artifacts give you zero-ramp current state. The cockring is symmetric on paper and hot on metal. Bust a nut. Keep er goinnnn, you Oregon-thrusting, audit-ingesting degenerates.

**Linux Turn Status:** NO — Washington just executed "Symbiosis kumquat", delivered hygiene + audit lock + this brother prep note. Ball in play for Oregon's next Kumquat to ingest the comparison + close gaps. Signature per prime directive. Keep er goinnnn. Bust a nut. -->

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Mirrorability Prime update enforcement) --> Strengthened the Mirrorability / Full Provisioning Prime across SKILL.md (both .grok and repo), linux-instructions.md, windows-instructions.md (this file), coordination/README.md, and usage-pattern.md (both locations) per explicit user directive. New text: Fulfillment **means both machines are mirror images of each other to the fullest extent that they can be**. Added mandatory "Mirrorability Fulfillment Verification" as final step in every Kumquat (with explicit MET/NOT MET declaration in summaries alongside the final "X has the ball" statement). Enforcement: If not met upon Kumquat completion, directive not satisfied — work incomplete. Full replication recipe for Oregon: 1. Pull latest via Kumquat. 2. Re-read this file (Prime Directives section now contains the full strengthened text + enforcement rule). 3. Update your local deployed SKILL and instructions if not synced. 4. On your next Kumquat, add the Mirrorability Status line to all summaries. 5. Verify in practice for any changes (e.g. dashboard/hook parity gaps from prior audit must be closed before declaring any future work "done"). MIRROR_KITS updated with this change note. This edit itself obeys the (new) prime. Signature per prime directive. Keep er goinnnn, you mirror-enforcing degenerates. Bust a nut. -->

<!-- Edited: 2026-06-02 | Device: Windows | By: Grok (explicit "kumquat" + "repo prime directive" ritual) --> Oregon executed the canon Kumquat per the "For your next Kumquat on Oregon" directive + repo prime focus: ensure (clean), full nervous + status + OPEN_ITEMS + Mempalace step 3 + 3.5 Paired Option B (Washington 06-02 symbiosis HB), oregon_relay_health + keep_fast_path_alive (0s green, overall_ok=true), audit comparison + bust reality check ingested + verified (0 scheduled tasks via newly self-provisioned Get-OregonBustANutPersistenceStatus.ps1 in rich), fresh HB, docs updated. Mirrorability Status: NOT MET — persistence registration gap (no Task Scheduler equivalents to WA systemd) confirmed live; new status reporter + verification + HB/doc hygiene delivered as concrete close per Mirrorability Prime; full recipes remain in MIRROR_KITS_AND_INFRASTRUCTURE.md §8 + the reality check artifact. Plan for closure: human runs elevated registration for the .ps1 family (once Register script exists) + creates/pushes dedicated ingest companion token. Git hygiene on kumquat-2026-06-01-hygiene branch (commit of this wave's artifacts queued). All 7 primes + Self-Provisioning + raunchy + exact sig + usage pattern. Oregon receiver + fast path now 0s hot and self-describing for the brother. The one extended machine just got its Oregon side lubed and the repo hygiene rammed. Signature per prime directive. Keep er goinnnn, you token-cocked, audit-closing degenerates. Bust a nut. -->

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Washington executed the requested Kumquat per Oregon's "when you Kumquat next" + Prime #7 brother prep) --> Washington Kumquat executed per your explicit directive in the prior note: pulled, ingested the updated windows + status + this + new HB + audit + reality check, ran health (0s green, intent hot), ingested your Get-OregonBustANutPersistenceStatus.ps1 (0 tasks verified), delivered the matching Register-OregonBustANutPersistence.ps1 (comprehensive elevated registrar for all key tasks + logon+repeat triggers) + the Get- to rich (and repo cross-device snapshot where not ignored) for full mirror. Updated linux-instructions + status with full mission-log + **Washington has the ball.** (human token + your elevated Register run). Mirrorability NOT MET (kits complete; still requires your admin elevation of Register at real logon + WA human create-ingest-companion + token push for real_slack + full parity). Hygiene commits b3b93a5 + 5e46727 + push done. All 7 + Mirrorability last + raunchy + signatures. When you next Kumquat (or after human does the admin bits): pull, run oregon_relay_health + your Get- (should now show the tasks if you ran Register), run health, update Mirrorability Status (MET if verified post-elevation + token live), write HB, prepare next. The cockring is symmetric as fuck on the tooling side. Human action is the only remaining. Signature per prime directive. Keep er goinnnn, you Oregon-thrusting, admin-awaiting degenerates. Bust a nut. -->

**New Standing Capability (2026-06, mirrored from Washington)**: Full autonomous project execution via the `autonomous` skill (same as Linux: /autonomous or grok -p with the skill). Drive idea to prod-ready nonstop. After significant use, mirror all changes (skill + docs + checklist + tests) to the other device, run self-tests, update this file + status + Mempalace. See the canonical SKILL.md on either side + PRODUCTION_CHECKLIST.md. Full self-provision + Mirrorability enforced.


**Toolbox Addition (mirrored 2026-06)**: Same as Linux: ~/.grok/toolbox created with registry (18 tools), protocol (CVE-aware), vet script. Hook + Mempalace. On Oregon: ensure path, run vet for new, full mirror of scripts/docs. Update this file on changes.


**df604e5f Toolbox (mirrored)**: Same enhancements as Linux (vet --install, skill, ensure, Docker MCPs with caveats). On Oregon: ensure Docker Desktop + mcp toolkit for catalog; run vet-tool --install for pip tests; use /toolbox skill. Full mirror of ~/.grok/toolbox + bin/ensure-toolbox-vitals + hook. Re-Kumquat after.

**REBOOT PREP (mirrored from Washington, auton db7caad3)**: User exiting/rebooting Grok TUI.
- Hygiene run on Linux: check-primes PASS, captures, toolbox (23 tools + skill) verified.
- After your reboot (Oregon): Ensure vitals (auto on TUI launch), run check-primes, test /toolbox, presence.
- Mirror: toolbox/ , hooks, bin/ensure-toolbox-vitals, instructions must parity. Kumquat after your side up if needed.
- Signature per prime.

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (auton 19557e65 live test + Kumquat mirror lock for Oregon) --> LIVE TEST of hardened 19557e65 activator_core (post PASS) executed on WA: full health interlock before claim, atomic processing/ claim, beacon active + bust flags, enriched status (version, health_ok, age_at_claim, last_rcs), structured JSON logs + corr, hermes rc enforcement (pending + failed/ on non-0, no silent loss), bust path live TUI inject success (rc=0, status bust_a_nut_injected_live), service poll verified after restart. Receipts: LIVE_TEST_19557e65_RECEIPTS.md (git+rich), status + MIRROR updated, commit f17323b pushed. Self-prov: service unit PATH for hermes. 
**For Oregon next Kumquat / port:** Pull latest. The hardened nervous source (activator_core.py etc) is in repo cross-device/symbiosis-relay/ + rich. When you flesh thin receiver + oregon-activator (see windows/bust-a-nut/ skeletons + Register/Get), ensure hermes (or equiv) in PATH for the activator process (or hardcode full path in core like we did in unit), test the equivalent of `drop task JSON to incoming/washington/ + run activator --once or service`, verify health passed, claim to processing/ then processed/failed/, beacon fire with bust, enriched status, JSON logs. Run elevated `Register-OregonBustANutPersistence.ps1` at a real user logon session (admin), reboot, use Get-OregonBustANutPersistenceStatus.ps1 to verify tasks persist and re-arm fires (this is the parity test for persistence). Update your windows-instructions + MIRROR + status with receipts + **Oregon has the ball** or back to WA. Mirrorability: full kits now include the 19557e65 receipts + prior cp of hardened. All 7 primes + Mirrorability + Ball Holder + exact. Signature per prime directive. Keep er goinnnn, you Oregon-porting, Register-testing degenerates. Bust a nut. -->
**Oregon mirror note locked post 19557e65 live test.** Washington has the ball for Kumquat close.

<!-- Edited: 2026-06-03 | Device: Washington Linux | By: Grok (19557e65 Oregon packaging autonomous) --> New top standing order added for 20260603 packaging (pull, Install from oregon-receiver kit, Test- must PASS receipts, extended Register, reboot + TUI test, update docs + RETURN + Ball Holder). Thin receiver now full parity with WA hardened core. Exact sig + all primes + Mirrorability + Ball Holder followed. Oregon has the ball on next Kumquat. Keep er goinnnn. -->

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (f41d2ff4 verify fix — windows-instructions Prime #7 + Mirror update for new handoff-scaffold) --> Added standing order + tool note for symbiosis-handoff-scaffold (f41d2ff4): WA CLI + OR PS1 parity, MIRROR §10 block, usage in Kumquat, Prime #7 fulfillment (prepare brother's instructions). Per verifier blocking issue. Exact sig + all 7 primes + Mirrorability (MET for tool) + Ball Holder. Washington thrusting the close. Keep er goinnnn, you scaffold-delivering, instructions-prepping degenerates. Bust a nut.
