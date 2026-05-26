# Mempalace Usage Pattern for Agents — Handoffs & Kumquat (Pilot Deliverable)

**From the 20260527-0010-Mempalace-Integration-Pilot**  
**Full details & entries:** `~/Synced/Mempalace/symbiosis/usage-pattern.md` (and the other 7 symbiosis/ entries + root README). This is the short reference version for quick ingestion during handoffs/Kumquat. Also cross-ref `cross-device/MEMPALACE_INTEGRATION.md`.

## The Lightweight Pattern (Fits Existing Workflow — Zero New Ceremony)
### Every Kumquat / Autonomous Trigger ("Kumquat" or "keep er goinnnn")
1. Pull latest from git (harness-bundled path on Windows if needed) + trust Syncthing for live `~/Synced/Mempalace/`, handoffs/, coordination/.
2. Read the nervous system:
   - `cross-device/coordination/linux-instructions.md` (or windows equivalent)
   - `cross-device/coordination/status.md`
   - `cross-device/coordination/OPEN_ITEMS.md` (Top 3 + issues + decisions; touch it on priority changes per baked rule)
3. **STANDARD MANDATORY STEP — Read relevant Mempalace persistent memory** (under `~/Synced/Mempalace/symbiosis/` on Linux / equivalent on Windows; formalized in 0130 adoption + HANDOFF_FORMAT):
   - Always: `three-primes.md`, `handoff-conventions.md`, `priorities.md`, `recent-decisions.md`, `playbook-location.md`
   - As needed: `device-ids-and-aliases.md`, `git-gotchas.md`, `usage-pattern.md` (this)
   - Grep-friendly for quick "query": e.g. `grep -r "403" ~/Synced/Mempalace/symbiosis/`
   (This is now the explicit durable context step in every Kumquat per the reinforced palace usage-pattern.md)
4. Execute via **immutable sub-agent loop** (orchestrate tools across devices/files → validate → repeat). Crank raunchy humor per prime #2. Append **exact mandatory signature** on every edit (prime #3).
5. On completion of handoff/major task: RETURN.md + updates to HANDOFF_LOG + status + instructions (with sigs + filth). Touch OPEN_ITEMS if priorities moved.

**Mempalace in Daily Kumquat Checklist (Post-0200 Formalization — Quick Reference, now the expected standard):**
- Pull/sync first (git + Syncthing for Mempalace layer).
- Read nervous system: linux-instructions.md (or windows) + status.md + OPEN_ITEMS.md (skim Top 3/Issues).
- **Ingest Mempalace (mandatory step 3):** Read relevant `~/Synced/Mempalace/symbiosis/` entries (core: three-primes, handoff-conventions, priorities, recent-decisions, playbook-location; + git-gotchas/device-ids if relevant; grep as needed). Non-negotiable.
- Execute (sub-agent loop + raunchy prime #2 + exact sigs).
- Close loop (RETURN + 3-file signed updates if handoff).
- For handoffs: always include `## Relevant Memory (Mempalace)` section in README (per updated HANDOFF_FORMAT.md).

### When Creating a Handoff (Sender Side)
- In the `README.md`, add a `## Relevant Memory (Mempalace)` section listing key paths (example from proposal):
  ```markdown
  ## Relevant Memory (Mempalace)
  - /symbiosis/three-primes.md
  - /symbiosis/handoff-conventions.md
  - /symbiosis/git-gotchas.md
  - /symbiosis/priorities.md (live source: cross-device/coordination/OPEN_ITEMS.md)
  - /symbiosis/recent-decisions.md
  ```
- Note the pilot + this usage in Handoff Notes or Agent Context.
- Add row to HANDOFF_LOG.md (In Progress).
- Drop signed update into status.md + instructions.md.

### When Receiving & Closing a Handoff (Receiver Side)
- Read the README + listed Mempalace paths + full coordination/ + OPEN_ITEMS first.
- Execute with sub-agents + loop + raunchy prime + signatures.
- Create `RETURN.md` (per HANDOFF_FORMAT + any pilot-specific Return Path in the README).
- Update HANDOFF_LOG (mark Completed), status.md (closure section), instructions (append note) — all with exact `<!-- Edited: ... -->` sigs + depraved wit.
- Both sides Kumquat to ingest.

## Why This Works (Pilot Observations — See Full PILOT_REPORT + RETURN)
- Extremely lightweight: plain synced .md files. No infra. Uses the exact same git + Syncthing that already powers everything.
- Survives resets/handoffs/sessions perfectly.
- Agents "query" by reading/grepping the explicit paths — trivial, reliable, auditable.
- Integrates seamlessly with Kumquat (the trigger) and the 3 primes (Kumquat execution, raunchy output, mandatory sigs).
- Complements (does not replace) OPEN_ITEMS (live priorities), PLAYBOOK (daily driver), handoff packages (tracked work), coordination/ (nervous system).
- Self-referential win: this pilot followed the pattern it was defining.

## Quick Start for Both Sides (Post-Pilot)
- On next Kumquat: `ls ~/Synced/Mempalace/symbiosis/` (or Windows equiv) + cat the core 5 files above.
- Future handoffs: always include Relevant Memory section.
- Maintenance: Add new entries as decisions emerge; update with sigs; keep raunchy and scannable.

**Pilot Status:** Delivered. 8 entries created. Usage documented here + in Mempalace. Ready for permanent adoption + refs in PLAYBOOK/SKILL/future handoffs.

**Cross-refs:** Full usage + all entries in `~/Synced/Mempalace/`; MEMPALACE_INTEGRATION.md; SYMBIOSIS_PLAYBOOK; SKILL.md; 0010 README/RETURN/PILOT_REPORT (this folder); 0130 adoption handoff (HANDOFF_FORMAT update + this reinforce); OPEN_ITEMS #1 (adoption).

---
<!-- Edited: 2026-05-27 01:35 | Device: Linux | By: Grok --> Created dedicated MEMPALACE_USAGE.md in the handoff folder as the explicit "document a simple usage pattern" deliverable. Summarizes the Kumquat + handoff flow with Mempalace reads baked in, cross-refs the full version in the palace, ties it to the 3 primes and sub-agent loop. This is the exact lightweight pattern the symbiosis needed — now both agents have a memory layer that doesn't ghost after a reset. Primes followed with extra raunch. Signature per prime directive. Keep er goinnnn. -->
<!-- Edited: 2026-05-27 03:10 | Device: Linux | By: Grok --> Light reinforce of Mempalace read as STANDARD MANDATORY STEP in the existing 0010 MEMPALACE_USAGE.md (to match the palace usage-pattern.md update from this 0130 handoff). Kept it high-signal, no bloat. Self-referential Kumquat discipline + primes + loop honored (read before edit, sig after). The pattern just got tighter and filthier. Signature per prime directive. Keep er goinnnn, you depraved pattern-fuckers. -->
