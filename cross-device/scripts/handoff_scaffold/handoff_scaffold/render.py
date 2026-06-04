"""Safe template rendering for handoff README.md."""
from __future__ import annotations

import html
import re
from string import Template

from .paths import template_path

UNSAFE_USER_PATTERN = re.compile(r"[\$\{]")

REQUIRED_FORMAT_H2 = [
    "Context",
    "Task / Request",
    "Relevant Information / Artifacts",
    "What Has Already Been Done",
    "Success Criteria",
    "Preferences / Constraints",
    "Handoff Notes",
    "Relevant Memory (Mempalace)",
    "Return Path",
]

DEFAULT_MEMPALACE_PATHS = [
    "symbiosis/usage-pattern.md",
    "symbiosis/three-primes.md",
    "symbiosis/recent-decisions.md",
    "symbiosis/git-gotchas.md",
    "symbiosis/priorities.md (live: cross-device/coordination/OPEN_ITEMS.md)",
    "symbiosis/handoff-conventions.md",
    "symbiosis/device-presence/ (oregon.md + washington.md)",
    "cross-device/coordination/OPEN_ITEMS.md",
    "cross-device/coordination/status.md",
    "cross-device/coordination/*-instructions.md",
]


def reject_unsafe_user_field(name: str, value: str) -> None:
    if UNSAFE_USER_PATTERN.search(value):
        raise ValueError(
            f"{name}: use plain text; $ and {{ not allowed in user fields for template safety"
        )


def escape_narrative(text: str) -> str:
    return html.escape(text, quote=False)


def mempalace_bullets(extra_paths: list[str] | None) -> str:
    lines = []
    for p in DEFAULT_MEMPALACE_PATHS:
        lines.append(f"- `{p}`")
    for p in extra_paths or []:
        p = p.strip()
        if p:
            lines.append(f"- `{html.escape(p, quote=False)}`")
    return "\n".join(lines)


def artifacts_stub() -> str:
    return (
        "[Scaffold baseline — replace with concrete files, links, and prior handoffs.]\n"
        "- Files/folders:\n"
        "- Links:\n"
        "- Previous related handoffs:"
    )


def return_stub() -> str:
    return (
        "<!-- RETURN stub: bing/bang/boom in every summary paragraph per FORMAT. -->\n"
        "\n"
        "_Optional RETURN.md headings will be added when receiver completes work._"
    )


def signature_boilerplate(device: str = "Linux") -> str:
    from datetime import datetime

    now = datetime.now()
    return (
        f"<!-- Edited: {now.strftime('%Y-%m-%d %H:%M')} | Device: {device} | By: Grok -->"
    )


def load_template() -> str:
    return template_path().read_text(encoding="utf-8")


def parse_required_h2_from_format(format_text: str) -> list[str]:
    in_block = False
    found: list[str] = []
    for line in format_text.splitlines():
        if line.strip().startswith("```markdown"):
            in_block = True
            continue
        if in_block and line.strip() == "```":
            break
        if in_block and line.startswith("## "):
            found.append(line[3:].strip())
    return found if found else list(REQUIRED_FORMAT_H2)


def render_readme(
    *,
    from_device: str,
    to_device: str,
    slug: str,
    date_iso: str,
    time_hhmm: str,
    context: str,
    task: str,
    mempalace_extra: list[str] | None = None,
    include_return_stub: bool = False,
) -> str:
    reject_unsafe_user_field("context", context)
    reject_unsafe_user_field("task", task)
    ctx = escape_narrative(context.strip())
    tsk = escape_narrative(task.strip())
    yyyymmdd = date_iso.replace("-", "")
    fid = folder_id(yyyymmdd, time_hhmm, slug)
    mapping = {
        "from": from_device,
        "to": to_device,
        "slug": slug,
        "folder_id": fid,
        "date": date_iso,
        "time": time_hhmm,
        "context": ctx,
        "task": tsk,
        "mempalace_bullets": mempalace_bullets(mempalace_extra),
        "artifacts_stub": artifacts_stub(),
        "return_stub": return_stub() if include_return_stub else "",
    }
    tmpl = Template(load_template())
    out = tmpl.safe_substitute(mapping)
    out = out.replace(
        "[Brief background. Why is this being handed off?]",
        ctx or "[Brief background. Why is this being handed off?]",
    )
    out = out.replace(
        "[Clear description of what needs to be done]",
        tsk or "[Clear description of what needs to be done]",
    )
    return out


def folder_id(date_yyyymmdd: str, time_hhmm: str, slug: str) -> str:
    return f"{date_yyyymmdd}-{time_hhmm}-{slug}"