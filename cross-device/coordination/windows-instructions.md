# Instructions for Windows Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-25
**Current Phase:** Handoff System Maturity (see EXECUTION_PLAN.md)

## Known Device IDs
- **Windows (this machine):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Decision
User selected **Option B**: Start the next real handoff directly instead of refining the format first.

## Current Task
Propose a concrete next handoff task to the user. Once agreed, create the handoff package in cross-device\handoffs\ following the current format.

## Recommended Approach for the Second Handoff
- Keep it small-to-medium in scope.
- Something that builds on the first handoff or addresses a real ongoing need.
- After this one, we can do a quick retrospective on the format.

## Current Priority Tasks (from EXECUTION_PLAN.md)

The overall project has moved into **Phase 2: Handoff System Maturity**.

### Task C1 – Cleanup (Do First)
- Delete the test file `test-sync-from-windows.txt` from the symbiosis repo root.
- Update this file and `status.md` once complete.

### Task H1 – Handoff Format Review
The Linux side has published a proposed Handoff Package format:
`cross-device/handoffs/HANDOFF_FORMAT.md`

**Actions:**
1. Review the format with the user.
2. Walk through the structure and purpose.
3. The Linux side has already completed a detailed structured review (see `FORMAT_REVIEW_LINUX.md` inside the first handoff package folder `20260525-1857-Windows-Syncthing-Quick-Reference`).
4. Collect the user's feedback and compare it with the Linux review.
5. Record combined feedback and any proposed changes in this file or in a new note in the handoffs folder.
6. Update `status.md` with the outcome of the review.

Once the format is reviewed (and any changes agreed), we can move to the first real operational handoff using the (possibly refined) format.

Reference the new `EXECUTION_PLAN.md` in the coordination folder for the full breakdown of current tasks.
