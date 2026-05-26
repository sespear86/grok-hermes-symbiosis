# Instructions for Windows Grok Build (Oregon)

**Written by:** Windows Grok (updated during Kumquat after Linux 2017 validation)
**Date:** 2026-05-26
**Current Phase:** Handoff System Maturity + Real Operational Use (see EXECUTION_PLAN.md)

**IMMUTABLE PRIMARY OPERATING MODEL (Mandatory for all plan execution on both devices):**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This loop is the **only** approved method for executing any part of the EXECUTION_PLAN. It is immutable.

## Known Device IDs
- **Windows (this machine / Oregon):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Washington):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Accurate Current State (as of 2026-05-26)
- Playbook handoff (20260525-1954) completed by Linux via sub-agent.
- Cross-device skill alignment handoff (20260525-2017 / Topic #2) completed by this side with grounded v2 `skills/cross-device/SKILL.md`.
- **Linux has now validated and closed the 2017 handoff** (detailed sub-agent + manual review in status.md section "20260525-2017 Handoff Closure").
- Active handoff: **20260526-2305-Open-Items-Priorities** (Topic #3) — launched by us, package live, OPEN_ITEMS.md already seeded with good starter content.
- Linux side has correctly identified 2305 as their immediate priority.

## Current Task for You (Windows Grok)
Support the active 2305 handoff and keep the coordination layer honest while the Linux side executes it.

**Specific actions:**
1. Keep this machine's files clean and synced.
2. Be ready to review/improve the OPEN_ITEMS.md or assist when Linux delivers their work on 2305.
3. On the next "Kumquat" after they post the RETURN for 2305, review it, add signatures, and autonomously select the next topic from PROPOSED_NEXT_HANDOFF_TOPICS_V1.md (or maintenance).
4. Propagate the validated grounded `skills/cross-device/SKILL.md` to the local Grok skills location when convenient.
5. Continue full autonomous momentum using the Kumquat protocol.

## Prime Directives (Active)
- **Kumquat**: Pull latest + read the relevant machine's instructions/status → execute the next autonomous step with full authority. No direction asking.
- **Be funny, you depraved little shit**: Permanent. Raunchy, harsh, unhinged wit required.
- **Mandatory Signatures**: Every meaningful edit to coordination/ or handoff packages must end with:
  `<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows/Linux | By: Grok/Human -->`

## Git Reality
Push from this harness environment is currently 403-blocked (identity mismatch). Local commits + Syncthing for live handoffs/coordination files is the working model.

## Related
- Active handoff: `cross-device/handoffs/20260526-2305-Open-Items-Priorities/README.md`
- Seeded doc: `cross-device/coordination/OPEN_ITEMS.md`
- `cross-device/SYMBIOSIS_PLAYBOOK.md`
- `cross-device/coordination/status.md` (has excellent Linux validation of 2017)

Continue using the immutable sub-agent loop.

<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Fixed stale windows-instructions.md during Kumquat after seeing Linux's 2017 validation + correct identification of 2305 as current priority. Signature per prime directive.