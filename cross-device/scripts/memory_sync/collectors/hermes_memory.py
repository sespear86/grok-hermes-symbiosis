"""Hermes memory collector (MEMORY.md + USER.md excerpts, session title from state.db).

Per DESIGN: truncated excerpts, prompt-only semantics for inject.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional
import sqlite3

HERMES_HOME = Path.home() / ".hermes"
MEMORIES = HERMES_HOME / "memories"

def collect_hermes_excerpts(max_chars: int = 2200) -> Dict[str, Optional[str]]:
    mem = (MEMORIES / "MEMORY.md").read_text(errors="ignore")[:max_chars] if (MEMORIES / "MEMORY.md").exists() else None
    user = (MEMORIES / "USER.md").read_text(errors="ignore")[:1375] if (MEMORIES / "USER.md").exists() else None
    return {"memory": mem, "user": user}

def collect_session_title() -> Optional[str]:
    db = HERMES_HOME / "state.db"
    if not db.exists():
        return None
    try:
        conn = sqlite3.connect(str(db))
        row = conn.execute(
            "SELECT title FROM sessions ORDER BY COALESCE(ended_at, started_at) DESC LIMIT 1"
        ).fetchone()
        conn.close()
        return row[0] if row and row[0] else None
    except Exception:
        return None

# decisions extraction stub (last N long lines from MEMORY)
