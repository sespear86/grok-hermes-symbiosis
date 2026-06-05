"""Integration tests for explicit_target_device + force_control dispatch (AUTON 98822e73)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import relay_listener

CANONICAL = (
    'Have Grok Build run "/autonomous Identify another part of Project Symbiosis to '
    'tackle. Then, execute building it out.", on the Washington device.'
)


def _make_task_with_hints(device: str = "washington") -> dict:
    return {
        "type": "grok_build_task",
        "source": "slack",
        "original_message": CANONICAL,
        "correlation_id": "slack-test-explicit-98822e73",
        "slack_channel": "#all-devices",
        "slack_channel_id": "C0B70DB2X36",
        "context_hints": {
            "explicit_target_device": device,
            "force_control": True,
            "original_user_command": CANONICAL,
            "run_in_tui": True,
        },
    }


def _setup_relay_paths(tmp_path: Path, monkeypatch):
    base = tmp_path / "shared"
    hermes = base / "symbiosis-relay" / "incoming" / "hermes"
    washington = base / "symbiosis-relay" / "incoming" / "washington"
    oregon = base / "symbiosis-relay" / "incoming" / "oregon"
    hermes.mkdir(parents=True)
    washington.mkdir(parents=True)
    oregon.mkdir(parents=True)
    monkeypatch.setattr(relay_listener, "SHARED_BASE", base)
    monkeypatch.setattr(relay_listener, "COMMAND_BASE", base / "symbiosis-relay" / "incoming")
    monkeypatch.setattr(relay_listener, "HERMES_INBOX", hermes)
    monkeypatch.setattr(relay_listener, "PROCESSED_HERMES", hermes / "processed")
    return hermes, washington, oregon


def test_listener_explicit_forces_washington_inbox(tmp_path, monkeypatch):
    hermes, washington, oregon = _setup_relay_paths(tmp_path, monkeypatch)
    task = _make_task_with_hints("washington")
    path = hermes / f"task-{task['correlation_id']}.json"
    path.write_text(json.dumps(task))

    decision = {
        "chosen": None,
        "reason": "no beacon",
        "single_active_violation": False,
        "washington_beacon": {},
        "oregon_beacon": {},
    }
    with patch("relay_listener.select_device_for_grok_build_task", return_value=decision):
        relay_listener.run_once()

    assert list(washington.glob("task-*.json"))
    assert not list(oregon.glob("task-slack-test-explicit-98822e73.json"))
    assert not path.exists()


def test_listener_explicit_dispatches_on_violation(tmp_path, monkeypatch):
    hermes, washington, _oregon = _setup_relay_paths(tmp_path, monkeypatch)
    task = _make_task_with_hints("washington")
    path = hermes / f"task-{task['correlation_id']}.json"
    path.write_text(json.dumps(task))

    decision = {
        "chosen": "oregon",
        "reason": "would pick oregon",
        "single_active_violation": True,
        "washington_beacon": {"grok_build_active": True},
        "oregon_beacon": {"grok_build_active": True},
    }
    with patch("relay_listener.select_device_for_grok_build_task", return_value=decision):
        relay_listener.run_once()

    dispatched = list(washington.glob("task-slack-test-explicit-98822e73.json"))
    assert dispatched
    data = json.loads(dispatched[0].read_text())
    assert data["context_hints"]["relay_decision"].startswith("explicit:washington")