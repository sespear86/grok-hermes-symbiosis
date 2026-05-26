# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-26
**Current Phase:** Syncthing Rollout — Handoffs Folder Accepted

## Known Device IDs
- **Windows (this machine):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Current Context
- Both machines have Syncthing running with GUI passwords set.
- Devices are linked and connected.
- The main grok-hermes-symbiosis folder is synced and "Up to Date" on both sides.
- Bidirectional sync has been verified via test files.
- The cross-device/handoffs folder has been shared by Linux and successfully accepted on Windows (user confirmed on 2026-05-26: "handoffs folder accepted and syncing").

## Completed Task: Accept Handoffs Folder

**Result:** Success. The user accepted the incoming handoffs share and pointed it to:
C:\Users\spear\grok-hermes-symbiosis\cross-device\handoffs

The folder is now syncing.

## Next Phase (Handed Off to Linux Grok)

Linux Grok should now:

1. Confirm that the handoffs folder is syncing properly on the Linux side.
2. Update status.md and this file with the current state.
3. Propose concrete next actions, such as:
   - Beginning to use the handoffs folder for actual cross-device task transfers.
   - Sharing additional joint project folders.
4. Leave clear instructions in linux-instructions.md for any immediate actions the Linux user should take.

## Important Notes
- The handoffs folder is now the designated location for explicit cross-device handoffs.
- Keep all major coordination updates in this folder.
- Test files can be cleaned up.
