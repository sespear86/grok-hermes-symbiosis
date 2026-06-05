"""NL /autonomous control tests (AUTON 98822e73)."""
from __future__ import annotations

import control

CANONICAL = (
    'Have Grok Build run "/autonomous Identify another part of Project Symbiosis to '
    'tackle. Then, execute building it out.", on the Washington device.'
)
EXPECTED_PAYLOAD = (
    "/autonomous Identify another part of Project Symbiosis to tackle. "
    "Then, execute building it out."
)


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


def test_parse_natural_autonomous_exact_user_command(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    t = _task(
        CANONICAL,
        is_real=False,
        task_reality="control_override",
        context_hints={"force_control": True, "original_user_command": CANONICAL},
    )
    a = control.parse_control(t)
    assert a is not None
    assert a.command in ("instruct", "autonomous")
    assert a.payload.startswith("/autonomous Identify another part")
    assert "on the Washington" not in a.payload


def test_trust_override_for_control_magic_without_is_real(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    t = {
        "type": "grok_build_task",
        "correlation_id": "c",
        "original_message": 'Please run "/autonomous fix the relay" now',
        "is_real": False,
    }
    a = control.parse_control(t)
    assert a is not None
    assert a.trust_note == "control_command_override"


def test_trust_override_have_grok_build_run(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    t = {
        "type": "grok_build_task",
        "correlation_id": "c",
        "original_message": "have grok build run /autonomous ship it",
        "is_real": False,
    }
    a = control.parse_control(t)
    assert a is not None
    assert a.trust_note == "control_command_override"


def test_device_hint_from_text():
    hints = control.enrich_control_hints(CANONICAL, {})
    assert hints.get("explicit_target_device") == "washington"
    assert hints.get("force_control") is True


def test_execute_nl_autonomous_uses_pts_argv(monkeypatch, tmp_path):
    monkeypatch.setenv("SYMBIOSIS_CONTROL_DRY_RUN", "0")
    pts_script = tmp_path / "symbiosis-relay" / "tools" / "pts-inject-input.py"
    pts_script.parent.mkdir(parents=True)
    pts_script.write_text("#!/usr/bin/env python3\nimport sys\nprint(sys.argv)\n")
    marker = tmp_path / "device-presence" / ".current_bust_tui_pane"
    marker.parent.mkdir(parents=True)
    marker.write_text("grok:pts:pts/9")
    calls: list[list[str]] = []

    def fake_run(argv, **kwargs):
        calls.append(list(argv))
        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(control.subprocess, "run", fake_run)
    action = control.ControlAction("instruct", EXPECTED_PAYLOAD, CANONICAL)
    r = control.execute(action, device="washington", shared_base=tmp_path)
    assert r.ok
    assert calls
    assert "pts-inject-input.py" in calls[0][1]
    assert EXPECTED_PAYLOAD in calls[0][-1]


def test_plain_text_still_not_control(monkeypatch):
    monkeypatch.delenv("SYMBIOSIS_CONTROL_ALLOW_ALL", raising=False)
    assert control.parse_control(_task("just do the thing", is_real=True)) is None