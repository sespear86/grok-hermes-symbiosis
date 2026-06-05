"""Path resolution for handoff kanban (delegates repo guard to handoff_scaffold)."""
from __future__ import annotations

from pathlib import Path

from handoff_scaffold.paths import (
    CANONICAL_FROM,
    default_repo_root,
    handoff_format_path,
    handoff_log_path,
)
from sync_report.paths import (
    brother_presence_filename,
    coordination_dir,
    default_mempalace_root,
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
    "default_mempalace_root",
    "default_repo_root",
    "handoff_format_path",
    "handoff_log_path",
    "handoffs_dir",
    "local_presence_filename",
    "open_items_path",
    "presence_dir",
    "status_md_path",
]


def handoffs_dir(repo_root: Path) -> Path:
    return (repo_root / "cross-device" / "handoffs").resolve()


def archived_dir(repo_root: Path) -> Path:
    return handoffs_dir(repo_root) / "archived"


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch1) -->