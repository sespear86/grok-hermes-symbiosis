import os
from pathlib import Path

import pytest

from grok_mcp.config import Settings
from grok_mcp.paths import PathValidationError, resolve_confined


def test_resolve_under_repo_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "repo"
    sub = repo / "pkg"
    sub.mkdir(parents=True)
    monkeypatch.chdir(sub)
    settings = Settings(
        grok_bin="grok",
        repo_root=str(repo),
        max_timeout_sec=7200,
        save_stdout=False,
        log_dir=str(tmp_path / "logs"),
    )
    p = resolve_confined(None, settings, default_cwd=True)
    assert p == sub.resolve()


def test_reject_outside_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    settings = Settings(
        grok_bin="grok",
        repo_root=str(repo),
        max_timeout_sec=7200,
        save_stdout=False,
        log_dir=str(tmp_path / "logs"),
    )
    with pytest.raises(PathValidationError):
        resolve_confined(str(other), settings)