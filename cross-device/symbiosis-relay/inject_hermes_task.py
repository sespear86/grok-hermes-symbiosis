#!/usr/bin/env python3
"""
Quick helper to inject a realistic Slack-derived task into the Relay's Hermes inbox.

Usage (from Washington or any synced machine):
    python3 inject_hermes_task.py "Your actual Slack message here" --priority high

This drops a properly formatted task that the relay_listener.py will pick up
as a "real" incoming Hermes/Slack event instead of generating a synthetic test.

Signature per prime directive. Keep er goinnnn.
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 inject_hermes_task.py 'Your Slack message / request'")
        print("       python3 inject_hermes_task.py 'message' --priority high")
        sys.exit(1)

    message = sys.argv[1]
    priority = "normal"
    channel = "#all-devices"

    if "--priority" in sys.argv:
        idx = sys.argv.index("--priority")
        if idx + 1 < len(sys.argv):
            priority = sys.argv[idx + 1]

    if "--channel" in sys.argv:
        idx = sys.argv.index("--channel")
        if idx + 1 < len(sys.argv):
            channel = sys.argv[idx + 1]

    # Smart shared base detection (SYMBIOSIS_SHARED first, per device_selector/relay_listener pattern)
    shared = Path(os.environ.get("SYMBIOSIS_SHARED", "/home/Irikash/Synced/grok-mempalace-integration"))
    if not shared.exists():
        shared = Path("/home/pi/Synced/grok-mempalace-integration")

    hermes_inbox = shared / "symbiosis-relay" / "incoming" / "hermes"
    hermes_inbox.mkdir(parents=True, exist_ok=True)

    correlation = f"slack-{int(time.time())}"
    task = {
        "type": "grok_build_task",
        "source": "slack",
        "original_message": message,
        "correlation_id": correlation,
        "priority": priority,
        "slack_channel": channel,
        "slack_thread_ts": str(time.time()),
        "context_hints": {
            "injected_via": "inject_hermes_task.py",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "simulated_channel": channel
        }
    }

    filename = f"task-{correlation}.json"
    (hermes_inbox / filename).write_text(json.dumps(task, indent=2))

    print(f"✅ Injected real-style Hermes/Slack task: {filename}")
    print(f"   Message: {message[:80]}{'...' if len(message) > 80 else ''}")
    print(f"   Channel: {channel} | Priority: {priority}")
    print("   The Relay should pick this up on its next 30s cycle (if a target is available).")


if __name__ == "__main__":
    main()
