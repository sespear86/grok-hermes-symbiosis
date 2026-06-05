"""Stderr-only structured logging — stdout is MCP protocol only."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any


def log_event(event: str, **fields: Any) -> None:
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "component": "grok_mcp",
        "event": event,
        **fields,
    }
    sys.stderr.write(json.dumps(payload, default=str) + "\n")
    sys.stderr.flush()