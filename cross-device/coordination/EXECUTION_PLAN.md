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

---

## Phase 2A: Cleanup & Stabilization (Short)

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| C1 | Remove test files (`test-sync-from-*.txt`) from symbiosis repo on both machines | Linux Grok + Windows Grok | In Progress | Files no longer exist in repo on either side |
| C2 | Confirm handoffs folder is clean and ready for real use | Linux Grok | Pending | Folder contains only legitimate handoff packages + format docs |

---

## Phase 2B: Handoff Format Review & Refinement

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| H1 | Both sides independently review `HANDOFF_FORMAT.md` | Both users + Groks | Not Started | Written feedback collected from both sides |
| H2 | Compare feedback and agree on changes (if any) | Both Groks (via repo) | Not Started | Updated `HANDOFF_FORMAT.md` committed |
| H3 | Decide on first real operational handoff | Both sides | Not Started | Clear task chosen and written into coordination |

---

## Phase 2C: First Operational Handoff

| Task ID | Description | Owner | Status | Validation Criteria |
|---------|-------------|-------|--------|---------------------|
| O1 | Execute first real handoff using the (possibly refined) format | TBD | Not Started | Completed handoff with RETURN.md |
| O2 | Post-handoff review: What worked? What didn’t? | Both sides | Not Started | Written retrospective in repo |

---

## Phase 2D: Expand Scope (Optional but Recommended)

- Share additional joint project folders under `~/Synced/Projects` (or equivalent on Windows).
- Begin using the handoffs system for real ongoing work.

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

**Owner of this plan**: Linux Grok (Washington) – with input from Windows Grok.