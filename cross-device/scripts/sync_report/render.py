"""Render sync report as markdown or JSON."""
from __future__ import annotations

import json
from typing import Any


def render_json(model: dict[str, Any]) -> str:
    return json.dumps(model, indent=2, sort_keys=True) + "\n"


def _fmt_presence(entry: dict[str, Any] | None) -> str:
    if not entry:
        return "_missing_"
    age = entry.get("age_seconds")
    age_s = f"{int(age)}s" if age is not None else "unknown"
    mode = entry.get("mode_hint") or "unknown"
    paired = "yes" if entry.get("paired_hint") else "no"
    return f"age={age_s}, mode={mode}, paired_hint={paired}"


def render_markdown(model: dict[str, Any]) -> str:
    meta = model["meta"]
    git = model["git"]
    syncthing = model["syncthing"]
    coordination = model["coordination"]
    presence = model["presence"]
    conflicts = model["conflicts"]
    warnings = model.get("warnings") or []
    relay = model.get("relay")

    lines: list[str] = [
        "# Symbiosis Sync Report",
        "",
        f"- **Device:** {meta['device']}",
        f"- **Timestamp (UTC):** {meta['timestamp_utc']}",
        f"- **Repo root:** `{meta['repo_root']}`",
        f"- **Rich root:** `{meta['rich_root']}`",
        f"- **Mempalace root:** `{meta['mempalace_root']}`",
        "",
        "## Git",
        "",
    ]
    if git.get("available"):
        lines.append(f"- Branch: `{git.get('branch')}`")
        lines.append(f"- Ahead/behind: {git.get('ahead', 0)}/{git.get('behind', 0)}")
        lines.append(f"- Dirty file count: {git.get('dirty_count', 0)}")
    else:
        lines.append("_git unavailable_")
    lines.extend(["", "## Syncthing", ""])
    if syncthing.get("available"):
        for folder in syncthing.get("folders") or []:
            lines.append(f"- `{folder['id']}`: **{folder['state']}** (rc={folder['rc']})")
        if syncthing.get("system"):
            lines.append("")
            lines.append("```")
            lines.append(str(syncthing["system"])[:800])
            lines.append("```")
    else:
        reason = syncthing.get("reason") or "unavailable"
        lines.append(f"_syncthing not reported ({reason})_")

    lines.extend(["", "## Coordination", "", "### Recent handoffs", ""])
    rows = coordination.get("handoff_log", {}).get("rows") or []
    if rows:
        lines.append("| Date | ID | From | To | Status |")
        lines.append("|------|-----|------|-----|--------|")
        for r in rows:
            lines.append(
                f"| {r['date']} | {r['id']} | {r['from']} | {r['to']} | {r['status']} |"
            )
    else:
        lines.append("_no handoff rows parsed_")

    lines.extend(["", "### OPEN_ITEMS Top 3", ""])
    top3 = coordination.get("open_items_top3")
    if top3:
        lines.append(top3)
    else:
        lines.append("_section missing_")

    lines.extend(["", "### status.md excerpt", ""])
    for ln in coordination.get("status_excerpt") or []:
        lines.append(f"> {ln.rstrip()}")

    lines.extend(["", "## Presence", ""])
    lines.append(f"- Local: {_fmt_presence(presence.get('local'))}")
    lines.append(f"- Brother: {_fmt_presence(presence.get('brother'))}")

    lines.extend(["", "## Conflicts", ""])
    lines.append(f"- `.sync-conflict-*` count: {conflicts.get('count', 0)}")
    if conflicts.get("samples"):
        for s in conflicts["samples"]:
            lines.append(f"  - `{s}`")

    lines.extend(["", "## Warnings", ""])
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- none")

    if relay is not None:
        lines.extend(["", "## Relay (optional)", ""])
        if relay.get("lines"):
            lines.append("```")
            lines.extend(relay["lines"])
            lines.append("```")
        else:
            lines.append("_relay section empty or unavailable_")

    lines.append("")
    return "\n".join(lines)