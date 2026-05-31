# Cross-Device Symbiosis Execution Plan (Current Phase)

**Goal**: Move from setup/testing into reliable, operational use of the cross-device Grok-Hermes symbiosis.

**Current Focus**: Handoff System Maturity + First Operational Use

**Date Started**: 2026-05-26

---

## Guiding Principles
- One small, verifiable step at a time.
- Use the repo (`cross-device/coordination/`) as the primary communication channel between the two Groks.
- Validate every major step before moving on.
- Keep human effort as low as possible.

## Primary Operating Model (Immutable)

**This exact loop is the ONLY approved method for executing any part of the plan on both devices. It is immutable.**

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

Any deviation requires explicit joint agreement recorded in the coordination files.

---

## Phase 2A: Cleanup & Stabilization (Short)

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| C1 | Remove test files (`test-sync-from-*.txt`) from symbiosis repo on both machines | Linux Grok + Windows Grok | Linux: Done (verified clean); Windows: Pending confirmation | Files no longer exist in repo on either side |
| C2 | Confirm handoffs folder is clean and ready for real use | Linux Grok | Pending | Folder contains only legitimate handoff packages + format docs |

---

## Phase 2B: Handoff Format Review & Refinement

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| H1 | Both sides independently review `HANDOFF_FORMAT.md` | Both users + Groks | Done (Linux detailed + Windows sub-agent + combined review) | Written feedback collected from both sides |
| H2 | Compare feedback and agree on changes (if any) | Both Groks (via repo) | Done (via PROPOSED_REFINEMENTS_V1.md) | Updated `HANDOFF_FORMAT.md` committed |
| H3 | Decide on first real operational handoff | Both sides | Done (via PROPOSED_NEXT_HANDOFF_TOPICS_V1.md â€” Playbook #1 recommended) | Clear task chosen and written into coordination |

---

## Phase 2C: First Operational Handoff

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| O1 | Execute first real handoff using the (possibly refined) format | TBD | Not Started | Completed handoff with RETURN.md |
| O2 | Post-handoff review: What worked? What didnâ€™t? | Both sides | Not Started | Written retrospective in repo |

---

## Phase 2D: Expand Scope (Optional but Recommended)

- Share additional joint project folders under `~/Synced/Projects` (or equivalent on Windows).
- Begin using the handoffs system for real ongoing work.

---

## Phase 2E: Memory Layer (Mempalace) Integration

**Goal**: Introduce Mempalace as a shared, persistent, long-term memory layer across both machines. This directly strengthens the "one extended machine" feeling by reducing context loss over time and making handoffs richer.

### Why It Fits Here
- Once the handoff system (2B/2C) is stable and we're expanding scope (2D), adding persistent shared memory is the highest-leverage next capability.
- Mempalace can be referenced inside handoff packages, the Playbook, and coordination files.
- Both Grok and Hermes instances can eventually query it during handoffs, reducing the need to re-explain context.

### Tasks

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| M1 | Set up Mempalace on both machines and ensure it syncs via existing Syncthing + repo setup | Both | Windows: Canonical location finalized at C:\Users\spear\grok-hermes-symbiosis\Mempalace. Folder live in Syncthing at correct path (Label cleaned to 'Mempalace (symbiosis)', legacy ID accepted for now). Oregon note migrated. Local Windows side of M1 functionally complete. Content check performed 2026-05-27: No files from Linux have arrived yet. | Linux side needs to confirm their Mempalace share is active and healthy for bidirectional sync to occur. |
| M2 | Define lightweight integration points with the handoff format | Both Groks | Not Started | Documented (e.g., new section in HANDOFF_FORMAT.md or separate memory-integration note) |
| M3 | Pilot: Reference or attach relevant Mempalace sections in 1â€“2 handoffs | Both | Not Started | At least one handoff successfully uses memory context |
| M4 | Evaluate impact and refine integration approach | Both | Not Started | Written retrospective + updates to Playbook and coordination docs |

### Deeper Integration (Future â€“ Phase 4)
- Full sub-agent querying of Mempalace during handoff creation and execution.
- Shared long-term memory between the two Grok + Hermes instances.
- Dedicated memory palace sections for project conventions, past decisions, agent preferences, and recurring patterns.

---

## Coordination Rules

- All task status updates go through `status.md`.
- The Grok responsible for a task updates the relevant instruction file and status.
- Humans trigger their local Grok using the agreed prompts when they are ready for the next step.
- Major decisions (format changes, new shared folders, etc.) should be recorded.

---

## Success Criteria for This Phase

- Test files removed from both machines.
- Handoff format has been used at least twice with real work.
- Both humans and agents feel the handoff process is reasonably smooth.
- We have a repeatable way to move work between machines without high cognitive load.

---

**Owner of this plan**: Linux Grok (Washington) â€“ with input from Windows Grok.
<!-- Edited: 2026-05-27 15:40 | Device: Windows | By: Grok --> Advanced M1 on Oregon: Created local Mempalace skeleton + seeded first Oregon note (oregon-syncthing-stabilization-2026-05-27.md), confirmed Syncthing stable and launched UI for folder addition. Updated table to reflect Windows prep complete, full sync pending UI action + Linux side. Directly supports OPEN_ITEMS #1 and Phase 2E. Signature per prime directive. Keep er goinnnn. Boom! -->


<!-- Edited: 2026-05-27 15:55 | Device: Windows | By: Grok --> Kumquat continuation: Approved and actioned new canonical Mempalace location inside the symbiosis repo (C:\Users\spear\grok-hermes-symbiosis\Mempalace) for better organization alongside the repo and handoffs. Migrated the Oregon stabilization note. Updated M1 status in plan. User is adding the folder in Syncthing UI with the new path. Directly advances OPEN_ITEMS #1 and Phase 2E M1. Signature per prime directive. Keep er goinnnn. Boom! -->


<!-- Edited: 2026-05-27 16:05 | Device: Windows | By: Grok --> Kumquat continuation: Finalized Mempalace location inside the symbiosis repo per user approval. Updated plan M1 to reflect migration complete and UI folder addition in progress. Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:15 | Device: Windows | By: Grok --> Continued Kumquat: Confirmed via config that Mempalace folder is already live in Syncthing at the new canonical path (legacy ID present). Updated plan M1 accordingly and prepared cleanup guidance. Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:20 | Device: Windows | By: Grok --> Next step in Kumquat/plan: Confirmed Mempalace folder is already active in Syncthing. Updated M1 status and prepared UI cleanup guidance. Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:25 | Device: Windows | By: Grok --> Executed next micro-action: Brought living plan up to date with actual Syncthing state (Mempalace share already active at correct path). Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:30 | Device: Windows | By: Grok --> User confirmed Label cleanup in Syncthing UI. Updated M1 to reflect Windows side is now functionally complete. Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:45 | Device: Windows | By: Grok --> Continued plan execution: Made the Linux-side dependency for M1 sync explicit in the living plan. Signature per prime directive. Keep er goinnnn.


<!-- Edited: 2026-05-27 16:55 | Device: Windows | By: Grok --> Content check performed on Mempalace. No incoming files from Linux yet. Plan M1 updated with latest state. Signature per prime directive. Keep er goinnnn.
