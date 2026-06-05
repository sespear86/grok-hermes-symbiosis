#!/usr/bin/env python3
"""
send_to_slack.py — Outbound Slack poster for relay control acks (AUTON 474101a5).
Token: SLACK_BOT_TOKEN from env or ~/.hermes/.env only (no hardcoded fallback).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

try:
    from slack_sdk.web import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    WebClient = None  # type: ignore[misc, assignment]
    SlackApiError = Exception  # type: ignore[misc, assignment]

RELAY_CHANNEL_MAP = {
    "#pi": os.environ.get("SYMBIOSIS_SLACK_CHANNEL_PI", ""),
    "#linux": os.environ.get("SYMBIOSIS_SLACK_CHANNEL_LINUX", ""),
    "#windows": os.environ.get("SYMBIOSIS_SLACK_CHANNEL_WINDOWS", ""),
    "#all-devices": os.environ.get("SYMBIOSIS_SLACK_CHANNEL_ALL", "C0B70DB2X36"),
}


def _load_token(name: str = "SLACK_BOT_TOKEN") -> Optional[str]:
    tok = os.environ.get(name)
    if tok:
        return tok
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.strip().startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip("\"'")
    return None


def resolve_channel_id(
    channel_name: str | None,
    *,
    web_client: Any = None,
) -> str:
    """Return channel ID or raise ValueError."""
    if channel_name and channel_name.startswith("C") and len(channel_name) > 8:
        return channel_name
    if channel_name:
        mapped = RELAY_CHANNEL_MAP.get(channel_name) or RELAY_CHANNEL_MAP.get(channel_name.lower())
        if mapped:
            return mapped
    if web_client is None and WebClient is not None:
        token = _load_token()
        if token:
            web_client = WebClient(token=token)
    if web_client is not None:
        resp = web_client.conversations_list(types="public_channel,private_channel", limit=200)
        for ch in resp.get("channels", []):
            name = "#" + ch.get("name", "")
            cid = ch.get("id", "")
            if channel_name and name == channel_name:
                RELAY_CHANNEL_MAP[channel_name] = cid
                return cid
    raise ValueError(f"cannot resolve channel: {channel_name!r}")


def send_message(
    channel_id: str,
    text: str,
    *,
    thread_ts: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Post message; returns {ok, ts, error}."""
    if WebClient is None:
        return {"ok": False, "ts": None, "error": "slack_sdk not installed"}
    tok = token or _load_token()
    if not tok:
        return {"ok": False, "ts": None, "error": "no SLACK_BOT_TOKEN"}
    client = WebClient(token=tok)
    try:
        kwargs: dict[str, Any] = {"channel": channel_id, "text": text}
        if thread_ts:
            kwargs["thread_ts"] = thread_ts
        resp = client.chat_postMessage(**kwargs)
        return {"ok": bool(resp.get("ok")), "ts": resp.get("ts"), "error": None}
    except SlackApiError as e:
        return {"ok": False, "ts": None, "error": str(e)}
    except Exception as e:
        return {"ok": False, "ts": None, "error": str(e)}


def format_nl_autonomous_ack(
    task: dict,
    result: Any,
    device: str,
    *,
    trust_note: str = "control_command_override",
    inject_mode: str = "",
) -> str:
    hints = task.get("context_hints") or {}
    channel = task.get("slack_channel") or hints.get("source_channel") or "#all-devices"
    short = (
        hints.get("original_user_command")
        or task.get("original_message")
        or ""
    )[:200]
    explicit = hints.get("explicit_target_device") or "none"
    explicit_label = explicit.title() if explicit != "none" else "none"
    if not inject_mode:
        detail = getattr(result, "detail", "") or ""
        if "injected" in detail.lower() or "pts" in detail.lower():
            inject_mode = f"Injecting into live {device.upper()} TUI (pts-inject)."
        else:
            inject_mode = f"Launching headless AUTON ({detail[:120]})."
    return (
        f"Command received from {channel}: {short}.\n"
        f"Explicit target: {explicit_label}.\n"
        f"Trust: {trust_note} (main token path; is_real missing until ingest token applied "
        f"— see PROJECT_FINISH_LINE for the human xapp- step).\n"
        f"{inject_mode}\n"
        f"Monitor TUI or ~/.grok/auton-projects/. (AUTON 98822e73 fix)"
    )


def format_ack(result: Any, device: str, correlation: str) -> str:
    cmd = getattr(result, "command", "") or "control"
    detail = getattr(result, "detail", "") or ""
    ok = getattr(result, "ok", False)
    prefix = "Ack" if ok else "Control failed"
    return f"{prefix}: {cmd} on {device} (corr {correlation}). {detail}"


def format_denial(reason: str, device: str) -> str:
    return f"Not authorized on {device}: {reason}"


def ack_control_result(
    task: dict,
    result: Any,
    *,
    device: str,
    action: Any = None,
) -> dict[str, Any]:
    ch = task.get("slack_channel_id")
    if not ch:
        try:
            ch = resolve_channel_id(task.get("slack_channel"))
        except ValueError as e:
            return {"ok": False, "ts": None, "error": str(e)}
    thread = task.get("slack_thread_ts") or task.get("slack_ts")
    corr = task.get("correlation_id", "")
    hints = task.get("context_hints") or {}
    payload = getattr(action, "payload", "") if action else ""
    trust_note = getattr(action, "trust_note", "") if action else ""
    if hints.get("force_control") or str(payload).startswith("/autonomous"):
        text = format_nl_autonomous_ack(
            task,
            result,
            device,
            trust_note=trust_note or "control_command_override",
        )
    else:
        text = format_ack(result, device, corr)
    return send_message(ch, text, thread_ts=thread)


def nack_control_unauthorized(task: dict, reason: str, *, device: str) -> dict[str, Any]:
    ch = task.get("slack_channel_id")
    if not ch:
        try:
            ch = resolve_channel_id(task.get("slack_channel"))
        except ValueError as e:
            return {"ok": False, "ts": None, "error": str(e)}
    thread = task.get("slack_thread_ts") or task.get("slack_ts")
    return send_message(ch, format_denial(reason, device), thread_ts=thread)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--channel-id", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--thread-ts")
    args = ap.parse_args()
    out = send_message(args.channel_id, args.text, thread_ts=args.thread_ts)
    sys.exit(0 if out.get("ok") else 1)


if __name__ == "__main__":
    main()