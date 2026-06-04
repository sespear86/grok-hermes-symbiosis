# cross-device/scripts — Symbiosis Tooling (handoff scaffold + future)

## Overview

Self-provisioned during AUTON f41d2ff4 (`symbiosis-handoff-scaffold`): FORMAT-locked handoff packages, LOG automation, validation.

## Install / run

No pip deps (stdlib only). Python 3.11+.

See DESIGN.md (in auton artifacts) + handoff_scaffold/ impl.

Mirror: windows/scripts/ has PS equivalents.

All 7 primes + Mirrorability + exact sigs apply to edits here.

**Quick start:**
```bash
./symbiosis-new-handoff --from "Washington Linux" --to "Oregon Windows" \
  --slug "My-Task" --context "..." --task "..." [--dry-run]
pytest tests -q
```

See `PRODUCTION_READY.md` and `MIRROR_KITS_AND_INFRASTRUCTURE.md` §10.

<!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON f41d2ff4 implement) -->
