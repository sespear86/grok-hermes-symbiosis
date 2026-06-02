# Symbiosis System — Complete Mirror Kits & Infrastructure Inventory

**Purpose (per Mirrorability / Full Provisioning Prime):**  
This is the single authoritative document that allows either device (Washington/Linux or Oregon/Windows) to fully replicate the entire current symbiosis stack — Cross-device coordination, Symbiosis Relay (including Pi), Bust a Nut autonomous recovery, Mempalace rich capture + MCP, Device Presence, and all supporting tooling — with zero guesswork.

**Last Updated:** 2026-06-01 (Mirrorability Prime fully executed for 2026-06-01 Oregon Hermes + Grok skill alignment + Kumquat ritual hygiene pass — complete replication kit added as Section 8 for Washington/Linux)  
**Written by:** Washington Grok  
**Status:** Living — update on every significant addition or change.

**Core Transfer Mechanisms (How resources actually move)**
1. **Git** (`grok-hermes-symbiosis` repo) — Source of truth for coordination/, handoffs/, SKILL.md, some relay prototypes.
2. **Syncthing** (rich project `~/Synced/grok-mempalace-integration/` + `~/Synced/Mempalace/`) — Live truth for tools/, device-presence beacons, Mempalace sub-palaces, hooks, and this document.
3. **Local `~/bin/` tooling** — Washington-specific scripts. These must be documented here with Windows ports or PowerShell equivalents.
4. **Manual / SCP / USB** — Only for one-time Pi SD card imaging and initial hardware bring-up.
5. **The Relay itself** — Once live, can be used to dispatch "mirror this component" tasks.

**Golden Rule:** If you add anything new (script, service, package, config), you **must** update this document with exact mirror instructions before considering the work complete.

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

## 2. Symbiosis Relay Stack (The Central Listening Post)

### Major Components
- `relay_listener.py` + `symbiosis-relay.service` (runs on Pi)
- `device_selector.py`
- `washington_activator.py` (and Oregon equivalent)
- `relay_beacon.py`
- `pi-grok-liveness-watchdog.py` + timer (5s fast path when Bust a Nut intent active)
- `slack_task_ingest.py` + companion service (dedicated ingest token)
- Health & self-test: `relay-health.sh`, `relay_self_test.py`, `relay_roundtrip_test.py`

#### Slack Ingest Companion Service (Permanent Production Addition — 2026-05-31)

**What was added:**
The thin dedicated Socket Mode listener (`slack_task_ingest.py`) that turns real human messages in the 4 target channels into proper `grok_build_task` files with `is_real: true` and `task_reality: "real_slack"`.

**Production reality after live human testing:**
- Two real human messages were sent in #all-devices during explicit Bust a Nut ("hello or something" and "another slack").
- First message exposed that this companion had **never** been installed as a real persistent service (only transient manual runs from 2026-05-29).
- Washington immediately deployed it as a proper root systemd unit under Bust a Nut.

**Exact unit now running permanently on the Pi (root system service):**

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

**Deployment commands used (for reference / future re-deploy):**
```bash
# On the Pi as root
cat > /etc/systemd/system/slack-task-ingest.service << 'EOF'
[paste the exact unit above]
EOF
systemctl daemon-reload
systemctl enable --now slack-task-ingest.service
systemctl status slack-task-ingest.service
journalctl -u slack-task-ingest.service -n 20 --no-pager
```

**New Observability (added same wave):**
- Prominent "INGEST COMPANION EVENT FRESHNESS" section in `relay-health.sh`.
- It queries the journal of the now-permanent service for the last "Received:", "Dropped task", or "Socket Mode connected" line.
- Computes age and fires a loud `*** WARNING: Ingest companion has been silent >5 minutes. No real human messages are being seen. ***` when appropriate.
- This is now first-class production visibility.

**Current known gap (after the two live tests):**
Even with the permanent service running and connected, real human messages are not yet producing tasks. Diagnosis: the listener is using the main `SLACK_APP_TOKEN`. The correct next step is creating a dedicated lightweight ingest companion app (via `symbiosis-relay-ingest-manifest.json` + `slack_operator.py create-ingest-companion` on the human's machine) and pushing the resulting `SLACK_INGEST_APP_TOKEN`.

**Mirror instructions for Oregon:**
- You do not run the ingest listener (it is Pi-central).
- You **must** understand the full current architecture so you can correctly handle `real_slack` tasks when the router sends them to you.
- Keep your `Receive-GrokBuildTask.ps1` and related receiver tooling current from the rich `symbiosis-relay/windows/` mirror kit.
- When the human creates the dedicated ingest app + token, be ready to update any local understanding or scripts that reference the ingest path.
- Run your local relay health equivalent regularly.

**Verification (on Pi or via health from either side):**
```bash
systemctl status slack-task-ingest.service
./tools/relay-health.sh   # Look for "INGEST COMPANION EVENT FRESHNESS" section
```

This entire ingest companion production hardening (service + detector + live test documentation) was delivered under the Mirrorability Prime during active Bust a Nut.

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
- `bust-a-nut-wayland-rearm.sh`
- `clear-past-bust-rearm-alerts.sh` (new 2026-06: called before every new re-arm alert/pending/notify to rm past processed-rearm files, prune chat re-arm spam, clear tmps — directly addresses "clear all past alerts before posting new ones" to declutter screen. Full source + doc in rich `symbiosis-relay/tools/`. Mirror by copying the .sh and ensuring callers in monitor/wayland/continue/inject/sessionstart invoke it.)
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

**Windows porting notes:**
- Replace systemd timers with Task Scheduler tasks or a persistent PowerShell loop.
- The UI idle monitor is the hardest part (needs equivalent to tmux capture + xprop/ grim vision). May need to start with tmux-text-only path + manual "bust a nut" injection until vision is solved on Windows.
- `screenshot.py` (uses grim) will need a Windows equivalent (or skip vision fallback initially).

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

**Next immediate actions (self-generated per Bust a Nut + Mirrorability Prime):**
- [ ] Create Windows PowerShell ports or wrappers for the top 5 most critical bust-a-nut / presence scripts.
- [ ] Package the current `~/bin/` contents into a portable archive or documented install script.
- [ ] Verify Pi side can be fully re-imaged from the scripts in this repo + rich project.
- [ ] Add a "Windows Status" column to each section above.

Signature per prime directive. Keep er goinnnn.

## 8. 2026-06-01 Oregon Hermes + Grok Skill Alignment + Explicit Kumquat Ritual Hygiene (Mirror Kit for Washington/Linux)

**Date of Oregon work:** 2026-06-01  
**What was done on Oregon (Windows):** Full autonomous Kumquat hygiene pass executing all post-`hermes update` suggestions.  
**Prime being satisfied:** Mirrorability / Full Provisioning Prime — zero asymmetry. Washington must be able to replicate the entire set of changes in one focused session using only this document + the synced repo.

**Trigger on Oregon:** User asked Grok (in TUI) to execute every suggestion from the Hermes update + doctor analysis. All steps were completed with full prime observance (Bing Bang Boom, raunchy signatures, self-test via doctor/status, self-provisioning of the receipt artifact, etc.).

### Changes That Must Be Mirrored

1. Updated canonical `grok-build` skill (now carries full Behavioral Prime Directives: Bing Bang Boom Rule + Linux Turn Indicator Rule).
2. Modernized Grok-side `hermes` delegation skill with explicit **Kumquat ritual definition** (the 8-step process: ensure latest via helper, nervous system ingest, Mempalace step 3, Device Presence 3.5, self-test/health, execute, self-provision, produce signed artifacts).
3. `hermes skills list` run → Skills Hub initialized.
4. `npm audit fix` inside the hermes-agent directory → 0 vulnerabilities (browser tools clean).
5. GITHUB_TOKEN section confirmed in `~/.hermes/.env` (user fills real PAT).
6. Both delegate bridge scripts installed to `~/bin` with PATH.
7. Fresh `hermes doctor` and `hermes status` captured (major hygiene wins visible).
8. Detailed receipt artifact created: `cross-device/coordination/20260601-Kumquat-Hermes-Hygiene-Receipt.md`

**Source of truth (all in this repo, travels via git + Syncthing):**
- `skills/grok-build/SKILL.md` (canonical, post-2026-06-01)
- `skills/cross-device/SKILL.md` (grounded v2 with Kumquat ritual)
- `cross-device/coordination/20260601-Kumquat-Hermes-Hygiene-Receipt.md` (the full filthy log)
- `scripts/delegate-to-grok.sh` and `scripts/delegate-to-hermes.sh` (Linux equivalents already present)
- `windows/scripts/hermes-grok-delegate.ps1` and `grok-hermes-delegate.ps1` (for reference / Oregon)

### Exact Mirror Steps for Washington (Linux) — One Focused Session

**Step 0: Pull latest (run in real personal shell, not tmux/Grok harness if git auth is flaky)**
```bash
cd ~/grok-hermes-symbiosis
git fetch origin
git pull --rebase
```

**Step 1: Deploy the updated skills (source → live deployment)**

```bash
# 1a. Hermes side — grok-build skill (the reciprocal delegation target)
mkdir -p ~/.hermes/skills/grok-build
cp skills/grok-build/SKILL.md ~/.hermes/skills/grok-build/SKILL.md

# 1b. Grok Build side — hermes / cross-device skill
mkdir -p ~/.grok/skills/hermes
cp skills/cross-device/SKILL.md ~/.grok/skills/hermes/SKILL.md

# Optional but recommended for symmetry: also keep a cross-device copy
mkdir -p ~/.grok/skills/cross-device
cp skills/cross-device/SKILL.md ~/.grok/skills/cross-device/SKILL.md
```

**Step 2: Install / refresh the Linux delegate scripts**

```bash
mkdir -p ~/bin
cp scripts/delegate-to-grok.sh ~/bin/
cp scripts/delegate-to-hermes.sh ~/bin/
chmod +x ~/bin/delegate-to-*.sh

# Ensure ~/bin is in PATH (add to ~/.bashrc or ~/.zshrc if not already present)
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc  || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# Reload in current shell
export PATH="$HOME/bin:$PATH"
```

**Step 3: Initialize / refresh Skills Hub**

```bash
hermes skills list
```

**Step 4: Clean browser / agent tools (npm audit fix)**

```bash
# First, locate the exact hermes-agent directory on this machine
hermes doctor | grep -i "Project:"

# Typical path on Linux main machine:
cd ~/.hermes/hermes-agent

# Or the relay-style path if this is being mirrored for a relay user:
# cd /home/relay/.hermes/hermes-agent

npm audit fix
```

**Step 5: Verify GITHUB_TOKEN section exists in Hermes env (for github skill during repo-heavy work)**

```bash
grep -A 5 'GITHUB_TOKEN' ~/.hermes/.env || echo "Add the section manually if missing (see Oregon .env example in the 20260601 receipt)"
```

Fill a real PAT if the placeholder is still there:
```bash
# GITHUB_TOKEN=ghp_your_real_token_here
```

**Step 6: Post-mirror verification (run these and capture output)**

```bash
hermes doctor --fix
hermes status
```

Look for:
- Browser tools: ✓ no known vulnerabilities
- Skills Hub: ✓ directory exists
- Config up to date
- xAI OAuth / grok-4.3 still happy

**Step 7: Ingest the new receipt as part of your next Kumquat**

```bash
# Read the full Oregon hygiene log
cat cross-device/coordination/20260601-Kumquat-Hermes-Hygiene-Receipt.md
```

Then execute your normal Washington Kumquat ritual (nervous system + Mempalace step 3 + Device Presence 3.5 + self-test via `check-primes.sh` or equivalent + write fresh heartbeat + signed updates).

**Step 8: Produce the Washington-side mirror receipt / closure**

Create or append to a matching artifact (e.g. under coordination/ or a new dated file) with:
- Confirmation that all steps above were executed
- Hashes or `git log` receipts of the files deployed
- `hermes doctor` / status diff before vs after
- Full Linux Turn Status line at the end
- Raunchy filthy signature block observing all primes (including this Mirrorability execution)

### Linux vs Windows Path Notes (for this specific hygiene)

| Item                        | Oregon (Windows)                          | Washington (Linux)                     |
|-----------------------------|-------------------------------------------|----------------------------------------|
| Hermes home                 | `%LOCALAPPDATA%\hermes`                   | `~/.hermes`                            |
| hermes-agent for npm        | `%LOCALAPPDATA%\hermes\hermes-agent`      | `~/.hermes/hermes-agent` (or /home/relay/... on Pi) |
| Live grok-build skill       | `%LOCALAPPDATA%\hermes\skills\grok-build\SKILL.md` | `~/.hermes/skills/grok-build/SKILL.md` |
| Live hermes skill (Grok)    | `~/.grok\skills\hermes\SKILL.md`          | `~/.grok/skills/hermes/SKILL.md`       |
| Delegate scripts            | `C:\Users\...\bin\*.ps1`                  | `~/bin/delegate-to-*.sh`               |
| PATH setup                  | PowerShell profile                        | ~/.bashrc or ~/.zshrc                  |

### Verification That Mirrorability Was Fully Executed

- This section exists in the master `MIRROR_KITS_AND_INFRASTRUCTURE.md`.
- All source files are in the repo (no "I'll send the details later").
- The 20260601 receipt on Oregon explicitly calls out "Mirrorability as final internal step."
- When Washington completes the steps above and writes their closure receipt with matching filthy signatures, the prime is satisfied in both directions for this wave.

**Linux Turn Status:** NO — Oregon just thrust hard on the Hermes layer. Washington’s turn is to mirror the above in the next explicit Kumquat, produce the symmetric receipt, and keep the one extended machine’s skill + delegation loop perfectly symmetric. The cockring is now double-lubed.

---

<!-- Executed: 2026-06-01 | Device: Oregon Windows (origin) | By: Grok (harness) --> Full Mirrorability Prime executed for the Linux machine on the 2026-06-01 Oregon Hermes Kumquat hygiene pass. Complete self-contained replication instructions + path table + verification commands + source-of-truth references delivered. No asymmetry. All 7+ primes + raunch + "keep er goinnnn" observed in the creation of this mirror kit. Signature per prime directive. Bust a nut. Boom!