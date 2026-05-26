# Instructions for Linux Grok Build (This Machine)

**Written by:** Linux Grok (self)
**Date:** 2026-05-25
**Current Phase:** Waiting on Windows Syncthing Phase 1 completion

## Current State
- Windows side has completed Phase 1 (Syncthing is running, UI visible).
- We are now waiting for the Windows Device ID (expected during their Phase 2).

## Linux-Side Preparation (Already Done)
- ~/Synced folder structure created
- .stignore added to the symbiosis repo
- linux/scripts/prepare-syncthing-folders.sh created and executed

## When Windows Provides Device ID

When the Windows Grok posts the Device ID (via update to status.md or windows-instructions.md), you should:

1. Pull latest from the repo.
2. Read the Device ID from the latest `windows-instructions.md`.
3. Install and configure Syncthing on this Linux machine:
   - Install Syncthing (preferred methods below).
   - Launch it and access the web UI.
   - Set a GUI password.
   - Obtain this machine’s Device ID.
4. Add the Oregon Windows Device ID as a remote device.
5. Share the key folders (`grok-hermes-symbiosis`, `handoffs`, `Projects`, etc.).
6. Update `status.md` and leave confirmation instructions for Windows.

## Recommended Syncthing Installation Options (Linux)

Option A (Easiest on most Debian/Ubuntu systems):
```bash
sudo apt update
sudo apt install syncthing
```

Option B (Latest version via official repo):
Follow the official instructions at https://apt.syncthing.net/

Option C (Portable binary - for maximum control):
Download from https://syncthing.net/downloads/ and run the binary directly.

## Current Action (User chose Option A)
✅ UI is now up (user confirmed).

Next immediate steps for the user:
1. Set a GUI password in the web UI (Actions → Settings → GUI tab).
2. Refresh and log in with the new password.
3. Go to Actions → Show ID and copy the Device ID.

Once the user has the Device ID, record it and wait for the Oregon Windows Device ID to proceed with pairing.
