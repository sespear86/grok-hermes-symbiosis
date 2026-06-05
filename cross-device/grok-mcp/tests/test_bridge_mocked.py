import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from grok_mcp.bridge import BridgeArgumentError, run_grok_z
from grok_mcp.config import Settings


def test_run_grok_z_argv(tmp_path: Path) -> None:
    settings = Settings(
        grok_bin="/fake/grok",
        repo_root=str(tmp_path),
        max_timeout_sec=60,
        save_stdout=False,
        log_dir=str(tmp_path),
    )
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = "ok"
    proc.stderr = ""
    with patch("grok_mcp.bridge.subprocess.run", return_value=proc) as mock_run:
        run_grok_z(
            prompt="hello",
            cwd=tmp_path,
            timeout_sec=30,
            settings=settings,
            extra_argv=["--effort", "2"],
        )
    argv = mock_run.call_args[0][0]
    assert argv[0] == "/fake/grok"
    assert argv[1] == "-z"
    assert argv[2] == "hello"
    assert "--effort" in argv
    assert "2" in argv
    assert mock_run.call_args[1]["cwd"] == str(tmp_path)


def test_disallow_extra_argv(tmp_path: Path) -> None:
    settings = Settings(
        grok_bin="grok",
        repo_root=str(tmp_path),
        max_timeout_sec=60,
        save_stdout=False,
        log_dir=str(tmp_path),
    )
    with pytest.raises(BridgeArgumentError):
        run_grok_z(
            prompt="x",
            cwd=tmp_path,
            timeout_sec=5,
            settings=settings,
            extra_argv=["--evil-flag"],
        )


def test_yolo_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SYMBIOSIS_GROK_DELEGATE_YOLO", "1")
    settings = Settings(
        grok_bin="grok",
        repo_root=str(tmp_path),
        max_timeout_sec=60,
        save_stdout=False,
        log_dir=str(tmp_path),
    )
    proc = MagicMock(returncode=0, stdout="", stderr="")
    with patch("grok_mcp.bridge.subprocess.run", return_value=proc) as mock_run:
        run_grok_z(prompt="p", cwd=tmp_path, timeout_sec=5, settings=settings)
    assert "--always-approve" in mock_run.call_args[0][0]