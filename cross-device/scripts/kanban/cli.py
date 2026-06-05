"""symbiosis-kanban CLI (AUTON 6239aa70)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collectors import collect_board
from .paths import CANONICAL_FROM, default_mempalace_root, default_repo_root, handoff_format_path
from .render import render_board, render_json, render_md


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="symbiosis-kanban",
        description="Read-only symbiosis handoff kanban board",
    )
    p.add_argument("--device", required=True)
    p.add_argument("--repo-root", type=Path, default=None)
    p.add_argument("--mempalace-root", type=Path, default=None)
    p.add_argument("--format", choices=("md", "json", "board", "markdown"), default="md")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--no-presence", action="store_true")
    p.add_argument("--completed-limit", type=int, default=5)
    return p.parse_args(argv)


def validate_completed_limit(n: int) -> int | None:
    if n < 1 or n > 50:
        return None
    return n


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

    repo_root = (ns.repo_root or default_repo_root()).expanduser().resolve()
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"repo root invalid (HANDOFF_FORMAT.md missing): {fmt}", file=sys.stderr)
        sys.exit(2)

    mempalace_root = (ns.mempalace_root or default_mempalace_root()).expanduser().resolve()
    fmt_name = "md" if ns.format == "markdown" else ns.format

    model = collect_board(
        device=ns.device,
        repo_root=repo_root,
        mempalace_root=mempalace_root,
        completed_limit=limit,
        include_presence=not ns.no_presence,
    )
    model["meta"]["format"] = fmt_name

    if fmt_name == "json":
        body = render_json(model)
    elif fmt_name == "board":
        body = render_board(model)
    else:
        body = render_md(model)

    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    sys.exit(0)


if __name__ == "__main__":
    main()


# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 6239aa70 batch1) -->