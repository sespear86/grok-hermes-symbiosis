"""Validation and path confinement."""
from __future__ import annotations

import pytest

from handoff_scaffold.paths import assert_under_handoffs, handoffs_root
from handoff_scaffold.render import render_readme
from handoff_scaffold.validate import validate_package


def test_path_confinement_rejects_escape(repo_root, tmp_path):
    outside = tmp_path / "evil"
    outside.mkdir()
    with pytest.raises(ValueError, match="not under handoffs"):
        assert_under_handoffs(outside, repo_root)


def test_validate_scaffolded_package(repo_root):
    fid = "20260604-1300-Validate-Me"
    pkg = handoffs_root(repo_root) / fid
    pkg.mkdir()
    readme = render_readme(
        from_device="Washington Linux",
        to_device="Oregon Windows",
        slug="Validate-Me",
        date_iso="2026-06-04",
        time_hhmm="1300",
        context="c",
        task="t",
    )
    (pkg / "README.md").write_text(readme, encoding="utf-8")
    res = validate_package(pkg, repo_root)
    assert res.ok, res.errors


def test_validate_fails_on_drifted_sections(repo_root):
    fid = "20260604-1301-Bad-Sections"
    pkg = handoffs_root(repo_root) / fid
    pkg.mkdir()
    (pkg / "README.md").write_text(
        "# Handoff\n\n**ID:** 20260604-1301-Bad-Sections\n\n## Context\n\nx\n",
        encoding="utf-8",
    )
    res = validate_package(pkg, repo_root)
    assert not res.ok