"""Tests for symbiosis-projects list (AUTON 61cdeb81 PR1)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from joint_projects.collectors import collect_list
from joint_projects.paths import assert_under_projects_root, default_projects_root, validate_slug
from joint_projects.render import render_json, render_md

SCRIPTS = Path(__file__).resolve().parents[1]
JP_PKG = SCRIPTS / "joint_projects"
SHIM = SCRIPTS / "symbiosis-projects"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _normalize_projects_md(text: str) -> str:
    out: list[str] = []
    for ln in text.splitlines():
        if ln.startswith("- **Timestamp (UTC):**"):
            out.append("- **Timestamp (UTC):** <TIMESTAMP>")
            continue
        if ln.startswith("- **Projects root:**"):
            out.append("- **Projects root:** `PLACEHOLDER`")
            continue
        if ln.startswith("- **Repo root:**"):
            continue
        out.append(ln)
    return "\n".join(out)


def test_validate_slug_rejects_bad():
    with pytest.raises(ValueError):
        validate_slug("..")
    with pytest.raises(ValueError):
        validate_slug("ab")


def test_assert_under_projects_root_rejects_escape(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(ValueError):
        assert_under_projects_root(outside, root)


def test_collect_list_basic(projects_mini_tree):
    repo_root, projects_root = projects_mini_tree
    model = collect_list(
        device="Washington Linux",
        projects_root=projects_root,
        repo_root=repo_root,
        include_coord=True,
    )
    slugs = [p["slug"] for p in model["projects"]]
    assert slugs == ["Alpha-App", "Beta-Only-Readme"]
    assert model["projects"][0]["has_stignore"] is True
    assert model["meta"]["ball_holder"] == "Washington has the ball."
    assert model["coordination"]["open_items_top3"] is not None


def test_collect_list_missing_root_no_mkdir(tmp_path):
    missing = tmp_path / "missing-projects"
    assert not missing.exists()
    model = collect_list(
        device="Washington Linux",
        projects_root=missing,
        repo_root=None,
        include_coord=False,
    )
    assert not missing.exists()
    assert model["projects"] == []
    assert any("projects root does not exist" in w for w in model["warnings"])


def test_golden_projects_list_markdown(projects_mini_tree):
    repo_root, projects_root = projects_mini_tree
    model = collect_list(
        device="Washington Linux",
        projects_root=projects_root,
        repo_root=repo_root,
        include_coord=True,
    )
    actual = _normalize_projects_md(render_md(model))
    golden = _normalize_projects_md(
        (FIXTURES / "expected_projects_list.md").read_text(encoding="utf-8")
    )
    for needle in (
        "# Symbiosis Shared Projects",
        "## Projects",
        "| Alpha-App | yes | yes |",
        "## Top Priorities",
        "First priority",
        "## Warnings",
        "- none",
    ):
        assert needle in actual
    for section in golden.split("\n\n"):
        s = section.strip()
        if not s:
            continue
        if s.startswith("# Symbiosis"):
            continue
        assert s in actual or s.split("\n")[0] in actual


def test_list_succeeds_without_repo_coord_warnings(tmp_path):
    projects_root = tmp_path / "projects"
    projects_root.mkdir()
    bad_repo = tmp_path / "not-repo"
    bad_repo.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={
            **os.environ,
            "SYMBIOSIS_REPO_ROOT": str(bad_repo),
            "SYMBIOSIS_PROJECTS_ROOT": str(projects_root),
        },
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert any("coordination skipped" in w for w in data.get("warnings", []))
    assert data["coordination"]["open_items_top3"] is None


def test_list_strict_coord_exit2_invalid_repo(tmp_path):
    bad_repo = tmp_path / "not-repo"
    bad_repo.mkdir()
    projects_root = tmp_path / "projects"
    projects_root.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--strict-coord",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={**os.environ, "SYMBIOSIS_REPO_ROOT": str(bad_repo)},
    )
    assert r.returncode == 2
    assert "HANDOFF_FORMAT" in r.stderr


def test_list_invalid_explicit_repo_root_exit2(tmp_path, projects_mini_tree):
    _repo, projects_root = projects_mini_tree
    bad_repo = tmp_path / "not-repo"
    bad_repo.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--repo-root",
            str(bad_repo),
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 2
    assert "HANDOFF_FORMAT" in r.stderr


def test_cli_invalid_device(projects_mini_tree):
    _repo, projects_root = projects_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Mars",
            "--projects-root",
            str(projects_root),
            "--no-coord",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 1
    assert "Washington Linux" in r.stderr


def test_cli_markdown_format_alias(projects_mini_tree):
    repo_root, projects_root = projects_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--repo-root",
            str(repo_root),
            "--format",
            "markdown",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    assert "# Symbiosis Shared Projects" in r.stdout
    assert "## Top Priorities" in r.stdout


def test_cli_no_coord_skips_coordination(projects_mini_tree):
    repo_root, projects_root = projects_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--repo-root",
            str(repo_root),
            "--no-coord",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["meta"]["format"] == "json"
    assert data["coordination"]["open_items_top3"] is None
    assert data["meta"].get("ball_holder") is None
    assert not any("coordination skipped" in w for w in data.get("warnings", []))


def test_cli_json_format(projects_mini_tree):
    repo_root, projects_root = projects_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "list",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
            "--repo-root",
            str(repo_root),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["schema_version"] == 1
    assert len(data["projects"]) == 2


def test_no_shell_true_in_joint_projects_sources():
    for py in JP_PKG.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        assert "shell=True" not in text, f"shell=True found in {py}"


def test_default_projects_root_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_PROJECTS_ROOT", str(tmp_path / "custom"))
    assert default_projects_root() == (tmp_path / "custom").resolve()


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR1) -->