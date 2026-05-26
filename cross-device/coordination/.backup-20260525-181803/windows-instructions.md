# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Last Updated:** 2026-05-26 (by Windows Grok)
**Current Phase:** Syncthing Rollout — Phase 3 (Devices Connected - Ready for Folder Sharing)

## Device IDs

**Windows (this machine):**
ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2

**Linux (Oregon):**
RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

---

## Progress Update

**User confirmed on 2026-05-26:** "the device is connected in the ui"

Excellent — the two Syncthing instances can now communicate directly.

## Immediate Next Steps

1. **Check for incoming folders**
   - In your Syncthing UI, look in the "Incoming Folders" section.
   - You should soon see folder share requests from the Linux machine (especially the symbiosis repo).

2. **If you see incoming folders:**
   - Review the folder path it wants to use on your side.
   - For the symbiosis repo, point it to your existing clone: C:\Users\spear\grok-hermes-symbiosis
   - Make sure the .stignore we created earlier is in place.
   - Accept as "Send & Receive".

3. **If no incoming folders yet:**
   - You can initiate sharing from your side.
   - Select the symbiosis repo → Edit → Sharing tab → Add the Linux device.
   - Do the same for the cross-device/handoffs folder if desired.

4. Reply here with what you see (e.g., "Incoming folder for grok-hermes-symbiosis" or "No folders yet").

## Recommended First Shares
- grok-hermes-symbiosis (the core repo)
- Any folders under C:\Synced\Projects
- cross-device/handoffs (for explicit handoffs)

## Notes
- Your .stignore in the symbiosis repo root already has good Windows-friendly patterns.
- Once the repo is syncing both ways, we can set up auto-start and more advanced usage.
