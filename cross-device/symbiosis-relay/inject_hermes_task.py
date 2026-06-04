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
    to_device = None
    as_real_slack = False
    slack_user = None
    slack_channel_id = os.environ.get("SYMBIOSIS_SLACK_CHANNEL_ALL", "C0B70DB2X36")

    if "--priority" in sys.argv:
        idx = sys.argv.index("--priority")
        if idx + 1 < len(sys.argv):
            priority = sys.argv[idx + 1]

    if "--channel" in sys.argv:
        idx = sys.argv.index("--channel")
        if idx + 1 < len(sys.argv):
            channel = sys.argv[idx + 1]

    if "--to-device" in sys.argv:
        idx = sys.argv.index("--to-device")
        if idx + 1 < len(sys.argv):
            to_device = sys.argv[idx + 1].strip().lower()

    if "--as-real-slack" in sys.argv:
        as_real_slack = True

    if "--slack-user" in sys.argv:
        idx = sys.argv.index("--slack-user")
        if idx + 1 < len(sys.argv):
            slack_user = sys.argv[idx + 1]

    if "--slack-channel-id" in sys.argv:
        idx = sys.argv.index("--slack-channel-id")
        if idx + 1 < len(sys.argv):
            slack_channel_id = sys.argv[idx + 1]

    # Smart shared base detection (SYMBIOSIS_SHARED first, per device_selector/relay_listener pattern)
    shared = Path(os.environ.get("SYMBIOSIS_SHARED", "/home/Irikash/Synced/grok-mempalace-integration"))
    if not shared.exists():
        shared = Path("/home/pi/Synced/grok-mempalace-integration")

    relay_root = shared / "symbiosis-relay"
    if to_device:
        inbox = relay_root / "incoming" / to_device
    else:
        inbox = relay_root / "incoming" / "hermes"
    inbox.mkdir(parents=True, exist_ok=True)

    correlation = f"slack-{int(time.time())}"
    ts = str(time.time())
    task = {
        "type": "grok_build_task",
        "source": "slack",
        "original_message": message,
        "correlation_id": correlation,
        "priority": priority,
        "slack_channel": channel,
        "slack_ts": ts,
        "slack_thread_ts": ts,
        "context_hints": {
            "injected_via": "inject_hermes_task.py",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "simulated_channel": channel,
        },
    }
    if as_real_slack:
        task["is_real"] = True
        task["task_reality"] = "real_slack"
        task["slack_channel_id"] = slack_channel_id
    if slack_user:
        task["slack_user"] = slack_user

    filename = f"task-{correlation}.json"
    (inbox / filename).write_text(json.dumps(task, indent=2))

    dest = f"incoming/{to_device or 'hermes'}"
    print(f"✅ Injected task: {filename} → {dest}")
    print(f"   Message: {message[:80]}{'...' if len(message) > 80 else ''}")
    print(f"   Channel: {channel} | Priority: {priority}")
    if to_device:
        print(f"   Run: SYMBIOSIS_CONTROL_ALLOW_ALL=1 python3 washington_activator.py --once  (device={to_device})")
    else:
        print("   The Relay should pick this up on its next 30s cycle (if a target is available).")


if __name__ == "__main__":
    main()
