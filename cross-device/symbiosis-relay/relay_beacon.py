#!/usr/bin/env python3
"""
Symbiosis Relay Presence Beacon Writer

The Relay (Pi) needs to publish its own liveness so Washington and Oregon can see
that the central listening post is alive and healthy.

This tiny script writes a simple beacon file into the shared device-presence directory.

Run it periodically (or from the main listener) so the rest of the symbiosis knows the Relay is up.

Follows the same spirit as the Grok Build liveness beacons we built earlier.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

# Default to the actual Pi path (production target), but fall back gracefully when testing on Washington/Oregon.
_default_shared = "/home/pi/Synced/grok-mempalace-integration"
if Path("/home/Irikash/Synced/grok-mempalace-integration").exists():
    _default_shared = "/home/Irikash/Synced/grok-mempalace-integration"
BEACON_DIR = Path(os.environ.get("SYMBIOSIS_SHARED", _default_shared)) / "device-presence"
BEACON_FILE = BEACON_DIR / "relay-presence.json"

BEACON_DIR.mkdir(parents=True, exist_ok=True)

def write_relay_beacon():
    data = {
        "machine": "symbiosis-relay",
        "source": "raspberry-pi-4-tl-sg108",
        "relay_active": True,
        "last_seen": datetime.now(timezone.utc).isoformat(),
        "role": "central-hermes-listening-post",
        "notes": "Slack gateway + intelligent router for the one extended machine"
    }
    BEACON_FILE.write_text(json.dumps(data, indent=2))
    print(f"Relay beacon written: {BEACON_FILE}")

def main():
    """Entry point for direct execution or import."""
    write_relay_beacon()

if __name__ == "__main__":
    main()
