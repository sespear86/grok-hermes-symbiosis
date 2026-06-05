"""Grok session collector (todos from updates.jsonl todo_write tool calls).

Per DESIGN B2 + R2 fixes: reverse scan for tool_call/tool_call_update with title=="todo_write",
parse rawInput.todos, last snapshot wins. Best-effort + warnings.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

def find_latest_session(cwd: Path) -> Path | None:
    encoded = str(cwd).replace("/", "%2F")
    base = Path.home() / ".grok" / "sessions" / encoded
    if not base.exists():
        return None
    sessions = sorted([d for d in base.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True)
    return sessions[0] if sessions else None

def collect_todos(session_dir: Path) -> tuple[List[Dict[str, Any]], List[str]]:
    """Return (todos, warnings). Last valid todo_write snapshot wins."""
    todos: List[Dict[str, Any]] = []
    warnings: List[str] = []
    updates = session_dir / "updates.jsonl"
    if not updates.exists():
        warnings.append("todos: no updates.jsonl in session")
        return todos, warnings
    lines = updates.read_text(errors="ignore").splitlines()[-5000:]
    last_raw = None
    for line in reversed(lines):
        try:
            obj = json.loads(line)
            t = obj.get("type")
            if t in ("tool_call", "tool_call_update"):
                title = obj.get("title") or (obj.get("rawInput") or {}).get("title")
                if title == "todo_write" or "todo_write" in str(title or "").lower():
                    raw = obj.get("rawInput") or {}
                    if isinstance(raw, dict) and "todos" in raw:
                        last_raw = raw
                        break
        except Exception:
            pass
    if last_raw and isinstance(last_raw.get("todos"), list):
        for t in last_raw["todos"]:
            if isinstance(t, dict) and t.get("content"):
                todos.append({
                    "id": str(t.get("id", "")),
                    "content": str(t.get("content", ""))[:500],
                    "status": str(t.get("status", "pending"))
                })
    else:
        warnings.append("todos: no todo_write events with todos array in recent updates")
    return todos, warnings

# ... (session title, decisions heuristics per DESIGN)
