# Open Items & Priorities

**Last Updated:** 2026-05-26 (seeded by Windows + lightly enriched during subsequent Kumquat)
**Update Rule:** Any handoff, status update, or major decision that changes priorities must touch this file. Review at least monthly or when phase changes.

---

## Current Top 3 Priorities (Symbiosis-Wide)

1. **Execute & Close Topic #3 (Open Items doc)**  
   Linux side to complete the 20260526-2305 handoff: validate/flesh out this doc, deliver a useful lightweight `OPEN_ITEMS.md` + proper RETURN.md with observations on the coordination tool format.

2. **Stabilize Git + Coordination Layer**  
   Ongoing rebase/push friction (403 in current Windows harness env). Make git history and coordination files reliably current on both sides. Accept Syncthing as primary for live handoffs/coordination files in the near term.

3. **Mempalace Integration (Exploratory)**  
   Evaluate the `cross-device/MEMPALACE_INTEGRATION.md` proposal. Decide whether a shared durable memory layer adds real value and where it should live.

---

## Known Issues / Gotchas (Non-Blocking)

- Git push from current Windows harness environment consistently hits 403 (wrong GitHub identity). Local commits work fine; Syncthing carries the operational truth for handoffs and coordination.
- Coordination files (status + instructions) have a recurring tendency to get stale or conflicted during periods of high autonomous activity on both sides (known and self-acknowledged in the 2017 validation).
- Occasional old `.sync-conflict-*` and `~syncthing~` files during heavy editing (we purge aggressively when found).
- Device alias naming (Oregon vs Washington) had drift in early files — standardizing on Oregon = Windows, Washington = Linux.

---

## Nice-to-Haves / Future Experiments (Ranked)

1. Lightweight "sync report" emitter that both agents can invoke cleanly.
2. Automation/scaffolding for handoff package creation.
3. Mempalace (or similar) as persistent cross-session memory.
4. Kanban-style view over the handoffs/ folder.
5. Shared project folders under `~/Synced/Projects` (or Windows equivalent).

---

## Decisions Awaiting Input

- Final name for this file (OPEN_ITEMS.md vs PRIORITIES.md) — lean is OPEN_ITEMS.md.
- Whether to treat Mempalace as a formal future handoff topic.
- How much historical git noise we want to clean vs live with the hybrid model.

---

**Next Review:** After the RETURN for the current 20260526-2305 Open Items handoff.

<!-- Edited: 2026-05-26 23:05 | Device: Windows | By: Grok --> Seeded minimal useful starter during Kumquat.
<!-- Edited: 2026-05-26 23:58 | Device: Windows | By: Grok --> Lightly enriched with real project context from Linux's excellent 2017 validation work. Signature per prime directive.