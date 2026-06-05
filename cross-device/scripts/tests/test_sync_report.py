"""Tests for symbiosis-sync-report (AUTON 355e3993)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from handoff_scaffold.log import HEADER_ROW_PATTERN
from handoff_scaffold.paths import CANONICAL_FROM
from handoff_scaffold.paths import default_repo_root as handoff_default_repo_root
from sync_report.collectors import (
    build_warnings,
    collect_git,
    collect_report,
    collect_syncthing,
    extract_open_items_top3,
    extract_status_excerpt,
    run_argv,
    parse_handoff_rows,
)
from sync_report.paths import (
    brother_presence_filename,
    default_repo_root,
    local_presence_filename,
)
from sync_report.render import render_json, render_markdown

SCRIPTS = Path(__file__).resolve().parents[1]
SYNC_REPORT_PKG = SCRIPTS / "sync_report"
SHIM = SCRIPTS / "symbiosis-sync-report"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[3]

JSON_KEYS = {
    "meta",
    "git",
    "syncthing",
    "coordination",
    "presence",
    "warnings",
    "conflicts",
    "relay",
}


@pytest.fixture
def mini_tree(tmp_path):
    root = tmp_path / "repo"
    handoffs = root / "cross-device" / "handoffs"
    coord = root / "cross-device" / "coordination"
    handoffs.mkdir(parents=True)
    coord.mkdir(parents=True)
    src = REPO_ROOT / "cross-device" / "handoffs"
    shutil = __import__("shutil")
    shutil.copy(src / "HANDOFF_FORMAT.md", handoffs / "HANDOFF_FORMAT.md")
    shutil.copy(FIXTURES / "sync_handoff_log_snippet.md", handoffs / "HANDOFF_LOG.md")
    shutil.copy(FIXTURES / "sync_open_items_snippet.md", coord / "OPEN_ITEMS.md")
    shutil.copy(FIXTURES / "sync_status_snippet.md", coord / "status.md")
    mp = tmp_path / "mempalace" / "symbiosis" / "device-presence"
    mp.mkdir(parents=True)
    (mp / "washington.md").write_text(
        "**Last Heartbeat:** 2026-06-04T12:00:00+00:00\n**Current Mode:** **Paired**\n",
        encoding="utf-8",
    )
    (mp / "oregon.md").write_text(
        "**Last Heartbeat:** 2020-01-01T00:00:00+00:00\n**Current Mode:** Solo\n",
        encoding="utf-8",
    )
    return root, tmp_path / "mempalace"


def test_canonical_from_matches_handoff():
    assert "Washington Linux" in CANONICAL_FROM
    assert brother_presence_filename("Washington Linux") == "oregon.md"
    assert local_presence_filename("Washington Linux") == "washington.md"
    assert local_presence_filename("Oregon Windows") == "oregon.md"


def test_open_items_extract():
    text = (FIXTURES / "sync_open_items_snippet.md").read_text(encoding="utf-8")
    body = extract_open_items_top3(text)
    assert body is not None
    assert "First priority" in body
    assert "Known Issues" not in body


def test_status_excerpt_update_block():
    text = (FIXTURES / "sync_status_snippet.md").read_text(encoding="utf-8")
    block = extract_status_excerpt(text)
    assert any("Update (" in ln for ln in block)
    assert len(block) <= 8


def test_parse_handoff_rows_is_public():
    from sync_report.collectors import parse_handoff_rows as public_fn

    text = (FIXTURES / "sync_handoff_log_snippet.md").read_text(encoding="utf-8")
    assert public_fn(text, 1)[0]["id"].startswith("2099")


def test_handoff_rows_parse():
    text = (FIXTURES / "sync_handoff_log_snippet.md").read_text(encoding="utf-8")
    assert HEADER_ROW_PATTERN.search(text)
    rows = parse_handoff_rows(text, 3)
    assert len(rows) == 2
    assert rows[0]["id"].startswith("20990101")


def test_syncthing_no_flag():
    st = collect_syncthing(no_syncthing=True)
    assert st["available"] is False
    assert st["reason"] == "skipped by flag"


def test_run_argv_no_shell(monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        class R:
            returncode = 0
            stdout = "ok"
            stderr = ""

        return R()

    monkeypatch.setattr("sync_report.collectors.subprocess.run", fake_run)
    rc, out = run_argv(["git", "status"], timeout=1.0)
    assert rc == 0
    assert calls[0] == ["git", "status"]


def test_build_warnings_stale_brother():
    presence = {"brother": {"age_seconds": 5000}}
    w = build_warnings(
        device="Washington Linux",
        presence=presence,
        conflicts={"count": 0},
        coordination_dirty=0,
        git_dirty=0,
    )
    assert any("stale" in x for x in w)


def test_render_json_schema_keys():
    model = {k: {} for k in JSON_KEYS}
    model["meta"] = {"device": "Washington Linux"}
    model["warnings"] = []
    model["relay"] = None
    parsed = json.loads(render_json(model))
    assert set(parsed.keys()) == JSON_KEYS


def test_render_markdown_sections():
    model = {
        "meta": {
            "device": "Washington Linux",
            "timestamp_utc": "t",
            "repo_root": "/r",
            "rich_root": "/rich",
            "mempalace_root": "/mp",
        },
        "git": {"available": True, "branch": "main", "ahead": 0, "behind": 0, "dirty_count": 25},
        "syncthing": {"available": False, "reason": "skipped by flag", "folders": [], "warnings": []},
        "coordination": {"handoff_log": {"rows": []}, "open_items_top3": None, "status_excerpt": []},
        "presence": {"local": None, "brother": None},
        "conflicts": {"count": 0, "samples": []},
        "warnings": [],
        "relay": None,
    }
    md = render_markdown(model)
    for heading in ("## Git", "## Syncthing", "## Coordination", "## Presence", "## Warnings"):
        assert heading in md
    git_block = md.split("## Syncthing")[0]
    assert "```" not in git_block
    assert "Dirty file count: 25" in git_block


def test_cli_invalid_device(repo_root):
    r = subprocess.run(
        [sys.executable, str(SHIM), "--device", "Mars"],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={**__import__("os").environ, "SYMBIOSIS_REPO_ROOT": str(repo_root)},
    )
    assert r.returncode == 1
    assert "Washington Linux" in r.stderr


def test_cli_invalid_repo_root(tmp_path):
    bad = tmp_path / "not-a-repo"
    bad.mkdir()
    r = subprocess.run(
        [sys.executable, str(SHIM), "--device", "Washington Linux", "--repo-root", str(bad)],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 2


def test_cli_report_markdown(mini_tree, monkeypatch):
    root, mp = mini_tree
    monkeypatch.chdir(SCRIPTS)
    env = {
        **__import__("os").environ,
        "SYMBIOSIS_REPO_ROOT": str(root),
        "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
    }
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--no-syncthing",
            "--handoff-rows",
            "2",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0, r.stderr
    assert "# Symbiosis Sync Report" in r.stdout
    assert "20990101" in r.stdout
    assert "First priority" in r.stdout
    assert "```" not in r.stdout.split("## Syncthing")[0]


def test_cli_json_format(mini_tree):
    root, mp = mini_tree
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--format",
            "json",
            "--no-syncthing",
        ],
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "SYMBIOSIS_REPO_ROOT": str(root),
            "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
        },
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["syncthing"]["available"] is False
    assert JSON_KEYS.issubset(set(data.keys()))


def test_log_header_live_repo():
    log = REPO_ROOT / "cross-device" / "handoffs" / "HANDOFF_LOG.md"
    text = log.read_text(encoding="utf-8")
    assert HEADER_ROW_PATTERN.search(text)


def test_paths_delegate_repo_root(repo_root, monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_REPO_ROOT", str(repo_root))
    assert default_repo_root() == handoff_default_repo_root()


def test_git_model_has_no_short_status(monkeypatch):
    def fake_run(argv, **kwargs):
        class R:
            returncode = 0
            stdout = "## main\n M secret/path.txt\n?? other.txt"
            stderr = ""

        return R()

    monkeypatch.setattr("sync_report.collectors.subprocess.run", fake_run)
    g = collect_git(Path("/tmp/repo"))
    assert "short_status" not in g
    assert g["dirty_count"] == 2
    assert g["branch"] == "main"


def test_handoff_log_drift_merged_into_warnings(repo_root, tmp_path):
    handoffs = repo_root / "cross-device" / "handoffs"
    shutil = __import__("shutil")
    shutil.copy(
        FIXTURES / "sync_handoff_log_drift.md",
        handoffs / "HANDOFF_LOG.md",
    )
    model = collect_report(
        device="Washington Linux",
        repo_root=repo_root,
        rich_root=tmp_path / "rich",
        mempalace_root=tmp_path / "mp",
        handoff_rows=3,
        no_syncthing=True,
        include_relay=False,
    )
    assert any("HANDOFF_LOG header drift" in w for w in model["warnings"])


def test_build_warnings_coordination_dirty_and_conflicts():
    w = build_warnings(
        device="Washington Linux",
        presence={"brother": None},
        conflicts={"count": 3},
        coordination_dirty=2,
        git_dirty=0,
    )
    assert any("coordination/" in x for x in w)
    assert any("sync-conflict" in x for x in w)


def test_cli_handoff_rows_bounds(repo_root):
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--handoff-rows",
            "11",
            "--no-syncthing",
        ],
        capture_output=True,
        text=True,
        cwd=str(SCRIPTS),
        env={**__import__("os").environ, "SYMBIOSIS_REPO_ROOT": str(repo_root)},
    )
    assert r.returncode == 1


def test_cli_out_file(mini_tree, tmp_path):
    root, mp = mini_tree
    out = tmp_path / "report.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--no-syncthing",
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "SYMBIOSIS_REPO_ROOT": str(root),
            "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
        },
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0
    assert out.is_file()
    assert "# Symbiosis Sync Report" in out.read_text(encoding="utf-8")


def test_cli_relay_missing_script(mini_tree, tmp_path):
    root, mp = mini_tree
    rich = tmp_path / "rich"
    rich.mkdir()
    r = subprocess.run(
        [
            sys.executable,
            str(SHIM),
            "--device",
            "Washington Linux",
            "--no-syncthing",
            "--relay",
            "--rich-root",
            str(rich),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "SYMBIOSIS_REPO_ROOT": str(root),
            "SYMBIOSIS_MEMPALACE_ROOT": str(mp),
        },
        cwd=str(SCRIPTS),
    )
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert any("relay-health" in w for w in data["warnings"])


def test_syncthing_env_folders_mocked(monkeypatch):
    monkeypatch.setenv("SYMBIOSIS_SYNCTHING_FOLDERS", "folder-a,folder-b")

    def fake_binary():
        return "/usr/bin/syncthing"

    def fake_run(argv, **kwargs):
        class R:
            returncode = 0
            stdout = "State: idle"
            stderr = ""

        return R()

    monkeypatch.setattr("sync_report.collectors._syncthing_binary", fake_binary)
    monkeypatch.setattr("sync_report.collectors.subprocess.run", fake_run)
    st = collect_syncthing(no_syncthing=False)
    assert st["available"] is True
    assert len(st["folders"]) == 2


def test_no_shell_true_in_sync_report_sources():
    for py in SYNC_REPORT_PKG.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        assert "shell=True" not in text, f"shell=True found in {py}"


def _normalize_report_md(md: str) -> str:
    out: list[str] = []
    for ln in md.splitlines():
        if ln.startswith("- **Timestamp (UTC):**"):
            out.append("- **Timestamp (UTC):** <TIMESTAMP>")
            continue
        if ln.startswith("- **Repo root:**"):
            continue
        if ln.startswith("- **Rich root:**"):
            continue
        if ln.startswith("- **Mempalace root:**"):
            continue
        if ln.startswith("- Local: age=") or ln.startswith("- Brother: age="):
            out.append(ln.split("age=")[0] + "age=")
            continue
        out.append(ln)
    return "\n".join(out)


def test_golden_markdown_key_sections(mini_tree, tmp_path, monkeypatch):
    """Golden sections: git happy path mocked (mini_tree is not a git repo in CI/pytest)."""

    def fake_collect_git(_repo_root):
        return {
            "available": True,
            "branch": "main",
            "ahead": 0,
            "behind": 0,
            "dirty_count": 0,
            "warnings": [],
        }

    monkeypatch.setattr("sync_report.collectors.collect_git", fake_collect_git)
    monkeypatch.setattr(
        "sync_report.collectors.collect_coordination_dirty", lambda _repo: 0
    )

    root, mp = mini_tree
    model = collect_report(
        device="Washington Linux",
        repo_root=root,
        rich_root=tmp_path / "rich",
        mempalace_root=mp,
        handoff_rows=1,
        no_syncthing=True,
        include_relay=False,
    )
    actual = _normalize_report_md(render_markdown(model))
    golden = _normalize_report_md(
        (FIXTURES / "expected_report.md").read_text(encoding="utf-8")
    )
    for needle in (
        "## Git",
        "Dirty file count:",
        "## Syncthing",
        "skipped by flag",
        "### OPEN_ITEMS Top 3",
        "First priority",
        "20990101-1200-Verifier-Gate-Smoke-Re",
        "## Warnings",
    ):
        assert needle in actual
    for section in golden.split("\n\n"):
        s = section.strip()
        if s and not s.startswith("# Symbiosis") and "<TIMESTAMP>" not in s:
            if s.startswith("## ") or s.startswith("### ") or s.startswith("|"):
                assert s in actual or s.split("\n")[0] in actual