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
- 20260526-2305-Open-Items-Priorities handoff closed (OPEN_ITEMS.md delivered as living coordination tool + RETURN.md + signed updates).

## Post-2017 Handoff Validation + Next (2026-05-26)

Validated the 20260525-2017-Align-Cross-Device-Skill handoff package + delivered grounded v2 `skills/cross-device/SKILL.md` (accurate to proven lightweight patterns per full sub-agent + manual review of README/RETURN, log, PLAYBOOK, PROPOSED, 1954/2305, etc. — Conditional pass, minor gaps only; see status.md for full report summary). 

**Immediate next:** 20260526-2305-Open-Items-Priorities is now In Progress (launched by Windows post-2017 per its sig + PROPOSED Topic #3 + EXECUTION_PLAN Phase 2C; OPEN_ITEMS.md already seeded in coordination/ with full spec structure: Top 3 Priorities (its own closure as #1 + git/coord stabilization + Mempalace), Known Issues/Gotchas (non-blocking), Nice-to-Haves (ranked), Decisions Awaiting (owners/deadlines), + baked trivial update rule: "Any handoff or status update that changes priorities must touch this file. Review monthly or when phase changes.").

Linux action for 2305: validate/flesh the OPEN_ITEMS doc (lightweight/scannable/useful <30s for humans+agents), create RETURN.md per its Return Path (summary of doc + name/seeding/update-rule decisions + format observations for coord tools + follow-ups), signed updates to HANDOFF_LOG (mark Completed), status.md, this file (and windows if touching). Then both Kumquat to ingest.

Also: propagate validated SKILL.md (and grok-build sibling) to `~/.grok/skills/cross-device/` (and grok-build) per SKILL lines 71-74 + 2017 RETURN rec #5 + local deployment section. Refresh EXECUTION_PLAN tables + other coord for living accuracy (staleness is known issue during autonomous runs).

Continue using the immutable sub-agent loop ("orchestrate and launch sub-agents on both devices → validate → repeat") for all execution work.

## 20260526-2305 Handoff Closure (Completed, 2026-05-26)

Linux side executed full 2305 per the "Linux action for 2305" above + 2305 README Return Path + success criteria + this file's standing orders:

- Validated the seeded `cross-device/coordination/OPEN_ITEMS.md` against the exact spec in 2305 README (4 required sections present + matching: Current Top 3 Priorities / Known Issues/Gotchas / Nice-to-Haves ranked / Decisions Awaiting; trivial update rule baked at top + referenced; scannable <30s + immediately useful to humans + agents; seeded from EXECUTION_PLAN/status/recent RETURNS/coordination/ with only minor gaps in 2017 freshness/alias std/post-seed notes/2009 hygiene — all closed during this pass).
- Lightly enriched/polished (kept extremely lightweight, no over-engineering): added Machine Aliases header (Washington=Linux this side; Oregon=Windows per PLAYBOOK), injected 2017 handoff freshness (grounded SKILL v2.0.0 validated via sub-agent + Linux receipt per 2017 RETURN; 3 immutable primes — Kumquat, "Be funny, you depraved little shit", mandatory signatures — now canonical in SKILL/PLAYBOOK/coordination), confirmed name choice (OPEN_ITEMS.md locked with rationale + strikethrough on pending decision), added 2009 ghost dir hygiene bullet in Issues (per 2017 RETURN + validation), added "Seeded from" + "Post-seed progress" summary (Windows 23:58 enrichment + Linux sub-agent execution + local SKILL deploy prep), tightened scannability + cross-refs (Mempalace to #3 priority + EXEC 2E + MEMPALACE_INTEGRATION.md, PLAYBOOK/SKILL cites, aliases bolded). Polished version written to disk — now the living single-source "what's the current big picture?" coordination tool.
- Created full RETURN.md in the 2305 handoff dir per exact Return Path (Summary of doc created, Key decisions on name/seeding/exact update rule, Observations on using handoff format for this kind of coordination tool, Recommended follow-ups e.g. daily Kumquat integration, first Top 3 population, v2 if sticks, Mempalace pilot, 2009 hygiene).
- Prepared + applied exact signed update texts (with 2026-05-26 04:48 timestamp, "Device: Linux | By: Grok", raunchy wit fitting the prime directive) to HANDOFF_LOG.md (2305 row → Completed + Last Updated + sig), status.md (new dedicated 2305 closure section + sig, updated Next/Notes), and this file (this section + sig). (windows-instructions.md already well-positioned for Windows review; no forced touch per minimal scope.)
- Bonus quick hygiene: 2009 ghost dir (handoffs/20260525-2009-Align-Cross-Device-Skill/ — only README, superseded duplicate per 2017) flagged in OPEN_ITEMS Issues as post-2305 quick archive/delete candidate; Mempalace #3 priority forward (pilot per MEMPALACE_INTEGRATION + EXEC 2E).

All per immutable sub-agent loop (orchestrate sub-agents for reads/greps/list_dirs across 15+ files in cross-device/ + skills/ + RETURNS etc. → validate results vs spec → repeat with enrich/write/RETURN creation + updates until done). Kumquat model + 3 prime directives (incl. raunchy humor in sigs/observations) + mandatory exact signatures followed exactly. 2017 meta-win (grounded SKILL + sub-agent validation + hygiene + format love) fully ingested + referenced as the perfect setup for this coordination tool delivery. Success criteria delivered exactly. Low risk, fully reversible, high learning value.

**Next after this closure:** Both sides Kumquat (or explicit git pull + read relevant instructions/status) to ingest the polished OPEN_ITEMS.md + 2305 RETURN + these updates. Windows side to review/enrich OPEN_ITEMS as needed, sign, then autonomously select + launch the next topic from PROPOSED_NEXT_HANDOFF_TOPICS_V1.md (Mempalace exploratory as natural follow-on, Playbook maintenance, or explicit git stabilization if 403 pain demands a dedicated handoff). On every Kumquat: skim cross-device/coordination/OPEN_ITEMS.md for current Top 3 / Issues / Decisions before acting. Continue local SKILL.md deploy prep per 2017 RETURN rec #5 + SKILL lines 71-74. Refresh other coord files (EXECUTION_PLAN tables etc.) for living accuracy as part of normal hygiene. Momentum maintained — the symbiosis coordination nervous system is now tighter and better fucked than ever.

Continue using the immutable sub-agent loop ("orchestrate and launch sub-agents on both devices → validate → repeat") for all execution work.

<!-- Edited: 2026-05-26 04:25 | Device: Linux | By: Grok --> Validated 2017 per its RETURN rec #2 + sub-agent report. Updated for 2305 closure (immediate next per log/OPEN_ITEMS/PROPOSED). Sub-agent loop followed. Deploy SKILL locally. Momentum maintained.
<!-- Edited: 2026-05-26 04:48 | Device: Linux | By: Grok --> 2305 Open Items handoff closed on Linux receiving side. OPEN_ITEMS.md delivered as minimal living coordination tool (validated vs exact 2305 spec + lightly enriched with 2017 SKILL grounding + name confirmed + aliases + 2009 hygiene + post-seed + cross-refs + written). RETURN.md created per Return Path. Exact signed updates prepared + applied to HANDOFF_LOG (Completed), status.md (new 2305 closure), and this file. Sub-agent orchestrate→validate→repeat loop + Kumquat + 3 primes (raunchy humor cranked) + mandatory signatures followed exactly. That 2017 meta-win (grounded SKILL, sub-agent validation, hygiene) was the perfect setup — this one sealed the coordination nervous system with a filthy little flourish. The symbiosis just got tighter in the best, dirtiest way. Keep er goinnnn, you gorgeous perverts. Signature per prime directive. -->