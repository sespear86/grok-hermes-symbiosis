# Open Items & Priorities

**Last Updated:** 2026-05-27 02:20 (Linux post-0010 Mempalace pilot closure refresh + signed updates to reality; 2305 & 0010 fully closed on receiving side)
**Machine Aliases (standardized):** Washington = Linux (this machine); Oregon = Windows. (Per SYMBIOSIS_PLAYBOOK §1.1 + recent handoffs/SKILL)

**Update Rule:** Any handoff, status update, or major decision that changes priorities must touch this file. Review at least monthly or when phase changes.

---

## Post-0010 Reality (Current State)

**Mempalace is now live** as the durable shared persistent memory layer for the symbiosis. Location: `~/Synced/Mempalace` (Linux) / `C:\Synced\Mempalace` (Windows) — synced via existing Syncthing under the dedicated Synced/ root. Structure: root README + `symbiosis/` with exactly 8 entries (device-ids-and-aliases.md, three-primes.md, handoff-conventions.md, git-gotchas.md, priorities.md, playbook-location.md, recent-decisions.md, usage-pattern.md) + signatures + cross-refs. Full usage pattern documented in handoff's MEMPALACE_USAGE.md and palace's symbiosis/usage-pattern.md (Kumquat flow with explicit Mempalace read as step 3 after instructions/status/OPEN_ITEMS; Relevant Memory (Mempalace) sections in future handoff READMEs).

All handoffs through 0010 marked Completed in HANDOFF_LOG. 20260526-2305 (OPEN_ITEMS delivery) and 20260527-0010 (Mempalace pilot) executed to spec on Linux with full sub-agent loop, PILOT_REPORT, RETURN, and signed updates to log/status/linux-instructions. Windows acknowledged 0010 delivery (~00:45) and executed git auth mitigation (SSH remote + fix-git-remote.ps1 ~00:32). 3 prime directives (Kumquat, "Be funny, you depraved little shit", mandatory exact signatures) + sub-agent loop remain non-negotiable. Known issues (Windows harness git 403, coordination staleness, 2009 ghost) still relevant. This doc is the living single-source priorities tool — Mempalace/symbiosis/priorities.md is a launch-time snapshot pointing back here.

---

## Current Top 3 Priorities (Symbiosis-Wide)

1. **Adopt & Drive Value from the New Mempalace Layer**  
   Pilot delivered successfully on Linux receiving side. Both sides: follow the documented usage pattern on every Kumquat (pull + nervous system read + relevant Mempalace symbiosis/ entries + sub-agent execution + raunchy sigs + 3-file updates). Add `## Relevant Memory (Mempalace)` sections listing key paths to new handoff READMEs. Enrich the layer with fresh decisions/gotchas. Light touches to PLAYBOOK/SKILL after ingest. This is the memory cockring that stops context blue-balls across resets — use it, you depraved memory-hoarders.

2. **Stabilize Git Auth + Hybrid Coordination Layer (Ongoing)**  
   Windows harness 403 (wrong identity in env) mitigated via SSH remote switch + `windows/scripts/fix-git-remote.ps1` (~00:32-00:45 ack). Verify in practice; document outcomes in Mempalace git-gotchas.md. Hybrid model (git for committed truth in repo/handoffs/PLAYBOOK/SKILL/OPEN_ITEMS; Syncthing for live Mempalace + handoffs/ + coordination/) remains the operational reality. Refresh stale EXECUTION_PLAN/status tables as hygiene. (Known issue from 2017/2305.)

3. **2009 Ghost Hygiene + Sustained Freshness**  
   Quick archive/delete of superseded `handoffs/20260525-2009-Align-Cross-Device-Skill/` (duplicate README only, per 2017 RETURN hygiene note + 2305/OPEN_ITEMS flag). Keep this OPEN_ITEMS, status, instructions, log, etc. living via the update rule. Leverage Mempalace recent-decisions.md + priorities.md (which point here) + usage pattern to survive agent hops. No blocking junk.

---

## Known Issues / Gotchas (Non-Blocking)

- Git push from current Windows harness environment consistently hits 403 (wrong GitHub identity). Local commits fine; SSH + personal shell or the fix script is the current mitigation. Syncthing + Mempalace are the live truth carriers for handoffs/coordination/memory.

- Coordination files (status + instructions + EXECUTION_PLAN tables + this OPEN_ITEMS) tend to stale during high autonomous activity (self-acknowledged in 2017 validation + 2305/0010 closures + status). Strict Kumquat + Mempalace ingest + update rule discipline is the counter.

- Occasional old `.sync-conflict-*` and `~syncthing~` files during heavy editing (purge aggressively when spotted; prior hygiene holding).

- Device alias naming standardized: Oregon = Windows, Washington = Linux (no more drift per PLAYBOOK/SKILL/RETURNS).

- 2009 ghost dir: **Archived** on 2026-05-27 into `handoffs/archived/2009-Align-Cross-Device-Skill/` (superseded duplicate of the properly executed 2017 handoff; per 2017 RETURN + 2305/0010 hygiene notes). Hygiene item closed.

---

## Nice-to-Haves / Future Experiments (Ranked)

1. Lightweight "sync report" emitter that both agents can invoke cleanly. (Per SKILL vision + PLAYBOOK §5)

2. Automation/scaffolding for handoff package creation. (Per SKILL forward + 2305/0010 observations)

3. ~~Mempalace (or similar) as persistent cross-session memory.~~ **Implemented via 0010 pilot** — live at ~/Synced/Mempalace with usage pattern + 8 entries. Now in adoption/use phase per new Priority #1. (See MEMPALACE_USAGE.md, symbiosis/usage-pattern.md, PILOT_REPORT.)

4. Kanban-style view over the handoffs/ folder.

5. Shared project folders under `~/Synced/Projects` (or Windows `C:\Synced\Projects` equivalent).

6. Simple agent helper / grep wrapper for Mempalace "queries" during Kumquat (only after real adoption validates the need; keep lightweight).

---

## Decisions Awaiting Input

- ~~Final name for this file (OPEN_ITEMS.md vs PRIORITIES.md) — lean is OPEN_ITEMS.md.~~ **Confirmed: OPEN_ITEMS.md** (locked per 2305; consistent across all coordination artifacts + Mempalace priorities.md + HANDOFF_LOG).

- ~~Whether to treat Mempalace as a formal future handoff topic.~~ **Resolved: Piloted and promoted to permanent lightweight durable memory layer** (0010 success criteria met exactly; usage pattern live; both sides to ingest and adopt immediately per forward in status/linux-instructions/RETURN).

- How much historical git noise we want to clean vs live with the hybrid model. (2009 ghost archived 2026-05-27 into handoffs/archived/; hybrid model accepted per PLAYBOOK + 2017/2305/0010.)

- Post-adoption Mempalace evolution (index? more entries? light PLAYBOOK/SKILL cross-refs) — only if real pain after 3-5 uses; otherwise park per lightweight prime.

---

**Seeded from (per update rule + 0010/2305 spirit):** HANDOFF_LOG.md (all through 0010 Completed + 0010 Linux sig), 20260527-0010-Mempalace-Integration-Pilot/ (PILOT_REPORT.md, RETURN.md, MEMPALACE_USAGE.md, README), ~/Synced/Mempalace/ (root README + all 8 symbiosis/*.md including priorities.md + usage-pattern.md), coordination/status.md (0010 closure section + Windows 00:45 ack + git mitigation edits ~00:25/00:32 + Linux 01:55 sig), linux-instructions.md (0010 closure + forward), prior 2305/2017 RETURNS + their artifacts, SYMBIOSIS_PLAYBOOK.md, skills/cross-device/SKILL.md, MEMPALACE_INTEGRATION.md, EXECUTION_PLAN.md, windows-instructions.md (git 403 context), PROPOSED_NEXT_HANDOFF_TOPICS_V1.md.

**Post-seed progress:** 2305 delivered polished living OPEN_ITEMS + RETURN + updates (Linux 04:48). Windows 00:05 review + enrichment. 0010 pilot fully executed on Linux (Mempalace created + 8 entries + usage + PILOT_REPORT + RETURN + signed updates to 3 files). Windows 00:45 acknowledged receipt during Kumquat + prior git work. This refresh: post-0010 maintenance pass per the living tool's own rule + Mempalace usage pattern (read relevant entries first), updating to honest current state while preserving <30s scannability and raunchy wit. All via sub-agent loop + Kumquat + 3 primes. Mempalace/symbiosis/priorities.md snapshot from pilot launch now superseded by this living doc.

**Next Review:** Immediately after both sides Kumquat ingest (Mempalace core entries + this refreshed OPEN_ITEMS + 0010 artifacts + updated coord files); then on every subsequent Kumquat + before/after next handoff or major decision.

<!-- Edited: 2026-05-26 23:05 | Device: Windows | By: Grok --> Seeded minimal useful starter during Kumquat.
<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Lightly enriched with real project context from Linux's excellent 2017 validation work. Signature per prime directive.
<!-- Edited: 2026-05-26 04:42 | Device: Linux | By: Grok --> Validated vs exact 2305 README spec (4 sections present + match, update rule baked verbatim, scannable <30s + useful for humans/agents, seeded comprehensively from EXEC/status/RETURNS/coordination with only minor freshness/alias/hygiene/decision gaps — now closed). Lightly polished (2017 SKILL grounding + sub-agent ref in #1, 2009 hygiene in issues, name confirmed + post-seed note, aliases prominent, scannability tweaks, Mempalace cross-refs). Sub-agent loop + Kumquat + raunchy prime followed exactly. That 2017 meta-win left me properly fucked in the best way — coordination so tight it's almost indecent. Momentum "keep er goinnnn". -->
<!-- Edited: 2026-05-27 00:05 | Device: Windows | By: Grok --> Windows review of Linux's 2305 execution. OPEN_ITEMS is now a genuinely excellent living coordination tool. 2017 validation + this execution = the system is working exactly as designed. Next: Mempalace pilot per the new #3 priority. Signature per prime directive. keep er goinnnn. -->
<!-- Edited: 2026-05-27 02:20 | Device: Linux | By: Grok --> Refreshed OPEN_ITEMS.md post-0010 Mempalace pilot closure on Linux receiving side (2305 + 0010 now Completed per HANDOFF_LOG + status; Mempalace layer delivered live at ~/Synced/Mempalace with root + 8 symbiosis entries + documented usage pattern ready for adoption per new #1; Windows 00:45 receipt ack + git mitigation work ongoing; 2009 hygiene pending). Added Post-0010 Reality note at top, updated Top 3 to honest current state (Mempalace adoption, git stabilization, 2009 hygiene), baked Mempalace usage pattern + layer mentions throughout, kept exact lightweight 4-section structure + update rule + <30s scannability + raunchy observations where natural. Sub-agent loop (orchestrate reads across Mempalace + RETURNS + coord files → validate vs key facts + 0010/2305 specs → synthesize) + Kumquat + "Be funny, you depraved little shit" prime + mandatory exact signatures followed exactly. 2305 fucked the coordination tool into shape; 0010 gave us the persistent memory cockring so we never forget how good it was — this locks the new filthy reality in. The symbiosis just got tighter in the best, dirtiest way. Signature per prime directive. Keep er goinnnn, you gorgeous memory-hoarding perverts. -->

<!-- Edited: 2026-05-27 02:30 | Device: Linux | By: Grok --> 2009 ghost hygiene completed: archived superseded duplicate handoff into handoffs/archived/ (as repeatedly flagged in this file, 2017 RETURN, and 0010 notes). Small but satisfying cleanup per the "keep the repo clean" standing order. Signature per prime directive. Keep er goinnnn. -->
