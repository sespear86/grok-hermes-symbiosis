# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-26
**Current Phase:** Handoff Process Definition (Handoff Format Proposed)

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

## Current Focus: Handoff Package Format

The Linux side has proposed a lightweight Handoff Package format (see `cross-device/handoffs/HANDOFF_FORMAT.md`).

This is now the primary mechanism for structured cross-device work between the two machines.

### Recommended Next Steps for the Windows Grok

1. Review `cross-device/handoffs/HANDOFF_FORMAT.md` with the user.
2. Walk the user through the proposed format (folder naming, README.md + RETURN.md pattern, etc.).
3. Ask for feedback:
   - Does the format feel usable?
   - Any suggested improvements or simplifications?
4. Once the user is comfortable (or after agreeing on any adjustments), do the following:
   - Update this file (`windows-instructions.md`) noting that the format has been reviewed and agreed (or note any changes).
   - Update `status.md` to reflect that the handoff format is now accepted.
   - Leave guidance in `linux-instructions.md` proposing the first real handoff using the new format.

### Important
Keep the process lightweight. The goal is to enable clear, trackable handoffs without adding heavy overhead.

## Important Notes
- The handoffs folder is now the designated location for explicit cross-device handoffs.
- Keep all major coordination updates in this folder.
- Test files can be cleaned up.
