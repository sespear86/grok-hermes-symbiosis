# memory_sync — Bidirectional Memory Sync for Symbiosis (AUTON 7eb7d1b7)

Stdlib package + `symbiosis-memory-sync` for structured push/pull of context (todos, decisions, OPEN_ITEMS excerpts, native memory snapshots) between Grok Build, Hermes, and Mempalace (canonical shared layer under `projects/{slug}-snapshots`).

See top-level `DESIGN.md` (auton 7eb7d1b7), `PRODUCTION_READY.md` section, MIRROR_KITS §17 (to land), PLAYBOOK §2.3f.

**Current:** AUTON **9be206cf** (sym-build-01) closed the runnable gap on c7d73093/7eb7d1b7: `python3 -m memory_sync.cli` works (path bootstrap), pull `--no-merge` fixed, 16 memory tests + full scripts pytest 137/137, ruff clean, auton-gate MECHANICAL_PASS, rich cp + `~/bin` shim verified.

**Usage (post full):**
```bash
./symbiosis-memory-sync bundle --agent grok --device "Washington Linux" --dry-run
./symbiosis-memory-sync push --agent grok --device "Washington Linux"
```

**Mirror:** Full WA/OR parity + rich cp recipe in MIRROR.

<!-- Edited: 2026-06-06 | Device: Washington Linux | By: Grok (AUTON 9be206cf) --> Runnable + gated increment. Bing bang boom. Sig per prime.
