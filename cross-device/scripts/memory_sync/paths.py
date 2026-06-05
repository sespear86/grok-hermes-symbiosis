"""Path resolution and constants for memory_sync (modeled on sync_report/paths.py + joint_projects).

See DESIGN.md for canonicals.
"""

from __future__ import annotations
from pathlib import Path
import os

# Default project for symbiosis (overridable via SYMBIOSIS_MEMORY_PROJECT)
DEFAULT_PROJECT_SLUG = "grok-hermes-symbiosis"

CANONICAL_DEVICES = frozenset({"Washington Linux", "Oregon Windows"})

def default_mempalace_root() -> Path:
    # Dual-source project palace preferred (linux/windows/shared)
    env = os.environ.get("SYMBIOSIS_MEMPALACE_ROOT")
    if env:
        return Path(env)
    # Fallback to rich integration or standard
    rich = Path.home() / "Synced" / "grok-mempalace-integration" / "mempalace"
    if rich.exists():
        return rich
    return Path.home() / "grokforge-palaces" / "sean-grok-collaboration"

def default_repo_root() -> Path:
    env = os.environ.get("SYMBIOSIS_REPO_ROOT")
    if env:
        return Path(env)
    # Assume running from within or sibling
    return Path(__file__).resolve().parents[3]  # cross-device/scripts -> repo root approx

# ... (full in DESIGN + implement B1)
