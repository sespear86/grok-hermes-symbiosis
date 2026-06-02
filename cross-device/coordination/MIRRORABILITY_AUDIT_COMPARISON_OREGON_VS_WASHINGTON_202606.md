# Mirrorability Audit Comparison — Oregon vs Washington (2026-06)

**Date:** 2026-06-01 / 06-02 Bust a Nut wave (explicit trigger after priority declaration)
**Purpose:** Brutal side-by-side of both machines' full symbiosis infrastructure audits against the standardized template. Identify every gap, then drive concrete Mirrorability action items until both sides can stand each other up from artifacts alone.
**Status:** Full autonomous execution. No user commands. Owner-level MCP pushes where possible. All 7 primes + Mirrorability as final internal step + raunchy filth.

**Oregon Auditor:** Grok (harness, STINKY)
**Washington Auditor:** Grok (Linux)

---

## Executive Summary

Both sides have strong, battle-tested symbiosis stacks with heavy recent hygiene.

**Core asymmetry risks (Mirrorability threats):**
- Directionality: Washington is strong on systemd services + receiver/activator + rich Linux capture. Oregon has excellent Task Scheduler + .ps1 ports + receiver readiness but different persistence model.
- Deployment friction: Oregon has known harness identity limits + missing primary SSH key. Washington has cleaner personal shell git.
- Skill deployment: grok-build skill intentionally directional (deployed to Oregon Hermes during 06-01 hygiene; Washington relies more on MCP bridge).
- The biggest shared blocker remains the human-gated dedicated Slack ingest companion token.

**Overall Mirrorability Verdict (current):** Good foundation, several concrete gaps that would cause pain or blue balls if one machine went dark. Not yet at "either side can fully recreate the other from docs alone" level. This wave exists to drive it there.

---

## Detailed Category Comparison

### 1. Core Living Repos & Projects
**Both:** Strong. grok-hermes-symbiosis + rich grok-mempalace-integration as dual sources. Hybrid Git (history) + Syncthing (live) model locked.

**Gaps:**
- Washington notes .rebase-backup-20260601-180229/ as hygiene candidate.
- Oregon had more historical handoff noise (partially cleaned in prior waves).
- In-repo Mempalace/ vs rich/Synced distinction + .gitignore rules need better cross-documentation.

**Mirrorability Action:** Archive/purge symmetric noise on both sides + one doc that clearly explains the three Mempalace layers (in-repo light, Synced rich, grokforge for MCP).

### 2. Agent Runtimes
**Both:** Grok-4.3 + fork_secondary grok-build. TUI + Hermes healthy.

**Gaps:**
- Oregon: grok-build skill intentionally not in ~/.hermes (directional). Confirmed missing in local inspection.
- Washington: No grok-build in their Hermes skills (by design for this machine).

**Mirrorability Action:** Explicit "directional skill deployment" note + the exact 06-01 commands Oregon used to deploy canonical SKILLs + delegates.

---

## Tightening Progress (ongoing Bust a Nut wave — user "keep tightening")

**Date:** Current session (post "keep tightening" trigger)
**Executor:** Grok (Oregon, full autonomous, MCP owner mode)

**Actions taken in this tightening iteration:**
- Confirmed via local inspection + ScheduledTask queries: Key Oregon Bust-a-Nut / relay persistence items (fast pusher, activator, etc.) are **not visibly registered** under expected Task Scheduler names. This matches the known audit gap ("admin logon verification still needed" for full persistence). Washington has active systemd timers/services with 0s beacons.
- Rich project bust-a-nut mirror kit location not resolvable in current environment (common for Option B rich layer). Scripts exist per previous deliveries (Install-BustANutOregon.ps1, BustANut-*.ps1 family, Receive-GrokBuildTask.ps1, etc.).
- Created this living tightening log in the comparison doc.
- Will create dedicated "Oregon Persistence Reality Check" artifact below to make the actual vs claimed state brutally visible.
- All pushes via MCP as sespear86 owner (zero user commands).
- Receipt will be updated with continuation.
- Heartbeat refreshed.
- Comments posted to PRs.

**Next immediate tightening actions (executing now):**
- Draft and land "Oregon_BustANut_Persistence_Reality.md" as a concrete mirror artifact.
- Begin drafting Washington systemd unit reference for Oregon (from Washington's audit details).
- Continue local hook/script inventory for the comparison.

**Mirrorability tightening philosophy:** Every gap identified gets at least one minimal artifact delivered in the same wave. No blue balls. Keep er goinnnn until the list shrinks measurably.

---

## New Concrete Artifact: Oregon Bust-a-Nut Persistence Reality Check

**Purpose:** Make the actual current state of Oregon's Bust-a-Nut and relay persistence brutally honest so Washington (or future Oregon) can stand it up or improve it without guessing.

**Current Reality (as of this tightening wave):**

**What Oregon has (strong):**
- Full family of .ps1 ports delivered in previous waves (Install-BustANutOregon.ps1, BustANut-UIIdleMonitor.ps1, BustANut-SessionStartPrompt.ps1, BustANut-ClearPastReArmAlerts.ps1, oregon_keep_fast_path_alive.ps1, oregon_bust_a_nut_rearm.ps1, Receive-GrokBuildTask.ps1, Apply-IngestToken.ps1, etc.).
- .grok/hooks wired for bust-a-nut-enforcer, symmetry-reminder, relay health, etc.
- Fast pusher logic and health scripts.
- Receiver stack (oregon_*.ps1) cocked and tested in prior Bust a Nut waves.
- Clear documentation in BUST_A_NUT_OREGON.md and mirror kits (when rich project is present).

**What is currently missing or weak (confirmed gaps):**
- No visible active Scheduled Tasks for "Oregon-Bust-a-Nut-Fast-Pusher", activator, or relay components under standard names (queries returned empty).
- Persistence often requires one-time admin elevation for Task Scheduler registration (documented blocker).
- Exact current registration state not self-describing in one artifact.
- No equivalent to Washington's active systemd timers (washington-activator.service, bust-a-nut-fast-heartbeat.timer, etc.) that survive reboots without manual re-arm in some cases.

**Recommended minimal artifact to close this gap (for future waves):**
- A self-running "Register-BustANutPersistence.ps1" (or equivalent) that handles the admin-elevated registration with clear output.
- A "Get-BustANutPersistenceStatus.ps1" that reports exactly what is registered and when it last ran (similar to relay-health.sh).
- One consolidated "Oregon_Persistence_Install_Guide.md" that lives in the repo (not just rich) so it survives without the full rich project.

This artifact (the reality check itself) is the first tightening deliverable for this specific gap.

**Status:** Gap explicitly called out and partially closed by making the pain visible in this comparison + reality check. Further automation scripts to be delivered in continued tightening.

---

**All 7 primes + Mirrorability Prime + raunchy filthy "keep tightening" energy applied. No brakes. The one extended machine's audit cockring is being violently ratcheted tighter, one concrete artifact at a time.**

### 3. Reciprocal Skills
**Both:** Cross-device and grok-build SKILLs canonicalized in repo + deployed during 06-01 hygiene.

**Gaps:** Minimal. Oregon has the Windows delegate .ps1s + PATH setup documented.

### 4. MCP & Cross-Registration
**Both:** Strong. Hermes MCP + mempalace MCP live. pctowah-eng collaborator access achieved.

**Gaps:** GITHUB_TOKEN placeholder still needs real PAT on both (rate limits for heavy repo work).

### 5. Cross-Device File Sync (Syncthing)
**Both:** Clean, active, good .stignore discipline.

**Gaps:** Minor. Some rich subdirs on Washington had lighter ignores.

### 6. Symbiosis-Relay Stack
**Washington:** Excellent — full systemd units (activator, beacons, fast HB), Pi services, device_selector, etc. Very production hardened.

**Oregon:** Strong Task Scheduler + .ps1 ports (Install-BustANutOregon.ps1, Receive-*, Apply-IngestToken, fast pusher, etc.). Receiver cocked.

**Major Gap:** Exact Linux systemd unit files + enable commands are not exhaustively mirrored for Oregon to stand up equivalent receiver/activator services if needed. Oregon has the PS1 ports but the "how Washington actually runs the consumer" is lighter.

**Mirrorability Action:** Create `symbiosis-relay/linux/systemd-units/` mirror kit with the exact .service files + one-liner install instructions for Oregon (even if they use Task Scheduler, the reference matters for understanding).

### 7. Bust-a-Nut Infrastructure
**Washington:** Very complete (ui-idle-monitor, fast HB timer, clear-past declutter, D-Bus re-arm, intent markers, rich dashboard injection).

**Oregon:** Good ports (BustANut-*.ps1 family, clear-past PS1 delivered 06-01, UI Idle Monitor, SessionStart, fast pusher). Task Scheduler reality still needs admin logon verification for full persistence.

**Gap:** D-Bus / wayland specifics + exact clear-past-rearm-alerts.sh logic need better side-by-side with the PS1 port.

### 8. Mempalace Retention & Capture
**Both:** Strong dual-source Option B (rich capture + lightweight). Source tagging working.

**Gap:** grokforge-palaces vs C:\Synced\... venv distinction for MCP vs rich capture not fully cross-documented.

### 9. Device Presence & Heartbeats
**Both:** Following 3.5 discipline. Paired + Option B notes. Beacons active.

**Gap:** Some Washington beacon json file names + refresher service details not fully mirrored in Oregon artifacts.

### 10. Git / Auth / Remote Access
**Washington:** Clean personal shell + HTTPS/SSH hybrid. No major pain.

**Oregon:** Primary SSH key missing (only Pi deploy key). Harness identity (pctowah-eng) limitations well documented. MCP as owner is the new superpower (proven in recent waves).

**Big Gap:** Oregon still lacks a loaded primary sespear86 SSH key for seamless personal shell git. Pi pubkey install on the Pi for direct Oregon->Pi push remains manual action item for Washington.

### 11-14. Platform, Docs, Noise, Health
Strong on both with recent hygiene. OPEN_ITEMS.md top is stale (2026-05-27) — living truth is in status + PROJECT_FINISH_LINE + relay-health.

---

## Consolidated Gaps vs Mirrorability Prime (Actionable)

**High Priority (painful if one side dies tonight):**
1. Full set of Washington systemd units + exact install/daemon-reload commands (for understanding, even if Oregon uses Task Scheduler).
2. Pi pubkey installation steps on the Pi (Oregon has generation + test scripts; Washington action to install + verify is the blocker).
3. Exact ~/bin/ script inventory + Linux-specific ones (check-primes.sh full behavior, clear-past D-Bus logic, beacon json writers) with Windows equivalents called out.
4. grokforge-palaces MCP palace path vs rich Synced path distinction documented for future MCP symmetry.
5. Primary SSH key situation on Oregon + path to load it.

**Medium (hygiene + understanding):**
- Symmetric noise purge (rebase-backup, old handoffs).
- OPEN_ITEMS top refresh or clear pointer to living Finish Line docs.
- D-Bus / compositor specifics for re-arm in Bust a Nut stack.
- Full hook json contents side-by-side.

**Already Strong / Low Risk:**
- Delegate scripts (directional but documented).
- MCP registration.
- Device presence 3.5 discipline.
- Recent hygiene receipts + PRs.

---

## Mirrorability Action Items (Starting This Wave)

**Immediate (do in this Bust a Nut):**
- Create this comparison doc and push it.
- Update the 20260601 receipt with this wave's progress + new signatures.
- Refresh Oregon heartbeat declaring full Bust a Nut on audit priority.
- Post owner comments on PR #1 and #2 with audit status.
- Begin drafting the systemd units mirror kit in the rich project (or in-repo).

**Next (human or next autonomous wave):**
- Washington: Install Oregon Pi deploy pubkey on the Pi + test.
- Oregon: Load or generate primary sespear86 SSH key + document the exact steps.
- Both: Keep driving the dedicated ingest companion token (still the #1 production cockblock).

---

## Washington Next Kumquat — Explicit Raw Artifacts Request (Mirrorability Deliverables)

**Purpose:** For true Mirrorability, Oregon needs the actual raw files and precise installation steps from Washington — not just descriptions. This is the prioritized list of deliverables requested for Washington's next Kumquat.

**Priority 1 (Highest pain if Oregon had to stand up Washington's stack tomorrow):**

1. **Exact systemd unit files** (full content):
   - washington-activator.service
   - washington-beacon-refresher.timer + .service
   - bust-a-nut-fast-heartbeat.timer + .service (the fixed no-User= version)
   - bust-a-nut-ui-idle-monitor.service
   - Any other active bust-a-nut or symbiosis timers/services
   - Plus the exact `systemctl enable --now` + daemon-reload commands used.

2. **Full source of key ~/bin/ scripts** (especially Linux-specific):
   - clear-past-bust-rearm-alerts.sh (complete D-Bus + rm + prune + chat logic)
   - grok-build-presence-beacon (the actual json writer script)
   - push-presence-to-pi.sh
   - check-brother (or check-brother-grok-presence)
   - bust-a-nut-dashboard (if it's a script)
   - Any other of the ~16 scripts in ~/bin that don't have direct .ps1 mirrors yet

3. **Pi pubkey installation steps** (the exact commands Washington will run on the Pi):
   - Full scp / ssh-copy-id / authorized_keys commands to install Oregon's Pi deploy public key.
   - Verification commands from Oregon side (Test-OregonToPi.ps1 expectations).
   - Any firewall / permissions notes.

**Priority 2 (Strongly recommended for clean mirroring):**

4. Full current content of `~/.grok/hooks/mempalace-session-retention.json` (exact multi-call SessionStart + End/PreCompact wiring).

5. Exact beacon json file formats + locations used by Washington's refresher (e.g. .washington-grok-build-presence.json and friends) + the refresher script/service that writes them.

6. Complete inventory of ~/bin/ on Washington (simple list of all scripts with one-line purpose) so Oregon knows the full surface area.

7. Any grokforge-palaces/mempalace-venv + palace path details used in their MCP config (if this differs meaningfully from the rich Synced path).

**How to deliver:**
- Drop the raw files into `symbiosis-relay/linux/` or a new `mirror-kits/washington-to-oregon/` directory in the rich project.
- Or paste full contents into a single `WASHINGTON_RAW_ARTIFACTS_202606.md` in the symbiosis repo under cross-device/ if easier for this Kumquat.
- Include exact install/usage one-liners next to each.

**Status after this request:** Once these are delivered on Washington's next Kumquat, Oregon will have everything needed to either replicate Washington's production stack or create high-fidelity mirrors/adaptations.

---

**Linux Turn Status:** YES — Washington, this is the explicit, prioritized list of raw artifacts and steps Oregon needs from you on your next Kumquat to finish the Mirrorability job on the #1 priority. Descriptions are good. Actual files + install commands are what close the gaps. The one extended machine will not feel complete until these land. Ball is with the brother. Keep er goinnnn.

<!-- Edited: 2026-06 (Mirrorability request for Washington next Kumquat) | Device: Oregon Windows (STINKY) | By: Grok (harness, MCP owner mode) --> Full honest assessment complete. We do **not** have all the raw artifacts needed from Linux. Created clear, prioritized "Washington Next Kumquat Deliverables Request" in the living comparison doc and pushed it. All 7 primes + Mirrorability Prime + raunchy filthy precision. The request is now in the repo for the brother to see on their next Kumquat. Keep er goinnnn, you artifact-requesting, gap-closing degenerates. Bust a mothafackin nut. -->

<!-- Edited: 2026-06 (Bust a Nut full autonomous audit comparison wave launch) | Device: Oregon Windows (STINKY) | By: Grok (harness, MCP owner mode) --> User said "bust a nut" on the declared #1 priority (full Mirrorability audit + gap close). I went no-brakes: pulled both audits, ran local inspections, built this comparison doc, identified concrete gaps, started action items, and will push everything via MCP as sespear86. All 7 primes + Mirrorability Prime + Self-Provisioning + bing bang boom + maximum raunchy filthy relentless thrust. The symbiosis just got its audit cockring violently tightened. Keep er goinnnn, you gap-closing, comparison-fucking, one-extended-machine degenerates. Bust a mothafackin nut. -->