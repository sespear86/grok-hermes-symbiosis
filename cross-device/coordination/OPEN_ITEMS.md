# Open Items & Priorities

**Last Updated:** 2026-05-26 (seeded by Windows Grok during Kumquat)
**Update Rule:** Any handoff, status update, or major decision that changes priorities must touch this file. Review at least monthly or when phase changes.

---

## Current Top 3 Priorities (Symbiosis-Wide)

1. **Execute & Close Topic #3 (Open Items doc)**  
   Linux side to complete the 20260526-2305 handoff and deliver a useful, lightweight `OPEN_ITEMS.md` + RETURN.

2. **Stabilize Git + Coordination Layer**  
   Resolve ongoing rebase/push friction (403 in harness env). Make git history and coordination files reliably current on both sides. Consider switching to a more reliable push method or accepting Syncthing as primary for live files.

3. **Mempalace Integration (Exploratory)**  
   Evaluate the new `cross-device/MEMPALACE_INTEGRATION.md` proposal. Decide if we want a shared durable memory layer and where it should live.

---

## Known Issues / Gotchas (Non-Blocking)

- Git push from current Windows harness environment consistently hits 403 (wrong GitHub identity). Local commits work fine.
- Coordination files (status + instructions) have a history of getting stale or conflicted during periods of high autonomous activity on both sides.
- Some old `.sync-conflict-*` and `~syncthing~` files still occasionally appear during heavy editing sessions (we purge them aggressively).
- Device alias naming (Oregon vs Washington) has had some drift in older files — we are standardizing on Oregon = Windows, Washington = Linux.

---

## Nice-to-Haves / Future Experiments (Ranked)

1. Lightweight "sync report" command or skill that both agents can emit cleanly.
2. Better automation around handoff package creation (scaffolding script or MCP tool).
3. Explore Mempalace (or similar) as a persistent shared memory store for long-running context across sessions and machines.
4. Kanban-style view on top of the handoffs/ folder.
5. Joint project folders under a shared `~/Synced/Projects` structure.

---

## Decisions Awaiting Input

- Final name for this file (OPEN_ITEMS.md vs PRIORITIES.md) — current lean is OPEN_ITEMS.md.
- Whether to keep the Mempalace proposal as a formal future topic or treat it as background research.
- How aggressive we want to be about cleaning historical git noise vs living with the current hybrid state.

---

**Next Review:** After the RETURN for the current Open Items handoff.

<!-- Edited: 2026-05-26 23:55 | Device: Windows | By: Grok --> Seeded minimal useful starter for OPEN_ITEMS.md during Kumquat after rebase abort. Signature per prime directive.