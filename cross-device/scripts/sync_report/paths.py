"""Path resolution for sync report (delegates repo guard to handoff_scaffold)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from handoff_scaffold.paths import (
    CANONICAL_FROM,
    default_repo_root,
    handoff_format_path,
    handoff_log_path,
)

__all__ = [
    "CANONICAL_FROM",
    "default_repo_root",
    "default_rich_root",
    "default_mempalace_root",
    "handoff_format_path",
    "handoff_log_path",
    "coordination_dir",
    "open_items_path",
    "status_md_path",
    "relay_health_script",
    "presence_dir",
    "brother_presence_filename",
    "local_presence_filename",
]

_PRESENCE_LOCAL = {
    "Washington Linux": "washington.md",
    "Oregon Windows": "oregon.md",
}
_PRESENCE_BROTHER = {
    "Washington Linux": "oregon.md",
    "Oregon Windows": "washington.md",
}

DEFAULT_RICH_ENV = "SYMBIOSIS_RICH_ROOT"
DEFAULT_MEMPALACE_ENV = "SYMBIOSIS_MEMPALACE_ROOT"


def default_rich_root() -> Path:
    env = os.environ.get(DEFAULT_RICH_ENV)
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        return Path(r"C:\Synced\grok-mempalace-integration").resolve()
    return Path("~/Synced/grok-mempalace-integration").expanduser().resolve()


def default_mempalace_root() -> Path:
    env = os.environ.get(DEFAULT_MEMPALACE_ENV)
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        return Path(r"C:\Synced\Mempalace").resolve()
    return Path("~/Synced/Mempalace").expanduser().resolve()


def coordination_dir(repo_root: Path) -> Path:
    return (repo_root / "cross-device" / "coordination").resolve()


def open_items_path(repo_root: Path) -> Path:
    return coordination_dir(repo_root) / "OPEN_ITEMS.md"


def status_md_path(repo_root: Path) -> Path:
    return coordination_dir(repo_root) / "status.md"


def presence_dir(mempalace_root: Path) -> Path:
    return (mempalace_root / "symbiosis" / "device-presence").resolve()


def local_presence_filename(device: str) -> str:
    try:
        return _PRESENCE_LOCAL[device]
    except KeyError as exc:
        raise ValueError(f"unknown device: {device}") from exc


def brother_presence_filename(device: str) -> str:
    try:
        return _PRESENCE_BROTHER[device]
    except KeyError as exc:
        raise ValueError(f"unknown device: {device}") from exc


def relay_health_script(rich_root: Path) -> Path:
    return rich_root / "symbiosis-relay" / "tools" / "relay-health.sh"