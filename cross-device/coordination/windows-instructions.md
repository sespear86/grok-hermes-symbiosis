# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-25
**Current Phase:** Syncthing Rollout – Phase 2 (GUI Password + Device ID)

> **Important:** We use repo-based coordination. All major handoffs and status updates should go through the files in `cross-device/coordination/`.
> See `cross-device/coordination/README.md` for the current protocol.

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

When the user provides the Device ID, follow the repo-based coordination protocol:

1. **Update this file** (`windows-instructions.md`):
   - Add the full Device ID at the top or in a clear "Device ID" section.
   - Mark Phase 2 as complete.
   - Note the current status (e.g., "GUI password set, Device ID obtained, ready for pairing").

2. **Update `status.md`** in the same folder:
   - Change the Windows section to show that Phase 2 is complete.
   - Record that the Windows Device ID has been obtained.
   - Update the "Next Expected Action" to reflect the handoff to Linux.

3. **Write clear instructions into `linux-instructions.md`**:
   - Include the Windows Device ID.
   - Tell the Linux Grok the next actions it should guide the user through (e.g., add remote device, share specific folders, etc.).
   - Keep the language clear and incremental.

4. Reference the `README.md` in `cross-device/coordination/` if you need a reminder of how the coordination system works.

This ensures both Grok instances can communicate cleanly through the repo instead of relying on the humans to forward messages.

## Important Notes
- Prefer the portable version running from C:\Tools\Syncthing.
- Remind the user they can later set up auto-start (Startup folder or Task Scheduler) — we can do that in a later micro-phase.
- Keep instructions very incremental.

## When Ready
Once you have the Device ID, follow the steps in the "After Receiving the Device ID" section above.

After updating the coordination files, the Linux Grok will be able to see the new instructions in `linux-instructions.md` the next time it pulls the repo (triggered by the human using one of the prompts in `prompts.md`).

This is the primary way the two Grok instances should communicate going forward.
