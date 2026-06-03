#!/usr/bin/env python3
"""
Symbiosis Relay Listener — The Central Cock of the Symbiosis

This is the persistent process that runs on the Raspberry Pi 4 (the Symbiosis Relay).

It is the always-on Hermes instance that:
- Listens for Slack messages (via Hermes gateway — to be wired)
- Uses our Device Presence + Grok Build Liveness Beacons to decide routing
- Enforces the global single-active-Grok-Build-instance rule
- Prioritizes Washington > Oregon
- Dispatches tasks to the chosen device's activator via the file-drop protocol (Option B friendly)

Current implementation: Fully functional decision + dispatch loop using the shared rich project folders.
Run this on the Pi (after bootstrap) for the Relay to start doing real work.

Real Slack/Hermes tasks are now ingested from the `incoming/hermes/` directory (dropped by the Hermes Slack gateway or manual injection).
Synthetic test tasks are only generated as fallback when no real work is queued.

Follows all 7 Primes. Raunchy. Autonomous. Keeps er goinnnn.
"""

import time
import json
import os
import signal
import sys
from pathlib import Path
from datetime import datetime, timezone

# Local imports for the Symbiosis Relay brain
import sys
sys.path.append(str(Path(__file__).parent))
from device_selector import select_device_for_grok_build_task
from relay_beacon import write_relay_beacon  # So the Relay can announce itself to the symbiosis

# === Configuration (Pi-friendly) ===
# Smart default: Pi production path, but auto-detect Washington when the folder exists (for testing the full relay stack locally).
_default_shared = "/home/pi/Synced/grok-mempalace-integration"
if Path("/home/Irikash/Synced/grok-mempalace-integration").exists():
    _default_shared = "/home/Irikash/Synced/grok-mempalace-integration"
SHARED_BASE = Path(os.environ.get("SYMBIOSIS_SHARED", _default_shared))
COMMAND_BASE = SHARED_BASE / "symbiosis-relay" / "incoming"
HERMES_INBOX = SHARED_BASE / "symbiosis-relay" / "incoming" / "hermes"
PROCESSED_HERMES = HERMES_INBOX / "processed"
STATUS_BASE = SHARED_BASE / "symbiosis-relay" / "status"
RELAY_STATUS_FILE = STATUS_BASE / "relay" / "status.json"  # Relay publishes its own health here for observability
LOG_DIR = Path.home() / "symbiosis-relay" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
COMMAND_BASE.mkdir(parents=True, exist_ok=True)
HERMES_INBOX.mkdir(parents=True, exist_ok=True)
PROCESSED_HERMES.mkdir(parents=True, exist_ok=True)
STATUS_BASE.mkdir(parents=True, exist_ok=True)

def log(msg: str, level: str = "info"):
    """Central logging. In production this will feed into Hermes gateway for Slack visibility."""
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] [{level.upper()}] {msg}"
    print(line)
    with open(LOG_DIR / "relay.log", "a") as f:
        f.write(line + "\n")

def dispatch_task_to_device(device: str, task: dict):
    """Drop a command JSON into the device's inbox (the file-drop protocol)."""
    inbox = COMMAND_BASE / device
    inbox.mkdir(parents=True, exist_ok=True)

    correlation = task.get("correlation_id", f"relay-{int(time.time())}")
    filename = f"task-{correlation}.json"
    (inbox / filename).write_text(json.dumps(task, indent=2))

    log(f"DISPATCHED task {correlation} → {device.upper()}")
    return filename

def read_status(device: str) -> dict | None:
    """Peek at the latest status from a device."""
    status_file = STATUS_BASE / device / "status.json"
    if status_file.exists():
        try:
            return json.loads(status_file.read_text())
        except Exception:
            return None
    return None


def get_pending_hermes_tasks() -> list[Path]:
    """Return list of pending real tasks dropped by Hermes/Slack gateway."""
    if not HERMES_INBOX.exists():
        return []
    tasks = [p for p in HERMES_INBOX.glob("task-*.json") if p.is_file()]
    # Oldest first (FIFO-ish for fairness)
    return sorted(tasks, key=lambda p: p.stat().st_mtime)


def consume_hermes_task(task_path: Path) -> dict | None:
    """Move a Hermes task to processed and return its contents."""
    try:
        data = json.loads(task_path.read_text())
        PROCESSED_HERMES.mkdir(parents=True, exist_ok=True)
        archive_name = f"{task_path.stem}-{int(time.time())}.json"
        (PROCESSED_HERMES / archive_name).write_text(task_path.read_text())
        task_path.unlink(missing_ok=True)
        return data
    except Exception as e:
        log(f"Failed to consume Hermes task {task_path.name}: {e}", "error")
        return None

_running = True

def _shutdown_handler(signum, frame):
    global _running
    log(f"Received signal {signum}, shutting down gracefully...")
    _running = False

def main_loop():
    global _running
    signal.signal(signal.SIGTERM, _shutdown_handler)
    signal.signal(signal.SIGINT, _shutdown_handler)

    log("=== SYMBIOSIS RELAY LISTENER STARTING ON RASPBERRY PI ===")
    log("Using Device Presence 3.5 + Liveness Beacons for routing + single-active enforcement")
    log("Washington priority active. Only one Grok Build instance allowed globally.")

    # Publish the Relay's own presence beacon immediately on startup so the symbiosis knows the central post is alive
    try:
        write_relay_beacon()
        log("Relay presence beacon published on startup.")
    except Exception as e:
        log(f"Failed to publish initial relay beacon: {e}", "warning")

    last_beacon_time = time.time()
    BEACON_INTERVAL = 90  # seconds — the Relay announces itself regularly

    while _running:
        try:
            # Periodically re-publish the Relay's own beacon so everyone sees it's healthy
            now = time.time()
            if now - last_beacon_time > BEACON_INTERVAL:
                try:
                    write_relay_beacon()
                    last_beacon_time = now
                except Exception as e:
                    log(f"Failed to refresh relay beacon: {e}", "warning")

            decision = select_device_for_grok_build_task()

            if decision.get("single_active_violation"):
                log("!!! GLOBAL SINGLE-ACTIVE VIOLATION !!!")
                log(decision["reason"])
                # Future: send alert to Slack via Hermes gateway

            elif decision.get("chosen"):
                target = decision["chosen"]
                log(f"DECISION: Route to {target.upper()} — {decision['reason']}")

                # === Real Hermes / Slack task ingestion (the goal) ===
                real_task = None
                pending = get_pending_hermes_tasks()
                if pending:
                    real_task_path = pending[0]
                    real_task = consume_hermes_task(real_task_path)
                    if real_task:
                        log(f"INGESTED real task from Hermes/Slack: {real_task_path.name}")

                if real_task:
                    # Enrich the real Slack task with current relay decision context
                    real_task.setdefault("context_hints", {})
                    real_task["context_hints"]["relay_decision"] = decision["reason"]
                    real_task["context_hints"]["beacon_state"] = {
                        "washington": bool(decision.get("washington_beacon", {}).get("grok_build_active")),
                        "oregon": bool(decision.get("oregon_beacon", {}).get("grok_build_active")),
                    }
                    task = real_task
                    task.setdefault("source", "slack")
                    task.setdefault("type", "grok_build_task")
                else:
                    # Fallback synthetic test task (only when no real work is queued)
                    # In production this path should be rare or disabled.
                    task = {
                        "type": "grok_build_task",
                        "source": "relay-internal-test",
                        "original_message": "Symbiosis Relay self-test task. Confirm you are alive and can accept work from the central listening post.",
                        "correlation_id": f"relay-test-{int(time.time())}",
                        "priority": "normal",
                        "context_hints": {
                            "relay_decision": decision["reason"],
                            "beacon_state": {
                                "washington": bool(decision.get("washington_beacon", {}).get("grok_build_active")),
                                "oregon": bool(decision.get("oregon_beacon", {}).get("grok_build_active")),
                            }
                        }
                    }

                dispatch_task_to_device(target, task)

                # Optional: peek at recent status from the target (for logging)
                status = read_status(target)
                if status:
                    log(f"Latest status from {target}: {status.get('state', 'unknown')} - {status.get('message', '')}")

            else:
                log(f"No viable target right now: {decision.get('reason', 'unknown')}")

        except Exception as e:
            log(f"ERROR in main loop: {e}")

        # Real Slack events arrive via file drop into incoming/hermes/ (from Hermes gateway).
        # 30s poll is acceptable for now; can be tightened or event-driven later.
        time.sleep(30)

    log("Symbiosis Relay listener shut down cleanly.")

if __name__ == "__main__":
    main_loop()
