"""Path resolution for shared joint projects workspace."""
from __future__ import annotations

import os
import re
from pathlib import Path

from handoff_scaffold.paths import CANONICAL_FROM, default_repo_root

DEFAULT_PROJECTS_ENV = "SYMBIOSIS_PROJECTS_ROOT"
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{2,80}$")

__all__ = [
    "CANONICAL_FROM",
    "DEFAULT_PROJECTS_ENV",
    "SLUG_RE",
    "assert_under_projects_root",
    "default_projects_root",
    "default_repo_root",
    "project_dir",
    "validate_slug",
]


def default_projects_root() -> Path:
    env = os.environ.get(DEFAULT_PROJECTS_ENV)
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / "Synced" / "Projects").expanduser().resolve()


def project_dir(root: Path, slug: str) -> Path:
    validate_slug(slug)
    return (root / slug).resolve()


def validate_slug(slug: str) -> str:
    if not SLUG_RE.match(slug):
        raise ValueError(
            f"invalid slug {slug!r}; use 3-81 chars, alphanumeric and hyphens"
        )
    if ".." in slug or slug.startswith("."):
        raise ValueError(f"invalid slug {slug!r}")
    return slug


def assert_under_projects_root(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    projects_root = root.resolve()
    try:
        ok = resolved.is_relative_to(projects_root)
    except AttributeError:
        ok = str(resolved).startswith(str(projects_root) + os.sep) or resolved == projects_root
    if not ok:
        raise ValueError(f"path not under projects root: {resolved}")
    return resolved


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR1) -->