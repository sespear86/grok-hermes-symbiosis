"""Render and template safety."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from handoff_scaffold.render import (
    REQUIRED_FORMAT_H2,
    reject_unsafe_user_field,
    render_readme,
)
from handoff_scaffold.validate import validate_format_drift


def test_reject_injection():
    with pytest.raises(ValueError, match="template safety"):
        reject_unsafe_user_field("task", "hello {evil}")
    with pytest.raises(ValueError):
        reject_unsafe_user_field("context", "price $5")


def test_render_includes_artifacts_and_mempalace():
    text = render_readme(
        from_device="Washington Linux",
        to_device="Oregon Windows",
        slug="Test-Render",
        date_iso="2026-06-04",
        time_hhmm="1200",
        context="Context bing.",
        task="Task bang.",
        mempalace_extra=["projects/symbiosis-handoff-scaffold"],
        include_return_stub=True,
    )
    assert "## Relevant Information / Artifacts" in text
    assert "projects/symbiosis-handoff-scaffold" in text
    assert "symbiosis/usage-pattern.md" in text
    assert "bing/bang/boom" in text
    assert "**ID:** 20260604-1200-Test-Render" in text


def test_format_drift_against_live_repo(repo_root):
    drift = validate_format_drift(repo_root, list(REQUIRED_FORMAT_H2))
    assert drift.ok, drift.errors


FIXTURES = Path(__file__).resolve().parent / "fixtures"
_AGE_TAIL_RE = re.compile(r"\|\s*\d+d\s*\|?\s*$")


def _normalize_kanban_md(md: str) -> str:
    out: list[str] = []
    for ln in md.splitlines():
        if ln.startswith("- **Timestamp (UTC):**"):
            out.append("- **Timestamp (UTC):** <TIMESTAMP>")
            continue
        if ln.startswith("- **Repo root:**") or ln.startswith("- **Mempalace root:**"):
            continue
        if ln.startswith("- **Local presence:**") or ln.startswith("- **Brother presence:**"):
            continue
        if ln.startswith("| ") and "|" in ln[2:]:
            ln = _AGE_TAIL_RE.sub("| <AGE> |", ln)
        out.append(ln)
    return "\n".join(out)


def _normalize_kanban_board(text: str) -> str:
    out: list[str] = []
    for ln in text.splitlines():
        if ln.startswith("Symbiosis Handoff Kanban |"):
            parts = ln.split("|", 2)
            if len(parts) >= 3:
                out.append(f"{parts[0].strip()} | {parts[1].strip()} | <TIMESTAMP>")
            else:
                out.append(ln)
            continue
        if " | RETURN:" in ln:
            ln = _AGE_TAIL_RE.sub("| <AGE>", ln)
        out.append(ln)
    return "\n".join(out)


def test_golden_kanban_markdown_key_sections(kanban_mini_tree):
    from kanban.collectors import collect_board
    from kanban.render import render_md

    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        completed_limit=5,
        include_presence=False,
    )
    actual = _normalize_kanban_md(render_md(model))
    golden = _normalize_kanban_md(
        (FIXTURES / "expected_kanban.md").read_text(encoding="utf-8")
    )
    for needle in (
        "# Symbiosis Handoff Kanban",
        "## Top Priorities",
        "First priority",
        "## Board",
        "### Awaiting (1)",
        "20260602-Awaiting-Row",
        "### In Progress (1)",
        "20990101-1200-Verifier-Gate-Smoke-Re",
        "### Completed (recent) (1)",
        "20260603-Test-Row",
        "### Archived (1)",
        "20260101-Archived-Only",
        "## Warnings",
        "verifier_smoke_dummy_row",
    ):
        assert needle in actual
    for section in golden.split("\n\n"):
        s = section.strip()
        if not s or s.startswith("<!--"):
            continue
        if s.startswith("# Symbiosis"):
            continue
        if s.startswith("## status.md"):
            continue
        assert s in actual or s.split("\n")[0] in actual


def test_golden_kanban_board_key_sections(kanban_mini_tree):
    from kanban.collectors import collect_board
    from kanban.render import render_board

    root, mp = kanban_mini_tree
    model = collect_board(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        completed_limit=5,
        include_presence=False,
    )
    actual = _normalize_kanban_board(render_board(model))
    golden = _normalize_kanban_board(
        (FIXTURES / "expected_kanban_board.txt").read_text(encoding="utf-8")
    )
    for needle in (
        "--- AWAITING (1) ---",
        "20260602-Awaiting-Row",
        "--- IN PROGRESS (1) ---",
        "20990101-1200-Verifier-Gate-Smoke-Re",
        "--- COMPLETED (1) ---",
        "20260603-Test-Row",
        "--- ARCHIVED (1) ---",
        "20260101-Archived-Only",
    ):
        assert needle in actual
    for block in golden.split("\n\n"):
        b = block.strip()
        if not b or b.startswith("<!--"):
            continue
        assert b in actual


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch3) -->