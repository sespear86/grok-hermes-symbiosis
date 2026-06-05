"""Render handoff kanban as markdown, JSON, or ASCII board."""
from __future__ import annotations

import json
from typing import Any


def render_json(model: dict[str, Any]) -> str:
    return json.dumps(model, indent=2, sort_keys=True) + "\n"


def _truncate_desc(text: str, limit: int = 40) -> str:
    t = (text or "").strip()
    if len(t) <= limit:
        return t
    return t[: limit - 1] + "…"


def _fmt_presence(entry: dict[str, Any] | None) -> str:
    if not entry:
        return "_missing_"
    age = entry.get("age_seconds")
    age_s = f"{int(age)}s" if age is not None else "unknown"
    mode = entry.get("mode_hint") or "unknown"
    return f"age={age_s}, mode={mode}"


def _card_table_rows(cards: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| ID | Route | Description | Status | RETURN | Age |",
        "|----|-------|-------------|--------|--------|-----|",
    ]
    for c in cards:
        route = f"{c.get('from', '')}→{c.get('to', '')}"
        ret = "yes" if c.get("has_return") else "no"
        age = c.get("age_days")
        age_s = f"{age}d" if age is not None else "—"
        lines.append(
            f"| {c['id']} | {route} | {c.get('short_description', '')} | "
            f"{c.get('effective_status', '')} | {ret} | {age_s} |"
        )
    return lines


def render_md(model: dict[str, Any]) -> str:
    meta = model["meta"]
    coordination = model.get("coordination") or {}
    columns = model.get("columns") or {}
    truncation = model.get("truncation") or {}
    warnings = model.get("warnings") or []
    presence = model.get("presence")

    lines: list[str] = [
        "# Symbiosis Handoff Kanban",
        "",
        f"- **Device:** {meta['device']}",
        f"- **Timestamp (UTC):** {meta['timestamp_utc']}",
        f"- **Repo root:** `{meta['repo_root']}`",
    ]
    if meta.get("ball_holder"):
        lines.append(f"- **Ball holder:** {meta['ball_holder']}")
    if presence:
        lines.append(f"- **Local presence:** {_fmt_presence(presence.get('local'))}")
        lines.append(f"- **Brother presence:** {_fmt_presence(presence.get('brother'))}")
    lines.extend(
        [
            "",
            "## Top Priorities",
            "",
        ]
    )
    top3 = coordination.get("open_items_top3")
    if top3:
        lines.append(top3)
    else:
        lines.append("_section missing_")

    lines.extend(["", "## Board", ""])
    for title, key in (
        ("Awaiting", "awaiting"),
        ("In Progress", "in_progress"),
        ("Completed (recent)", "completed"),
        ("Archived", "archived"),
    ):
        cards = columns.get(key) or []
        lines.append(f"### {title} ({len(cards)})")
        lines.append("")
        if cards:
            lines.extend(_card_table_rows(cards))
        else:
            lines.append("_empty_")
        lines.append("")

    omitted = truncation.get("completed_omitted", 0)
    if omitted:
        lines.extend(
            [
                "## Older completed (not shown)",
                "",
                f"_{omitted} additional Completed handoffs in LOG; use --completed-limit "
                "or json for full list._",
                "",
            ]
        )

    lines.extend(["## Warnings", ""])
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- none")

    excerpt = coordination.get("status_excerpt") or []
    if excerpt:
        lines.extend(["", "## status.md excerpt", ""])
        for ln in excerpt[:8]:
            lines.append(f"> {ln.rstrip()}")

    lines.append("")
    return "\n".join(lines)


def render_board(model: dict[str, Any]) -> str:
    meta = model["meta"]
    columns = model.get("columns") or {}
    lines: list[str] = [
        f"Symbiosis Handoff Kanban | {meta['device']} | {meta['timestamp_utc']}",
        "",
    ]
    if meta.get("ball_holder"):
        lines.append(meta["ball_holder"])
        lines.append("")

    for title, key in (
        ("AWAITING", "awaiting"),
        ("IN PROGRESS", "in_progress"),
        ("COMPLETED", "completed"),
        ("ARCHIVED", "archived"),
    ):
        cards = columns.get(key) or []
        lines.append(f"--- {title} ({len(cards)}) ---")
        for c in cards:
            route = f"{c.get('from', '')}→{c.get('to', '')}"
            ret = "yes" if c.get("has_return") else "no"
            age = c.get("age_days")
            age_s = f"{age}d" if age is not None else "—"
            desc = _truncate_desc(c.get("short_description", ""))
            lines.append(
                f"{c['id']} | {route} | {desc} | RETURN:{ret} | {age_s}"
            )
        if not cards:
            lines.append("(empty)")
        lines.append("")

    omitted = (model.get("truncation") or {}).get("completed_omitted", 0)
    if omitted:
        lines.append(f"(+{omitted} older completed not shown)")
    lines.append("")
    return "\n".join(lines)


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch1) -->