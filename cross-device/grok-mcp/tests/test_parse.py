from pathlib import Path

from grok_mcp.parse import extract_result


def test_fence_ok(fixtures_dir: Path) -> None:
    text = (fixtures_dir / "grok_stdout_ok.txt").read_text()
    r = extract_result(stdout=text, exit_code=0, elapsed_sec=1.0)
    assert r["ok"] is True
    assert r["verdict"] == "complete"
    assert r["summary"] == "Implemented feature X"
    assert len(r["artifacts"]) == 1


def test_check_verdict_pass(fixtures_dir: Path) -> None:
    text = (fixtures_dir / "grok_stdout_check_pass.txt").read_text()
    r = extract_result(
        stdout=text,
        exit_code=0,
        elapsed_sec=2.0,
        require_check_verdict=True,
    )
    assert r["verdict"] == "pass"


def test_fallback_exit_code() -> None:
    r = extract_result(stdout="plain text only", exit_code=1, elapsed_sec=0.5)
    assert r["ok"] is False
    assert "parse_warning" in r


def test_timeout() -> None:
    r = extract_result(stdout="partial", exit_code=-9, elapsed_sec=10.0, timed_out=True)
    assert r["verdict"] == "timeout"
    assert r["ok"] is False