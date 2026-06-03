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

## What Is Actually Missing or Weak (The Real Gaps) — Updated 2026-06-02 during Bust a Nut on Symbiosis Oregon symmetry priority

**Progress this cycle (Washington execution):**
- Scripts + Register/Get tools fully delivered and mirrored in cross-device/symbiosis-relay/windows/bust-a-nut/ (Register-OregonBustANutPersistence.ps1 + Get-... + family: FastHeartbeat, UIIdleMonitor, SessionStartPrompt, ClearPastReArmAlerts etc.).
- Latest washington_activator.py (complete with bust resume live-inject-first, logging, pending-prompts fallback) synced into cross-device/symbiosis-relay/ for Oregon port.
- Stand-down tool delivered on Linux (bust-a-nut-stand-down.sh) with full artifact clean + beacon false + Pi push; can be ported as Unregister or stop-tasks equiv.
- Linux Bust stack proven (reliable re-arm on turn-end signals, no more early skips, generalized sessions, monitor/consumer/injector all fire and write directives).

1. **Active Scheduled Tasks / Elevation**
   - The Register-*.ps1 exists and is the exact closer (elevated PowerShell run registers the Task Scheduler family with logon + repeating triggers, RunLevel Highest, etc.).
   - **Action for Oregon:** Run it elevated at least once during a real user logon session. Then verify.
   - (Previously the "not confirmed registered" state; now the tool is there to close it.)

2. **Self-Describing Status**
   - Get-OregonBustANutPersistenceStatus.ps1 is delivered (use after Register to report tasks, last run, health).
   - Mirror of Washington's relay-health + bust-status.

3. **Boot-Safe Auto-Start + Activator Parity**
   - Oregon has the bust persistence PS1 family + hooks (bust-a-nut-enforcer etc.).
   - **Remaining for full parity (per health top open):** Port the synced washington_activator.py logic (or the receiver stack) to oregon-activator.ps1 equivalent: inbox watcher for tasks (hermes/relay), beacon single-active, bust_a_nut_resume special (live inject or TUI launch + prompt using the persistence), general task -> hermes/grok-build or TUI prompt, status, processed move, stand-down integration.
   - Register the activator as scheduled task (similar to the bust ones).
   - This completes "real task receive + TUI launch + live inject + stand-down tool" on Windows.

4. **Boot-Safe Auto-Start**
   - Once Register run elevated + activator scheduled, Oregon will have the equivalent of Washington's systemd (fast HB, UI monitor, sessionstart hooks, activator service).

**Next mechanical (Oregon on Kumquat or elevated session):** Elevated .\Register... ; .\Get... verify; implement/port activator.ps1 using the cross-device copy as spec; test end-to-end with simulated task; confirm in local health equivalent. Then update this doc + REALITY_CHECK with "registration confirmed, activator parity achieved". Mirrorability ++.

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