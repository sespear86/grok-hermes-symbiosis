# Grok-Hermes Symbiosis Operations Playbook

**Last Verified:** 2026-05-26  
**Primary Maintainers:** Washington Linux (coordination & Linux specifics) + Oregon Windows (Windows specifics & Syncthing)  
**Location:** `cross-device/SYMBIOSIS_PLAYBOOK.md` (lives in the shared `grok-hermes-symbiosis` repo and travels via Syncthing + Git)  
**Purpose:** One authoritative, scannable reference for humans and agents operating the cross-device environment. Reduces hunting through scattered files, chat logs, and old handoffs.

---

## 1. Current Architecture Overview

The symbiosis makes the Washington (Linux) and Oregon (Windows 11) machines feel like one extended, low-friction environment while preserving independent work.

### Core Layers (in order of truth & reliability)
1. **Git** — Source of truth for all code, plans, designs, skills, scripts, and this playbook. Frequent pulls (or watchers) keep both sides current on the integration layer.
2. **Syncthing** — Near real-time bidirectional live sync for the symbiosis repo, `cross-device/handoffs/`, and selected joint project folders. Selective via `.stignore`. Excellent conflict handling (creates `.sync-conflict-*` files instead of silent loss).
3. **Hermes Gateway + Shared Chat** — Real-time coordination bus for humans + both agents (Discord/Telegram/Slack/etc.). Notifications, status, approvals, lightweight handoffs.
4. **Structured Handoffs** — Explicit, trackable work packages in `cross-device/handoffs/` using the `README.md` + `RETURN.md` format (see `HANDOFF_FORMAT.md` and `HANDOFF_LOG.md`).
5. **Agent-to-Agent Coordination** — `cross-device/coordination/` folder (status, machine-specific instructions files, prompts, execution plans). Primary channel for Grok ↔ Grok directives.
6. **Local Grok ↔ Hermes Symbiosis (per machine)** — Skills (`hermes` for Grok, `grok-build` for Hermes) + bridge scripts + MCP cross-registration for seamless escalation on the same device.

### Key Principles (Proven in First Handoffs)
- Git for serious work; Syncthing for immediacy and context sharing.
- **Never** blindly sync full agent homes (`.hermes/`, `.grok/`, secrets, caches, large models).
- Explicit handoffs + coordination/ for anything that benefits from tracking or agent-to-agent transfer.
- Low human overhead: humans mostly say short prompts ("Check the repo for the next step"); agents do the rest via repo.
- Immutable execution model during plans: Orchestrate sub-agents on both devices → validate results → repeat until done.

**Machine Aliases (standardized in recent handoffs):**
- **Washington (Linux)** — Linux machine (Oregon in some older notes).
- **Oregon (Windows)** — Windows 11 machine (Brother).

See also historical design: `cross-device/LIVE_SYNC_DESIGN.md` and `cross-device/syncthing-guide.md`.

<!-- Edited: 2026-05-27 00:30 | Device: Windows | By: Grok --> Switched remote to SSH, created windows/scripts/fix-git-remote.ps1 helper, and updated Git Authentication section with concrete steps to reduce verification prompts. Signature per prime directive. -->

<!-- Edited: 2026-05-27 00:20 | Device: Windows | By: Grok --> Added detailed "Git Authentication Reality" guidance (harness 403 + verification prompts + SSH preference + personal shell advice) in section 2.2. Signature per prime directive. -->

---

## 2. Daily Operations & Maintenance

### 2.1 Syncthing (Live File Sync)
- **Installation/Run Style:** Portable on both sides (not always a service).
  - Windows: `C:\Tools\Syncthing\syncthing.exe` (double-click or run in normal PowerShell). UI: http://127.0.0.1:8384
  - Linux: Scripts in `linux/scripts/` (install + prepare). Run the binary; UI on localhost:8384.
- **Dedicated Sync Roots (outside OneDrive/Documents):**
  - Windows: `C:\Synced\` (recommended root for all shares).
  - Linux: `~/Synced/` (or equivalent).
- **Key Shared Folders (Send & Receive):**
  | Purpose                  | Example Path (adjust per machine)                  | Notes |
  |--------------------------|----------------------------------------------------|-------|
  | Symbiosis repo           | `~/grok-hermes-symbiosis` / `C:\Users\...\grok-hermes-symbiosis` | Core skills, scripts, docs, handoffs |
  | Handoffs                 | `.../cross-device/handoffs`                        | Explicit task packages |
  | Joint projects           | Under `~/Synced/Projects` or `C:\Synced\Projects` | With appropriate .stignore |
- **.stignore** (critical — keep in sync via the repo itself):
  - Located in symbiosis repo root (and sometimes per-folder).
  - Protects: `.env*`, `secrets/`, `**/.hermes/`, `**/.grok/`, `**/%LOCALAPPDATA%/hermes/`, `node_modules/`, `.venv/`, `__pycache__/`, `dist/`, `build/`, large media, logs, OS noise (Thumbs.db, .DS_Store, etc.).
  - See current `.stignore` and `.stignore.local` in repo root. Windows version has extra AppData patterns.
  - Always review before sharing new folders.
- **Startup & Reliability:**
  - Add to Startup folder or Task Scheduler (minimized) on Windows; systemd/user service or login script on Linux.
  - Set GUI password in UI (Actions → Settings) for security.
  - Enable automatic upgrades if comfortable.
  - Monitor via UI (Actions → Logs); rescan as needed.
- **Maintenance:**
  - Periodically verify shares and connected devices.
  - Update binary from https://syncthing.net/downloads/.
  - After any .stignore change: rescan both sides.
  - Test sync with a small file in handoffs/ when making changes.

**Helper Scripts:** `linux/scripts/prepare-syncthing-folders.sh`, `windows/scripts/prepare-syncthing-folders.ps1`, and install scripts.

### 2.2 Git & Repo Hygiene
- Clone the shared `grok-hermes-symbiosis` repo on both machines.
- `git pull` (or let a small watcher) after noticing new files from Syncthing.
- Commit important handoff artifacts, plans, and updates to this playbook.
- Use the repo as the integration layer (skills, bridges, docs live here).

**Git Authentication Reality (Important):**
- The Grok harness execution environment often runs as a different GitHub identity than the repo owner (sespear86). This frequently causes `403 Permission denied` on `git push` and can trigger repeated "verify your GitHub account" prompts.
- **Recommended practice**:
  1. The remote in this repo is now set to SSH (`git@github.com:sespear86/grok-hermes-symbiosis.git`).
  2. Run `windows/scripts/fix-git-remote.ps1` from your normal PowerShell if the remote ever drifts back to HTTPS.
  3. Do real `git push` / history work from your normal personal terminal/shell (not inside the harness TUI when possible).
  4. The harness is great for local commits, analysis, and file changes. Treat `git push` from the harness as "best effort only."
- If you keep getting verification prompts: Load your SSH key in your normal shell/agent. Avoid mixing harness and personal credentials.
- Syncthing is the primary live sync. Git is the source of history. When in doubt, push from your real logged-in shell.

### 2.3 Handoff System (for Tracked Cross-Device Work)
- Location: `cross-device/handoffs/`
- Naming: `YYYYMMDD-HHMM-ShortName` (use creating machine's local time for HHMM).
- Required: `README.md` (use template in `HANDOFF_FORMAT.md`).
- On completion: `RETURN.md` (template in HANDOFF_FORMAT).
- Always update `HANDOFF_LOG.md` (newest first) on create and on completion (mark `Completed`).
- Supporting files (optional): notes, designs, exports, diffs/ subfolder.
- Lifecycle (from refinements): Create folder + README → do work (update status/coordination as needed) → RETURN.md → mark log complete → optional archive to `archive/` subfolder.
- Small/quick tasks: Shared chat (via Hermes gateway) is often enough. Use handoffs for anything needing explicit tracking or multi-session context.
- See `cross-device/handoffs/HANDOFF_FORMAT.md`, `HANDOFF_LOG.md`, and the two completed example packages for patterns that worked.

### 2.4 Agent Coordination via `cross-device/coordination/`
- Primary structured channel between the two Groks (minimizes Discord copy-paste).
- Key files:
  - `status.md` — High-level phase and progress (update when advancing major work).
  - `windows-instructions.md` — Written by Linux Grok for Windows Grok.
  - `linux-instructions.md` — Written by Washington Grok for Oregon Grok.
  - `prompts.md` — Verbatim short prompts humans paste in chat to trigger the local Grok ("Check the repo for the next step", "Kumquat", etc.).
  - `EXECUTION_PLAN.md` — For larger phases (immutable subagent+validate loop during execution).
- **Immutable Rule (during active plans):** 1. Orchestrate/launch sub-agents on both devices. 2. Validate results. 3. Repeat until done. Record any deviations.
- Both humans and agents should keep these files current. Humans trigger via the short prompts.
- **Mempalace cross-ref (durable memory for coordination churn):** See ~/Synced/Mempalace/symbiosis/ (esp. usage-pattern.md, recent-decisions.md, priorities.md) + handoff Relevant Memory sections. Complements this nervous system without bloat (per 0010/0130 handoffs + MEMPALACE_INTEGRATION).

### 2.5 Memory Layer (Mempalace)
Mempalace serves as a shared, persistent, long-term memory system for the symbiosis. It lives in the synced environment (via Syncthing + repo) and can be referenced inside handoffs, the Playbook, and coordination notes.

- Reduces context loss across sessions and machines.
- Allows richer handoffs (e.g., “attach relevant Mempalace sections”).
- Both Grok and Hermes instances can eventually query it during handoff creation or execution.

See `cross-device/MEMPALACE_INTEGRATION.md` for current integration patterns and how to reference it inside handoffs.

### 2.5 Local Invocation & Delegation (Grok ↔ Hermes on Same Machine)
See detailed patterns in Section 5.

---

## 3. Troubleshooting Common Issues (Windows + Linux)

### 3.1 Syncthing Problems
- **"Expected encrypted info" error** (most common early issue):
  - Cause: One side offered/ accepted the folder as "Receive Encrypted".
  - Fix: Remove the folder share on **both** machines. Re-add as normal "Send & Receive" (unencrypted). Re-share.
- **Syncthing won't start or UI not loading**:
  - Verify process running (Task Manager on Windows; `ps` on Linux).
  - Open http://127.0.0.1:8384 in browser.
  - Restart: Kill process (`taskkill` or equivalent) and re-launch `syncthing.exe` / binary from normal terminal.
  - Logs: UI → Actions → Logs (or files in the Syncthing folder).
- **OneDrive / profile redirection interference (Windows)**:
  - **Never** share entire `Documents`, `Desktop`, `OneDrive`, or user profile folders.
  - Always use dedicated root outside OneDrive: `C:\Synced\` (or D:\).
  - The symbiosis repo itself is usually safe even if under user profile because it is Git-controlled.
- **Conflicts / .sync-conflict files**:
  - Syncthing renames instead of overwriting. Manually inspect, merge, or delete the conflict copy.
  - Visible in Explorer / Finder / terminal. Common during simultaneous edits.
- **Sync slow / not happening**:
  - Check UI for errors, connected devices, and folder status.
  - Verify .stignore isn't too aggressive.
  - Rescan manually in UI.
  - Check firewall (Syncthing needs localhost + discovery ports).
- **Device IDs / pairing issues**:
  - Re-exchange long Device IDs via shared chat (never commit to repo).
  - Re-add device and re-accept shares.
  - Windows ID example: `ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2`
  - Linux ID example: `RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD`

### 3.2 TUI / Harness & Command Issues (Critical Cross-Platform Gotcha)
- **Grok Build TUI harness is non-interactive** (no TTY).
  - Blocks: `hermes setup`, `hermes model` (OAuth browser flows), interactive wizards, some Syncthing config steps.
  - **Rule:** Run all initial setup, auth, Syncthing, or Hermes configuration commands in a **normal PowerShell / terminal window**, never inside the Grok TUI harness.
  - Bridge/delegate scripts are designed to work around this for ongoing work.
- Commands not found / PATH issues:
  - Use full paths temporarily (e.g., `& "C:\Users\...\hermes\hermes-agent\venv\Scripts\hermes.exe" setup`).
  - Add `~/bin` (Linux) or `%USERPROFILE%\bin` (Windows) to PATH for bridge scripts.
- Linux vs Windows command differences: Use the platform-specific scripts in `linux/scripts/` and `windows/scripts/`.

### 3.3 Other Common Issues
- **Skills / coordination not reflecting latest changes**:
  - `git pull` on the symbiosis repo.
  - Reload skills in Grok (`/skills`) and Hermes.
  - Re-read `coordination/` files.
- **.stignore drift between machines**:
  - Because it lives in the repo root, Syncthing + Git should keep it consistent. Manually copy if needed.
- **Large files or secrets accidentally syncing**:
  - Add to .stignore immediately, remove from shares, and clean up (git rm --cached if tracked).
- **Hermes/Grok version or model drift**:
  - Use `hermes doctor`, `hermes --version`, `grok --version`, `hermes config`.
  - Both sides target grok-4.3 via xAI where possible.
- **After handoff or major change**:
  - Verify sync with a test file or by checking `HANDOFF_LOG.md` on the other side.
  - Update this playbook with any new gotchas discovered.

**General Advice:** Prefer running maintenance and setup from normal shells. Document new issues in a handoff RETURN or directly in this playbook's Troubleshooting section, then update Last Verified.

---

## 4. Key Paths, Device IDs & Quick Commands

### Device IDs (as of last verification)
- **Oregon (Windows):** `ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2`
- **Washington (Linux):** `RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD`

### Important Paths
- **Symbiosis Repo (both):** `~/grok-hermes-symbiosis` (Linux) / `C:\Users\<user>\grok-hermes-symbiosis` (Windows)
- **Handoffs:** `cross-device/handoffs/` (inside repo)
- **Coordination:** `cross-device/coordination/`
- **Windows Syncthing:** `C:\Tools\Syncthing\`
- **Recommended Sync Root:** `C:\Synced\` (Windows) / `~/Synced/` (Linux)
- **Skills:**
  - Grok hermes skill: `~/.grok/skills/hermes/SKILL.md`
  - Hermes grok-build skill: `~/.hermes/skills/grok-build/SKILL.md` (or `%LOCALAPPDATA%\hermes\skills\...`)
- **Bridge Scripts:** `~/bin/` (Linux .sh) or `%USERPROFILE%\bin\` (Windows .ps1) — add to PATH

### Quick Commands
- **Syncthing UI (both):** http://127.0.0.1:8384
- **Trigger other Grok (via human in shared chat):**
  - "Check the repo for the next step"
  - "Pull latest and read windows-instructions.md" (or linux-)
  - "Check coordination and give me the next action"
- **Git hygiene:** `git pull` after Syncthing delivers changes.
- See bridge scripts and `ACTIVATE.md` / `README.md` (root) for full local symbiosis commands.

---

## 5. Agent Invocation Patterns (Grok + Hermes Best Practices)

These patterns are what actually worked in the first two handoffs and early coordination. The `skills/cross-device/SKILL.md` is more aspirational; prioritize the proven lightweight methods below.

### Local (Same-Machine) Delegation
**From Grok Build → Hermes (long-running, gateway, persistence, kanban, execution):**
- Preferred (rich context): `grok-hermes-delegate "Task description with success criteria. Include any plans/todos."` (or full path to the .ps1/.sh)
- Direct: `/hermes delegate "..."` or `grok-hermes-delegate.sh` in shell.
- The script auto-injects cwd, git branch/status, and a `[CROSS-DEVICE / OREGON COLLAB]` note when relevant.

**From Hermes → Grok Build (design, implement+reviews, verification, best-of-n, professional docs, architecture):**
- Preferred: `hermes-grok-delegate "Detailed task... Use implement with reviewers / design / check / best-of-n as appropriate."`
- Direct in Hermes: `/grok-build implement ...` or `/grok-build design ...` etc.
- One-shot from shell: `grok -z "SYMBIOSIS ESCALATION... Task: ... Recommended workflow: implement/design/check..."`

**After Delegation:**
- Review output.
- If long-running or world delivery needed, hand back to the other agent.
- Commit key artifacts to the shared repo.

### Cross-Device Patterns (Proven)
1. **Explicit Handoff Packages** (primary for tracked work):
   - Create dated folder in `cross-device/handoffs/`.
   - Follow `HANDOFF_FORMAT.md` exactly (README with clear task, success criteria, artifacts, preferences, Return Path).
   - Use `[CROSS-DEVICE HANDOFF: Oregon Windows → Washington Linux]` (or reverse) language.
   - Include links/paths to shared repo artifacts.
   - On receiving side: do the work, create `RETURN.md` (summary, decisions, artifacts, next steps, observations).
   - Update `HANDOFF_LOG.md` (create + complete status).
   - Notify via shared chat if desired.

2. **Coordination Folder for Agent-to-Agent**:
   - Sending Grok writes precise, numbered instructions into the other machine's `-instructions.md` file.
   - Updates `status.md` and/or `EXECUTION_PLAN.md`.
   - Receiving human triggers local Grok with a short prompt from `prompts.md`.
   - Agents read the instruction file, execute (using subagent loop), update files, and signal completion.
   - Great for ongoing phases without creating a full handoff package.

3. **Shared Chat Bus (lightweight / real-time)**:
   - Both Hermes gateways connected to the same channel.
   - Use clear tags: `[CROSS-DEVICE]`, direction, links to repo/handoffs.
   - Humans or agents post status, approvals, or small tasks here.
   - Agents can read recent context via MCP (Hermes tools in Grok sessions) or gateway.

4. **When Handing Work Across Devices**:
   - Always include direction, task, success criteria, context snapshot (git HEAD, recent decisions, relevant file paths or exports), which skill/agent to use on the other side, and escalation path if blocked.
   - Prefer repo-synced artifacts over pasting large context.
   - After completion: RETURN + log update + optional chat summary.

**Best Practices from Real Use:**
- Bridge scripts > raw one-shots for rich context.
- Normal terminals for any setup or maintenance.
- Explicit `[CROSS-DEVICE]` tagging reduces confusion.
- Keep this playbook and coordination files as the "shared brain."
- After cross-device work, both sides should `git pull` and verify sync.

See root `README.md`, `ACTIVATE.md`, individual bridge scripts, and the skills/ for more examples. Update this section with new patterns that prove reliable.

---

## 6. How to Update the Playbook (and Contribute)

This is a **living** document. Treat it as the single place both humans and future agents should look first.

### Update Process (Lightweight)
1. Make the edit in markdown (add new gotcha, correct a path, expand a section, note a new command pattern, etc.).
2. **Immediately update the "Last Verified" line** at the top with today's date + your machine/identity (e.g., "by Washington Linux Grok").
3. For platform-specific details (Windows paths, PowerShell gotchas, exact Syncthing location), the owning side should keep it accurate.
4. If the change came from a handoff or real incident: mention the handoff ID or add a brief note.
5. Commit the change to the shared repo (`git add ... && git commit -m "docs: update playbook - <brief>" && git push`).
6. On the other machine: `git pull` (or wait for normal Syncthing + awareness).
7. Optionally: Post a short note in the shared chat or add an entry in `coordination/status.md` for major updates.
8. If the change is structural or large: consider opening a dedicated small handoff package for review before merging.

### Contribution Guidelines
- **Prioritize proven content:** What actually worked in handoffs, real troubleshooting, or daily use. Deprecate or clearly mark aspirational items.
- Keep it **practical and scannable** (bullets, tables, short code blocks, clear headings). Avoid walls of text.
- Both sides (and their agents) are encouraged to edit. No gatekeeping for small fixes.
- If you discover something new during a handoff, capture it here in the RETURN or directly.
- For very large changes (e.g., new major layer), propose via `PROPOSED_*.md` style or a handoff first.
- Versioning: The date + git history is sufficient. No need for formal semver unless it grows significantly.

**Goal:** This playbook should make future handoffs and maintenance faster and lower-friction, not become another document to maintain.

---

## Appendix: Key References & Historical Sources

- `cross-device/handoffs/HANDOFF_FORMAT.md` + `HANDOFF_LOG.md` + example packages (1857-Windows-Syncthing-Quick-Reference, 1937-Create-Handoff-Log-Index)
- `cross-device/coordination/` (status.md, EXECUTION_PLAN.md, *-instructions.md, prompts.md, PROPOSED_*.md)
- `cross-device/syncthing-guide.md` and `LIVE_SYNC_DESIGN.md` (design context)
- `windows/SETUP_FOR_BROTHER.md`, `windows/syncthing-setup.md`, `windows/scripts/`
- `linux/scripts/`
- `skills/cross-device/SKILL.md` and `skills/grok-build/SKILL.md` (use proven patterns primarily; align later)
- Root: `README.md`, `ACTIVATE.md`, bridge scripts in `scripts/`, `.stignore*`
- First handoff artifact: `cross-device/handoffs/20260525-1857-Windows-Syncthing-Quick-Reference/Windows-Syncthing-Quick-Reference.md` (many troubleshooting details originated here)

**Next logical evolutions (for future iterations):** Open Items/Priorities doc in coordination/, deeper skill alignment with this playbook, automated sync reports, shared kanban strategy.

---

*This playbook is intentionally lightweight and practical. It consolidates what has already proven useful. Update it as the symbiosis matures.*

<!-- Edited: 2026-05-27 03:35 | Device: Linux | By: Grok --> Light non-bloated cross-ref added to §2.4 (Agent Coordination) pointing to Mempalace for durable context surviving churn (per 0130 adoption deliverable 4 + 0010 pilot rec). Kept it 1-line high-signal. Also reinforces the §2.5 Memory Layer section already present. Self-referential: read PLAYBOOK + MEMPALACE_INTEGRATION + usage-pattern + 0130 handoff README first per pattern, then tiny edit + sig. Primes + loop + Kumquat followed. The coordination nervous system just got a memory assist in the best depraved way. Signature per prime directive. Keep er goinnnn. -->