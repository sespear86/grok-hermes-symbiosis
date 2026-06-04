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


def format_ack(result: Any, device: str, correlation: str) -> str:
    cmd = getattr(result, "command", "") or "control"
    detail = getattr(result, "detail", "") or ""
    ok = getattr(result, "ok", False)
    prefix = "Ack" if ok else "Control failed"
    return f"{prefix}: {cmd} on {device} (corr {correlation}). {detail}"


def format_denial(reason: str, device: str) -> str:
    return f"Not authorized on {device}: {reason}"


def ack_control_result(task: dict, result: Any, *, device: str) -> dict[str, Any]:
    ch = task.get("slack_channel_id")
    if not ch:
        try:
            ch = resolve_channel_id(task.get("slack_channel"))
        except ValueError as e:
            return {"ok": False, "ts": None, "error": str(e)}
    thread = task.get("slack_thread_ts") or task.get("slack_ts")
    corr = task.get("correlation_id", "")
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