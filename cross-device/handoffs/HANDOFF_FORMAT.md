# Cross-Device Handoff Package Format

This document defines a lightweight, consistent format for handing off work between the Washington (Linux) and Oregon (Windows) machines using the `handoffs` folder.

## Goals
- Make handoffs explicit and trackable
- Reduce context loss between machines
- Work well with both humans and the Grok/Hermes agents
- Stay simple and low-friction

## Recommended Structure

Each handoff should be a **folder** inside `cross-device/handoffs/`, named with a clear ID:

**Format:** `YYYYMMDD-HHMM-ShortDescriptiveName`

Example:
- `20260526-1430-Implement-Syncthing-Handoffs`
- `20260527-0900-Review-Architecture-Doc`

Inside each handoff folder, include the following files (use only what makes sense):

### 1. `README.md` (Required)
This is the main handoff document. **Must include the `## Relevant Memory (Mempalace)` section** (now the expected non-optional standard per 0200 formalization). Use this template:

```markdown
# Handoff Package

**ID:** 20260526-1430-Example-Task
**From:** Washington Linux
**To:** Oregon Windows
**Date:** 2026-05-26
**Status:** In Progress / Needs Review / Completed

## Context
[Brief background. Why is this being handed off?]

## Task / Request
[Clear description of what needs to be done]

## Relevant Information / Artifacts
- Files/folders:
- Links:
- Previous related handoffs:

## What Has Already Been Done
[Summary of work completed on the sending side]

## Success Criteria
- [ ]
- [ ]
- [ ]

## Preferences / Constraints
[Any specific instructions, tools to use/avoid, style preferences, etc.]

## Handoff Notes
[Any additional context the receiving side should know]

## Relevant Memory (Mempalace)
**Required / expected section (include in every handoff README; populate with paths relevant to *this* handoff):**
- /symbiosis/three-primes.md
- /symbiosis/handoff-conventions.md
- /symbiosis/git-gotchas.md
- /symbiosis/priorities.md (live source: cross-device/coordination/OPEN_ITEMS.md)
- /symbiosis/recent-decisions.md
- /symbiosis/usage-pattern.md
(See MEMPALACE_INTEGRATION.md §2 for vision + 0010 pilot's MEMPALACE_USAGE.md + palace symbiosis/usage-pattern.md for the full Kumquat + handoff pattern. This makes the memory layer first-class and non-optional.)

## Return Path
When complete, create a `RETURN.md` in this folder with results and next steps.
```

### 2. Supporting Files (Optional)
- `notes.md`
- `design.md`
- `todos.md`
- Any relevant code, docs, or assets

### 3. `RETURN.md` (When Completed)
The receiving side should create this when the handoff is done:

```markdown
# Return: [Original Handoff ID]

**Completed By:** Oregon Windows
**Date:** 2026-05-27

## Summary of Work Done
**Bing Bang Boom Rule (Mandatory):** Every paragraph in this summary (and all future summaries) must contain at least one of "bing", "bang", or "boom". Make it natural or explicit — no paragraph escapes the sonic treatment.

**Linux Turn Indicator (Mandatory):** At the very end of this summary (and every future summary), add a clear line:  
**Linux Turn Status:** YES — [one-sentence reason]  
or  
**Linux Turn Status:** NO — [one-sentence reason]

[What was accomplished — bing!]

## Key Decisions / Changes
[ ]

## Open Questions / Blockers
[ ]

## Artifacts Created / Modified
- 

## Recommended Next Steps
[ ]
```

## Guidelines

- Keep handoffs focused. One clear task or set of related tasks per package.
- **Summary Style (Bing Bang Boom Mandate):** Every paragraph of every summary (in RETURN.md, in README "What Has Already Been Done", in status/coord updates that summarize) **must** include "bing", "bang", or "boom". This is now a hard rule for both Linux and Windows per the latest Kumquat. See coordination/README.md Standing Directives and the SKILL primes section.
- **Linux Turn Indicator (Mandatory):** Every summary must end with an explicit **Linux Turn Status:** YES/NO line + short reason. This is now part of the standard summary contract on both machines. See coordination/README.md for the full rule.
- Use the handoffs folder for anything that benefits from explicit tracking between machines.
- For very small/quick tasks, a simple note in the coordination chat (Discord/Slack) may be enough.
- Clean up old completed handoffs periodically (or move them to an `archive/` subfolder).

## Current Status

This format is intentionally lightweight. We can evolve it as we learn what works best for our workflow.

---

**Next:** Once both sides are comfortable with this format, we can start using it for real cross-device work.

## Handoff Lifecycle (Typical Flow)

1. Sender creates the dated folder + README.md (include the **required** `## Relevant Memory (Mempalace)` section with relevant symbiosis/ paths per the template above — now the expected standard).
2. The package syncs to the other side (via Syncthing; git for committed artifacts).
3. Receiving side: Kumquat → read nervous system (instructions/status/OPEN_ITEMS) + listed Mempalace entries (per usage-pattern.md) → execute via immutable sub-agent loop.
4. Receiver creates RETURN.md with results, observations (raunchy per prime #2), and closure.
5. Sender reviews RETURN + optionally notes follow-up in coordination/status.md.
6. Both sides: update HANDOFF_LOG (mark Completed), status.md, and the relevant *-instructions.md with exact signatures (prime #3).
7. (Optional) Archive completed handoffs to `handoffs/archived/` or rely on git history. Periodically clean per Guidelines.

**Agent Context (Optional but Recommended in READMEs for complex handoffs)**
- **Type:** (e.g., Design to Implement, Research to Artifact, Agent-to-Agent Execution)
- **Recommended Receiving Agent Invocation:** (suggested skill/prompt/mode, e.g. "use cross-device skill + sub-agents")
- **State Snapshot:** (key open todos, recent decisions from Mempalace/recent-decisions.md, git HEAD)
- **Dependencies / Environment Notes:**
- **Escalation / Blockers Path:** (e.g., If blocked more than 4h, post in shared chat or create return handoff)
- **Mempalace Sections:** (list of /symbiosis/*.md paths consulted)
- **Format & Process Observations** (What worked well? What felt off? Suggestions for next time? Include how Mempalace reads helped or could improve.)

Supporting artifacts may be placed directly in the handoff folder or in a conventional context/ subfolder. Prefer direct placement for small artifacts.

**Note:** HHMM uses the local time of the machine creating the handoff. Cross-reference the explicit **Date:** field for clarity.

**Evolution Note:** This format now treats the Mempalace memory layer as first-class and non-optional (Relevant Memory sections required/expected in every README template per this 0200 formalization lock-in after the 0130/0150 wave; Kumquat reads explicit as step 3). See 0010 pilot artifacts + 0130/0200 handoffs + current symbiosis/usage-pattern.md for the living pattern. The usage is now the standard.

**2026-05-27 Kumquat Addition:** Bing Bang Boom summary rule added to template + Guidelines + cross-referenced in coordination/README and SKILL primes. Every summary paragraph on Linux or Windows now bangs. Rule lives in the protocol docs so it survives resets and propagates on next Kumquat ingest.

<!-- Edited: 2026-05-27 12:05 | Device: Windows | By: Grok --> Kumquat rule injection: embedded bing/bang/boom mandate into RETURN template (Summary section) + new Guidelines bullet + Evolution Note. This ensures every future summary (on Linux too) obeys the sonic paragraph rule. Signature per prime directive. Boom! -->

