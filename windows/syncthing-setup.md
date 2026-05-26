# Windows 11 Syncthing Setup Guide (Grok-Hermes Symbiosis)

**Goal**: Get reliable, near real-time bidirectional file sync between this Windows 11 machine and the Oregon Linux machine with minimal friction and maximum safety.

This document is the **Windows-specific companion** to `cross-device/syncthing-guide.md` in the shared repo.

## Prerequisites

- You have already cloned `grok-hermes-symbiosis` (done in previous steps).
- You have a normal PowerShell or Command Prompt available (not inside the Grok TUI harness for initial setup).
- Administrator rights are **not** required if using the portable version.

## Recommended Download & Installation Method for Windows

**Strongly recommended: Portable version (ZIP)**

1. Go to https://syncthing.net/downloads/
2. Under **Windows**, download the **64-bit** portable `.zip` (not the installer unless you have a specific reason).
3. Extract it to a stable location outside OneDrive, e.g.:
   - `C:\Tools\Syncthing\`
   - `D:\Syncthing\` (if you have a second drive)
4. Run `syncthing.exe` from the extracted folder.

**Why portable over installer?**
- No UAC prompts every time.
- Easy to move or backup.
- Runs under your user account (easier permission management).
- You control exactly where it lives.

**Making it start automatically (recommended)**

Option A (Simplest):
- Create a shortcut to `syncthing.exe` in your Startup folder:
  - Press `Win + R`, type `shell:startup`, press Enter.
  - Paste a shortcut to `syncthing.exe` there.

Option B (Better – minimized):
- Create a `.bat` or use Task Scheduler to run it hidden.

After first run, the web UI will open automatically at: http://127.0.0.1:8384

## Important Windows 11 Gotcha: OneDrive Redirection

Your user profile likely has `Documents` (and possibly `Desktop`) redirected to OneDrive.

**Never add these as Syncthing shares:**
- Entire `C:\Users\spear\Documents`
- Entire `C:\Users\spear\OneDrive`
- Entire `C:\Users\spear\Desktop`

**Recommended practice:**
- Create a dedicated root folder **outside** OneDrive:
  - `C:\Synced\`
  - Or `D:\Synced\` (best if available)
- Place all shared project material under this root.
- The symbiosis repo itself (`C:\Users\spear\grok-hermes-symbiosis`) is usually fine to share directly because it is already under Git.

## Recommended Initial Shares (Start Small)

Share these folders first (in order of priority):

1. **The symbiosis repo itself**
   - Path on Windows: `C:\Users\spear\grok-hermes-symbiosis`
   - Mode: Send & Receive (both sides)
   - .stignore: See below

2. **Dedicated joint project root** (create if needed)
   - Example: `C:\Synced\Projects\`
   - Or specific project folders inside it.

3. **Handoff exchange folder**
   - `C:\Users\spear\grok-hermes-symbiosis\cross-device\handoffs`
   - Very useful for explicit cross-device packages.

**Rule of thumb**: Start with 1–2 folders. Only add more after everything is working smoothly for a few days.

## Windows-Friendly .stignore Patterns

Place a `.stignore` file in the **root** of each folder you share.

Recommended starter content for the symbiosis repo (save as `.stignore` in the repo root):

```gitignore
# === Grok-Hermes Symbiosis Windows .stignore ===

# Build / dependency artifacts
node_modules/
.venv/
__pycache__/
dist/
build/
*.log
.cache/
*.tmp

# Secrets & machine-specific (NEVER SYNC THESE)
.env*
secrets/
**/.git/
**/.ssh/
**/.grok/
**/.hermes/
**/%LOCALAPPDATA%/hermes/
**/%APPDATA%/hermes/
**/.config/hermes/

# Large / unnecessary
*.mp4
*.iso
*.zip
models/
downloads/
*.pt
*.bin
*.safetensors

# Windows-specific noise
Thumbs.db
desktop.ini
$RECYCLE.BIN/
```

For general project folders, use a slightly lighter version without the agent homes.

## Step-by-Step Windows Setup Checklist

1. **Download & run Syncthing** (portable recommended, see above).
2. **Open the UI** at http://127.0.0.1:8384
3. **Set a GUI password** immediately (Actions → Settings → GUI).
4. **Get your Device ID**:
   - Actions → Show ID
   - Copy the long ID and send it to your brother (via the shared chat).
5. **Add the Linux device**:
   - In the UI: "Add Device"
   - Paste the Device ID from the Oregon machine.
   - Give it a clear name: "Oregon-Linux"
6. **Add folders to share**:
   - "Add Folder"
   - Choose the local path (e.g., the symbiosis repo).
   - Set the Folder ID to something stable (e.g., `grok-hermes-symbiosis`).
   - Choose "Send & Receive".
   - On the "Ignore Patterns" tab, paste the patterns above.
7. **Accept incoming shares** from the Linux machine when they appear.
8. **Watch the status** in the UI. First sync can take a while depending on size.

## Making Syncthing Reliable on Windows

- Run it at login (see Startup folder method above).
- Do **not** run it as Administrator unless you have a very good reason.
- Add an exception in Windows Defender Firewall if it prompts (Syncthing needs local port 8384 and discovery ports).
- Consider enabling "Automatic Upgrade" in Settings (it is usually safe).

## Integration with the Symbiosis Workflow

After Syncthing is running:

- Both machines will stay in sync on the `grok-hermes-symbiosis` repo automatically.
- When one side creates or updates a skill, script, or handoff package, it appears on the other side within seconds/minutes.
- Always `git pull` (or let a small watcher do it) after noticing new files.
- Use the `cross-device` skill (once implemented) to generate proper handoff reports inside the synced folders.

## Next Actions After Initial Setup

- Exchange Device IDs in the shared chat.
- Both sides add the same initial folders.
- Test by creating a small test file in `cross-device/handoffs/test-sync.md` on one machine and watching it appear on the other.
- Document your Device IDs in a private note or the shared repo (never commit secrets).

This setup + Git + the Hermes gateway in the shared chat is currently the most practical way to make the two machines feel like one extended environment.

---

**See also**:
- `cross-device/syncthing-guide.md` (general concepts)
- `cross-device/LIVE_SYNC_DESIGN.md` (architecture)
- `windows/scripts/prepare-syncthing-folders.ps1` (Windows helper script)

Run the helper script first when you're ready to begin the actual setup in a normal PowerShell window.