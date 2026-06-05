#!/usr/bin/env python3
"""
Symbiosis Relay - Slack to Hermes Inbox Bridge

Listens to Slack (using Socket Mode) for messages in the target channels
(#pi, #linux, #windows, #all-devices) and drops structured task JSON files
into the hermes incoming directory that relay_listener.py already watches.

Requires:
- SLACK_BOT_TOKEN (xoxb-PLACEHOLDER-...)
- SLACK_APP_TOKEN (xapp-...) for Socket Mode

Run this under the relay user, ideally as a systemd service alongside the main listener.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

import control

# === Configuration ===
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN") or ""  # legacy bridge; prefer env + ~/.hermes/.env (see slack_task_ingest.py); no hardcoded secrets (X1)
APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")  # Must be provided for Socket Mode

# Target channels (by name - we resolve IDs at startup)
TARGET_CHANNELS = {"#pi", "#linux", "#windows", "#all-devices"}

# Paths (works on both Pi and Washington for testing)
SHARED = Path(os.environ.get("SYMBIOSIS_SHARED", "/home/relay/Synced/grok-mempalace-integration"))
HERMES_INBOX = SHARED / "symbiosis-relay" / "incoming" / "hermes"
HERMES_INBOX.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {msg}")

def create_task_from_message(event: dict, channel_name: str) -> dict:
    """Turn a Slack message event into a relay task."""
    text = event.get("text", "").strip()
    user = event.get("user", "unknown")
    ts = event.get("ts", "")
    channel = event.get("channel", "")
    thread_ts = event.get("thread_ts")

    hints = control.enrich_control_hints(
        text,
        {
            "source_channel": channel_name,
            "received_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    task = {
        "type": "grok_build_task",
        "source": "slack",
        "original_message": text,
        "correlation_id": f"slack-{channel}-{int(time.time())}",
        "priority": "normal",
        "slack_channel": channel_name,
        "slack_channel_id": channel,
        "slack_user": user,
        "slack_ts": ts,
        "slack_thread_ts": thread_ts,
        "context_hints": hints,
    }
    if hints.get("force_control"):
        task["is_real"] = False
        task["task_reality"] = "control_override"
    return task

def write_task_to_inbox(task: dict):
    """Drop the task JSON into the hermes inbox for the listener."""
    filename = f"task-{task['correlation_id']}.json"
    path = HERMES_INBOX / filename
    path.write_text(json.dumps(task, indent=2))
    log(f"Dropped task for channel #{task.get('slack_channel')}: {filename}")

def process_message(client: WebClient, event: dict):
    """Handle an incoming message event."""
    channel_id = event.get("channel")
    if not channel_id:
        return

    # Resolve channel name (simple cache could be added later)
    try:
        info = client.conversations_info(channel=channel_id)
        channel_name = info["channel"]["name"]
    except Exception as e:
        log(f"Could not resolve channel name for {channel_id}: {e}")
        return

    if channel_name not in [c.lstrip("#") for c in TARGET_CHANNELS]:
        return

    # Ignore bot messages and our own echoes
    if event.get("bot_id") or event.get("subtype") in ("bot_message", "message_changed"):
        return

    text = event.get("text", "").strip()
    if not text:
        return

    log(f"Received message in #{channel_name}: {text[:80]}...")

    task = create_task_from_message(event, channel_name)
    write_task_to_inbox(task)

def main():
    if not APP_TOKEN:
        print("ERROR: SLACK_APP_TOKEN (xapp-...) is required for Socket Mode.")
        print("Please set it as environment variable and restart.")
        return

    if not BOT_TOKEN.startswith("xoxb-"):
        print("WARNING: SLACK_BOT_TOKEN does not look like a valid bot token.")

    web_client = WebClient(token=BOT_TOKEN)
    socket_client = SocketModeClient(
        app_token=APP_TOKEN,
        web_client=web_client
    )

    def handle_events(client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            event = req.payload.get("event", {})
            if event.get("type") == "message":
                process_message(web_client, event)

            # Acknowledge the event
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

    socket_client.socket_mode_request_listeners.append(handle_events)
    socket_client.connect()
    log("Symbiosis Relay Slack bridge connected via Socket Mode.")

    # Keep the process alive
    while True:
        time.sleep(30)

if __name__ == "__main__":
    main()
