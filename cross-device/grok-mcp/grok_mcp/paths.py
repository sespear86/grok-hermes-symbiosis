"""Path confinement for cwd and context_paths (AUTON b045169b)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from grok_mcp.config import Settings


class PathValidationError(ValueError):
    """Raised when cwd or context path escapes allowed roots."""


def _allowed_roots(settings: Settings) -> list[Path]:
    roots: list[Path] = []
    if settings.repo_root:
        roots.append(Path(settings.repo_root).resolve())
    extra = os.environ.get("GROK_MCP_ALLOWED_ROOTS", "").strip()
    if extra:
        for part in extra.split(","):
            part = part.strip()
            if part:
                roots.append(Path(part).expanduser().resolve())
    if not roots:
        roots.append(Path.cwd().resolve())
    return roots


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_confined(path_str: str | None, settings: Settings, *, default_cwd: bool = False) -> Path:
    if path_str is None or (isinstance(path_str, str) and not path_str.strip()):
        if default_cwd:
            candidate = Path.cwd().resolve()
        else:
            raise PathValidationError("path is required")
    else:
        candidate = Path(path_str).expanduser().resolve()

    if not candidate.exists():
        raise PathValidationError(f"path does not exist: {candidate}")

    for root in _allowed_roots(settings):
        if _is_under(candidate, root):
            return candidate

    raise PathValidationError(
        f"path {candidate} is outside allowed roots (SYMBIOSIS_REPO_ROOT / GROK_MCP_ALLOWED_ROOTS)"
    )


def validate_context_paths(paths: list[str] | None, settings: Settings) -> list[Path]:
    if not paths:
        return []
    return [resolve_confined(str(p), settings) for p in paths if p and str(p).strip()]


def git_snippet(cwd: Path) -> str:
    try:
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        lines: list[str] = []
        if branch.stdout.strip():
            lines.append(f"branch: {branch.stdout.strip()}")
        if status.stdout.strip():
            lines.extend(status.stdout.strip().splitlines()[:8])
        return "\n".join(lines) if lines else "(no git context)"
    except (OSError, subprocess.TimeoutExpired):
        return "(git unavailable)"