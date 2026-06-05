"""Read-only collectors for symbiosis shared projects list (AUTON 61cdeb81)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanban.collectors import extract_ball_holder
from sync_report.collectors import extract_open_items_top3, extract_status_excerpt
from sync_report.paths import handoff_format_path, open_items_path, status_md_path

MANIFEST_NAME = ".symbiosis-project.json"


def _read_manifest(project_path: Path) -> dict[str, Any] | None:
    manifest_path = project_path / MANIFEST_NAME
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _list_project_entries(projects_root: Path) -> list[dict[str, Any]]:
    if not projects_root.is_dir():
        return []
    entries: list[dict[str, Any]] = []
    for child in sorted(projects_root.iterdir(), key=lambda p: p.name.casefold()):
        if not child.is_dir():
            continue
        name = child.name
        if name.startswith("."):
            continue
        entries.append(
            {
                "slug": name,
                "has_readme": (child / "README.md").is_file(),
                "has_stignore": (child / ".stignore").is_file(),
                "manifest": _read_manifest(child),
            }
        )
    return entries


def _coordination_block(
    repo_root: Path,
) -> tuple[dict[str, Any], list[str], str | None]:
    coordination: dict[str, Any] = {
        "open_items_top3": None,
        "status_excerpt": [],
    }
    warnings: list[str] = []
    ball_holder: str | None = None
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        warnings.append(f"coordination skipped: HANDOFF_FORMAT.md missing at {fmt}")
        return coordination, warnings, ball_holder

    oi_path = open_items_path(repo_root)
    if oi_path.is_file():
        coordination["open_items_top3"] = extract_open_items_top3(
            oi_path.read_text(encoding="utf-8", errors="replace")
        )
    else:
        warnings.append(f"OPEN_ITEMS.md missing: {oi_path}")

    st_path = status_md_path(repo_root)
    if st_path.is_file():
        status_text = st_path.read_text(encoding="utf-8", errors="replace")
        coordination["status_excerpt"] = extract_status_excerpt(status_text)
        ball_holder = extract_ball_holder(status_text)
    else:
        warnings.append(f"status.md missing: {st_path}")

    return coordination, warnings, ball_holder


def collect_list(
    *,
    device: str,
    projects_root: Path,
    repo_root: Path | None,
    include_coord: bool = True,
) -> dict[str, Any]:
    projects_root = projects_root.resolve()
    warnings: list[str] = []
    coordination: dict[str, Any] = {
        "open_items_top3": None,
        "status_excerpt": [],
    }
    ball_holder: str | None = None

    if not projects_root.exists():
        projects_root.mkdir(parents=True, exist_ok=True)
        warnings.append(f"projects root created: {projects_root}")
    elif not projects_root.is_dir():
        raise ValueError(f"projects root is not a directory: {projects_root}")

    projects = _list_project_entries(projects_root)

    if include_coord and repo_root is not None:
        repo_root = repo_root.resolve()
        coordination, coord_warnings, ball_holder = _coordination_block(repo_root)
        warnings.extend(coord_warnings)
    elif include_coord and repo_root is None:
        warnings.append("coordination skipped: no repo root resolved")

    return {
        "schema_version": 1,
        "meta": {
            "device": device,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "projects_root": str(projects_root),
            "repo_root": str(repo_root) if repo_root else None,
            "ball_holder": ball_holder,
            "format": "md",
        },
        "projects": projects,
        "coordination": coordination,
        "warnings": warnings,
    }


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR1) -->