# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->
"""Thin wrapper around kanban collectors for the live dashboard."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanban.collectors import collect_board
from kanban.render import render_board, render_json, render_md


def collect_board_for_device(
    *,
    device: str,
    repo_root: Path,
    mempalace_root: Path,
    completed_limit: int = 5,
    include_presence: bool = True,
) -> dict[str, Any]:
    return collect_board(
        device=device,
        repo_root=repo_root,
        mempalace_root=mempalace_root,
        completed_limit=completed_limit,
        include_presence=include_presence,
    )


def render_format(model: dict[str, Any], fmt: str) -> tuple[str, str]:
    """Return (body, content_type). fmt in json|md|board."""
    if fmt == "json":
        return render_json(model), "application/json; charset=utf-8"
    if fmt == "board":
        return render_board(model), "text/plain; charset=utf-8"
    if fmt in ("md", "markdown"):
        return render_md(model), "text/plain; charset=utf-8"
    raise ValueError(f"unsupported format: {fmt}")