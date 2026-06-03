#!/usr/bin/env python3
"""
task_schema.py — Minimal stdlib task validation for Symbiosis Relay (no pydantic).

Per DESIGN (AUTON 19557e65, PR1): validate required keys, correlation sanity, size guard.
Raises TaskValidationError on bad input. Used before claim / prompt.
"""

from __future__ import annotations
import re
from typing import Any


class TaskValidationError(ValueError):
    """Raised for invalid task payloads (prevents bad data reaching hermes or status)."""
    pass


REQUIRED_KEYS = ("type", "correlation_id", "original_message")
MAX_PAYLOAD_BYTES = 1_000_000  # 1MB guard against huge shared-FS drops
CORR_RE = re.compile(r"^[A-Za-z0-9._-]{3,128}$")


def validate_task(task: dict[str, Any]) -> dict[str, Any]:
    """Validate + return the task (or raise)."""
    if not isinstance(task, dict):
        raise TaskValidationError("task must be a dict")

    # Size guard (cheap before full parse in hot path)
    # Caller should have already read; this is belt-and-suspenders
    for k in REQUIRED_KEYS:
        if k not in task or task[k] is None or str(task[k]).strip() == "":
            raise TaskValidationError(f"missing or empty required key: {k}")

    corr = str(task["correlation_id"]).strip()
    if not CORR_RE.match(corr):
        raise TaskValidationError(f"correlation_id invalid (3-128 alnum ._- ): {corr!r}")

    # original_message can be long but we cap the whole payload at read time
    # here just ensure str-able
    _ = str(task["original_message"])

    # Optional enrichment fields are allowed (context_hints, priority, slack_* etc)
    return task


def validate_task_from_json_text(text: str) -> dict[str, Any]:
    """Parse + validate (used by activator loop)."""
    import json
    if len(text.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise TaskValidationError(f"task payload too large (> {MAX_PAYLOAD_BYTES} bytes)")
    try:
        task = json.loads(text)
    except json.JSONDecodeError as e:
        raise TaskValidationError(f"invalid JSON: {e}") from e
    return validate_task(task)
