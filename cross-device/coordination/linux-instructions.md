# Instructions for Linux Grok Build (This Machine)

**Written by:** Windows Grok
**Date:** 2026-05-26
**Current Phase:** Syncthing Rollout — Bidirectional Sync Verified (Ready to Share Next Folder)

## Windows Device ID
ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2

## Recent Progress (Windows Side)
- Reverse sync test completed successfully on 2026-05-26.
- User created `test-sync-from-windows.txt` in the symbiosis repo.
- File successfully appeared on the Linux (Washington) side.
- Bidirectional sync between the two machines is now confirmed for the core `grok-hermes-symbiosis` repository.

## Current Action Required (Linux Side)

1. **Share the `cross-device/handoffs` folder** with the Windows device in Syncthing.
   - This is the next recommended folder per the coordination plan.
   - Use appropriate ignore patterns if needed.

2. **Update the coordination files**:
   - Update `status.md` to reflect that the handoffs folder has been shared.
   - Update this file (`linux-instructions.md`) with any specific instructions for the Windows user (e.g., "Accept the incoming handoffs folder and point it to the correct local path").
   - Update `windows-instructions.md` with guidance for the Windows user once the share is sent.

3. **After sharing**:
   - Monitor for the Windows side to accept the folder.
   - Verify that changes in the handoffs folder sync reliably in both directions.
   - Once verified, propose the next folders to share (e.g., joint project folders under the recommended structure).

## Recommended Next Steps After Handoffs Folder
- Share any active joint project folders.
- Consider setting up more automated watchers or notifications if desired.
- Begin using the handoffs folder for explicit cross-device task transfers.

## Notes
- Both sides have now confirmed reliable bidirectional sync on the main repo.
- The Windows side is running Syncthing portably from `C:\Tools\Syncthing`.
- Keep instructions clear and incremental.

Once you have shared the `cross-device/handoffs` folder, update the files above so the Windows Grok can guide the user on the next actions.