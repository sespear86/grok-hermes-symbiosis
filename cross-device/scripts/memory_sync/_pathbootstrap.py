"""Insert cross-device/scripts (+ handoff_scaffold parent) on sys.path for CLI -m runs."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_scripts_path() -> None:
    scripts = Path(__file__).resolve().parent.parent
    for entry in (scripts, scripts / "handoff_scaffold"):
        s = str(entry)
        if s not in sys.path:
            sys.path.insert(0, s)