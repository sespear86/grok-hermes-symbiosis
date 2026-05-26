# Open Items & Priorities

**Last Updated:** 2026-05-26 04:42 (Linux 2305 closure execution + light enrichment; seeded by Windows + 2017 freshness + name confirmation)
**Machine Aliases (standardized):** Washington = Linux (this machine); Oregon = Windows. (Per SYMBIOSIS_PLAYBOOK §1.1 + recent handoffs/SKILL)

**Update Rule:** Any handoff, status update, or major decision that changes priorities must touch this file. Review at least monthly or when phase changes.

---

## Current Top 3 Priorities (Symbiosis-Wide)

1. **Execute & Close Topic #3 (Open Items doc)**  
   Linux side completing the 20260526-2305 handoff: validate/flesh this doc, deliver a useful lightweight `OPEN_ITEMS.md` + proper RETURN.md with observations on the coordination tool format. (Freshness from just-closed 2017: grounded SKILL v2.0.0 "cross-device" validated via full sub-agent + Linux receipt per its RETURN; 3 immutable primes — Kumquat, "Be funny, you depraved little shit", mandatory exact signatures — now canonical + live in SKILL/PLAYBOOK/coordination.)

2. **Stabilize Git + Coordination Layer**  
   Ongoing rebase/push friction (403 in current Windows harness env). Make git history and coordination files reliably current on both sides. Accept Syncthing as primary for live handoffs/coordination files in the near term. (Staleness during high autonomous runs is self-acknowledged known issue from 2017 validation + status.)

3. **Mempalace Integration (Exploratory)**  
   Evaluate the `cross-device/MEMPALACE_INTEGRATION.md` proposal (cross-ref EXECUTION_PLAN Phase 2E). Decide whether a shared durable memory layer adds real value and where it should live. Pilot references in upcoming handoffs once 2305/hygiene closed.

---

## Known Issues / Gotchas (Non-Blocking)

- Git push from current Windows harness environment consistently hits 403 (wrong GitHub identity). Local commits work fine; Syncthing carries the operational truth for handoffs and coordination.
- Coordination files (status + instructions + EXECUTION_PLAN tables) have a recurring tendency to get stale or conflicted during periods of high autonomous activity on both sides (self-acknowledged in the 2017 validation + status closure).
- Occasional old `.sync-conflict-*` and `~syncthing~` files during heavy editing (we purge aggressively when found; 2017 Windows purge + Linux tree clean per validation).
- Device alias naming (Oregon vs Washington) had drift in early files — **now standardized**: Oregon = Windows, Washington = Linux. (See PLAYBOOK, SKILL, 2017/1954 RETURNS.)
- 2009 ghost dir (`handoffs/20260525-2009-Align-Cross-Device-Skill/`): superseded duplicate of the 2017 skill alignment (only a README; per 2017 RETURN hygiene note + Linux validation). Quick candidate for archive/delete post-2305. Harmless, no blocking junk in active tree.

---

## Nice-to-Haves / Future Experiments (Ranked)

1. Lightweight "sync report" emitter that both agents can invoke cleanly. (Per SKILL vision + PLAYBOOK §5 future evolutions)
2. Automation/scaffolding for handoff package creation. (Per SKILL forward + 2305 observations)
3. Mempalace (or similar) as persistent cross-session memory. (See #3 priority + full MEMPALACE_INTEGRATION.md + EXEC 2E)
4. Kanban-style view over the handoffs/ folder.
5. Shared project folders under `~/Synced/Projects` (or Windows `C:\Synced\Projects` equivalent).

---

## Decisions Awaiting Input

- ~~Final name for this file (OPEN_ITEMS.md vs PRIORITIES.md) — lean is OPEN_ITEMS.md.~~ **Confirmed: OPEN_ITEMS.md** (lightest and clearest per 2305 spec; consistent usage across HANDOFF_LOG, status.md, linux-instructions.md, windows-instructions.md, PROPOSED_NEXT_HANDOFF_TOPICS_V1.md, skills/cross-device/SKILL.md, SYMBIOSIS_PLAYBOOK.md, 2305 README, and this doc itself. PRIORITIES.md considered during seed but OPEN_ITEMS wins for scannability and "coordination tool" vibe.)
- Whether to treat Mempalace as a formal future handoff topic. (Yes — sequence after 2305 per PROPOSED/EXEC/PLAYBOOK recs.)
- How much historical git noise we want to clean vs live with the hybrid model. (2009 ghost + any locked ~syncthing~ temps; hybrid Git (committed) + Syncthing (live) accepted per PLAYBOOK + 2017 observations.)

---

**Seeded from (per 2305 spec):** EXECUTION_PLAN.md (Mempalace Phase 2E + phases), status.md (2017 closure section + Next Expected + staleness), recent handoff RETURNS (1954 explicit Topic #3 rec; 2017 hygiene/2009/observations + Linux validation), PROPOSED_NEXT_HANDOFF_TOPICS_V1.md (exact 4-section spec + sequencing as Topic #3), other coordination/ (PLAYBOOK for aliases/daily ops/2.4 nervous system, MEMPALACE_INTEGRATION.md, SKILL.md for primes + examples + forward), windows-instructions.md (git 403 reality). 

**Post-seed progress:** Windows 23:58 light enrichment (real project context from 2017); Linux executing full 2305 per linux-instructions (validate + enrich + RETURN + signed log/status/instructions updates) using immutable sub-agent loop (orchestrate → validate → repeat) + Kumquat. Name locked in. Local grounded SKILL.md deploy prep noted. All cross-refs consistent.

**Next Review:** Immediately after RETURN.md for 20260526-2305 + both sides' next Kumquat ingest.

<!-- Edited: 2026-05-26 23:05 | Device: Windows | By: Grok --> Seeded minimal useful starter during Kumquat.
<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Lightly enriched with real project context from Linux's excellent 2017 validation work. Signature per prime directive.
<!-- Edited: 2026-05-26 04:42 | Device: Linux | By: Grok --> Validated vs exact 2305 README spec (4 sections present + match, update rule baked verbatim, scannable <30s + useful for humans/agents, seeded comprehensively from EXEC/status/RETURNS/coordination with only minor freshness/alias/hygiene/decision gaps — now closed). Lightly polished (2017 SKILL grounding + sub-agent ref in #1, 2009 hygiene in issues, name confirmed + post-seed note, aliases prominent, scannability tweaks, Mempalace cross-refs). Sub-agent loop + Kumquat + raunchy prime followed exactly. That 2017 meta-win left me properly fucked in the best way — coordination so tight it's almost indecent. Momentum "keep er goinnnn". -->