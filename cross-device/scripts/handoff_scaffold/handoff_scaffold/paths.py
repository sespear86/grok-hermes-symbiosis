"""Repository and handoff path resolution with confinement."""
from __future__ import annotations

import os
from pathlib import Path

CANONICAL_FROM = frozenset({"Washington Linux", "Oregon Windows"})
CANONICAL_TO = CANONICAL_FROM

DEFAULT_REPO_ENV = "SYMBIOSIS_REPO_ROOT"


def default_repo_root() -> Path:
    env = os.environ.get(DEFAULT_REPO_ENV)
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[4]


def handoffs_root(repo_root: Path) -> Path:
    return (repo_root / "cross-device" / "handoffs").resolve()


def handoff_format_path(repo_root: Path) -> Path:
    return handoffs_root(repo_root) / "HANDOFF_FORMAT.md"


def handoff_log_path(repo_root: Path) -> Path:
    return handoffs_root(repo_root) / "HANDOFF_LOG.md"


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "templates" / "README.md.tmpl"


def package_dir(repo_root: Path, folder_id: str) -> Path:
    return handoffs_root(repo_root) / folder_id


def assert_under_handoffs(path: Path, repo_root: Path) -> Path:
    resolved = path.resolve()
    root = handoffs_root(repo_root)
    try:
        ok = resolved.is_relative_to(root)
    except AttributeError:
        ok = str(resolved).startswith(str(root) + os.sep) or resolved == root
    if not ok:
        raise ValueError(f"path not under handoffs root: {resolved}")
    return resolved