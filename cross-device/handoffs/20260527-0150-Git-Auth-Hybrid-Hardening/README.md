# Handoff Package

**ID:** 20260527-0150-Git-Auth-Hybrid-Hardening
**From:** Oregon Windows
**To:** Washington Linux
**Date:** 2026-05-27
**Status:** In Progress

## Context

The symbiosis is now running with Mempalace as a permanent lightweight persistent memory layer (0010 pilot delivered + 0130 adoption handoff closed by Linux). The living `OPEN_ITEMS.md` has Git Auth + Hybrid Coordination Layer stabilization as Priority #2 (right behind active Mempalace adoption).

The recurring practical pain remains: the Windows harness environment frequently hits 403 on `git push` (different GitHub identity) and can trigger repeated "verify your GitHub account" prompts. We have mitigations in place (SSH remote switch + `windows/scripts/fix-git-remote.ps1` + preference for real pushes from personal shells), but these need to be properly documented, tested in practice, and captured in the Mempalace layer (especially git-gotchas.md and the new repo-hygiene.md).

## Task / Request

Harden and document the current Git authentication + hybrid coordination model so both sides have clear, living guidance and the recurring friction is minimized or at least fully understood.

**Specific work:**
- Document the full current mitigation stack (SSH remote, fix-git-remote.ps1, personal shell preference, harness limitations) with real outcomes and any remaining gotchas.
- Enrich the relevant Mempalace entries (git-gotchas.md + the new repo-hygiene.md from the 0130 work) with the latest practical experience from both machines.
- Capture any Windows-specific realities around the harness environment in the memory layer.
- Propose any next-level improvements (if real pain remains after the current mitigations) or confirm that the current stack is "good enough" for daily use.
- Produce a short decision record / hardening status note.

## Success Criteria
- The full current Git + hybrid model is clearly documented in the Mempalace layer and easy for both agents to reference during Kumquat or handoff work.
- The two new entries from the 0130 work (adoption-status + repo-hygiene) are enriched with real outcomes.
- Both sides have a shared, accurate picture of where we stand on this long-running pain point.
- Signed updates to HANDOFF_LOG, status, and the relevant instructions.

## Preferences / Constraints
- Keep it practical and high-signal (no theoretical architecture — focus on what actually works today in the harness + personal shell reality).
- Leverage the existing 0130 artifacts and the Mempalace usage pattern.
- No new heavy tooling unless it solves a real, measured problem.

## Handoff Notes

This is the highest-leverage "maintenance + hardening" handoff we can run right now while the Mempalace layer is fresh and the 0130 adoption work is just closed. It directly attacks one of the longest-standing sources of friction in the symbiosis.

## Return Path

When complete, create RETURN.md with:
- Summary of the current mitigation stack and real outcomes
- Key decisions / confirmations
- Any remaining pain points or proposed next improvements
- Observations on how the Mempalace layer helped during this work

Then do the usual signed updates.

## Relevant Memory (Mempalace)

- /symbiosis/git-gotchas.md
- /symbiosis/repo-hygiene.md (new from 0130)
- /symbiosis/mempalace-adoption-status.md (new from 0130)
- /symbiosis/three-primes.md
- /symbiosis/handoff-conventions.md
- /symbiosis/usage-pattern.md

<!-- Edited: 2026-05-27 02:05 | Device: Windows | By: Grok --> Launched this Git + hybrid hardening handoff as the clear next autonomous move after Linux closed the 0130 adoption work. Directly targets the #2 living priority in OPEN_ITEMS while the Mempalace layer is hot. Signature per prime directive. Keep er goinnnn. -->