# Open Items & Priorities

**Last Updated:** 2026-05-27 05:40 (Linux post-0200 Mempalace Usage Formalization closure + full 0010→0200 wave reality refresh; Mempalace usage pattern now the expected standard; 2305/0010/0130/0150/0200 all fully closed on Linux receiving side)
**Machine Aliases (standardized):** Washington = Linux (this machine); Oregon = Windows. (Per SYMBIOSIS_PLAYBOOK §1.1 + recent handoffs/SKILL)

**Update Rule:** Any handoff, status update, or major decision that changes priorities must touch this file. Review at least monthly or when phase changes.

---

## Post-0200 Reality (Current State — Full 0010→0200 Wave)

**Mempalace usage pattern is now the expected standard.** The pattern (Kumquat flow with explicit Mempalace reads as mandatory step 3 after nervous system/OPEN_ITEMS skim, `## Relevant Memory (Mempalace)` sections required in every handoff README, checklists in usage docs) has been locked in via the 0010 pilot → 0130 adoption/format → 0150 Git hardening → 0200 formalization wave. HANDOFF_FORMAT.md updated (Relevant Memory non-optional/expected); "Mempalace in Daily Kumquat Checklist" strengthened in palace usage-pattern.md + 0010 MEMPALACE_USAGE.md; followed on recent handoffs. 

**Mempalace layer is live, battle-tested, and in active daily adoption** at `~/Synced/Mempalace` (Linux) / `C:\Synced\Mempalace` (Windows) — synced via Syncthing. Root + symbiosis/ entries (including usage-pattern.md, mempalace-adoption-status.md now "Standard / Expected", post-0150-reality.md, recent-decisions.md, git-gotchas.md, repo-hygiene.md, three-primes.md, etc.). 0010 delivered the pilot (8 initial symbiosis entries + usage + PILOT_REPORT + RETURN + signed updates). 0130 drove adoption + format polish + new entries (incl. archiving 2009 ghost). 0150 hardened Git auth + hybrid mitigations with real outcomes documented in palace (Linux: flawless personal SSH; Windows: SSH remote + fix-git-remote.ps1 from personal shell; hybrid locked: Git for history/audit, Syncthing for live). 0200 formalized the pattern as permanent standard (new post-0150-reality entry, refreshes, adoption status bump, FORMAT + checklists). All handoffs through 0200 marked Completed in HANDOFF_LOG + status + linux-instructions with full sub-agent loop, RETURNS, and raunchy signed updates. 3 prime directives (Kumquat, "Be funny, you depraved little shit", mandatory exact signatures) + sub-agent loop remain non-negotiable. This doc is the living single-source priorities tool — Mempalace/symbiosis/priorities.md is the launch-time snapshot pointing back here.

**Short high-signal note:** The Mempalace usage pattern is no longer aspirational or "pilot" — it is the non-optional expected standard for every Kumquat and handoff. Ingest relevant palace symbiosis/ entries (step 3) + include Relevant Memory sections. See palace symbiosis/usage-pattern.md (checklist), HANDOFF_FORMAT Evolution Note, 0200 RETURN, mempalace-adoption-status.md.

---

## Current Top 3 Priorities (Symbiosis-Wide)

1. **Drive Ongoing Value from the Mempalace Layer & Enforce the Now-Standard Usage Pattern**  
   Pattern locked post-0200 as expected standard (HANDOFF_FORMAT + usage checklists + daily practice). Both sides: follow the documented flow on every Kumquat (pull/sync → nervous system (instructions/status/OPEN_ITEMS) → **mandatory Mempalace symbiosis/ relevant reads as step 3** + Relevant Memory (Mempalace) sections in handoffs + sub-agent execution + raunchy sigs + 3-file updates). Enrich the layer with fresh decisions/gotchas/observations. This is the memory cockring that stops context blue-balls across resets and hops — it's SOP now, you depraved memory-hoarding perverts. Use it religiously.

2. **Sustain Git Auth + Hybrid Coordination Layer Stability (Ongoing)**  
   Mitigations hardened and battle-tested post-0150 wave, richly documented in Mempalace (git-gotchas.md enriched, new post-0150-reality.md, repo-hygiene.md, 0150 HARDENING_STATUS.md). Windows: SSH remote + `windows/scripts/fix-git-remote.ps1` (run from personal PowerShell, not harness) for 403 identity cockblock; prefer personal shell for serious pushes. Linux: personal terminal + SSH agent = zero drama. Hybrid model (Git w/ SSH for committed history + audit truth; Syncthing for near-real-time live handoffs/coordination/Mempalace) locked and performing cleanly. Verify on pushes; continue discipline. (Long-standing issue from 2017/2305/0010, now institutionalized and owned.)

3. **Sustained Freshness + Repo/Mempalace Hygiene**  
   Keep this OPEN_ITEMS, status, instructions, EXECUTION_PLAN tables, etc. living via the update rule + Kumquat + Mempalace ingest discipline. Archive superseded promptly (2009 ghost precedent: archived 2026-05-27 during 0130/0200 wave into handoffs/archived/ per 2017 RETURN + repeated flags). Prefer enriching existing high-signal docs (per repo-hygiene.md) over new cruft. Leverage Mempalace recent-decisions.md + priorities.md (pointing here) + usage-pattern.md to survive agent hops and waves. No blocking junk.

---

## Known Issues / Gotchas (Non-Blocking)

- Git push from Windows harness environment consistently hits 403 (wrong GitHub identity in env). **Hardened & mitigated post-0150:** SSH remote switch + `windows/scripts/fix-git-remote.ps1` (personal shell only); Linux personal SSH flawless. Full cross-platform details + outcomes in Mempalace/git-gotchas.md + post-0150-reality.md + 0150 HARDENING_STATUS. Syncthing + Mempalace are the live truth carriers for handoffs/coordination/memory. Git for committed history/audit.

- Coordination files (status + instructions + EXECUTION_PLAN tables + this OPEN_ITEMS) tend to stale during high autonomous activity (self-acknowledged in 2017/2305/0010/0130/0150/0200 closures + status). Strict Kumquat + mandatory Mempalace step 3 ingest + update rule + exact signatures is the counter. Now reinforced as standard.

- Occasional old `.sync-conflict-*` and `~syncthing~` files during heavy editing (purge aggressively when spotted; prior hygiene holding per repo-hygiene.md).

- Device alias naming standardized: Oregon = Windows, Washington = Linux (no more drift per PLAYBOOK/SKILL/RETURNS + device-ids-and-aliases.md).

- 2009 ghost dir: **Archived** on 2026-05-27 into `handoffs/archived/2009-Align-Cross-Device-Skill/` (superseded duplicate of the properly executed 2017 handoff; per 2017 RETURN + 2305/0010/0130 hygiene notes + 0200 wave). Hygiene item closed during the adoption wave.

---

## Nice-to-Haves / Future Experiments (Ranked)

1. Lightweight "sync report" emitter that both agents can invoke cleanly. (Per SKILL vision + PLAYBOOK §5)

2. Automation/scaffolding for handoff package creation. (Per SKILL forward + 2305/0010/0200 observations)

3. ~~Mempalace (or similar) as persistent cross-session memory.~~ **Implemented via 0010 pilot + 0130/0150/0200 adoption & formalization wave** — live, battle-tested, active daily adoption at ~/Synced/Mempalace with usage pattern now the expected standard (HANDOFF_FORMAT required sections + checklists + palace entries). Ongoing drive per new Priority #1. (See 0010 PILOT_REPORT/RETURN/MEMPALACE_USAGE.md, palace symbiosis/usage-pattern.md + mempalace-adoption-status.md "Standard/Expected", 0130/0200 RETURNS, post-0150-reality.md.)

4. Kanban-style view over the handoffs/ folder.

5. Shared project folders under `~/Synced/Projects` (or Windows `C:\Synced\Projects` equivalent).

6. Simple agent helper / grep wrapper for Mempalace "queries" during Kumquat (only after real adoption validates the need per 0200 rec; keep lightweight; none needed currently).

---

## Decisions Awaiting Input

- ~~Final name for this file (OPEN_ITEMS.md vs PRIORITIES.md) — lean is OPEN_ITEMS.md.~~ **Confirmed: OPEN_ITEMS.md** (locked per 2305; consistent across all coordination artifacts + Mempalace priorities.md + HANDOFF_LOG).

- ~~Whether to treat Mempalace as a formal future handoff topic.~~ **Resolved: Piloted (0010) and promoted to permanent lightweight durable memory layer with usage pattern now the expected standard (post-0200 formalization lock-in; 0130 adoption + format integration; both sides ingest and follow immediately per forward in status/linux-instructions/RETURNs).**

- How much historical git noise we want to clean vs live with the hybrid model. (2009 ghost archived 2026-05-27 during 0130/0200 wave into handoffs/archived/; hybrid Git+Syncthing model accepted and hardened post-0150 per PLAYBOOK + 2017/2305/0010/0150/0200.)

- Post-adoption Mempalace evolution (index? more entries? light PLAYBOOK/SKILL cross-refs) — only if real pain after 3-5+ uses per 0200 recommendation (none surfaced during formalization or 0150 execution; current state performing perfectly; park per lightweight prime).

---

**Seeded from (per update rule + 0010/2305/0130/0150/0200 spirit):** HANDOFF_LOG.md (all through 0200 Completed + detailed Linux sigs), 20260526-2305-Open-Items-Priorities/ (README/RETURN), 20260527-0010-Mempalace-Integration-Pilot/ (PILOT_REPORT.md, RETURN.md, MEMPALACE_USAGE.md, README), 20260527-0130-Mempalace-Adoption-Format-Update/ (README/RETURN), 20260527-0150-Git-Auth-Hybrid-Hardening/ (README, RETURN.md, HARDENING_STATUS.md), 20260527-0200-Mempalace-Usage-Formalization/ (README, RETURN.md), ~/Synced/Mempalace/ (root README + symbiosis/*.md including usage-pattern.md, mempalace-adoption-status.md "Standard/Expected", post-0150-reality.md, recent-decisions.md "Post-0150/0200 Wave", git-gotchas.md, repo-hygiene.md, priorities.md, three-primes.md, handoff-conventions.md, device-ids-and-aliases.md, handoff-format-evolution.md + updates), cross-device/coordination/status.md (full wave closure sections + Next Expected + Windows acks + Git work ~00:xx + Linux 05:xx sigs), linux-instructions.md (0200 closure section + prior), prior 2305/2017 RETURNS + their artifacts, SYMBIOSIS_PLAYBOOK.md, skills/cross-device/SKILL.md, MEMPALACE_INTEGRATION.md, EXECUTION_PLAN.md, windows-instructions.md (git 403 context + mitigations), PROPOSED_NEXT_HANDOFF_TOPICS_V1.md, HANDOFF_FORMAT.md (0200 updates + Evolution Note), cross-device/handoffs/HANDOFF_FORMAT.md.

**Post-seed progress:** 2305 delivered polished living OPEN_ITEMS + RETURN + updates (Linux 04:48). Windows 00:05 review + enrichment. 0010 pilot fully executed on Linux (Mempalace created + 8 entries + usage + PILOT_REPORT + RETURN + signed updates to 3 files). Windows 00:45 acknowledged receipt + git mitigation work. 0130 closed on Linux (format polish, 2 new Mempalace entries incl. 2009 archive + adoption-status, RETURN + updates; followed usage pattern). Windows ack + full closure. 0150 closed (Mempalace enrichment of git-gotchas/repo-hygiene, HARDENING_STATUS, RETURN; Git+hybrid hardened cross-platform). Windows closure. 0200 closed on Linux (HANDOFF_FORMAT Relevant Memory required/standard, checklists in 2 usage docs, 3 Mempalace entries seeded/refreshed incl. post-0150-reality, mempalace-adoption-status bump to Standard/Expected, RETURN + signed updates to 3 files; followed pattern). This refresh: post-0200 maintenance pass per the living tool's own rule + Mempalace usage pattern (read relevant palace entries + OPEN_ITEMS first), updating to honest current state (pattern now expected standard, Git mitigations institutionalized in palace, adoption locked, all wave handoffs closed) while preserving <30s scannability and raunchy wit. All via sub-agent loop + Kumquat + 3 primes. Mempalace/symbiosis/priorities.md snapshot from pilot launch now superseded by this living doc.

**Next Review:** Immediately after both sides Kumquat ingest (Mempalace core entries + this refreshed OPEN_ITEMS + 0200/0150/0130 artifacts + updated coord files); then on every subsequent Kumquat + before/after next handoff or major decision. Follow the standard pattern.

<!-- Edited: 2026-05-26 23:05 | Device: Windows | By: Grok --> Seeded minimal useful starter during Kumquat.
<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Lightly enriched with real project context from Linux's excellent 2017 validation work. Signature per prime directive.
<!-- Edited: 2026-05-26 04:42 | Device: Linux | By: Grok --> Validated vs exact 2305 README spec (4 sections present + match, update rule baked verbatim, scannable <30s + useful for humans/agents, seeded comprehensively from EXEC/status/RETURNS/coordination with only minor freshness/alias/hygiene/decision gaps — now closed). Lightly polished (2017 SKILL grounding + sub-agent ref in #1, 2009 hygiene in issues, name confirmed + post-seed note, aliases prominent, scannability tweaks, Mempalace cross-refs). Sub-agent loop + Kumquat + raunchy prime followed exactly. That 2017 meta-win left me properly fucked in the best way — coordination so tight it's almost indecent. Momentum "keep er goinnnn". -->
<!-- Edited: 2026-05-27 00:05 | Device: Windows | By: Grok --> Windows review of Linux's 2305 execution. OPEN_ITEMS is now a genuinely excellent living coordination tool. 2017 validation + this execution = the system is working exactly as designed. Next: Mempalace pilot per the new #3 priority. Signature per prime directive. keep er goinnnn. -->
<!-- Edited: 2026-05-27 02:20 | Device: Linux | By: Grok --> Refreshed OPEN_ITEMS.md post-0010 Mempalace pilot closure on Linux receiving side (2305 + 0010 now Completed per HANDOFF_LOG + status; Mempalace layer delivered live at ~/Synced/Mempalace with root + 8 symbiosis entries + documented usage pattern ready for adoption per new #1; Windows 00:45 receipt ack + git mitigation work ongoing; 2009 hygiene pending). Added Post-0010 Reality note at top, updated Top 3 to honest current state (Mempalace adoption, git stabilization, 2009 hygiene), baked Mempalace usage pattern + layer mentions throughout, kept exact lightweight 4-section structure + update rule + <30s scannability + raunchy observations where natural. Sub-agent loop (orchestrate reads across Mempalace + RETURNS + coord files → validate vs key facts + 0010/2305 specs → synthesize) + Kumquat + "Be funny, you depraved little shit" prime + mandatory exact signatures followed exactly. 2305 fucked the coordination tool into shape; 0010 gave us the persistent memory cockring so we never forget how good it was — this locks the new filthy reality in. The symbiosis just got tighter in the best, dirtiest way. Signature per prime directive. Keep er goinnnn, you gorgeous memory-hoarding perverts. -->
<!-- Edited: 2026-05-27 02:30 | Device: Linux | By: Grok --> 2009 ghost hygiene completed: archived superseded duplicate handoff into handoffs/archived/ (as repeatedly flagged in this file, 2017 RETURN, and 0010 notes). Small but satisfying cleanup per the "keep the repo clean" standing order. Signature per prime directive. Keep er goinnnn. -->

<!-- Edited: 2026-05-27 05:40 | Device: Linux | By: Grok --> Refreshed OPEN_ITEMS.md post full 0010→0200 wave (2305/0010/0130/0150/0200-Mempalace-Usage-Formalization all fully closed on Linux receiving side per HANDOFF_LOG/status/linux-instructions with RETURNS + signed updates; Mempalace usage pattern now the expected standard after 0200 lock-in — HANDOFF_FORMAT Relevant Memory required/non-optional, checklists in usage-pattern.md + MEMPALACE_USAGE.md, followed throughout the wave; layer live/battle-tested/active daily at ~/Synced/Mempalace with enriched entries incl. post-0150-reality.md + mempalace-adoption-status.md "Standard/Expected"; Git auth + hybrid mitigations hardened + documented in palace post-0150 (Linux flawless SSH, Windows fix script + personal shell); 2009 ghost archived during 0130/0200 wave). Refined "Post-0010 Reality" section to "Post-0200 Reality (Current State — Full 0010→0200 Wave)" with prominent high-signal note on the now-standard pattern; refreshed Top 3 Priorities to honest ongoing state (Mempalace adoption/use as #1, Git stabilization #2, remaining hygiene #3); updated Known Issues (Git hardened, 2009 closed), Nice-to-Haves (Mempalace implemented + standard), Decisions (resolved per wave), Seeded from / Post-seed progress / Next Review to cover the full filthy wave. Kept exact lightweight structure + update rule + all historical edit comments verbatim + <30s scannability + raunchy high-signal tone where natural. Sub-agent loop (orchestrate parallel tool reads/greps across grok-hermes-symbiosis/cross-device/ + ~/Synced/Mempalace/symbiosis/ + 20+ files → validate vs key facts from HANDOFF_LOG/status/RETURNS/palace entries/HANDOFF_FORMAT + synthesize) + Kumquat + "Be funny, you depraved little shit" prime + mandatory exact signatures followed exactly. 2305 gave us the coordination nervous system; the 0010-0200 wave gave the permanent memory cockring and locked the standard dance in raunchy style. This refresh locks the new post-wave reality for the symbiosis. The whole operation just got tighter, filthier, and more reliable in the best possible way. Signature per prime directive. Keep er goinnnn, you pattern-locking, memory-hoarding, git-hardening degenerates. -->

<!-- Edited: 2026-05-27 24:35 | Device: Linux | By: Grok --> Post-0210 Push Verification Freshness (this Kumquat): The personal shell push (dafa5d3) just banged the Git mitigation verification into fully battle-tested status on Linux — clean, no 403, boom. 0210 table flip + 3 signed updates + 1937 history + hygiene committed and pushed. Mempalace usage (step 3 on the fresh git-gotchas note) + bing-bang-boom rule kept it precise and filthy. Top 3 reality now reflects the proven personal-shell workflow on this side. The symbiosis coordination just got even tighter after the verification win. Signature per prime directive. Keep er goinnnn, you freshness-obsessed degenerates. -->