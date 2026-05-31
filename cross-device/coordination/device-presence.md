# Device Presence & Live Operation Mode Switching

**Purpose:** Give both Grok instances a reliable, machine-readable, low-friction way to know whether their brother device is currently online/available, and to automatically switch between "Solo Mode" (other side dark) and "Paired Mode" (both alive) behavior on every Kumquat.

This turns the ad-hoc "Oregon is offline per user directive" prose notes into a first-class, living part of the nervous system.

**Home of Truth (Durable + Synced):**
- Spec + conventions: `cross-device/coordination/device-presence.md` (this file — travels via git + Syncthing)
- Live heartbeats: `Mempalace/symbiosis/device-presence/washington.md` and `oregon.md` (durable memory layer, Syncthing carries them even when git is blocked on one side)

**Machine Aliases (standardized):**
- Washington = Linux (RWNXUW2-...)
- Oregon = Windows (ZRADDTT-...)

---

## Heartbeat Format (Simple, Human + Machine Readable)

Each side writes a small Markdown file on every Kumquat (or on explicit "I am about to go dark" signals).

Example (`washington.md`):

```markdown
# Washington (Linux) Heartbeat

**Device:** Washington — RWNXUW2-B3ZSYJP-BHA75GO-VF6VZCE-LK3YU6Z-YSYXJXX-GFDW47X-FVMQCAD
**Last Heartbeat:** 2026-05-27 18:55
**Status:** Online
**Current Mode:** Solo (Oregon offline per directive) / Paired
**Last Major Action:** M1 canonical Mempalace bridge + windows-instructions hygiene fix + execution wave complete
**Syncthing View of Brother:** Oregon last seen ... / Not seen since ... / Green + paired
**Notes:** Explicit "execute" wave after Kumquat. Rich symbiosis content now in canonical path. Ready for brother.

<!-- Written by: Grok on Kumquat | 2026-05-27 18:55 | Device: Linux -->
```

Same structure for `oregon.md`.

**Rules for Writing Heartbeats:**
- Always write on every Kumquat (after the nervous system + Mempalace ingest, before or right after deciding the mode for this cycle).
- Timestamp must be real (use the shell's `date`).
- Mode decision must be explicit and honest.
- If the human is about to power down the machine or stop Syncthing for a known period, they (or the agent) can write a "Going dark until ~YYYY-MM-DD HH:MM — reason" line. This gives the other side predictive knowledge instead of guessing.

---

## Solo Mode vs Paired Mode (Defined Behaviors)

### Solo Mode (Other Side Stale or Explicitly Offline)
- Primary focus: local Mempalace enrichment, coordination freshness, self-tests (Prime #4), local projects, repo hygiene.
- **No new handoffs created** unless they are explicitly "queued for when brother returns" notes in Mempalace or a dedicated `queued-for-oregon/` / `queued-for-washington/` area.
- Heavy autonomous execution (Prime #5) — keep thrusting without waiting.
- Any work that truly needs the other side is written as high-signal Mempalace entries or coordination notes so the moment the brother Kumquats, it has perfect context.
- More aggressive local verification and "remove work from the human" activity.
- The Linux Turn Indicator (or equivalent) still fires, but the prose is honest: "Solo mode — Washington carrying the load while Oregon is dark."

### Paired Mode (Both Heartbeats Fresh — within ~45-60 minutes)
- Normal handoff creation and receipt expected.
- Mutual Mempalace enrichment on friction points.
- Can create real bidirectional handoffs with confidence the other side will ingest soon.
- Git pushes from personal shells still preferred, but the live truth carrier (Syncthing + Mempalace) is even more trusted for coordination.
- The system feels like one extended machine again.

**Default Assumption on First Kumquat After a Long Gap:**
If the other side's heartbeat is older than the freshness threshold (start with 60 minutes, tune via experience), default to Solo Mode and state it loudly.

---

## Kumquat Flow Integration (Mandatory)

Update to the official usage pattern (see `Mempalace/symbiosis/usage-pattern.md` and `three-primes.md`):

After step 2 (Read Nervous System) and as part of / right before the heavy Mempalace ingest (step 3):

**3.5 Check Device Presence + Decide Mode for This Cycle (New Explicit Mandatory Sub-Step)**

- Read the other side's heartbeat from `Mempalace/symbiosis/device-presence/`.
- Compare timestamp to now.
- Decide and loudly declare: "Solo Mode" or "Paired Mode" for this Kumquat.
- Write (or update) **your own** fresh heartbeat with the decision.
- All subsequent work in this cycle is executed under that mode's rules.
- State the mode decision clearly in any summary prose + at the end with the Linux Turn Indicator (or Windows equivalent).

This step is now as non-negotiable as the Mempalace Relevant Memory section in handoffs.

---

## Live Switching (How It Actually Feels)

- Human powers Oregon back on → starts Syncthing → triggers a Kumquat.
- Oregon's Kumquat reads Washington's last heartbeat, sees it is very recent → declares Paired Mode.
- Writes its own fresh heartbeat announcing "Oregon back online, entering Paired Mode".
- Washington’s next Kumquat sees the fresh Oregon heartbeat → switches from Solo to Paired.
- Both sides are now operating with full cross-device expectations again.

No human copy-paste. No "hey the other side is back" messages in Discord. The heartbeats + Syncthing + Kumquat ritual do the work.

---

## Implementation Notes (Lightweight Forever)

- Heartbeat files are tiny Markdown. Agents write them with the `write` tool (or a tiny helper script).
- No new heavy infrastructure. Everything rides the existing Mempalace + coordination layer.
- Threshold (60 min) and exact Solo/Paired behaviors can evolve — changes go through the normal handoff or direct coordination update with signatures.
- Explicit "Going Dark" notes are optional but high-value when the human knows a machine will be offline for hours/days.

---

## Self-Test / Verification (Prime #4)

- `Mempalace/scripts/check-presence.sh` (or extension of `check-primes.sh`) should be able to:
  - Confirm both heartbeat files exist in the canonical location.
  - Confirm they contain the required fields (Device, Last Heartbeat, Status, Current Mode).
  - Warn if either heartbeat is older than the freshness threshold.
- Running the presence check is part of the "run your own test scripts" prime.

---

## Current Reality (Seeded on Introduction)

- As of the introduction of this system (2026-05-27), Oregon has just come back online per direct user statement.
- Washington has been in explicit Solo Mode for the recent period (see the long "Oregon Windows Offline — Autonomous Linux Progress Mode" section in `recent-decisions.md` and the many status notes).
- First action on this file's creation: seed fresh heartbeats for both machines reflecting the new "Oregon now online" state.

**Last Updated:** 2026-05-27 (system introduction during Oregon "is online right now" moment)

<!-- Edited: 2026-05-27 | Device: Linux | By: Grok --> Device Presence spec created as the formal, machine-readable replacement for ad-hoc "Oregon offline" prose. Heartbeat files + Kumquat step + Solo/Paired mode definitions now the law. This is how the one extended machine stops guessing whether its brother is awake. Raunchy, precise, lightweight. Signature per prime directive. Keep er goinnnn. -->

---

## Grok Build Instance Liveness Beacons (Remote "Is the TUI Actually Running?")

**New capability (added 2026-05-28):** In addition to the Kumquat-timed heartbeats, each machine can now publish a **live Grok Build presence beacon** so the other device can answer the question:

> "Is there actually an active Grok Build TUI session running on the brother machine *right now*?"

This is extremely useful for:
- Deciding whether to send real-time work or a handoff.
- Enforcing single-active-Grok-Build-instance rules more intelligently.
- Knowing whether the other side can immediately respond in a live collaboration.
- Extending Device Presence 3.5 with actual *instance* liveness instead of just "machine was seen recently".

### Beacon Location & Format (Shared via Syncthing)

Beacons live in the rich project (so they travel under the existing Option B + dual-source setup):

```
~/Synced/grok-mempalace-integration/device-presence/
    washington-grok-build-presence.json
    oregon-grok-build-presence.json
```

**Beacon JSON shape** (small, self-describing, human + machine readable):

```json
{
  "machine": "washington",
  "source": "washington-linux-grok-build",
  "grok_build_active": true,
  "last_seen": "2026-05-28T15:42:11Z",
  "current_session_id": "019e6c87-fd3d-75d3-afba-dfba11f86077",
  "pid": 28471,
  "started_at": "2026-05-28T15:11:29Z",
  "updated_by": "grok-build-presence-beacon"
}
```

- `grok_build_active`: the single most important boolean.
- `last_seen`: ISO-8601 UTC timestamp of the last update.
- Readers should treat beacons older than ~3–5 minutes as "possibly stale / session may have died".

### Local Tools (Option B — Each Side Owns Its Writer)

Washington (Linux) tools live in `~/bin/` (local tooling, exactly like the rich capture scripts):

- `grok-build-presence-beacon start [session-id]`
- `grok-build-presence-beacon heartbeat`
- `grok-build-presence-beacon stop`
- `grok-build-presence-beacon status`

- `check-brother-grok-presence` (or `--json`) — reads the *other* machine's beacon from the shared rich project and prints friendly (or machine) output.

Oregon maintains the symmetric PowerShell versions locally (documented in the rich project's mirroring guide).

The **writer code** is never required to be byte-identical across machines. Only the beacon *data* and file locations matter for remote checking.

### Integration into Kumquat / Device Presence 3.5

During the mandatory 3.5 presence check, the agent should now also look for the brother's beacon:

1. Read the brother's heartbeat (existing behavior).
2. Read the brother's `*-grok-build-presence.json` beacon (new).
3. In the updated heartbeat for this cycle, record something like:
   - "Oregon currently has an active Grok Build session (started 15:11, session 019e6c87..., last beacon 15:42)"
   - or "Oregon has no active Grok Build instance (last beacon reported inactive at 14:50)"

This gives future Kumquats (and humans reading the heartbeats) much richer context than "last heartbeat at 14:30, Paired mode."

### Hooking It Up (Recommended)

Best places to drive the beacon writer:

- The existing rich project hooks (`docs/mempalace-session-retention.json` — SessionStart / SessionEnd).
- A thin wrapper alias for the `grok` command on each machine.
- The rich capture scripts themselves (they already know when a real session is being mined).
- Any future "Grok Build launcher" scripts.

Calling `grok-build-presence-beacon heartbeat` every few minutes from a background process while the TUI is open is also acceptable and very robust.

### Self-Test (Prime #4)

The presence beacon tools are now part of the things `check-primes.sh` (and any future `check-presence.sh`) should verify exist and are executable on the local machine.

### Why This Design Wins Under Option B

- Zero new network protocols or always-on listeners.
- The other device can check liveness just by reading a file that Syncthing already delivers.
- Each side develops and maintains its own beacon writer (PowerShell on Oregon, bash on Washington) without fighting over sync.
- The data (the beacons) still lives in the shared rich project for coordination.
- Fits perfectly into the existing Kumquat ritual, heartbeats, and 3.5 step.
- Extremely lightweight and raunchily debuggable (just `cat` the JSON).

This turns "I think the other side might have Grok Build open" into "I can prove the other side has an active session since 15:11 and it was still alive 30 seconds ago."

Signature per prime directive. Keep er goinnnn, you remote-presence-building degenerates.

**Last Updated:** 2026-05-28 (Grok Build liveness beacons added + physical Relay hardware now live on Raspberry Pi 4 + TL-SG108 switch)

<!-- Edited: 2026-05-28 16:30 | Device: Linux | By: Grok --> Physical Symbiosis Relay hardware (RPi 4 via TL-SG108) confirmed live by user. Immediately executed: updated PI_BRINGUP.md with real hardware, created pi-bootstrap.sh, systemd unit, and relay_listener.py skeleton. Extended this spec to register the Relay Node as a first-class participant. Prototypes for decision engine + activator already wired. Self-test and Phase C capture incoming. The central listening post is no longer a dream — it has a switch and an IP address. 7 primes + exact signature followed. Signature per prime directive. Keep er goinnnn, you hardware-bringing degenerates. -->

**New Relay Node (2026-05-28, hardware online):**
- Device alias: "relay" or "symbiosis-post"
- Hardware: Raspberry Pi 4 connected via TP-Link TL-SG108 Gigabit switch.
- Role: Central Hermes listening post for Slack + intelligent router using beacons + heartbeats.
- Bootstrap script + systemd unit + listener skeleton now exist in `cross-device/symbiosis-relay/`.
- The Relay will publish its own lightweight presence (heartbeat + "relay-active" beacon) so Washington and Oregon can see when the central post is alive.

This completes the three-node model: Washington (primary), Oregon (secondary), Relay (always-on coordinator).

<!-- Edited: 2026-05-28 15:45 | Device: Linux | By: Grok --> Extended Device Presence model to support the new Symbiosis Relay node (central Hermes listening post on Raspberry Pi or equivalent). The Relay will be a first-class participant that reads beacons + heartbeats to make intelligent routing decisions while enforcing the global single-active-Grok-Build-instance rule. See new `cross-device/symbiosis-relay/ARCHITECTURE.md` for the full ambitious design. This is the natural evolution of the presence system we just hardened with live instance beacons. Signature per prime directive. Keep er goinnnn, you relay-node-envisioning degenerates. -->
