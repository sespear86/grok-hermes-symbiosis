"""Coordination collectors (reuse sync_report for OPEN_ITEMS, git, device presence).

Per DESIGN + sync_report pattern.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import subprocess
from pathlib import Path

try:
    from sync_report.collectors import extract_open_items_top3  # reuse
except Exception:
    def extract_open_items_top3(repo_root: Path) -> str:  # type: ignore
        return "OPEN_ITEMS top3 unavailable (import failed)"

def get_git_meta(repo: Path) -> Dict[str, Any]:
    try:
        sha = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], text=True).strip()
        branch = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        return {"sha": sha, "branch": branch}
    except Exception:
        return {"sha": "unknown", "branch": "unknown"}

def get_presence_age(device: str) -> Optional[str]:
    # Simple; full in status or device-presence heartbeats
    return None  # extended in status subcommand

# ... (full per DESIGN B2)
