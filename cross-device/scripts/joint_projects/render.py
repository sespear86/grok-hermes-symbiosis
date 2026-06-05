"""Render shared projects list as markdown or JSON."""
from __future__ import annotations

import json
from typing import Any


def render_json(model: dict[str, Any]) -> str:
    return json.dumps(model, indent=2, sort_keys=True) + "\n"


def _yes_no(flag: bool) -> str:
    return "yes" if flag else "no"


def _project_table_rows(projects: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Slug | README | .stignore |",
        "|------|--------|-----------|",
    ]
    for p in projects:
        lines.append(
            f"| {p['slug']} | {_yes_no(p.get('has_readme', False))} | "
            f"{_yes_no(p.get('has_stignore', False))} |"
        )
    return lines


def render_md(model: dict[str, Any]) -> str:
    meta = model["meta"]
    coordination = model.get("coordination") or {}
    projects = model.get("projects") or []
    warnings = model.get("warnings") or []

    lines: list[str] = [
        "# Symbiosis Shared Projects",
        "",
        f"- **Device:** {meta['device']}",
        f"- **Timestamp (UTC):** {meta['timestamp_utc']}",
        f"- **Projects root:** `{meta['projects_root']}`",
    ]
    if meta.get("ball_holder"):
        lines.append(f"- **Ball holder:** {meta['ball_holder']}")
    if meta.get("repo_root"):
        lines.append(f"- **Repo root:** `{meta['repo_root']}`")

    lines.extend(["", "## Projects", ""])
    if projects:
        lines.extend(_project_table_rows(projects))
    else:
        lines.append("_no project directories_")
    lines.append("")

    lines.extend(["", "## Top Priorities", ""])
    top3 = coordination.get("open_items_top3")
    if top3:
        lines.append(top3)
    else:
        lines.append("_section missing_")
    lines.append("")

    excerpt = coordination.get("status_excerpt") or []
    if excerpt:
        lines.extend(["## status.md excerpt", ""])
        for ln in excerpt[:8]:
            lines.append(f"> {ln.rstrip()}")
        lines.append("")

    lines.extend(["## Warnings", ""])
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR1) -->