# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->
"""Tests for symbiosis-handoff-live-dashboard (AUTON 3694a72b)."""
from __future__ import annotations

import http.client
import json
import re
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from handoff_dashboard.cli import main as cli_main
from handoff_dashboard.cli import parse_args, validate_completed_limit
from handoff_dashboard.collectors import collect_board_for_device, render_format
from handoff_dashboard.paths import static_dir
from handoff_dashboard.server import create_server, make_handler, validate_bind_host
SCRIPTS = Path(__file__).resolve().parents[1]
SHIM = SCRIPTS / "symbiosis-handoff-dashboard"
PKG = SCRIPTS / "handoff_dashboard"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

JSON_KEYS = {
    "schema_version",
    "meta",
    "presence",
    "coordination",
    "columns",
    "counts",
    "truncation",
    "warnings",
}


def _normalize_model(model: dict) -> dict:
    out = json.loads(json.dumps(model))
    meta = out.get("meta") or {}
    if "timestamp_utc" in meta:
        meta["timestamp_utc"] = "<normalized>"
    if "format" in meta:
        meta["format"] = "<normalized>"
    for key in ("repo_root", "mempalace_root"):
        if key in meta:
            meta[key] = "<normalized>"
    out["meta"] = meta
    if "warnings" in out:
        out["warnings"] = sorted(out["warnings"])
    return out


@pytest.fixture
def dashboard_server(kanban_mini_tree):
    root, mp = kanban_mini_tree
    handler = make_handler(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        completed_limit_default=5,
        include_presence=False,
    )
    httpd = create_server("127.0.0.1", 0, handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield "127.0.0.1", port, root, mp
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_static_dir_exists():
    assert (static_dir() / "index.html").is_file()
    assert (static_dir() / "app.js").is_file()


def test_collect_board_for_device_reuses_kanban(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board_for_device(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    assert model["schema_version"] == 1
    assert model["counts"]["awaiting"] >= 1


def test_render_format_types(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board_for_device(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    j, ct_j = render_format(model, "json")
    assert "application/json" in ct_j
    assert json.loads(j)["schema_version"] == 1
    md, ct_m = render_format(model, "md")
    assert "text/plain" in ct_m
    assert "Symbiosis Handoff Kanban" in md
    board, ct_b = render_format(model, "board")
    assert "AWAITING" in board


def test_api_json_schema_keys(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=json")
    resp = conn.getresponse()
    assert resp.status == 200
    data = json.loads(resp.read().decode())
    assert set(data.keys()) == JSON_KEYS


def test_healthz(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/healthz")
    resp = conn.getresponse()
    assert resp.status == 200
    assert resp.getheader("Content-Type", "").startswith("text/plain")
    body = resp.read()
    assert body == b"ok\n"


def test_api_md_format(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=md")
    resp = conn.getresponse()
    assert resp.status == 200
    text = resp.read().decode()
    assert "## Top Priorities" in text


def test_api_board_format(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=board")
    resp = conn.getresponse()
    assert resp.status == 200
    assert b"AWAITING" in resp.read()


def test_api_formats_match_kanban_render(kanban_mini_tree, dashboard_server):
    root, mp = kanban_mini_tree
    host, port, _, _ = dashboard_server
    model = collect_board_for_device(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=json")
    api = json.loads(conn.getresponse().read().decode())
    assert _normalize_model(api) == _normalize_model(model)


def test_index_html_served(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/")
    resp = conn.getresponse()
    assert resp.status == 200
    assert b"Symbiosis Handoff" in resp.read()


def test_static_css_served(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/static/style.css")
    resp = conn.getresponse()
    assert resp.status == 200


def test_warnings_present_in_api(kanban_mini_tree, dashboard_server):
    host, port, root, mp = dashboard_server
    model = collect_board_for_device(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=True,
    )
    assert model["warnings"]
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=json")
    api = json.loads(conn.getresponse().read().decode())
    assert api["warnings"]


def test_cli_argparse_device_required():
    with pytest.raises(SystemExit):
        parse_args([])


def test_cli_invalid_device():
    with pytest.raises(SystemExit) as exc:
        cli_main(["--device", "Mars", "--check-only"])
    assert exc.value.code == 1


def test_validate_completed_limit():
    assert validate_completed_limit(5) == 5
    assert validate_completed_limit(0) is None


def test_server_bind_guard_no_lan():
    assert validate_bind_host("0.0.0.0", False) is not None
    assert validate_bind_host("127.0.0.1", False) is None
    assert validate_bind_host("0.0.0.0", True) is None


def test_cli_check_only_exit(kanban_mini_tree):
    root, mp = kanban_mini_tree
    with pytest.raises(SystemExit) as exc:
        cli_main(
            [
                "--device",
                "Washington Linux",
                "--repo-root",
                str(root),
                "--mempalace-root",
                str(mp),
                "--check-only",
                "--no-presence",
            ]
        )
    assert exc.value.code == 0


def test_cli_invalid_repo_exit_2(tmp_path):
    bad = tmp_path / "empty"
    bad.mkdir()
    with pytest.raises(SystemExit) as exc:
        cli_main(
            [
                "--device",
                "Washington Linux",
                "--repo-root",
                str(bad),
                "--check-only",
            ]
        )
    assert exc.value.code == 2


def test_no_shell_in_handoff_dashboard_sources():
    for py in PKG.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        assert "shell=True" not in text, py.name


def test_shim_importable():
    assert SHIM.is_file()


def test_start_launcher_script_exists():
    launcher = SCRIPTS / "start-handoff-dashboard.sh"
    assert launcher.is_file()
    assert launcher.stat().st_mode & 0o111


def test_cli_module_help():
    proc = subprocess.run(
        [sys.executable, str(SHIM), "--help"],
        cwd=str(SCRIPTS),
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert proc.returncode == 0
    assert "--device" in proc.stdout


def test_api_bad_format(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=xml")
    assert conn.getresponse().status == 400


def test_completed_limit_query(dashboard_server):
    host, port, _, _ = dashboard_server
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", "/api/kanban?format=json&completed_limit=1")
    data = json.loads(conn.getresponse().read().decode())
    assert data["counts"]["completed_shown"] <= 1


def test_golden_api_structure_file(kanban_mini_tree):
    root, mp = kanban_mini_tree
    model = collect_board_for_device(
        device="Washington Linux",
        repo_root=root,
        mempalace_root=mp,
        include_presence=False,
    )
    golden_path = FIXTURES / "expected_dashboard_api.json"
    if not golden_path.is_file():
        golden_path.write_text(
            json.dumps(_normalize_model(model), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    assert _normalize_model(model) == _normalize_model(golden)


def test_poll_constant_in_app_js():
    js = (static_dir() / "app.js").read_text(encoding="utf-8")
    assert re.search(r"POLL_MS\s*=\s*5000", js)


def test_shim_check_only_subprocess(kanban_mini_tree):
    root, mp = kanban_mini_tree
    proc = subprocess.run(
        [
            str(SHIM),
            "--device",
            "Washington Linux",
            "--repo-root",
            str(root),
            "--mempalace-root",
            str(mp),
            "--check-only",
            "--no-presence",
        ],
        cwd=str(SCRIPTS),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0