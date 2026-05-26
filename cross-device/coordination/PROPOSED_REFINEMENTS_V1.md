# Proposed Handoff Format Refinements v1 (Linux Side)

**Date:** 2026-05-26
**Source:** Combined review of Linux sub-agent feedback + Windows sub-agent feedback + real usage from first two handoffs

## Recommendation
Adopt the following 5 lightweight, high-value improvements. They are additive and optional — the existing format remains fully usable even if none are adopted.

### 1. Explicit Handoff Lifecycle Guidance (High Value)
Add a short "Handoff Lifecycle" section under Guidelines:
- Create folder + README.md
- Sync to other side
- Receiving side executes + creates RETURN.md
- Both sides optionally note completion / follow-ups in coordination/status.md
- Optional: Archive older completed handoffs

### 2. Lightweight Agent-Oriented Sections (Highest Agent Utility)
Add an optional "Agent Context" block in the README template (frontmatter style or short section):

**Agent Context (Optional)**
- **Type:** (e.g., Design→Implement, Research→Artifact, Agent-to-Agent Execution, Human Review Needed)
- **Recommended Receiving Agent Invocation:** (e.g., "Use /grok-build with plan mode + reviewer loop" or "Hermes grok-build skill")
- **State Snapshot (at handoff creation):** (key open todos, recent decisions, git HEAD or branch)
- **Dependencies / Environment Notes:** (e.g., "Requires Syncthing running, access to shared Discord thread")
- **Escalation / Blockers Path:** (e.g., "If blocked > 4h, post [CROSS-DEVICE BLOCKER] in shared chat or create return handoff")

### 3. Encourage "Process & Format Observations" in RETURN.md
Add an encouraged (not required) subsection after "Recommended Next Steps":
- **Format & Process Observations** (What worked well? What felt off? Suggestions for next time?)

(This already happened organically in the first two handoffs and produced the highest-signal feedback.)

### 4. Clarify Supporting Files Convention
Add one sentence in Guidelines:
"Supporting artifacts (todos-export.md, plan.md, diffs/, screenshots, etc.) may be placed directly in the handoff folder or in a conventional `context/` subfolder. Prefer direct placement for small artifacts."

### 5. Timestamp Convention for IDs
Add note: "HHMM uses the local time of the machine creating the handoff."

## Adoption Guidance
- Keep changes additive and optional.
- Validate on the next 1–2 handoffs.
- Do not force use of new sections on simple handoffs.

These refinements close the gap between the current proven manual format and the agent-aware vision without adding ceremony when unused.