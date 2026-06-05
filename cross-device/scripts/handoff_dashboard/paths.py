# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->
"""Path resolution for handoff dashboard (re-exports kanban paths + static dir)."""
from __future__ import annotations

import os
from pathlib import Path

from handoff_scaffold.paths import (
    CANONICAL_FROM,
    default_repo_root,
    handoff_format_path,
    handoff_log_path,
)
from kanban.paths import (
    archived_dir,
    brother_presence_filename,
    coordination_dir,
    default_mempalace_root,
    handoffs_dir,
    local_presence_filename,
    open_items_path,
    presence_dir,
    status_md_path,
)

__all__ = [
    "CANONICAL_FROM",
    "archived_dir",
    "brother_presence_filename",
    "coordination_dir",
    "dashboard_lockfile",
    "dashboard_package_dir",
    "default_mempalace_root",
    "default_repo_root",
    "get_repo_root",
    "handoff_format_path",
    "handoff_log_path",
    "handoffs_dir",
    "local_presence_filename",
    "open_items_path",
    "presence_dir",
    "static_dir",
    "status_md_path",
]

DEFAULT_PORT_ENV = "SYMBIOSIS_HANDOFF_DASHBOARD_PORT"
DEFAULT_LOCK = "/tmp/symbiosis-handoff-dashboard.lock"


def dashboard_package_dir() -> Path:
    return Path(__file__).resolve().parent


def static_dir() -> Path:
    return dashboard_package_dir() / "static"


def dashboard_lockfile() -> Path:
    return Path(os.environ.get("SYMBIOSIS_HANDOFF_DASHBOARD_LOCK", DEFAULT_LOCK))


def get_repo_root(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    return default_repo_root()