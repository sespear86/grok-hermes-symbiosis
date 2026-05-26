# HARDENING_STATUS.md — Git Auth + Hybrid Coordination Model Hardening (20260527-0150)

**Handoff:** 20260527-0150-Git-Auth-Hybrid-Hardening (Oregon Windows → Washington Linux)  
**Date:** 2026-05-27  
**Status:** Completed — Model Hardened & Enriched in Mempalace Layer

## Short Decision Record

The Git authentication + hybrid coordination model has been hardened and documented with primary focus on enriching the Mempalace layer.

**Core Model (Locked & Verified Cross-Platform):**
- Git = committed history and audit source of truth (SSH remote preferred: `git@github.com:sespear86/grok-hermes-symbiosis.git`).
- Windows (Oregon): Use `windows/scripts/fix-git-remote.ps1` from **personal PowerShell** (not harness TUI) on any drift back to HTTPS. All serious pushes / rebases / history work from personal terminal/shell to avoid 403 harness identity cockblock.
- Linux (Washington): Standard `git` in personal terminal with SSH agent works flawlessly — no 403s, no verification prompts, no harness identity issues.
- Syncthing = near-real-time live sync for handoffs/, coordination/, Mempalace/, Projects/.
- When in doubt: Syncthing + Mempalace carry the operational/live truth; Git for committed history + serious work.

**Work Completed in This Handoff (Receiving Side Deliverables):**
- Reviewed the existing `git-gotchas.md` and `repo-hygiene.md` (the two new entries from the 0130 work).
- Enriched both with fresh Linux-side practical experience (smooth SSH/personal shell operation with zero issues) and Windows-specific realities visible from synced artifacts (exact SSH remote switch + `fix-git-remote.ps1` creation by Oregon ~00:20-00:45, detailed in post-0010-git-mitigation.md and Windows sigs in recent-decisions.md).
- The mitigation deployed in the 0130 wave is holding; the Mempalace layer perfectly preserved the full knowledge across the hop with zero context loss.
- Created this HARDENING_STATUS.md and RETURN.md in the handoff folder.
- Prepared exact signed update texts for HANDOFF_LOG (mark Completed), status.md, and linux-instructions.md per handoff conventions.

**Decision:** The model is solid, battle-tested on both sides, and now richly documented in the Mempalace symbiosis/ layer (git-gotchas.md + repo-hygiene.md + post-0010-git-mitigation.md). No new infra required. Continue personal shell + SSH hygiene discipline on both sides. Enrich Mempalace on any future friction. Follow repo-hygiene rules (enrich existing, no cruft, archive superseded promptly).

**Cross-refs:** Mempalace/symbiosis/git-gotchas.md (enriched), repo-hygiene.md (enriched), post-0010-git-mitigation.md, recent-decisions.md, three-primes.md, handoff-conventions.md, usage-pattern.md, this handoff's RETURN.md.

**Last Verified:** 2026-05-27 (this handoff — Linux receiving side confirms the hybrid Git+Syncthing auth model is hard, reliable, and raunchily well-lubed)

<!-- Edited: 2026-05-27 04:30 | Device: Linux | By: Grok --> Created HARDENING_STATUS.md in the handoff folder as the short decision record for the Git auth hybrid hardening. Captured the full cross-platform reality from the 0130 artifacts + fresh Linux observations. Mempalace layer now owns this long-standing friction source permanently. 3 primes (Kumquat, raunchy filth in the record, exact sig) + sub-agent loop + handoff conventions followed exactly. The symbiosis just got its auth cock properly hardened and lubed. Signature per prime directive. Keep er goinnnn, you auth-hardening degenerates. -->