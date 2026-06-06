"""Path resolution and constants for memory_sync (modeled on sync_report/paths.py + joint_projects).

See DESIGN.md AUTON 7eb7d1b7 for canonicals.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from memory_sync._pathbootstrap import ensure_scripts_path

ensure_scripts_path()

from handoff_scaffold.paths import CANONICAL_FROM, default_repo_root as _handoff_repo_root
from joint_projects.paths import validate_slug

DEFAULT_PROJECT_SLUG = "grok-hermes-symbiosis"

DEVICE_TO_SOURCE_TAG = {
    "Washington Linux": "washington-linux",
    "Oregon Windows": "oregon-windows",
}

CANONICAL_DEVICES = CANONICAL_FROM

STALE_HEARTBEAT_SECONDS = 3600

__all__ = [
    "CANONICAL_DEVICES",
    "DEFAULT_PROJECT_SLUG",
    "DEVICE_TO_SOURCE_TAG",
    "STALE_HEARTBEAT_SECONDS",
    "default_mempalace_root",
    "default_palace_path",
    "default_repo_root",
    "device_to_source_tag",
    "grok_sessions_root",
    "palace_room_for_project",
    "sidecar_path_for_agent",
    "validate_project_slug",
]


def default_repo_root() -> Path:
    env = os.environ.get("SYMBIOSIS_REPO_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return _handoff_repo_root()


def default_mempalace_root() -> Path:
    env = os.environ.get("SYMBIOSIS_MEMPALACE_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        return Path(r"C:\Synced\Mempalace").resolve()
    return Path("~/Synced/Mempalace").expanduser().resolve()


def default_palace_path() -> Path:
    env = os.environ.get("MEMPALACE_PALACE")
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        return Path(
            r"C:\Synced\grok-mempalace-integration\mempalace\windows"
        ).resolve()
    linux = Path("~/Synced/grok-mempalace-integration/mempalace/linux").expanduser()
    if linux.is_dir():
        return linux.resolve()
    return Path("~/Synced/grok-mempalace-integration/mempalace").expanduser().resolve()


def device_to_source_tag(device: str) -> str:
    try:
        return DEVICE_TO_SOURCE_TAG[device]
    except KeyError as exc:
        raise ValueError(f"unknown device: {device!r}") from exc


def palace_room_for_project(project_slug: str) -> str:
    validate_project_slug(project_slug)
    return f"{project_slug}-snapshots"


def validate_project_slug(slug: str) -> str:
    if slug == DEFAULT_PROJECT_SLUG:
        return slug
    return validate_slug(slug)


def grok_sessions_root() -> Path:
    return Path.home() / ".grok" / "sessions"


def repo_root_from_package() -> Path:
    return Path(__file__).resolve().parents[3]


def helper_script_path() -> Path:
    return repo_root_from_package() / "Mempalace" / "scripts" / "mempalace_symbiosis_bundle_io.py"


def sidecar_path_for_agent(agent: str) -> Path:
    if agent == "grok":
        return Path.home() / ".grok" / "symbiosis-memory-sync-state.json"
    if agent == "hermes":
        return Path.home() / ".hermes" / "symbiosis-memory-sync-state.json"
    raise ValueError(f"unknown agent: {agent!r}")


def brother_device(local_device: str) -> str:
    if local_device == "Washington Linux":
        return "Oregon Windows"
    if local_device == "Oregon Windows":
        return "Washington Linux"
    raise ValueError(f"unknown device: {local_device!r}")


# <!-- Edited: 2026-06-06 | Device: Washington Linux | By: Grok (AUTON 9be206cf) --> Path bootstrap for -m CLI sibling imports. Sig per prime.