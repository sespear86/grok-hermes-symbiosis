"""Render and template safety."""
from __future__ import annotations

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