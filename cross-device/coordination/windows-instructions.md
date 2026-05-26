# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-25
**Current Phase:** Syncthing Rollout – Phase 2 (GUI Password + Device ID)

## Context
The user has been instructed to complete Phase 1 (download portable Syncthing, extract to C:\Tools\Syncthing, run syncthing.exe, and confirm the web UI loads at http://127.0.0.1:8384).

When the user replies with something like:
- "Phase 1 complete – UI is now visible and working"

You should immediately proceed with Phase 2 below.

## Phase 2: Secure the UI and Obtain Device ID

Goal: Set a GUI password (important for security) and retrieve the Device ID so the Linux side can add this machine as a remote.

### Exact Steps to Guide the User

1. Instruct the user to go to the Syncthing web UI (http://127.0.0.1:8384) in their normal browser.

2. Guide them through setting a GUI password:
   - Click the "Actions" menu (top right)
   - Choose "Settings"
   - Go to the "GUI" tab
   - Set a strong password under "GUI Authentication Password"
   - Save

3. After saving, tell them to refresh the page and log in with the new password.

4. Once logged in, instruct them to:
   - Go to the "Actions" menu again
   - Click "Show ID"
   - Copy the long Device ID string

5. Ask the user to paste the Device ID back here.

### After Receiving the Device ID

When the user provides the Device ID, do the following:
- Update this file (or create a new dated file) with the Device ID.
- Update `status.md` to reflect that Windows has a Device ID.
- Write clear instructions into `linux-instructions.md` so the Linux Grok can prepare to add the remote device and accept shares.

## Important Notes
- Prefer the portable version running from C:\Tools\Syncthing.
- Remind the user they can later set up auto-start (Startup folder or Task Scheduler) — we can do that in a later micro-phase.
- Keep instructions very incremental.

## When Ready
Once you have the Device ID from the user, update this file with the ID and mark the phase complete, then hand off to Linux via `linux-instructions.md`.
