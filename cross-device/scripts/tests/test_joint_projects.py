"""Tests for symbiosis-projects list (AUTON 61cdeb81 PR1)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import json as json_mod

from joint_projects.collectors import collect_list
from joint_projects.init import init_project
from joint_projects.paths import (
    assert_under_projects_root,
    default_projects_root,
    project_dir,
    validate_slug,
)
from joint_projects.render import render_json, render_md
from joint_projects.verify import verify_all, verify_project

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


def test_init_dry_run_no_writes(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    res = init_project(
        slug="Dry-Run-App",
        root=root,
        device="Washington Linux",
        template="minimal",
        dry_run=True,
    )
    assert res.ok
    assert not (root / "Dry-Run-App").exists()
    assert len(res.planned_paths) == 3


def test_init_minimal_materializes(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    res = init_project(
        slug="My-Joint-App",
        root=root,
        device="Washington Linux",
        template="minimal",
        dry_run=False,
    )
    assert res.ok, res.errors
    proj = root / "My-Joint-App"
    assert (proj / "README.md").is_file()
    assert (proj / ".stignore").is_file()
    st = (proj / ".stignore").read_text(encoding="utf-8")
    assert "**/.grok/" in st
    assert "**/.hermes/" in st
    manifest = json_mod.loads((proj / ".symbiosis-project.json").read_text(encoding="utf-8"))
    assert manifest["slug"] == "My-Joint-App"
    assert manifest["created_by_device"] == "Washington Linux"
    assert manifest["template"] == "minimal"
    assert manifest["auton_id"] == "61cdeb81"


def test_init_app_template_src_gitkeep(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    res = init_project(
        slug="App-Template",
        root=root,
        device="Oregon Windows",
        template="app",
        dry_run=False,
    )
    assert res.ok
    assert (root / "App-Template" / "src" / ".gitkeep").is_file()
    readme = (root / "App-Template" / "README.md").read_text(encoding="utf-8")
    assert "Suggested layout" in readme


def test_init_existing_dir_fails(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    (root / "Collide").mkdir()
    res = init_project(
        slug="Collide",
        root=root,
        device="Washington Linux",
        dry_run=False,
    )
    assert not res.ok


def test_init_path_confinement_invalid_slug(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    with pytest.raises(ValueError):
        project_dir(root, "..")
    res = init_project(
        slug="..",
        root=root,
        device="Washington Linux",
        dry_run=False,
    )
    assert not res.ok


def test_verify_project_ok_after_init(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    init_project(
        slug="Verify-Me",
        root=root,
        device="Washington Linux",
        dry_run=False,
    )
    res = verify_project(root, "Verify-Me")
    assert res.ok
    assert not res.errors


def test_verify_project_legacy_warnings(projects_mini_tree):
    _repo, projects_root = projects_mini_tree
    alpha = verify_project(projects_root, "Alpha-App")
    assert alpha.ok
    assert any(".symbiosis-project.json" in w for w in alpha.warnings)

    beta = verify_project(projects_root, "Beta-Only-Readme")
    assert not beta.ok
    assert any(".stignore" in e for e in beta.errors)


def test_verify_all_projects(projects_mini_tree):
    _repo, projects_root = projects_mini_tree
    results = verify_all(projects_root)
    slugs = {r.slug for r in results}
    assert slugs == {"Alpha-App", "Beta-Only-Readme"}


def test_verify_warns_git_and_agent_home(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    slug = "Warn-Dirs"
    init_project(slug=slug, root=root, device="Washington Linux", dry_run=False)
    proj = root / slug
    (proj / ".git").mkdir()
    agent = proj / "nested" / ".grok"
    agent.mkdir(parents=True)
    res = verify_project(root, slug)
    assert res.ok
    assert any(".git/" in w for w in res.warnings)
    assert any(".grok" in w for w in res.warnings)


def test_cli_init_dry_run(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "init",
            "--slug",
            "Cli-Dry",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(root),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    assert "[dry-run]" in r.stdout
    assert not (root / "Cli-Dry").exists()


def test_cli_init_and_verify(tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "init",
            "--slug",
            "Cli-Full",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(root),
            "--template",
            "app",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    r2 = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "verify",
            "--slug",
            "Cli-Full",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(root),
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r2.returncode == 0, r2.stderr
    assert "OK" in r2.stdout


def test_cli_verify_all_exit1_on_errors(projects_mini_tree):
    _repo, projects_root = projects_mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "verify",
            "--device",
            "Washington Linux",
            "--projects-root",
            str(projects_root),
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 1
    assert "Beta-Only-Readme" in r.stdout


def test_init_list_verify_no_handoff_log_write(repo_root, tmp_path):
    log = repo_root / "cross-device" / "handoffs" / "HANDOFF_LOG.md"
    mtime_before = log.stat().st_mtime
    projects_root = tmp_path / "projects"
    projects_root.mkdir()
    init_project(
        slug="No-Log-Touch",
        root=projects_root,
        device="Washington Linux",
        dry_run=False,
    )
    verify_project(projects_root, "No-Log-Touch")
    collect_list(
        device="Washington Linux",
        projects_root=projects_root,
        repo_root=repo_root,
        include_coord=True,
    )
    assert log.stat().st_mtime == mtime_before


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR2) -->