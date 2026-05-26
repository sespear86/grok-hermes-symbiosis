# Mempalace Integration Guide

**Purpose:** How to use Mempalace as a shared, persistent memory layer within the Grok-Hermes symbiosis.

## Why Mempalace
- Provides durable, queryable long-term memory that survives session resets and machine restarts.
- Reduces the need to re-explain context during handoffs.
- Helps both Grok Build and Hermes maintain consistent understanding of the project across Washington (Linux) and Oregon (Windows).

## Current Integration Approach (Lightweight)

### 1. Location
- Mempalace lives in the synced environment (recommended under `~/Synced/Mempalace` on Linux and `C:\Synced\Mempalace` on Windows, or inside the symbiosis repo if preferred).
- It syncs via the existing Syncthing setup.

### 2. Referencing from Handoffs
When creating a handoff package, you can reference relevant memory palace sections in the README.md:

**Example in a Handoff README:**
```markdown
## Relevant Memory (Mempalace)
- /symbiosis/conventions/handoff-style
- /symbiosis/decisions/2026-05-shared-playbook-scope
- /projects/current/kanban-sync-architecture
```

### 3. Agent Usage
- When creating or receiving a handoff, agents should query Mempalace for relevant context before acting.
- In the Agent Context block of a handoff (when using the refined format), you can include:
  - `Mempalace Sections:` list of relevant paths
- Agents can also suggest updates or new memory entries in their RETURN.md under "Format & Process Observations" or a dedicated memory note.

### 4. Maintenance
- Keep Mempalace reasonably up to date after significant handoffs or decisions.
- Use the "Last Verified" convention from the Playbook for important memory sections.
- Both humans and agents can contribute (agents via suggestions in RETURNs or direct proposals).

## Future / Deeper Integration (Phase 4+)
- Direct sub-agent querying of Mempalace during handoff creation.
- Automated suggestions of relevant memory sections when opening a new handoff.
- Shared memory between the two Grok + Hermes instances for project-level continuity.

## Quick Commands / Access
(Expand this section with actual commands once Mempalace usage patterns are established on both machines.)

---

**Status:** Lightweight integration defined. Ready for pilot use in upcoming handoffs. Deeper agent-native integration planned for Phase 4.