"""Render mirror audit report."""
from __future__ import annotations

import json
from typing import Any

from .collectors import AuditModel


def render_json(model: AuditModel) -> str:
    payload: dict[str, Any] = {
        "meta": {
            "device": model.device,
            "repo_root": model.repo_root,
            "rich_root": model.rich_root,
            "grok_root": model.grok_root,
            "bin_dir": model.bin_dir,
            "mirror_kits_present": model.mirror_kits_present,
            "gap_count": model.gap_count,
        },
        "mirror_sections": model.mirror_sections,
        "health": model.health,
        "components": [
            {
                "id": c.spec.component_id,
                "title": c.spec.title,
                "mirror_section": c.spec.mirror_section,
                "ok": c.ok,
                "gaps": c.gaps,
                "provision_hint": c.spec.provision_hint,
                "checks": [
                    {"kind": ch.kind, "rel": ch.rel, "exists": ch.exists}
                    for ch in c.checks
                ],
            }
            for c in model.components
        ],
    }
    return json.dumps(payload, indent=2) + "\n"


def render_markdown(model: AuditModel) -> str:
    lines = [
        f"# Symbiosis mirror audit — {model.device}",
        "",
        f"- **Repo:** `{model.repo_root}`",
        f"- **Rich:** `{model.rich_root}`",
        f"- **Grok:** `{model.grok_root}`",
        f"- **Bin:** `{model.bin_dir}`",
        f"- **MIRROR_KITS:** {'present' if model.mirror_kits_present else 'MISSING'}",
        f"- **Gaps:** {model.gap_count}",
        "",
        "## Health probes",
    ]
    for k, v in model.health.items():
        lines.append(f"- `{k}`: {v!r}")
    lines.extend(["", "## Components"])
    for comp in model.components:
        status = "OK" if comp.ok else "GAP"
        lines.append(f"### [{status}] {comp.spec.component_id} ({comp.spec.mirror_section})")
        lines.append(f"_{comp.spec.title}_")
        if comp.gaps:
            for g in comp.gaps:
                lines.append(f"- missing: `{g}`")
            if comp.spec.provision_hint:
                lines.append(f"- **Self-provision:** {comp.spec.provision_hint}")
        else:
            lines.append("- all checked paths present")
        lines.append("")
    if model.mirror_sections:
        lines.append("## MIRROR_KITS sections (parsed)")
        for sec in model.mirror_sections[:25]:
            lines.append(f"- {sec}")
        if len(model.mirror_sections) > 25:
            lines.append(f"- ... +{len(model.mirror_sections) - 25} more")
    return "\n".join(lines) + "\n"