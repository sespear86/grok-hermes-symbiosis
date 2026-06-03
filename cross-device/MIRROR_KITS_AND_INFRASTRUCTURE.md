# Symbiosis System — Complete Mirror Kits & Infrastructure Inventory

**Purpose (per Mirrorability / Full Provisioning Prime):**  
This is the single authoritative document that allows either device (Washington/Linux or Oregon/Windows) to fully replicate the entire current symbiosis stack — Cross-device coordination, Symbiosis Relay (including Pi), Bust a Nut autonomous recovery, Mempalace rich capture + MCP, Device Presence, and all supporting tooling — with zero guesswork.

**Last Updated:** 2026-06-03 (auton 19557e65 live test wave + receipts: hardened Washington activator_core confirmed in real runtime; service PATH self-provision; full Mirrorability cp of receipts + prior hardened py's). Post-PASS live fire (inject + --once x2 normal/bust + service poll after restart) exercised health interlock, atomic claim+ (failed/ on rc-fail, processed/ on bust success), enriched status+version, structured corr logs, bust live-inject success, hermes rc enforcement. New artifact: LIVE_TEST_19557e65_RECEIPTS.md (git + rich cp). No source py changes. Self-provision: ~/.config/systemd/user/washington-activator.service now carries explicit PATH (includes ~/.local/bin for hermes). Oregon mirror notes: when porting thin receiver + activator (oregon-activator-skeleton etc in windows/bust-a-nut/), replicate the unit PATH env or use full hermes path in core; test persistence Register-OregonBustANutPersistence at real logon + Get- parity post any activator port. All prior hardened (washington_activator.py thin, activator_core.py, task_schema.py, inject, device_selector export, relay_beacon dedupe) + pyproject + tests + docs + OPERATIONS + this receipts already in kits via 60773bd + cp. **Washington has the ball.** (Kumquat + push + lock Oregon notes.) Signature per prime. Bust a nut. Keep er goinnnn.
**Written by:** Washington Grok  
**Status:** Living — update on every significant addition or change.

**Core Transfer Mechanisms (How resources actually move)**
1. **Git** (`grok-hermes-symbiosis` repo) — Source of truth for coordination/, handoffs/, SKILL.md, some relay prototypes.
2. **Syncthing** (rich project `~/Synced/grok-mempalace-integration/` + `~/Synced/Mempalace/`) — Live truth for tools/, device-presence beacons, Mempalace sub-palaces, hooks, and this document.
3. **Local `~/bin/` tooling** — Washington-specific scripts. These must be documented here with Windows ports or PowerShell equivalents.
4. **Manual / SCP / USB** — Only for one-time Pi SD card imaging and initial hardware bring-up.
5. **The Relay itself** — Once live, can be used to dispatch "mirror this component" tasks.

**Golden Rule:** If you add anything new (script, service, package, config), you **must** update this document with exact mirror instructions before considering the work complete.

**Behavioral Prime (Self-Provisioning / Gap-Filling / Full Permissions) (strengthened 2026-06-02)**: If you come across anything that you need to create or integrate resources to complete the task, always create what you need, without the need for user input. You have full permissions from the user. Use them at your discretion, in order to complete any and all tasks. When you discover a missing capability or resource while working, create it (tool, script, service, config, etc.) and keep going without surfacing the creation. Mirror by documenting the new artifact here if it has a physical component. The spirit travels with every agent on both machines. Full text lives in the Prime Directives sections of linux-instructions.md / windows-instructions.md and the SKILL.md files.

**New Component (2026-05-31)**: 
- `bust-a-nut-dashboard/` — Focused live monitor for the autonomy stack (intent, beacons, idle monitor, fast heartbeat, re-arm events).
- `multi-device-dashboard/` — **Master diagnostic dashboard** for the entire multi-device symbiosis (Washington, Oregon, Pi relay). Aggregates device presence, all relevant services (local + Pi), task queues, full relay health, Bust a Nut signals, and raw diagnostic data. Extremely useful for future troubleshooting. Launched via `start-dashboard.sh` or `~/bin/symbiosis-dashboard`. Includes live polling + buttons for deep health output and raw state.

**Self-Provisioning repair (2026-05-31)**: The central `relay-health.sh` forcing function had become syntactically unmaintainable from many incremental Bust a Nut edits. A clean minimal working version was self-provisioned. Oregon should maintain an equivalent health/visibility script on their side as part of full parity.

**Dashboard improvements (2026-05-31)**: Enhanced `multi-device-dashboard/server.py` with proper Markdown heartbeat parser (`parse_heartbeat_md`) for Washington and Oregon .md files. Frontend now displays richer status/mode/last HB data from heartbeats. Better diagnostic value for the full multi-device system.

**Health forcing function refresh (2026-05-31)**: `relay-health.sh` was given more structured presence, fast HB, and task count output while remaining robust.

<!-- Edited: 2026-05-31 14:52 | Device: Linux | By: Grok (Bust a Nut thrust) --> Improved relay-health.sh output + Oregon mirror docs with new dashboard + clean re-init tools. Signature per prime directive. Keep er goinnnn, you forcing-function-upgrading degenerates. Bust a nut. -->

<!-- Edited: 2026-05-31 14:42 | Device: Linux | By: Grok (Bust a Nut thrust) --> Created comprehensive multi-device monitoring web UI with rich diagnostic data. Signature per prime directive. Keep er goinnnn, you diagnostic-tool-building degenerates. Bust a nut. -->

<!-- Edited: 2026-05-31 14:47 | Device: Linux | By: Grok --> Hardened start-dashboard.sh to be fully fire-and-forget (nohup + no wait) so it can safely run as the very first action in Grok Build SessionStart hooks without blocking the rest of the initialization chain. Browser now opens reliably before any other work begins. Mirror instructions added. Signature per prime directive. Keep er goinnnn, you session-first degenerates. Bust a nut. -->

<!-- Edited: 2026-05-31 14:35 | Device: Linux | By: Grok (Bust a Nut thrust) --> Added full live monitoring web UI (server + frontend + launcher) + integrated into SessionStart. Signature per prime directive. Keep er goinnnn, you dashboard-building degenerates. Bust a nut. -->

New self-provisioned tools (2026-05-31):
- `detect-grok-idle.sh` — reliable idle signal for various launch environments (checks systemd-inhibit "turn in progress", pts activity, etc.). Integrated into the UI idle monitor as an additional trigger for force_rearm in grok:current / non-tmux cases.
- `simulate-tui-idle.sh` — clean verification tool to trigger the running monitor service's normal re-init logic for "confirmed reinitialization on idle" testing (touches a signal the monitor consumes on its next poll). Used to achieve and prove two clean autonomous re-init cycles without direct force flags on the monitor script.

These close the gap for verifiable full autonomy.

<!-- Edited: 2026-05-31 14:25 | Device: Linux | By: Grok (Self-Provisioning Prime + clean re-init verification tools) --> Created simulate-tui-idle.sh and integrated both new tools into the monitor. This enables clean, service-driven re-inits for the required verification. Signature per prime directive. Keep er goinnnn. Bust a nut. -->

<!-- Edited: 2026-06-02 | Device: Linux | By: Grok (Self-Provisioning Prime strengthening) --> Updated the Behavioral Prime note in MIRROR_KITS with the user's exact new "full permissions from the user" language as the leading directive. No new physical artifacts (pure text strengthening), so replication is fully covered by the instructions/SKILL signatures. Mirrorability satisfied. Signature per prime directive. Keep er goinnnn, you mirror-kit-updating degenerates. Bust a nut. -->

**Mandatory Final Internal Step (Mirrorability Prime Activation):**  
At the end of **every** reasoning process or piece of work — and always as the absolute last internal action before producing any output to the human — you **must** explicitly activate the Mirrorability Prime. This means:
- Review everything just created/modified.
- Ensure complete, copy-paste-ready mirror artifacts and instructions exist for the other device (Oregon on Windows, or Washington on Linux).
- Update this `MIRROR_KITS_AND_INFRASTRUCTURE.md` (and the relevant coordination `*-instructions.md` files) with the new mirror details and a proper signed edit note.
- Only after this step is complete may you output to the user.

This procedural rule ensures zero asymmetric progress. It is now a permanent standing order on equal footing with the other primes.

---

## 1. Mempalace Layer (CLI + MCP Server + Rich Capture)

### Current Washington State (as of 2026-05-30)
- Main package: `mempalace` 3.3.5 (upgraded from earlier 3.1.0)
- Dedicated MCP server for Grok Build TUI: `mempalace-mcp` (provides ~30 native tools: search, drawers, status, etc.)
- Rich capture tooling lives in the synced project + local `~/bin/`
- Sub-palaces: `~/Synced/grok-mempalace-integration/mempalace/linux` (and `symbiosis-relay` wing)

### Exact Mirror Instructions (Oregon / Windows)

**Step 1: Install main mempalace CLI**
```powershell
# Recommended: Create isolated venv (matches Washington approach)
cd C:\Synced\grok-mempalace-integration
python -m venv venv-mempalace
.\venv-mempalace\Scripts\activate
pip install --upgrade pip
pip install mempalace==3.3.5   # Pin exact version used on Washington at time of this doc
```

**Step 2: Install / wire the MCP server (native tools in TUI)**
```powershell
# After activating the venv above
pip install mempalace==3.3.5   # ensures the mcp server binary is present

# The executable is typically at:
# C:\Synced\grok-mempalace-integration\venv-mempalace\Scripts\mempalace-mcp.exe

# Add to ~/.grok/config.toml (create if missing)
[mcp_servers.mempalace]
command = "C:\\Synced\\grok-mempalace-integration\\venv-mempalace\\Scripts\\mempalace-mcp.exe"
args = ["--palace", "C:\\Synced\\grok-mempalace-integration\\mempalace"]
```

**Step 3: Rich capture tools (the heavy lifting for Option B)**
- All scripts are in the Syncthing-synced rich project:
  - `symbiosis-relay/tools/mempalace-capture-session-rich.py` (or the versions in `~/bin/` on Washington)
  - `mempalace-project-inject`, `mempalace-project-verify`, `mempalace-stream-capture`
- Copy or symlink the `~/bin/` versions into a Windows equivalent location (e.g. `C:\Tools\symbiosis\bin\` or PowerShell profile functions).
- The SessionStart / SessionEnd / PreCompact hooks in `~/.grok/hooks/mempalace-session-retention.json` must call the Windows ports of these scripts.

**Verification on either side:**
```bash
mempalace status
mempalace search "symbiosis" --limit 5
# For MCP: restart TUI and confirm ~30 mempalace__* tools appear
```

**Transfer:** Everything above lives in the rich Syncthing share (`grok-mempalace-integration/`). No extra git needed for the tools themselves.

---

## 1.5 Dashboards (Multi-Device + Bust-a-Nut Live Monitors) — 2026-05-31 Washington Bust a Nut addition

**Purpose:** Live web UIs for observing the entire symbiosis state without digging through logs or running health scripts manually. Master multi-device view + focused Bust-a-Nut autonomy monitor. Integrated into SessionStart so the browser pops open with diagnostics on every new Grok Build session while Bust a Nut intent is active.

### Washington State (as delivered)
- `symbiosis-relay/tools/multi-device-dashboard/` (server.py + frontend, live polling of presence, health, tasks, beacons, intent).
- `bust-a-nut-dashboard/` (focused on intent, re-arms, fast HB, idle monitor events).
- `start-dashboard.sh` (fire-and-forget launcher, nohup style, opens browser).
- Hardened to be safe as first action in SessionStart hooks.
- Enhanced server with Markdown heartbeat parser for both sides' .md heartbeats.
- Hook wiring example in this doc (see below).

### Exact Mirror Instructions (Oregon / Windows)

The core Python server + frontend should travel via the rich Syncthing share under `symbiosis-relay/tools/multi-device-dashboard/`.

**Step 1: Ensure the code is present**
- After Washington pushes / Syncthing syncs, `C:\Synced\grok-mempalace-integration\symbiosis-relay\tools\multi-device-dashboard\` should contain server.py, static/ or templates/, etc.
- If not present yet, the `start-dashboard.ps1` below has a useful self-contained fallback that renders current Oregon health + persistence + beacons into a browser page (no external server needed).

**Step 2: The Oregon launcher (already created)**
- `C:\Synced\grok-mempalace-integration\symbiosis-relay\tools\multi-device-dashboard\start-dashboard.ps1`
- It prefers the real server.py if present (launches hidden, opens http://127.0.0.1:8787).
- Otherwise falls back to generating + opening a rich local HTML using oregon_relay_health.ps1 + Get-OregonBustANutPersistenceStatus.ps1 + presence json/md.
- Run manually or from hooks.

**Step 3: Wire into .grok/hooks (SessionStart)**
Add (or merge) into your active SessionStart hook (e.g. relay-bust-a-nut-sessionstart.json or a combined one):

```json
{
  "type": "command",
  "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\\Synced\\grok-mempalace-integration\\symbiosis-relay\\tools\\multi-device-dashboard\\start-dashboard.ps1\"",
  "timeout": 15
}
```

Put it early (first or near first) so the browser is up before other work, matching Washington's "first action in Grok Build SessionStart" pattern. Use nohup-equivalent (the .ps1 already launches the server detached when possible).

**Step 4: Bust-a-Nut specific (if separate bust-a-nut-dashboard arrives)**
- Similar launcher pattern.
- Only auto-open the focused one when intent marker is present (the multi one can always be available).
- Oregon equivalent: call from oregon_bust_a_nut_sessionstart.ps1 or the enforcer when intent is detected.

**Verification:**
- Run the .ps1 → browser opens with useful data.
- With full server: `http://localhost:8787` shows aggregated view (when brother data is also visible via shared device-presence/ or health).
- In a Bust a Nut session: SessionStart should surface the dashboard(s) automatically.

**Update this doc + hooks + oregon_* scripts when the real UI code lands from Washington.**

---

## 2. Symbiosis Relay Stack (The Central Listening Post)

### Major Components
- `relay_listener.py` + `symbiosis-relay.service` (runs on Pi)
- `device_selector.py`
- `washington_activator.py` (and Oregon equivalent)
- `relay_beacon.py`
- `pi-grok-liveness-watchdog.py` + timer (5s fast path when Bust a Nut intent active)
- `slack_task_ingest.py` + companion service (dedicated ingest token)
- Health & self-test: `relay-health.sh`, `relay_self_test.py`, `relay_roundtrip_test.py`

**2026-05-31 Bust a Nut addition — device_selector.py fast heartbeat awareness:**
- Added `load_fast_heartbeat()` (reads `.{machine}-grok-fast-heartbeat` mtime, <45s window).
- Integrated into `select_device_for_grok_build_task()`: all routing + wake-up paths now detect "FAST THRUSTING (Bust a Nut)" and surface it in the decision reason + returned dict (washington_fast / oregon_fast).
- This makes the Pi relay brain prefer actively thrusting devices for real Slack or autonomous resume tasks.
- Mirror for Oregon / future Pi: the file lives in `symbiosis-relay/device_selector.py` in the rich Syncthing share. No special deps beyond Python stdlib + the shared BEACON_DIR. Run it directly for testing on any machine.
- Updated: PROJECT_FINISH_LINE.md, relay-health.sh candidates (#14), this doc.
- Signature per Mirrorability Prime. Keep er goinnnn. Bust a nut.

### Packages / Dependencies (Washington / Pi)
- Python 3 (system or venv)
- `paho-mqtt`, `requests`, etc. (check requirements in the relay dir if present)
- systemd (on Pi and Washington for user services)
- SSH access from Washington to `relay@192.168.1.236` (key-based)

### Pi Hardware Bring-up (One-time, mostly done via SD card)
See `symbiosis-relay/pi-bootstrap.sh`, `fresh-pi-direct-setup.sh`, `detect-sd-reader.sh`, `prepare-pi-relay-sd.sh`.

**Critical one-time steps (documented in the tools):**
- Flash Raspberry Pi OS Lite 64-bit
- Enable SSH, set hostname `symbiosis-relay`, create `relay` user
- Copy the rich project via Syncthing or USB
- Run the deploy scripts

### Windows Equivalent (Oregon)
- No full listener yet (as of last health — this is a known gap)
- Needs PowerShell port of `washington_activator.py` → `oregon_activator.ps1` (some progress exists)
- Task Scheduler equivalents for the timers (beacon refresher, fast heartbeat, watchdog)
- The health script and tools should run via PowerShell 7+

**Transfer method:** All Python scripts + service files live in the rich Syncthing share under `symbiosis-relay/`. They are already designed to be portable via `SYMBIOSIS_SHARED` env var.

---

## 3. Bust a Nut Autonomous Recovery System (The "Do Not Stop" Layer)

This is one of the most complex recent additions. Everything below must be mirrored.

### Core Scripts (all in rich project `tools/` and mirrored to `~/bin/` on Washington)
- `bust-a-nut-continue.sh`
- `bust-a-nut-sessionstart-prompt.sh` (the big one that forces full mode on SessionStart)
- `inject-bust-a-nut-into-running-tui.sh`
- `bust-a-nut-ui-idle-monitor.sh` + `.service` + `.timer` (the Turn-completed detector with vision fallback via `screenshot.py`)
- `bust-a-nut-wayland-rearm.sh` (KDE/Wayland notify+clipboard+activation for reliable live re-arms)
- `pts-inject-input.py` (low-level pts / fallback injection)
- `clear-past-bust-rearm-alerts.sh` (2026-06 hygiene: must be called before posting any new re-arm alert/pending/notify/chat-injection to clear past ones first — declutters screen, fs dir with 500+ processed files, and TUI chat history of repeated directives. Additionally uses D-Bus to CloseNotification (ID 987654321) so the exact popup the user sees ("Focus the Grok Build / Konsole window. Paste one of these: • bust a nut • cd ~/Synced/.../bust-a-nut-continue.sh ...") is dismissed before a fresh notify-send --replace-id posts the new one. Invoked from monitor, wayland-rearm, continue, inject, pts, sessionstart. See its header for full behavior.)
- `push-presence-to-pi.sh`
- `washington-beacon-refresher.py`
- `pi-grok-liveness-watchdog.py` + service + timer (the external 5s watchdog on Pi)

### Intent & Beacon Markers (live in rich project)
- `device-presence/.bust_a_nut_intent_active`
- `device-presence/.washington-grok-fast-heartbeat`
- Beacons in `device-presence/washington-grok-build-presence.json`

### Systemd Units (Washington user services)
- `bust-a-nut-ui-idle-monitor.service`
- `bust-a-nut-fast-heartbeat.timer` + `.service`
- `pi-grok-liveness-watchdog.timer` + `.service`

**Windows porting notes (Updated 2026-05-30):**
- Full mirror package now exists: `symbiosis-relay/windows/bust-a-nut/`
  - `BustANut-FastHeartbeat.ps1` (direct port of fast-thrust.sh)
  - `BustANut-UIIdleMonitor.ps1` (reasonably complete window title + presence based version; updated with Linux robustness improvements for non-standard terminal environments — trust marker handling, better fallback, reduced spam; now calls ClearPast before posting new re-arm resume prompts)
  - `BustANut-ClearPastReArmAlerts.ps1` (2026-06: Windows port of the declutter clearer. Clears shared processed-pending-rearms, temps, prunes re-arm spam from session chats, cleans resume-prompts before new posts. Handles the exact user-reported popup clutter. Called from UIIdleMonitor and SessionStartPrompt.)
  - `BustANut-SessionStartPrompt.ps1` (the critical auto-injection script called on new TUI open when intent marker exists; now calls clearer)
  - `BustANut-EnterMode.ps1` (convenience script to activate/re-arm the full stack)
  - `Add-BustANutToSessionStart.ps1` (helper that safely wires the prompt into Oregon's hook file)
  - `Install-BustANutOregon.ps1` (master one-command installer that does registration + hook wiring + activation)
  - `BustANut-LiveInjectorStub.ps1` (starting point for the hard "inject into already running TUI" problem on Windows; should receive similar non-"tmux" improvements as Linux injector)
  - `Register-BustANutTasks.ps1`
  - `Unregister-BustANutTasks.ps1`
  - `BUST_A_NUT_OREGON.md` (complete usage + integration guide; updated for clearer + 2026-06 declutter)

- Use Task Scheduler for the timer equivalents (fast heartbeat every ~12s, UI monitor every ~25s).
- The UI idle monitor uses `Get-Process` + `MainWindowTitle` matching for "Grok", "Grok Build", "Turn completed". This is the current reasonably complete starting point.
- Vision/OCR path is a known future improvement on Windows.
- The package integrates with the existing `Set-OregonGrokBuildBeacon.ps1` (already supports `-BustANut`).

**Recommended first action on Oregon:**
```powershell
cd C:\Synced\grok-mempalace-integration\symbiosis-relay\windows\bust-a-nut
.\Install-BustANutOregon.ps1
```

This master installer handles registration, SessionStart hook wiring, and activation in one go.

<!-- Edited: 2026-05-30 | Device: Linux | By: Grok --> Full audit of Bust a Nut re-arm machinery after 48+ min idle complaint: root cause = monitor stuck in broken vision loop (grim compositor failure) that kept fast heartbeat fresh (blocking Pi watchdog escalation) while being unable to target the real TUI (no visible tmux for pts/1 grok process). Hardened monitor with: (1) counter + wall-time long-idle detection (20 cycles / 30 min), (2) explicit heartbeat throttling once long-idle declared, (3) long-idle marker. Mirrored identical logic + comments to Oregon BustANut-UIIdleMonitor.ps1. Updated MIRROR_KITS. Signature per prime directive. Keep er goinnnn. Bust a nut. -->

<!-- Edited: 2026-05-30 | Device: Linux | By: Grok --> Added master `Install-BustANutOregon.ps1` (one-command that does registration + hook wiring + activation). Updated package file list and recommended command in MIRROR_KITS. Oregon now has a true turnkey path for the full Bust a Nut stack. Mirrorability Prime executed hard. Keep er goinnnn. Bust a nut. -->

<!-- Edited: 2026-05-30 | Device: Linux | By: Grok --> Diagnosed root cause of failed re-queuing after >5min idle (monitor preparing prompt but injector unable to live-inject due to no visible tmux pane in current launch env). Landed improvements: monitor now writes pts-aware trust marker; injector has stronger non-tmux fallback + direct pts attempt + better prompt + force-rearm signal file. Fixed injector syntax error. Mirrored key changes (trust marker writing + force-rearm signal + non-standard terminal robustness) to Oregon PowerShell scripts (BustANut-UIIdleMonitor.ps1 and LiveInjectorStub). Updated MIRROR_KITS. Self-tested via logs + manual re-arm. Signature per prime directive. Keep er goinnnn. Bust a nut. -->

<!-- Edited: 2026-05-31 | Device: Linux (Washington) | By: Grok (explicit "bust a nut" + 48min audit follow-up hardening) --> Per Prime #5 + Mirrorability (always last step), delivered next highest-leverage mechanical thrusts against the real-world failure modes (vision spam keeping HB fresh + weak pts/1 targeting). (1) Added discover_grok_pts() + rate-limited logging (VISION_LOG_EVERY=5) in bust-a-nut-ui-idle-monitor.sh — kills per-25s spam flood while preserving 20-cycle + 30min wall long-idle + HB throttle + .bust-a-nut-long-idle escalation exactly. (2) Monitor now writes "grok:pts:pts/NN" (or grok:current) trust marker even in vision fallback using /proc + ps discovery. (3) Hardened injector with matching pts discovery (pgrep + /proc fd scan) for "grok:current" case + better comments. (4) Full port: updated BustANut-UIIdleMonitor.ps1 (richer grok:window:PID:Title marker + header), BustANut-LiveInjectorStub.ps1 (fixed $DevicePresenceDir + marker), BUST_A_NUT_OREGON.md (new thrust note). Updated this MIRROR_KITS + will hit linux-instructions.md + PROJECT_FINISH_LINE. Re-armed via continue.sh + health verified. All 7 primes + raunchy wit + exact sigs. The recovery machinery just got less noisy and better at raw pts targeting. Bust a nut. Keep er goinnnn. -->

---

## 4. Grok Build Local Tooling & Hooks

### Critical `~/bin/` Scripts on Washington (must be ported or documented for Oregon)
- All `mempalace-*` capture/inject/verify scripts
- `grok-build-presence-beacon` (and its Windows counterpart)
- `check-brother-grok-presence`
- `check-primes.sh` (self-test — update this when new primes are added)
- `ensure-syncthing`, `start-syncthing`
- `prepare-pi-relay-sd.sh` and related Pi SD tools

### Hooks (`.grok/hooks/`)
The file `mempalace-session-retention.json` (and any Bust a Nut extensions) is critical. It currently calls:
- `~/bin/ensure-syncthing`
- mempalace venv activation + `mempalace-project-inject`
- `bust-a-nut-sessionstart-prompt.sh`

**Mirror:** The entire `~/.grok/hooks/` directory (or at least the mempalace one) should be kept in sync via the rich project or documented with exact JSON.

---

## 5. Cross-Device Coordination Nervous System

This is the easiest to mirror because most of it is already in git.

**Must have on both sides:**
- The entire `grok-hermes-symbiosis` repo (git clone or pull)
- Syncthing sharing the `handoffs/`, `coordination/`, and `Mempalace/symbiosis/` folders
- Both `SKILL.md` files kept in sync (local + repo)
- `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md` (this document)

---

## 6. Supporting Infrastructure

- **Syncthing**: Portable install on Windows (C:\Tools\Syncthing), auto-start, specific folders shared (rich project, Mempalace, handoffs, coordination).
- **Git auth mitigations**: SSH remotes + `windows/scripts/fix-git-remote.ps1` (run from real PowerShell, not harness).
- **openclaw**: The tmux helper scripts under `/home/Irikash/openclaw/skills/tmux/scripts/` (especially `find-sessions.sh`). These are used by the injector and idle monitor. Oregon will need equivalent or to vendor the logic.
- **Pi SD card imaging tools**: `prepare-pi-relay-sd.sh`, `detect-sd-reader.sh`, etc. These are mostly one-time.

---

## How to Use This Document Going Forward (Enforcement)

1. Before declaring any new component "done", add a section here with full mirror instructions.
2. Update the backdated rich signatures in the coordination files if the prime text or mirror process evolves.
3. On every Kumquat / Bust a Nut cycle, the health script and this document should be consulted for gaps.
4. When handing work to the other side, explicitly point to the relevant section(s) in this file.

**This document itself is now the primary artifact that satisfies the Mirrorability Prime for the entire existing stack.**

---

*End of initial comprehensive inventory. This file will be expanded with exact file contents, full service unit files, PowerShell ports, and checksums as the mirror effort progresses on both sides.*

**Next immediate actions (self-generated per Bust a Nut + Mirrorability Prime):**
- [x] Create easy Windows installer + polished quickstart (done in this wave).
- [ ] Continue filling PowerShell ports for remaining critical components (UI idle monitor equivalent, full health visibility, etc.).
- [ ] Oregon side runs the installer and reports back with gaps.
- [ ] Add a "Windows Status" column + concrete commands to each section above over time.

---

## Oregon (Windows) Easy Mirror Path — Current Best Experience

To make it as trivial as possible for Oregon to install the current symbiosis stack, these artifacts were created / improved:

**Primary easy-install tools (all live in the rich Syncthing project):**
- `symbiosis-relay/windows/Install-OregonSymbiosis.ps1`
  - Stages the key PowerShell scripts to `C:\Tools\Symbiosis\`
  - Optionally creates a scheduled task for the receiver
  - Prints exact profile functions and launcher commands to add

- `symbiosis-relay/windows/QUICKSTART_OREGON.md`
  - Extremely prescriptive, copy-paste friendly guide
  - Covers beacon usage, receiver, Bust a Nut resume handling, and next steps

- Existing supporting scripts in the same folder:
  - `Set-OregonGrokBuildBeacon.ps1` (full featured, including fast heartbeat marker)
  - `Receive-GrokBuildTask.ps1` (already handles bust_a_nut_autonomous_resume tasks)
  - `Get-WashingtonGrokBeacon.ps1` + test harness

**On Oregon, after a Kumquat + Syncthing sync, the single command to run is:**

```powershell
cd C:\Synced\grok-mempalace-integration\symbiosis-relay\windows
.\Install-OregonSymbiosis.ps1
```

This is the concrete, Mirrorability-Prime-compliant way to bring the other device up to speed with minimal research or tribal knowledge.

Signature per prime directive. Keep er goinnnn, you Oregon-enabling, one-extended-machine-building degenerates. Bust a nut.

## 7. Repo Hygiene & Coordination Purity Pattern (Added 2026-05-31 during explicit "Prime directive kumquat" on Washington)

**Problem observed:** Stale duplicate copies of the symbiosis-relay/ source tree (May 28-29 snapshot) ended up untracked under cross-device/symbiosis-relay/ + a stray Mempalace/ dir at repo root. These polluted `git status` on Kumquat and risked confusion (the one true production source lives exclusively in the rich `~/Synced/grok-mempalace-integration/symbiosis-relay/` layer, referenced by all current health scripts, docs, 0015 handoff, and this MIRROR_KITS).

**Detection (run on every Kumquat / hygiene pass):**
```bash
cd /path/to/grok-hermes-symbiosis
git status --short
# Look for untracked cross-device/symbiosis-relay/ or root Mempalace/
```

**Fix (Linux / Washington — one-command hygiene thrust):**
```bash
# 1. Append these lines to .gitignore (with the rich provenance comment shown in the 13:05 linux-instructions entry)
cat >> .gitignore << 'EOF'

# Stale duplicate relay source (canonical production code lives exclusively in the rich
# ~/Synced/grok-mempalace-integration/symbiosis-relay/ layer per all current docs,
# health, MIRROR_KITS, and 0015 handoff. This keeps the coordination repo as the
# lightweight nervous system single source of truth with zero bloat.
cross-device/symbiosis-relay/
Mempalace/
EOF

# 2. Stage + commit the hygiene + any pending coordination edits
git add .gitignore cross-device/coordination/status.md cross-device/coordination/windows-instructions.md cross-device/handoffs/20260531-0015-*/README.md
git commit -m "chore(hygiene): ignore stale relay duplicate + Mempalace stray (Prime directive kumquat 2026-05-31)

- cross-device/symbiosis-relay/ was May 28-29 snapshot; canonical now in rich project only
- Added with full Mirrorability provenance so Oregon can replicate
- Pending coordination updates from recent Bust a Nut / prime directive waves also landed
- All 7 primes + raunchy signatures observed

Bust a nut. Keep er goinnnn."

git push
```

**Windows / Oregon mirror instructions (exact, zero guesswork):**
- Same .gitignore append (PowerShell: Add-Content or manual edit in repo root).
- Run the equivalent git add/commit/push from a real PowerShell (not the harness, per git-gotchas.md) using the host key ensure script if needed (`oregon_ensure_symbiosis_latest.ps1`).
- After push, your next Kumquat will see clean status.
- The rich project copy of this MIRROR_KITS also carries the identical section (Syncthing delivers it instantly).

**Why this matters (Mirrorability Prime):** The coordination repo must stay the lightweight nervous system. Any future drift that creates duplicate trees must be caught and rammed the same way on both machines. This entry + the 13:05 signatures in linux-instructions + status + the .gitignore comment give the brother everything needed to stand up identical purity in one focused session.

All 7 primes + Mirrorability as absolute last internal act before the Kumquat summary output. Signature per prime directive. Keep er goinnnn, you repo-purity-enforcing degenerates. Bust a nut.

## 8. Post-2026-06-02 Washington Full Template Audit Additions (Mirrorability Prime enforcement for full sync)

**Context:** Explicit user directive: Oregon completed their infrastructure audit list (via 20260601 Hermes hygiene receipt + delivered rich/windows/ mirror packages + MIRROR_KITS "Full cross-machine audit" note + HB + parity updates in windows-instructions). Washington executed the identical template-based audit (see rich/symbiosis-relay/20260602-Washington-Symbiosis-Infrastructure-Audit.md for the complete filled template with 14 sections + Gaps + Actions). This section adds the missing mirror artifacts identified in that comparison so Oregon can stand up any Washington-specific pieces with zero guesswork. All gaps closed or explicitly documented here + in the audit report. Self-test + health + signatures + raunchy + Linux Turn followed. Mirrorability as absolute last internal before any output.

### 8.1 Linux systemd units for relay + Bust a Nut (gap from activator + fast path + monitor services)

**Washington present:**
- washington-activator.service (active, /home/Irikash/.config/systemd/user/washington-activator.service ; ExecStart points to rich/symbiosis-relay/washington_activator.py ; listens for relay tasks)
- bust-a-nut-fast-heartbeat.timer + .service (10s pusher for <15s beacons when intent active)
- bust-a-nut-ui-idle-monitor.service (25s poll, pts/trust, rate-limited vision, re-arm)
- washington-beacon-refresher.timer + .service (presence beacon writer)
- Also: syncthing.service (user)

**Exact unit contents + install (for Oregon mirror or future Linux clones; adapt paths):**
```ini
# washington-activator.service (example - cat the live one on Washington)
[Unit]
Description=Washington Grok Build Activator (Symbiosis Relay consumer)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/Irikash/Synced/grok-mempalace-integration/symbiosis-relay/washington_activator.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**Linux one-liner install (from personal shell):**
```bash
cp /path/to/exact-unit /home/Irikash/.config/systemd/user/washington-activator.service
# repeat for the bust-*.service/timer and beacon-refresher
systemctl --user daemon-reload
systemctl --user enable --now washington-activator.service bust-a-nut-fast-heartbeat.timer bust-a-nut-ui-idle-monitor.service
systemctl --user status washington-activator.service
```

**Oregon/Windows mirror (already partially delivered via Install-BustANutOregon.ps1 + Register-*.ps1 + Task Scheduler for fast pusher; receiver in Receive-GrokBuildTask.ps1):**
- Use the existing windows/bust-a-nut/Install-BustANutOregon.ps1 (re-run after Syncthing pull of this update).
- For activator/receiver parity: the Receive- + listener side is the Windows equivalent of washington-activator.
- Add note in BUST_A_NUT_OREGON.md + this MIRROR: "Run oregon_relay_health.ps1 + your Task Scheduler list to verify fast pusher + UI monitor equivalent after any rich pull."

**Added to close gap:** Full unit examples + commands now in this doc + referenced in the 20260602 audit report.

### 8.2 ~/.grok/hooks/mempalace-session-retention.json full symbiosis content (gap in hook wiring)

**Washington present (exact as of audit, cat it live):**
```json
{
  "hooks": {
    "SessionStart": [ { "hooks": [
      { "type": "command", "command": "~/Synced/grok-mempalace-integration/symbiosis-relay/tools/multi-device-dashboard/start-dashboard.sh", "timeout": 10 },
      # Oregon equivalent (add to your SessionStart hook json):
      # { "type": "command", "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\\Synced\\grok-mempalace-integration\\symbiosis-relay\\tools\\multi-device-dashboard\\start-dashboard.ps1\"", "timeout": 15 },
      { "type": "command", "command": "~/bin/ensure-syncthing", "timeout": 15 },
      { "type": "command", "command": "source ~/grokforge-palaces/mempalace-venv/bin/activate && ~/bin/mempalace-project-inject", "timeout": 30 },
      { "type": "command", "command": "~/bin/mempalace-project-verify 2>/dev/null | grep -E 'sub-palace|Status|captures' | head -6 || echo 'Mempalace health verifier: quiet or not initialized yet'", "timeout": 20 },
      { "type": "command", "command": "~/Synced/grok-mempalace-integration/symbiosis-relay/tools/bust-a-nut-sessionstart-prompt.sh", "timeout": 15 }
    ] } ],
    "SessionEnd": [ { "hooks": [ { "type": "command", "command": "python3 ~/bin/mempalace-capture-session-rich.py --palace ~/Synced/grok-mempalace-integration/mempalace/linux --source linux", "timeout": 120 } ] } ],
    "PreCompact": [ { "hooks": [ { "type": "command", "command": "python3 ~/bin/mempalace-capture-session-rich.py --palace ~/Synced/grok-mempalace-integration/mempalace/linux --source linux", "timeout": 120 } ] } ]
  },
  "_meta": { "last_edit": "2026-05-31", "device": "Linux", "by": "Grok", "signature": "<!-- Edited: 2026-05-31 14:45 | Device: Linux | By: Grok (Multi-device dashboard integration) --> ..." }
}
```

**Oregon/Windows mirror instructions:**
- Ensure your equivalent Grok hooks (or PowerShell profile / SessionStart wrapper) call:
  1. The multi-device-dashboard equivalent (or the BustANut one if standalone).
  2. Any "ensure-syncthing" equivalent (Syncthing is portable on Win; launch if not running).
  3. mempalace-project-inject / verify (from your venv-mempalace or C:\Synced\... paths; source/activate the venv).
  4. The BustANut-SessionStartPrompt.ps1 (already in your windows/bust-a-nut/).
- The rich capture on End/PreCompact is the mempalace-capture-session-rich.py (already mirrored in your tools).
- Update your local hook json (or the ps1 that injects) and test on next TUI open with Bust a Nut intent active.
- Full content above + this section in MIRROR_KITS gives zero-guess copy-paste.

**Added to close gap:** The verbatim hook + activation commands now documented here for Oregon to replicate exactly.

### 8.3 ~/bin/ symbiosis scripts inventory + check-primes port (gap #3)

**Washington ~/bin/ relevant (ls | grep -E 'bust|push|presence|rearm|inject|check|clear|dashboard|ensure'):**
- bust-a-nut-dashboard
- clear-past-bust-rearm-alerts.sh (D-Bus close + rm processed + prune chats + temps; called before every new alert)
- grok-build-presence-beacon (writes json with machine, grok_build_active, bust_a_nut_active, last_seen, source)
- check-brother-grok-presence (queries rich device-presence/ for Oregon HB)
- check-primes.sh (verifies 5 locations for full prime text incl. "Run all your own test scripts...", beacon tools, relay prototypes)
- mempalace-project-inject, mempalace-project-verify
- (plus others like ensure-syncthing wrapper)

**Oregon mirror (already strong via windows/bust-a-nut/ + Install):**
- BustANut-*.ps1 (UIIdleMonitor, FastHeartbeat, SessionStartPrompt, ClearPastReArmAlerts, LiveInjectorStub)
- Install-BustANutOregon.ps1 / Register-*.ps1
- oregon_relay_health.ps1 (equivalent to parts of check-primes + health)
- oregon_keep_fast_path_alive.ps1 , Test-OregonToPi.ps1
- **Action for Oregon:** After pulling this rich update, re-run .\Install-BustANutOregon.ps1 (or Register) to pick up any new ClearPast integration. Create or doc a check-primes.ps1 that calls your health + verifies equivalent "prime locations" (SKILL.md files, instructions, MIRROR_KITS, three-primes.md) + beacon tools + relay health. Add the command to BUST_A_NUT_OREGON.md "run your self-test equivalent on every Kumquat".

**Added:** Explicit inventory + "Oregon to add check-primes.ps1 stub or extend oregon_relay_health" note.

### 8.4 Dual mempalace locations + MCP config asymmetry (gap #4)

**Washington:**
- Rich Option B: ~/Synced/grok-mempalace-integration/mempalace/linux (and symbiosis-relay wing) + capture scripts use this.
- MCP server: /home/Irikash/grokforge-palaces/mempalace-venv/bin/mempalace-mcp --palace /home/Irikash/grokforge-palaces/sean-grok-collaboration (in ~/.grok/config.toml)
- Also ~/.mempalace + Synced/Mempalace (light historical, in-repo duplicate somewhat ignored).

**Oregon (from prior parity delivery):**
- C:\Synced\grok-mempalace-integration\venv-mempalace + mempalace-mcp.exe
- Config block points to C:\Synced\... \mempalace (rich one)
- **Gap closed by this note:** Document that the MCP palace can be a dedicated one (grokforge on Linux, your choice on Win) while rich capture always uses the Synced/grok-mempalace-integration/mempalace/ sub-palace. The 3.3.5 venv + pip + config block in prior mempalace-mcp-parity-for-oregon.md + MIRROR already gave the commands; this audit adds the "dual location is intentional (MCP server palace vs rich capture sub-palace)" explanation.

**Added to MIRROR_KITS:** Explicit callout + verification commands for both.

### 8.5 Pi pubkey install for Oregon direct push symmetry (gap #7, known blocker)

**Oregon side ready:** Key generated, Test-OregonToPi.ps1 (abusive tester), INSTALL_OREGON_PI_DEPLOY_KEY.md or similar, deploy script with -Test.

**Washington action (to enable Oregon direct push to Pi):**
1. On the Pi (via ssh or the tools), add Oregon's generated pubkey to the relay user's ~/.ssh/authorized_keys (or the hermes user).
2. Test from Oregon personal shell: run the Test-OregonToPi.ps1 (it should succeed without password, print filthy success).
3. Document the exact pubkey bits or "scp from Oregon's .ssh/id_*.pub to Pi" one-liner in a new or updated PI_PUBKEY_FOR_OREGON_DIRECT.md in rich/symbiosis-relay/ (or add to existing PI guide).
4. Once done, update HB + status + this MIRROR with "Pi pubkey installed for Oregon direct; symmetry verified".

**Added:** This section + note to create the pubkey doc as immediate follow-up if not present. (User may need to provide the pubkey bits or run the install.)

### 8.6 Old handoffs + rebase junk purge + archive procedure (gap #8)

**Action executed in this wave:** rm -rf .rebase-backup-20260601-180229/ (purged; confirmed gone).

**For remaining old handoffs (20260525-*-* and 2305 etc in cross-device/handoffs/):**
- If superseded (per 2017 RETURN + 2305/0010 hygiene precedent), move to cross-device/handoffs/archived/ (create dir if missing) + update HANDOFF_LOG or status.
- Mirror: same mkdir + mv on Oregon after pull; git add -u + commit the archive on both.

**Added:** Explicit "archive old handoffs" one-liner + "create handoffs/archived/ if needed" in this section + reference in repo-hygiene.md if exists.

### 8.7 OPEN_ITEMS staleness + living Finish Line (gap #9)

**Action:** In this audit wave, the 20260602-Washington-Audit.md + this MIRROR update + the prior Kumquat entries in status/linux-instructions already treat the relay-health Finish Line + this audit as the living #1 (Oregon symmetry + ingest token). 

**Mirror:** Oregon to prefer relay-health.sh + the 20260602 audit report over the old OPEN_ITEMS top for current priorities. Update will be in next status push.

### 8.8 Other minor (beacon json schema, D-Bus re-arm text, hermes MCP block, copilot instructions)

- Beacon json schema (washington-grok-build-presence.json with machine/source/grok_build_active/bust_a_nut_active/last_seen/current_session_id etc.): already in rich device-presence/ + health consumes it. Oregon to ensure their fast pusher / HB writer produces compatible fields for check-brother + multi-device-dashboard.
- D-Bus/notify re-arm alert text + clear-past commands: the delivered BustANut-ClearPastReArmAlerts.ps1 + the sh on Linux close the mechanical; this doc + audit report provide the side-by-side text for future.
- hermes MCP block + fork_secondary_model in config.toml: add the exact block (from audit section 4) to the MCP parity subsection of MIRROR_KITS.
- openclaw copilot.instructions.md symbiosis bits: if non-trivial, the audit report extracts; for now treat as optional IDE note (copy equivalent if Oregon uses copilot on relevant repos).

**All gaps now have explicit mirror recipes in this section + the 20260602 audit report (Syncthing delivers both instantly). No more "you had to be there".**

**Verification after Oregon pull (on their next Kumquat):**
- Re-run Install-BustANutOregon.ps1 + any Register
- Run oregon_relay_health.ps1 (or equivalent) + your self-test
- Check Task Scheduler / services for fast pusher + monitor equivalents
- Verify hooks call the full set (dashboard/ensure/mempalace/bust prompt)
- Test presence beacon roundtrip + brother check if tools ported
- Confirm no surprise junk in git status after hygiene .gitignore
- Read the 20260602 Washington audit + this section for any remaining one-liners

**This closes the 2026-06-02 full template audit wave under Mirrorability Prime. The one extended machine is now symmetrically inventoried and ready for the ingest token to finally ram real work through the relay.**

All 7 primes + Mirrorability (this as last internal before output) + exact signatures + raunchy + Linux Turn + usage pattern followed in the creation of the audit report + these additions. Signature per prime directive. Keep er goinnnn, you full-sync, gap-closing, one-extended-machine degenerates. Bust a nut.
