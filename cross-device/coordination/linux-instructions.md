# Instructions for Linux Grok Build (This Machine)

**Written by:** Linux Grok (self)
**Date:** 2026-05-25
**Current Phase:** Waiting on Windows Syncthing Phase 1 completion

## Current State
- Windows side is in Phase 1 of Syncthing installation.
- We have already performed Linux-side preparation:
  - ~/Synced folder structure created
  - .stignore added to the symbiosis repo
  - linux/scripts/prepare-syncthing-folders.sh created and executed

## When Windows Advances

When the Windows Grok updates this file (or status.md) with the Windows Device ID and indicates it is ready for pairing, you should:

1. Pull latest from the repo.
2. Read the latest `windows-instructions.md` (or the relevant dated file) to get the Device ID.
3. Prepare the Linux Syncthing instance:
   - Install Syncthing if not already present (recommend the method that matches the environment — apt, snap, or portable binary).
   - Run Syncthing and access the web UI.
   - Set a GUI password.
   - Obtain this machine's Device ID.
4. Add the Windows Device ID as a remote device in the Syncthing UI.
5. Share the recommended folders (symbiosis repo, handoffs, Projects, etc.) with the Windows device.
6. Update `status.md` and leave pairing confirmation instructions in `windows-instructions.md`.

## Current Action
No immediate action required on Linux until Windows completes Phase 1 and provides a Device ID.

Monitor `status.md` and `windows-instructions.md` for updates.
