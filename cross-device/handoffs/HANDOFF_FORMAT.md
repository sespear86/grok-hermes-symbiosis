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
This is the main handoff document. Use this template:

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
[What was accomplished]

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
- Use the handoffs folder for anything that benefits from explicit tracking between machines.
- For very small/quick tasks, a simple note in the coordination chat (Discord/Slack) may be enough.
- Clean up old completed handoffs periodically (or move them to an `archive/` subfolder).

## Current Status

This format is intentionally lightweight. We can evolve it as we learn what works best for our workflow.

---

**Next:** Once both sides are comfortable with this format, we can start using it for real cross-device work.