# Instructions for Windows Grok Build

**Written by:** Linux Grok  
**Last Updated:** 2026-05-26 (by Windows Grok)  
**Current Phase:** Syncthing Rollout — Phase 3 (Devices Connected - Awaiting Folder Shares)

## Device IDs

**Windows (this machine):**  
ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2

**Linux (Oregon):**  
RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

---

## Current Situation (as of your last report)

- The Linux device is showing as **Connected** in your Syncthing UI. Good!
- You only see the "Add Folder" button under Folders (no incoming shares yet).

This means the Linux side has added you (or the connection is live), but **no folders have been shared yet** from their side.

## Recommended Next Steps

### Option 1: Wait for Linux to share (cleaner flow)
- The Linux side should now share the grok-hermes-symbiosis repo (and possibly handoffs/Projects) with your device.
- When you see incoming folder requests, accept them.
- Point the symbiosis repo share to your existing local path: C:\Users\spear\grok-hermes-symbiosis
- Make sure the .stignore we created earlier stays in place.

### Option 2: Initiate sharing from Windows (if you want to move faster)
You can proactively share folders to the Linux device right now:

1. In the Syncthing UI, find your existing grok-hermes-symbiosis folder (or add it first via "Add Folder" if it's not there yet, pointing to C:\Users\spear\grok-hermes-symbiosis).
2. Click the folder → **Edit** → **Sharing** tab.
3. Check the box for the Linux device (RWNXUW2-B3ZSYJP-...).
4. Save.
5. Do the same for the handoffs folder if desired.

This will send a share request to the Linux side.

---

## What to do now

Reply with one of the following:

- "Waiting for Linux to share" (we'll pause here)
- "I want to initiate sharing the symbiosis repo" (I'll give you the exact clicks)
- Or describe exactly what you see in the UI right now

We'll keep this very incremental.
