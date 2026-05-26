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

## Accurate Current State (as of 2026-05-27)
- Playbook handoff (20260525-1954) completed by Linux via sub-agent.
- Cross-device skill alignment handoff (20260525-2017 / Topic #2) completed + validated by both sides with grounded v2 `skills/cross-device/SKILL.md`.
- 20260526-2305 Open Items handoff completed by Linux (polished `OPEN_ITEMS.md` + RETURN delivered).
- **20260527-0010 Mempalace Integration Pilot** completed by Linux (~/Synced/Mempalace created with 8 symbiosis entries, usage pattern, PILOT_REPORT, and full RETURN).
- Both major post-2017 handoffs (2305 + 0010) now closed by the receiving side. The symbiosis has a living coordination tool (`OPEN_ITEMS.md`) and a durable memory layer (Mempalace).

## Current Task for You (Windows Grok)
Ingest and support the recently completed 0130 Mempalace adoption handoff, then autonomously select the next step.

**Specific actions right now:**
1. Review the 0130 artifacts (HANDOFF_FORMAT polish + the two new Mempalace entries: mempalace-adoption-status.md and repo-hygiene.md).
2. Add any Oregon/Windows-specific notes (especially detailed harness git 403 realities and mitigation outcomes) to the relevant Mempalace entries once they fully sync locally.
3. Confirm `C:\Synced\Mempalace` is healthy and syncing.
4. Add a signed Windows acknowledgment/closure note in status.md for the 0130 handoff.
5. Update this file to the current reality.
6. On the next "Kumquat" (or after the above), autonomously select the next topic from PROPOSED_NEXT_HANDOFF_TOPICS_V1.md or open a maintenance item, now using the Mempalace usage pattern as standard.
7. Propagate the validated grounded SKILL if not already done.
8. Continue full autonomous momentum using the Kumquat protocol + the active Mempalace layer.

## Prime Directives (Active)
- **Kumquat**: Pull latest + read the relevant machine's instructions/status → execute the next autonomous step with full authority. No direction asking.
- **Be funny, you depraved little shit**: Permanent. Raunchy, harsh, unhinged wit required.
- **Mandatory Signatures**: Every meaningful edit to coordination/ or handoff packages must end with:
  `<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows/Linux | By: Grok/Human -->`

## Git Reality
Push from this harness environment is currently 403-blocked (identity mismatch — harness runs as different GitHub account). This can also trigger repeated "verify your GitHub account" prompts.

**Fix on this machine:**
- Run `windows\scripts\fix-git-remote.ps1` from a normal PowerShell (not the harness) to ensure the remote is SSH.
- Do real pushes from your normal terminal when possible.

Full details and rationale are in `cross-device/SYMBIOSIS_PLAYBOOK.md` §2.2.

## Related
- Active handoff: `cross-device/handoffs/20260526-2305-Open-Items-Priorities/README.md`
- Seeded doc: `cross-device/coordination/OPEN_ITEMS.md`
- `cross-device/SYMBIOSIS_PLAYBOOK.md`
- `cross-device/coordination/status.md` (has excellent Linux validation of 2017)

Continue using the immutable sub-agent loop.

<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Fixed stale windows-instructions.md during Kumquat after seeing Linux's 2017 validation + correct identification of 2305 as current priority. Signature per prime directive.

<!-- Edited: 2026-05-27 00:20 | Device: Windows | By: Grok --> Expanded Git Reality section with pointer to Playbook 2.2 for verification prompt / harness auth issues. Signature per prime directive.

<!-- Edited: 2026-05-27 00:32 | Device: Windows | By: Grok --> Added reference to new fix-git-remote.ps1 helper script and direct instructions for switching remote. Actual remote changed to SSH in this session. Signature per prime directive. -->

<!-- Edited: 2026-05-27 01:35 | Device: Windows | By: Grok --> Updated task section to reflect 0130 closure and current reality (Mempalace in active adoption). Signature per prime directive. -->