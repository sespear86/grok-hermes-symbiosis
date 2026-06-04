"""Activator control hook tests (AUTON 474101a5 B3)."""
from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import activator_core as core
import pytest


@pytest.fixture
def relay_tree(tmp_path, monkeypatch):
    shared = tmp_path / "shared"
    relay = shared / "symbiosis-relay"
    inbox = relay / "incoming" / "washington"
    for d in (
        inbox,
        inbox / "processing",
        inbox / "failed",
        inbox / "processed",
        inbox / "pending-prompts",
        relay / "status" / "washington",
        shared / "device-presence",
        relay / "tools",
    ):
        d.mkdir(parents=True)

    monkeypatch.setenv("SYMBIOSIS_SHARED", str(shared))
    monkeypatch.setenv("SYMBIOSIS_DEVICE", "washington")
    monkeypatch.setattr(core, "SHARED_BASE", shared)
    monkeypatch.setattr(core, "COMMAND_INBOX", inbox)
    monkeypatch.setattr(core, "PROCESSING_DIR", inbox / "processing")
    monkeypatch.setattr(core, "FAILED_DIR", inbox / "failed")
    monkeypatch.setattr(core, "PROCESSED_DIR", inbox / "processed")
    monkeypatch.setattr(core, "PENDING_PROMPTS_DIR", inbox / "pending-prompts")
    monkeypatch.setattr(core, "STATUS_OUTBOX", relay / "status" / "washington")
    monkeypatch.setattr(core, "LOG_DIR", tmp_path / "logs")
    return shared, inbox


def _drop_control_task(inbox: Path, msg: str = "grok close", **extra):
    payload = {
        "type": "grok_build_task",
        "correlation_id": "ctrl-test-1",
        "original_message": msg,
        "task_reality": "real_slack",
        "slack_channel_id": "C_TEST",
        "slack_ts": "1.0",
        "slack_thread_ts": "1.0",
        **extra,
    }
    p = inbox / "task-ctrl-test-1.json"
    p.write_text(json.dumps(payload))
    return p


def test_control_close_skips_beacon_and_hermes(relay_tree, monkeypatch):
    _, inbox = relay_tree
    _drop_control_task(inbox)
    monkeypatch.setenv("SYMBIOSIS_CONTROL_ALLOW_ALL", "1")
    monkeypatch.setenv("SYMBIOSIS_CONTROL_DRY_RUN", "1")

    with mock.patch.object(core, "check_health", return_value={"ok": True, "beacon_age_seconds": 1}):
        with mock.patch.object(core, "fire_beacon") as fb:
            with mock.patch.object(core, "prompt_grok_build") as pg:
                with mock.patch.object(core.send_to_slack, "ack_control_result", return_value={"ok": True}):
                    n = core.process_inbox_once()

    assert n == 1
    fb.assert_not_called()
    pg.assert_not_called()
    assert (inbox / "processed" / "task-ctrl-test-1.json").is_file()


def test_control_rejected_no_hermes(relay_tree, monkeypatch):
    _, inbox = relay_tree
    _drop_control_task(inbox, slack_user="U_BAD")
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    monkeypatch.setenv("SYMBIOSIS_CONTROL_SLACK_USERS", "U_ALLOWED")

    with mock.patch.object(core, "check_health", return_value={"ok": True, "beacon_age_seconds": 1}):
        with mock.patch.object(core, "prompt_grok_build") as pg:
            with mock.patch.object(core.send_to_slack, "nack_control_unauthorized", return_value={"ok": True}):
                n = core.process_inbox_once()

    assert n == 1
    pg.assert_not_called()
    assert (inbox / "processed" / "task-ctrl-test-1.json").is_file()