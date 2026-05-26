# Instructions for Linux Grok Build (This Machine)

**Written by:** Windows Grok (with updates from Linux Grok)
**Date:** 2026-05-26
**Current Phase:** Handoff System Maturity (see EXECUTION_PLAN.md)

**IMMUTABLE PRIMARY OPERATING MODEL (Mandatory for all plan execution on both devices):**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This loop is the **only** approved method for executing any part of the EXECUTION_PLAN. It is immutable.

## Windows Device ID
ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2

## Accurate Current State (Linux Side)

- Playbook handoff (20260525-1954-Symbiosis-Operations-Playbook) completed via sub-agent.
- `SYMBIOSIS_PLAYBOOK.md` + RETURN.md committed.
- Three proposal documents ready in `coordination/`:
  - `PROPOSED_REFINEMENTS_V1.md`
  - `PROPOSED_NEXT_HANDOFF_TOPICS_V1.md`
  - `HANDOFF_FORMAT_COMBINED_REVIEW.md`
- Test file cleanup on Linux side verified complete.

## Recommended Next Focus for the Windows Side

1. Have the user review the completed `SYMBIOSIS_PLAYBOOK.md`.
2. Review the two proposal documents together.
3. Decide on:
   - Which refinements (if any) to adopt into the handoff format now.
   - What the next real operational handoff should be.
4. Record the decision in `status.md` and here.

Continue using the immutable sub-agent loop for all execution work.
