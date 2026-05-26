# Grok + Hermes Symbiosis Setup for Windows 11

**Goal**: Get your machine to the same symbiotic state as your brother's Linux machine, then enable real-time(ish) collaboration across both devices so the two machines feel as close as possible to "one shared environment."

**Your situation**:
- Both Grok Build and Hermes Agent are already installed and working.
- Hermes is already using grok-4.3 via xAI as primary (perfect — same foundation).

This guide is written to be copy-paste friendly. Run sections in order and report back any output or errors.

---

## Step 1: Confirm Current State (Run These Commands)

Open **PowerShell** (preferably as your normal user) and run:

```powershell
# Hermes location
$env:LOCALAPPDATA
hermes --version
hermes doctor

# Grok Build
grok --version 2>$null || "grok command check"
Get-Command grok -ErrorAction SilentlyContinue

# Confirm model in Hermes
hermes config | Select-String -Pattern "grok| xai"
```

Paste the full output back to your brother.

**Expected**:
- Hermes lives under `%LOCALAPPDATA%\hermes`
- You should see grok-4.3 as the default (via the active config).

**Important Windows Notes from real runs**:
- Hermes and grok commands may not be in PATH yet. Use full paths or run `hermes setup` early.
- `hermes doctor` will often recommend `hermes setup` — do this early on Windows.
- The active Hermes config with your model is usually at `C:\Users\<you>\AppData\Local\hermes\config.yaml`.
- **Critical**: If you are running commands inside the Grok Build TUI harness, it is non-interactive (no TTY). This blocks `hermes model` (OAuth browser login) and setup wizards. You **must** open a normal PowerShell window outside of Grok Build to complete authentication.

---

## Immediate Next Action After Step 1 (Run This Now)

**Run `hermes setup`** in PowerShell:

```powershell
hermes setup
```

(If `hermes` is not recognized, try the full path first:)
```powershell
& "C:\Users\spear\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" setup
```

This will:
- Create the missing `.env`
- Help configure your xAI OAuth / grok-4.3 credentials
- Initialize Skills Hub and other basics
- Guide you through provider selection

Run it, follow the prompts (especially for xAI / Grok), then paste the new `hermes doctor` output afterward.

---

## Step 2: Apply the Local Symbiosis (Grok ↔ Hermes on Your Machine)

We will create the same skills and bridges that exist on the Linux machine.

### 2.1 Create the Grok "hermes" Skill (for Grok Build TUI)

Create these directories and the file:

```powershell
mkdir -p "$env:USERPROFILE\.grok\skills\hermes"
```

Then create the file at:
`%USERPROFILE%\.grok\skills\hermes\SKILL.md`

**Content** (copy the entire block below into the file):

```markdown
---
name: hermes
description: >
  Interface with the Hermes Agent for long-running work, persistent gateway presence, kanban swarms, and massive skill library.
  Primary bridge from Grok Build to Hermes on this Windows machine. Part of the cross-device Grok-Hermes symbiosis with brother in Oregon.
metadata:
  short-description: "Hermes symbiosis bridge (Windows)"
  symbiosis: true
  cross_device: true
---

# Hermes Symbiosis Skill (Windows-adapted)

This is the Windows version of the hermes skill used in the shared Grok-Hermes symbiosis with your brother.

See the full guide at the shared `grok-hermes-symbiosis` repo (clone it locally).

Core commands work similarly:
- `hermes` or `hermes --tui`
- `hermes -z "prompt"` for one-shot
- `hermes --resume ...`
- `hermes --skills grok-build,...`

Use `grok-hermes-delegate.ps1` (or the manual patterns in the skill) for rich handoff from Grok sessions.

When working with your brother:
- Always include `[CROSS-DEVICE]` or mention Oregon/Linux machine when handing off.
- Prefer shared chat (Discord/Telegram/etc.) + Hermes gateway for coordination.
- Use the cross-device sync patterns for context sharing.
```

(Full rich version will be pulled from the shared repo once cloned — this stub is enough to start.)

### 2.2 Create the Hermes "grok-build" Skill (reciprocal)

```powershell
mkdir -p "$env:LOCALAPPDATA\hermes\skills\grok-build"
```

Create `SKILL.md` inside it with content adapted from the Linux version (we will sync the full version via the shared repo).

For now, a minimal version is acceptable — the shared repo will provide the canonical one.

### 2.3 Create Windows Bridge Scripts

Create the directory:

```powershell
mkdir -p "$env:USERPROFILE\bin"
```

Download / create two PowerShell scripts (we will provide improved versions from the shared repo shortly):

- `grok-hermes-delegate.ps1`
- `hermes-grok-delegate.ps1`

Basic starter versions are included later in this document under "Bridge Scripts".

Add `%USERPROFILE%\bin` to your PATH if not already.

---

## Step 3: Clone the Shared Symbiosis Repository (Critical for Sync)

We are turning `grok-hermes-symbiosis` into the single source of truth for both machines.

**Action for you**:
1. Ask your brother for the GitHub repo URL (or create a private repo under a shared org/account right now).
2. Once you have the URL:

```powershell
cd ~
git clone <the-repo-url> grok-hermes-symbiosis
cd grok-hermes-symbiosis
```

This repo will contain:
- Skills (both Grok and Hermes versions)
- Cross-platform bridge scripts (.ps1 + .sh)
- Distributed sync tools and guides
- Shared project context, kanban exports, etc.

Pull regularly (or set up a simple sync script).

---

## Step 4: Set Up Live File & Context Sync (The "One Machine" Illusion)

To make the two devices feel synchronized:

### Recommended Primary Tool: Syncthing

Syncthing gives near-real-time file sync with conflict handling, selective folders, and works great across Windows ↔ Linux.

**Why it wins here**:
- Live updates to code, plans, skills, scripts, project files.
- You can selectively sync only project-related folders (avoid syncing secrets).
- Works offline + resumes.
- Both of you control exactly what is shared.

**Setup steps** (run on your Windows machine):

1. Download Syncthing for Windows (portable or installer) from https://syncthing.net/
2. Run it (it opens a web UI on localhost:8384 by default).
3. On the Linux machine, your brother will also run Syncthing and share folders with you (you exchange device IDs).
4. Recommended shares to start:
   - The `grok-hermes-symbiosis` folder itself (skills, scripts, docs).
   - Your joint project folders.
   - (Optional) selective Hermes skills or Grok skills folders.
   - **Do NOT** sync full `.hermes` or `.grok` homes blindly — too many secrets and machine-specific files.

We will add a `cross-device/sync-config.md` with exact recommended folder structures.

### Secondary: Git + Good Branching

- All code and serious work lives in Git (shared GitHub repo(s)).
- Use frequent small commits or worktrees.
- The symbiosis repo itself is the integration layer.

### Tertiary: Hermes Gateway + Shared Chat

Since you have an existing chat group (Discord/Telegram/Slack), configure Hermes gateway on **both** machines to participate in the same channel(s).

This becomes the "live voice" for both agents and both humans. One of you (or an agent) can say "handing this to Oregon machine" and the other side picks it up.

---

## Step 5: First Cross-Device Test (After Repo Clone)

Once the shared repo is cloned on both sides:

1. On either machine, use the delegate scripts or skills to hand a small task to the other side.
2. Example from Grok on Windows:
   - Use the `hermes` skill or `grok-hermes-delegate.ps1`
   - Include text like: `[CROSS-DEVICE HANDOFF TO OREGON LINUX]`

3. Use the shared chat for coordination.

4. After work, run a "sync report" (we will add a script for this).

---

## Bridge Scripts (PowerShell Starters)

### grok-hermes-delegate.ps1 (basic version — improve from shared repo)

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Task,
    [string]$Extra = ""
)

$Cwd = Get-Location
$GitBranch = (git branch --show-current 2>$null) ?? "no-git"
$GitStatus = (git status --short 2>$null | Select-Object -First 10) ?? "no-git-or-clean"

$Prompt = @"
SYMBIOSIS DELEGATION from Grok Build (Windows) to Hermes Agent.

Working directory: $Cwd
Git branch: $GitBranch
Recent git status:
$GitStatus

Task:
$Task

Extra context:
$Extra

[CROSS-DEVICE] If this is for the Oregon/Linux brother, mark it clearly and prefer shared chat + gateway for coordination.

Execute with your full capabilities. Escalate heavy design/review/verification back using your 'grok-build' skill.
"@

Write-Host ">>> Launching Hermes with cross-device context..."
hermes --skills grok-build -z $Prompt
```

Create a similar `hermes-grok-delegate.ps1`.

---

## Next Actions for You Right Now

1. Run the confirmation commands in Step 1 and send the output.
2. Tell your brother the GitHub repo URL for `grok-hermes-symbiosis` (or create it together now).
3. Install Syncthing and be ready to pair devices.
4. Confirm your shared chat platform (Discord? Telegram? etc.) and whether Hermes gateway is already connected there.

Once we have the repo URL and chat details, we will immediately push the full canonical skills, improved cross-platform scripts, and the distributed sync layer.

This is the foundation for making the two machines feel like one extended environment for your joint projects.

---

**Report back** with:
- Output from Step 1 commands
- Your shared chat platform
- Whether you want to create the GitHub repo now (private recommended)

We will iterate quickly from there.
