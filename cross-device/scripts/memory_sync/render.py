"""Render helpers (inject markdown, status). Stub for B1; full in B3."""
from __future__ import annotations
from typing import Any, Dict

def render_inject(bundle: Dict[str, Any]) -> str:
    return f"# Memory Sync Inject (stub)\n\n```json\n{bundle}\n```"

def render_status(data: Dict[str, Any]) -> str:
    return json.dumps(data)  # type: ignore
