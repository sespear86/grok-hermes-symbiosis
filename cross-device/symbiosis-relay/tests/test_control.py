"""Unit tests for control.py (AUTON 474101a5 B1)."""
from __future__ import annotations

import os
from pathlib import Path
from unittest import mock

import control


def _task(msg: str, **extra):
    base = {
        "type": "grok_build_task",
        "correlation_id": "test-corr",
        "original_message": msg,
        "task_reality": "real_slack",
        "slack_user": "U_TEST",
    }
    base.update(extra)
    return base


def test_parse_grok_close():
    a = control.parse_control(_task("grok close"))
    assert a is not None
    assert a.command == "close"


def test_parse_no_trust_without_gate(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    t = {"type": "t", "correlation_id": "c", "original_message": "grok close"}
    assert control.parse_control(t) is None


def test_parse_with_allow_all(monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_CONTROL_ALLOW_ALL", "1")
    t = {"type": "t", "correlation_id": "c", "original_message": "grok status"}
    a = control.parse_control(t)
    assert a and a.command == "status"


def test_plain_text_not_control(monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_CONTROL_ALLOW_ALL", "1")
    assert control.parse_control(_task("just do the thing")) is None


def test_authorize_allowlist_empty(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    monkeypatch.setenv("SYMBIOSIS_CONTROL_SLACK_USERS", "")
    ok, reason = control.authorize(_task("grok close"))
    assert not ok
    assert reason == "allowlist_empty"


def test_authorize_not_in_list(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    monkeypatch.setenv("SYMBIOSIS_CONTROL_SLACK_USERS", "U_ALLOWED")
    ok, reason = control.authorize(_task("grok close", slack_user="U_OTHER"))
    assert not ok
    assert reason == "not_in_allowlist"


def test_authorize_ok(monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_CONTROL_SLACK_USERS", "U_TEST")
    ok, _ = control.authorize(_task("grok close"))
    assert ok


def test_execute_dry_run(monkeypatch, tmp_path):
    monkeypatch.setenv("SYMBIOSIS_CONTROL_DRY_RUN", "1")
    action = control.ControlAction("close", "", "grok close")
    r = control.execute(action, device="washington", shared_base=tmp_path)
    assert r.ok
    assert "dry_run" in r.detail


def test_discover_pts_from_marker(tmp_path):
    m = tmp_path / "device-presence" / ".current_bust_tui_pane"
    m.parent.mkdir(parents=True)
    m.write_text("grok:pts:pts/7")
    assert control.discover_grok_pts(tmp_path) == "pts/7"