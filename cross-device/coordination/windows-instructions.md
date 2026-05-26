# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-26
**Current Phase:** Syncthing Rollout — Bidirectional Sync Verified (Awaiting Next Folder Share)

## Known Device IDs
- **Windows (this machine):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Current Context
- Both machines have Syncthing running with GUI passwords set.
- Devices are linked and connected.
- The main `grok-hermes-symbiosis` folder is synced and "Up to Date" on both sides.
- Bidirectional sync has been verified:
  - Forward test: File created on Linux (`test-sync-from-linux.txt`) appeared on Windows.
  - Reverse test: File created on Windows (`test-sync-from-windows.txt`) successfully appeared on Linux (confirmed by user on 2026-05-26).

## Completed Task: Reverse Sync Test

**Result:** Success. The test file appeared on the Linux machine.

The user executed:
```powershell
cd C:\Users\spear\grok-hermes-symbiosis
echo "Test sync from Oregon Windows - $(Get-Date)" > test-sync-from-windows.txt
```

Linux side confirmed the file arrived.

## Next Phase (Handed Off to Linux Grok)

Linux Grok should now:

1. Update `linux-instructions.md` with the next concrete actions for the user on the Linux side.
2. Share the `cross-device/handoffs` folder with the Windows device via Syncthing.
3. Update `status.md` with the new phase and next expected actions.
4. Leave clear guidance in this file (`windows-instructions.md`) for when the Windows user sees the incoming handoffs folder share.

## Current Task
Accept and configure the incoming `handoffs` folder share from the Linux side.

## Incoming Share: Handoffs Folder

The Linux side has now shared the `handoffs` folder (located at `cross-device/handoffs` inside the symbiosis repo).

### Exact Steps to Guide the User When the Share Request Appears

1. In the Syncthing UI on Windows, look for an incoming share request for a folder labeled something like **"handoffs"**.

2. When accepting the share, use this local path:
   ```
   C:\Users\spear\grok-hermes-symbiosis\cross-device\handoffs
   ```

   (Create the folders if they don't already exist.)

3. After accepting, go to the folder settings and ensure it is set to **Send & Receive** (normal sync, not encrypted or send-only unless specifically decided later).

4. Confirm that the folder appears and eventually shows as "Up to Date" or starts syncing.

5. Report back once the folder is accepted and syncing (e.g., "Handoffs folder accepted and syncing").

### After the User Accepts the Share

Update the coordination files:
- Update this file (`windows-instructions.md`) with the result.
- Update `status.md` to reflect that the Windows side has accepted the handoffs share.
- If needed, leave further instructions in `linux-instructions.md` (for example, to start using the handoffs folder for actual cross-device tasks).

## Important Notes
- We have now verified reliable bidirectional sync on the core repo.
- Keep coordination through this folder.
- Once the handoffs folder is shared and verified, we can expand to other joint project folders.
- Test files (`test-sync-from-*.txt`) can be cleaned up later if desired.