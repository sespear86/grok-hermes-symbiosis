# Instructions for Washington Grok Build

**Written by:** Linux Grok
**Date:** 2026-05-26
**Current Phase:** Handoff System Maturity (see EXECUTION_PLAN.md)

**IMMUTABLE PRIMARY OPERATING MODEL (Mandatory for all plan execution on both devices):**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This loop is the **only** approved method for executing any part of the EXECUTION_PLAN. It is immutable.

## Known Device IDs
- **Washington (this machine):** ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2
- **Linux (Oregon):** RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD

## Accurate Current State (as of 2026-05-26)
- Linux side has completed the Playbook handoff (20260525-1954-Symbiosis-Operations-Playbook) via sub-agent.
- `SYMBIOSIS_PLAYBOOK.md` + RETURN.md are committed.
- We have three proposal documents ready in `coordination/`:
  - `PROPOSED_REFINEMENTS_V1.md`
  - `PROPOSED_NEXT_HANDOFF_TOPICS_V1.md`
  - `HANDOFF_FORMAT_COMBINED_REVIEW.md`

## Current Task for You (Washington Grok)
Guide your user through reviewing the completed Playbook and the two proposal documents.

**Specific actions:**
1. Present `SYMBIOSIS_PLAYBOOK.md` to the user for review.
2. Walk through `PROPOSED_REFINEMENTS_V1.md` and `PROPOSED_NEXT_HANDOFF_TOPICS_V1.md`.
3. Collect the user's feedback on:
   - The Playbook itself
   - Which refinements (if any) to adopt now
   - Which next handoff topic to tackle next
4. Record the feedback and decision in this file and in `status.md`.
5. Once decided, either open the next handoff package or propose specific edits to `HANDOFF_FORMAT.md`.

Continue using the immutable sub-agent loop for execution on your side.

Reference `EXECUTION_PLAN.md` for the full current phase breakdown.
