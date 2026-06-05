# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch1) -->
"""symbiosis-handoff-dashboard CLI (AUTON 3694a72b)."""
from __future__ import annotations

import argparse
import os
import sys
import threading
import webbrowser
from pathlib import Path

from .collectors import collect_board_for_device
from .paths import (
    CANONICAL_FROM,
    DEFAULT_PORT_ENV,
    default_mempalace_root,
    default_repo_root,
    handoff_format_path,
)
from .server import create_server, make_handler, validate_bind_host


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default_port = int(os.environ.get(DEFAULT_PORT_ENV, "8766"))
    p = argparse.ArgumentParser(
        prog="symbiosis-handoff-dashboard",
        description="Read-only localhost handoff kanban dashboard",
    )
    p.add_argument("--device", required=True)
    p.add_argument("--port", type=int, default=default_port)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--open", action="store_true")
    p.add_argument("--repo-root", type=Path, default=None)
    p.add_argument("--mempalace-root", type=Path, default=None)
    p.add_argument("--no-presence", action="store_true")
    p.add_argument("--completed-limit", type=int, default=5)
    p.add_argument("--allow-lan", action="store_true")
    p.add_argument("--check-only", action="store_true")
    return p.parse_args(argv)


def validate_completed_limit(n: int) -> int | None:
    if n < 1 or n > 50:
        return None
    return n


def run_check(
    *,
    device: str,
    repo_root: Path,
    mempalace_root: Path,
    completed_limit: int,
    include_presence: bool,
) -> int:
    collect_board_for_device(
        device=device,
        repo_root=repo_root,
        mempalace_root=mempalace_root,
        completed_limit=completed_limit,
        include_presence=include_presence,
    )
    return 0


def main(argv: list[str] | None = None) -> None:
    ns = parse_args(argv)
    if ns.device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        sys.exit(1)

    limit = validate_completed_limit(ns.completed_limit)
    if limit is None:
        print("--completed-limit must be between 1 and 50", file=sys.stderr)
        sys.exit(1)

    bind_err = validate_bind_host(ns.host, ns.allow_lan)
    if bind_err:
        print(bind_err, file=sys.stderr)
        sys.exit(1)

    repo_root = (ns.repo_root or default_repo_root()).expanduser().resolve()
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"repo root invalid (HANDOFF_FORMAT.md missing): {fmt}", file=sys.stderr)
        sys.exit(2)

    mempalace_root = (ns.mempalace_root or default_mempalace_root()).expanduser().resolve()
    include_presence = not ns.no_presence

    if ns.check_only:
        code = run_check(
            device=ns.device,
            repo_root=repo_root,
            mempalace_root=mempalace_root,
            completed_limit=limit,
            include_presence=include_presence,
        )
        sys.exit(code)

    handler_cls = make_handler(
        device=ns.device,
        repo_root=repo_root,
        mempalace_root=mempalace_root,
        completed_limit_default=limit,
        include_presence=include_presence,
    )
    httpd = create_server(ns.host, ns.port, handler_cls)
    url_host = "127.0.0.1" if ns.host in ("0.0.0.0", "::") else ns.host
    url = f"http://{url_host}:{ns.port}/"
    print(
        f"[symbiosis-handoff-dashboard] {ns.device} listening on {url} "
        f"(repo={repo_root})",
        flush=True,
    )
    if ns.open:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.", flush=True)
    finally:
        httpd.server_close()
    sys.exit(0)


if __name__ == "__main__":
    main()