"""Tests for send_to_slack (AUTON 474101a5 B2)."""
from __future__ import annotations

from unittest import mock

import send_to_slack


def test_resolve_channel_id_from_map():
    cid = send_to_slack.resolve_channel_id("#all-devices")
    assert cid.startswith("C") or len(cid) > 5


def test_send_message_thread_ts(monkeypatch):
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")
    mock_resp = {"ok": True, "ts": "123.456"}
    with mock.patch.object(send_to_slack, "WebClient") as WC:
        client = WC.return_value
        client.chat_postMessage.return_value = mock_resp
        out = send_to_slack.send_message("C_TEST", "hello", thread_ts="111.222")
    assert out["ok"] is True
    client.chat_postMessage.assert_called_once()
    kwargs = client.chat_postMessage.call_args.kwargs
    assert kwargs.get("thread_ts") == "111.222"


def test_ack_control_result_uses_channel_id(monkeypatch):
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")
    with mock.patch.object(send_to_slack, "send_message", return_value={"ok": True, "ts": "1"}) as sm:
        task = {
            "slack_channel_id": "C_CHAN",
            "slack_ts": "ts1",
            "correlation_id": "corr-1",
        }
        class R:
            ok = True
            detail = "done"
            command = "close"

        send_to_slack.ack_control_result(task, R(), device="washington")
        sm.assert_called_once()
        assert sm.call_args[0][0] == "C_CHAN"