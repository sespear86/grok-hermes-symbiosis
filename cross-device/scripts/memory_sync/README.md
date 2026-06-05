# memory_sync — Bidirectional Memory Sync for Symbiosis (AUTON 7eb7d1b7)

Stdlib package + `symbiosis-memory-sync` for structured push/pull of context (todos, decisions, OPEN_ITEMS excerpts, native memory snapshots) between Grok Build, Hermes, and Mempalace (canonical shared layer under `projects/{slug}-snapshots`).

See top-level `DESIGN.md` (auton 7eb7d1b7), `PRODUCTION_READY.md` section, MIRROR_KITS §17 (to land), PLAYBOOK §2.3f.

**Current:** Bootstrap + early B1-B3 skeleton + smoke + tests green. Full impl + gates in progress.

**Usage (post full):**
```bash
./symbiosis-memory-sync bundle --agent grok --device "Washington Linux" --dry-run
./symbiosis-memory-sync push --agent grok --device "Washington Linux"
```

**Mirror:** Full WA/OR parity + rich cp recipe in MIRROR.
