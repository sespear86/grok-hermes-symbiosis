#!/usr/bin/env python3
"""
Symbiosis Relay — Device Selector (Early Prototype)

Reads the existing Grok Build liveness beacons + heartbeats from the shared
rich project and decides which physical device should handle an incoming task.

Core rules (initial version):
- Hard global constraint: At most ONE Grok Build instance active across the entire system.
- Prioritization: Washington > Oregon when both are viable.
- The Relay (this code, running on the Pi) is the ultimate arbiter.

This is the decision brain that the central Hermes listener on the Raspberry Pi
will call when a new Slack message arrives.

Location during design: inside the grok-hermes-symbiosis coordination layer.
Will be deployed to the actual Relay hardware later.

Follows all 7 Primes. Will receive full raunchy treatment and signatures as it matures.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

# These paths assume the rich project is synced to the Relay device via Syncthing.
# Use SYMBIOSIS_SHARED env var for portability across Washington / Oregon / Raspberry Pi Relay.
# Smart default: Pi production path, auto-detect Washington for local testing of the relay stack.
_default_shared = "/home/pi/Synced/grok-mempalace-integration"
if Path("/home/Irikash/Synced/grok-mempalace-integration").exists():
    _default_shared = "/home/Irikash/Synced/grok-mempalace-integration"
SHARED_BASE = Path(os.environ.get("SYMBIOSIS_SHARED", _default_shared))
BEACON_DIR = SHARED_BASE / "device-presence"
HEARTBEAT_DIR = SHARED_BASE / "symbiosis" / "device-presence"

DEVICES = ["washington", "oregon"]


def load_beacon(machine: str) -> dict | None:
    path = BEACON_DIR / f"{machine}-grok-build-presence.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def load_heartbeat(machine: str) -> dict | None:
    path = HEARTBEAT_DIR / f"{machine}.md"
    if not path.exists():
        return None
    text = path.read_text()

    # Parse key fields from the structured Markdown heartbeat format
    status = "unknown"
    current_mode = ""
    last_heartbeat_str = ""

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("**Status:**"):
            status = line.split("**Status:**", 1)[1].strip().lower()
        elif line.startswith("**Current Mode:**"):
            current_mode = line.split("**Current Mode:**", 1)[1].strip()
        elif line.startswith("**Last Heartbeat:**"):
            last_heartbeat_str = line.split("**Last Heartbeat:**", 1)[1].strip()

    is_online = "online" in status
    is_paired = "paired" in current_mode.lower()
    appears_healthy = is_online and is_paired

    return {
        "status": status,
        "current_mode": current_mode,
        "last_heartbeat_raw": last_heartbeat_str,
        "appears_paired_and_healthy": appears_healthy,
        "raw_preview": text[:1500],
    }


def load_relay_presence() -> dict | None:
    """Check if the central Raspberry Pi relay itself is alive (via its own beacon)."""
    path = BEACON_DIR / "relay-presence.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        # Reuse the freshness check
        if is_beacon_fresh(data, max_age_seconds=300):
            return data
        return {"stale": True, **data}
    except Exception:
        return None


def is_beacon_fresh(beacon: dict, max_age_seconds: int = 300) -> bool:
    if not beacon or not beacon.get("last_seen"):
        return False
    try:
        last = datetime.fromisoformat(beacon["last_seen"].replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - last).total_seconds()
        return age < max_age_seconds
    except Exception:
        return False


def beacon_age_seconds(machine: str) -> float | None:
    """Exported for activator health interlock + status enrichment (DESIGN PR2)."""
    path = BEACON_DIR / f"{machine}-grok-build-presence.json"
    if not path.exists():
        return None
    try:
        b = json.loads(path.read_text())
        last = datetime.fromisoformat(b.get("last_seen", "").replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - last).total_seconds()
    except Exception:
        return None


def select_device_for_grok_build_task() -> dict:
    """
    Returns a decision dict with full reasoning.
    The Relay uses this to decide routing while strictly enforcing the single-active rule.
    """
    washington_beacon = load_beacon("washington")
    oregon_beacon = load_beacon("oregon")
    washington_heartbeat = load_heartbeat("washington")
    oregon_heartbeat = load_heartbeat("oregon")
    relay_presence = load_relay_presence()

    w_beacon_active = bool(washington_beacon and washington_beacon.get("grok_build_active"))
    o_beacon_active = bool(oregon_beacon and oregon_beacon.get("grok_build_active"))

    w_beacon_fresh = is_beacon_fresh(washington_beacon)
    o_beacon_fresh = is_beacon_fresh(oregon_beacon)

    w_heartbeat_healthy = bool(washington_heartbeat and washington_heartbeat.get("appears_paired_and_healthy"))
    o_heartbeat_healthy = bool(oregon_heartbeat and oregon_heartbeat.get("appears_paired_and_healthy"))

    # === Global single-active enforcement (non-negotiable) ===
    if w_beacon_active and o_beacon_active:
        return {
            "chosen": None,
            "reason": "HARD VIOLATION: Both devices report active Grok Build beacons. The Relay refuses to route until one stands down.",
            "washington_beacon": washington_beacon,
            "oregon_beacon": oregon_beacon,
            "washington_heartbeat": washington_heartbeat,
            "oregon_heartbeat": oregon_heartbeat,
            "single_active_violation": True,
        }

    # === Normal routing with Washington priority ===
    if w_beacon_active and w_beacon_fresh:
        return {
            "chosen": "washington",
            "reason": "Washington has a fresh active Grok Build beacon + healthy heartbeat. Highest priority target.",
            "washington_beacon": washington_beacon,
            "oregon_beacon": oregon_beacon,
            "washington_heartbeat": washington_heartbeat,
            "oregon_heartbeat": oregon_heartbeat,
            "single_active_violation": False,
        }

    if o_beacon_active and o_beacon_fresh:
        return {
            "chosen": "oregon",
            "reason": "Oregon has a fresh active Grok Build beacon. Washington has none → falling back (lower priority).",
            "washington_beacon": washington_beacon,
            "oregon_beacon": oregon_beacon,
            "washington_heartbeat": washington_heartbeat,
            "oregon_heartbeat": oregon_heartbeat,
            "single_active_violation": False,
        }

    # === Wake-up decisions (no active sessions) ===
    # Prefer Washington if it looks healthy on heartbeat (even without beacon yet)
    if w_heartbeat_healthy:
        return {
            "chosen": "washington",
            "reason": "No active Grok Build sessions detected. Washington has healthy Paired/Online heartbeat → preferred wake-up target.",
            "washington_beacon": washington_beacon,
            "oregon_beacon": oregon_beacon,
            "washington_heartbeat": washington_heartbeat,
            "oregon_heartbeat": oregon_heartbeat,
            "single_active_violation": False,
        }

    if o_heartbeat_healthy:
        return {
            "chosen": "oregon",
            "reason": "No active sessions. Washington not reporting healthy presence → falling back to Oregon.",
            "washington_beacon": washington_beacon,
            "oregon_beacon": oregon_beacon,
            "washington_heartbeat": washington_heartbeat,
            "oregon_heartbeat": oregon_heartbeat,
            "single_active_violation": False,
        }

    return {
        "chosen": None,
        "reason": "No devices currently reporting healthy presence (beacons or heartbeats). Task should be queued or manual intervention requested.",
        "washington_beacon": washington_beacon,
        "oregon_beacon": oregon_beacon,
        "washington_heartbeat": washington_heartbeat,
        "oregon_heartbeat": oregon_heartbeat,
        "relay_presence": relay_presence,
        "single_active_violation": False,
    }


if __name__ == "__main__":
    decision = select_device_for_grok_build_task()
    print(json.dumps(decision, indent=2, default=str))
