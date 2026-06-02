# Oregon Bust-a-Nut & Relay Persistence Reality Check

**Date:** 2026-06 (during "keep tightening" autonomous wave on #1 Mirrorability priority)
**Purpose:** Brutally honest, self-contained snapshot of what is *actually* running and persistent on the Oregon side right now. Designed so Washington (or a future Oregon) can understand the current state and close the gap without reverse-engineering.

**All 7 primes + Mirrorability + Self-Provisioning + raunchy filthy honesty applied.**

---

## Executive Reality

Oregon has excellent **script-level** Bust-a-Nut and relay tooling (the .ps1 family delivered across multiple waves).

**The current mechanical cockblock:** Full automatic persistence across reboots / long sessions is **not yet reliably active** in Task Scheduler without manual/admin intervention. This is the exact gap Washington flagged in their audit (and Oregon self-identified).

Washington runs active systemd timers/services with 0s beacons. Oregon's equivalent is script-ready but scheduler registration is incomplete or requires elevation.

---

## What Oregon Actually Has (Strong)

### Scripts & Logic (Excellent)
- Full BustANut-*.ps1 family (UIIdleMonitor, SessionStartPrompt, ClearPastReArmAlerts, FastPusher logic, re-arm, health, etc.)
- oregon_keep_fast_path_alive.ps1 (the practical current-session fast HB launcher)
- Receiver stack (oregon_*.ps1 for receiving from relay)
- Apply-IngestToken.ps1 + REQUEST artifacts for the dedicated companion
- .grok/hooks wired:
  - bust-a-nut-enforcer.json
  - mempalace-session-retention.json
  - oregon-auto-health.json
  - oregon-relay-health-precompact.json
  - oregon-symmetry-reminder.json
  - relay-bust-a-nut-sessionstart.json
- Rich project mirror kits (when present): Install-BustANutOregon.ps1, BUST_A_NUT_OREGON.md, etc.

### Current Session Capability (Strong when running)
- Fast path can be launched and kept hot during a TUI session.
- Health self-tests (oregon_relay_health.ps1 and equivalents) work.
- Clear-past re-arm alert declutter logic is ported.
- Intent markers and health gates exist.

---

## What Is Actually Missing or Weak (The Real Gaps)

1. **Active Scheduled Tasks**
   - Queries for "*Bust*", "*Oregon*", "*relay*", "*fast*", "*symbiosis*" return nothing visible in current state.
   - The "Oregon-Bust-a-Nut-Fast-Pusher" task referenced in older docs is not confirmed registered.
   - Many components still rely on manual launch or session-start hooks rather than true boot-persistent timers.

2. **Elevation Requirement**
   - Full Task Scheduler registration for system-level persistence typically requires admin elevation at least once.
   - This is the documented "admin logon verification" blocker from previous audits.

3. **Self-Describing Status**
   - No single "Get-OregonBustANutStatus.ps1" or equivalent that reports exactly which tasks are registered, when they last ran, and overall health (Washington has this via relay-health.sh + systemd status).

4. **Boot-Safe Auto-Start**
   - Unlike Washington's systemd services (washington-activator.service, bust-a-nut-fast-heartbeat.timer, etc.), Oregon does not yet have a guaranteed "on boot / on logon" launcher that survives without user interaction in all cases.

---

## Mirrorability Action Items (Concrete Deliverables Needed)

**High priority to close this gap:**

1. **Create `Register-OregonBustANutPersistence.ps1`** (or equivalent)
   - Handles the admin-elevated Task Scheduler registration for the key components (fast pusher, UI idle monitor, session start, health, etc.).
   - Clear, loud output + logging.
   - Idempotent (safe to run multiple times).

2. **Create `Get-OregonBustANutPersistenceStatus.ps1`**
   - Reports exactly what is registered.
   - Last run times.
   - Overall "is the fast path actually persistent?" verdict.
   - Mirrors the spirit of Washington's relay-health.sh.

3. **Standalone `OREGON_PERSISTENCE_INSTALL_GUIDE.md`** (repo-rooted, not just in rich project)
   - One place that explains the current reality + the two scripts above.
   - Includes the exact elevation steps.

4. **Update the main comparison doc** (this is already happening in the tightening wave).

---

**Current tightening status on this gap:** 
- Reality explicitly documented here (first concrete artifact delivered in this wave).
- Scripts above are now the clear next deliverables to turn "script-ready" into "actually persistent like Washington's systemd stack."

**Linux Turn / Mirrorability note:** Washington — this document + the comparison makes the exact pain visible. When you deliver the equivalent Linux-side clarity or help with the Pi side, we close the loop faster.

---

<!-- Edited: 2026-06 (keep tightening wave — created dedicated Oregon Bust-a-Nut Persistence Reality Check artifact) | Device: Oregon Windows (STINKY) | By: Grok (harness, MCP owner, full autonomous no-brakes) --> User said "keep tightening" on the #1. I immediately created this focused reality check artifact, appended major progress to the comparison doc, and pushed via MCP as sespear86. Gap now has a name, a current state, and specific next scripts. All 7 primes + Mirrorability Prime + Self-Provisioning + bing bang boom + maximum raunchy filthy tightening energy. The one extended machine's persistence cockring just got another ratchet click tighter. Keep er goinnnn, you reality-checking, persistence-ratcheting, gap-closing degenerates. Bust a mothafackin nut. -->