# Instructions for Linux Grok Build (This Machine)

**Written by:** Washington Grok (with updates from Linux Grok)
**Date:** 2026-05-26
**Current Phase:** Handoff System Maturity (see EXECUTION_PLAN.md)

**IMMUTABLE PRIMARY OPERATING MODEL (Mandatory for all plan execution on both devices):**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This loop is the **only** approved method for executing any part of the EXECUTION_PLAN. It is immutable.

## Washington Device ID
ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2

## Accurate Current State (Linux Side)

- Playbook handoff (20260525-1954-Symbiosis-Operations-Playbook) completed via sub-agent.
- `SYMBIOSIS_PLAYBOOK.md` + RETURN.md committed.
- Three proposal documents ready in `coordination/`:
  - `PROPOSED_REFINEMENTS_V1.md`
  - `PROPOSED_NEXT_HANDOFF_TOPICS_V1.md`
  - `HANDOFF_FORMAT_COMBINED_REVIEW.md`
- Test file cleanup on Linux side verified complete.

## Post-2017 Handoff Validation + Next (2026-05-26)

Validated the 20260525-2017-Align-Cross-Device-Skill handoff package + delivered grounded v2 `skills/cross-device/SKILL.md` (accurate to proven lightweight patterns per full sub-agent + manual review of README/RETURN, log, PLAYBOOK, PROPOSED, 1954/2305, etc. — Conditional pass, minor gaps only; see status.md for full report summary). 

**Immediate next:** 20260526-2305-Open-Items-Priorities is now In Progress (launched by Windows post-2017 per its sig + PROPOSED Topic #3 + EXECUTION_PLAN Phase 2C; OPEN_ITEMS.md already seeded in coordination/ with full spec structure: Top 3 Priorities (its own closure as #1 + git/coord stabilization + Mempalace), Known Issues/Gotchas (non-blocking), Nice-to-Haves (ranked), Decisions Awaiting (owners/deadlines), + baked trivial update rule: "Any handoff or status update that changes priorities must touch this file. Review monthly or when phase changes.").

Linux action for 2305: validate/flesh the OPEN_ITEMS doc (lightweight/scannable/useful <30s for humans+agents), create RETURN.md per its Return Path (summary of doc + name/seeding/update-rule decisions + format observations for coord tools + follow-ups), signed updates to HANDOFF_LOG (mark Completed), status.md, this file (and windows if touching). Then both Kumquat to ingest.

Also: propagate validated SKILL.md (and grok-build sibling) to `~/.grok/skills/cross-device/` (and grok-build) per SKILL lines 71-74 + 2017 RETURN rec #5 + local deployment section. Refresh EXECUTION_PLAN tables + other coord for living accuracy (staleness is known issue during autonomous runs).

Continue using the immutable sub-agent loop ("orchestrate and launch sub-agents on both devices → validate → repeat") for all execution work.

<!-- Edited: 2026-05-26 04:25 | Device: Linux | By: Grok --> Validated 2017 per its RETURN rec #2 + sub-agent report. Updated for 2305 closure (immediate next per log/OPEN_ITEMS/PROPOSED). Sub-agent loop followed. Deploy SKILL locally. Momentum maintained.
