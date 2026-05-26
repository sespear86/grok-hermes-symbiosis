# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-26
**Current Phase:** Syncthing Rollout – Folder Sharing & Sync Verification

> **Important:** We use repo-based coordination. All major handoffs and status updates should go through the files in `cross-device/coordination/`.
> See `cross-device/coordination/README.md` for the current protocol.

## Known Device IDs
- **Windows (Oregon):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Current Context
- Both machines have Syncthing running with GUI passwords set.
- Devices are linked and connected.
- The main `grok-hermes-symbiosis` folder has been shared and both sides currently show it as "Up to Date".
- A one-way sync test succeeded (file created on Linux appeared on Windows).

## Next Task: Reverse Sync Test

Goal: Verify that file changes also flow reliably from Windows → Linux.

### Exact Steps to Guide the User

1. Instruct the user to open a normal PowerShell / Command Prompt and go to their copy of the symbiosis repo:
   ```powershell
   cd C:\Users\spear\grok-hermes-symbiosis
   ```

2. Have them create a small test file with a clear name and timestamp:
   ```powershell
   echo "Test sync from Oregon Windows - $(Get-Date)" > test-sync-from-windows.txt
   ```

3. Ask the user to wait 15–30 seconds, then check with the person on the Linux side (Washington) whether the file `test-sync-from-windows.txt` has appeared in their `grok-hermes-symbiosis` folder.

4. Once the Linux side confirms (or reports it did not appear), have the user report the result back.

### After the Test

When you have the result of the test, do the following using the repo coordination protocol:

1. Update this file (`windows-instructions.md`):
   - Note the result of the reverse sync test.
   - Update the current phase/status.

2. Update `status.md`:
   - Record whether bidirectional sync has been confirmed.
   - Update the "Next Expected Action" section.

3. If the test succeeds, write the next set of instructions into `linux-instructions.md` (e.g., "Both sides have now verified bidirectional sync. Next: Share the handoffs folder").

4. Reference `cross-device/coordination/README.md` and `prompts.md` if needed.

Keep all updates clear, dated, and actionable so the Linux Grok can continue without the humans having to forward long messages.

## Important Notes
- We are currently prioritizing verification of reliable folder sync before sharing additional folders.
- Keep instructions incremental.
- Once bidirectional sync is confirmed, the next recommended folder to share is `cross-device/handoffs`.
