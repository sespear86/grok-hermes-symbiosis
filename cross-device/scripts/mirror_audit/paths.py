"""Path resolution for mirror audit."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from handoff_scaffold.paths import CANONICAL_FROM, default_repo_root

__all__ = [
    "CANONICAL_FROM",
    "default_repo_root",
    "default_rich_root",
    "default_grok_root",
    "default_bin_dir",
    "mirror_kits_path",
]

DEFAULT_RICH_ENV = "SYMBIOSIS_RICH_ROOT"
DEFAULT_GROK_ENV = "SYMBIOSIS_GROK_ROOT"


def default_rich_root() -> Path:
    env = os.environ.get(DEFAULT_RICH_ENV)
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        return Path(r"C:\Synced\grok-mempalace-integration").resolve()
    return Path("~/Synced/grok-mempalace-integration").expanduser().resolve()


def default_grok_root() -> Path:
    env = os.environ.get(DEFAULT_GROK_ENV)
    if env:
        return Path(env).expanduser().resolve()
    return Path("~/.grok").expanduser().resolve()


def default_bin_dir() -> Path:
    return Path("~/bin").expanduser().resolve()


def mirror_kits_path(repo_root: Path) -> Path:
    return (repo_root / "cross-device" / "MIRROR_KITS_AND_INFRASTRUCTURE.md").resolve()