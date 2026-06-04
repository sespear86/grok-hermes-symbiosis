"""symbiosis-sync-report CLI (AUTON 355e3993)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collectors import collect_report
from .paths import (
    CANONICAL_FROM,
    default_mempalace_root,
    default_repo_root,
    default_rich_root,
    handoff_format_path,
)
from .render import render_json, render_markdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="symbiosis-sync-report",
        description="Read-only symbiosis sync & coordination snapshot",
    )
    p.add_argument("--device", required=True)
    p.add_argument("--repo-root", type=Path, default=None)
    p.add_argument("--rich-root", type=Path, default=None)
    p.add_argument("--mempalace-root", type=Path, default=None)
    p.add_argument("--format", choices=("markdown", "json"), default="markdown")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--no-syncthing", action="store_true")
    p.add_argument("--relay", action="store_true")
    p.add_argument("--handoff-rows", type=int, default=3)
    return p.parse_args(argv)


def validate_handoff_rows(n: int) -> int | None:
    if n < 1 or n > 10:
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

    rows = validate_handoff_rows(ns.handoff_rows)
    if rows is None:
        print("--handoff-rows must be between 1 and 10", file=sys.stderr)
        sys.exit(1)

    repo_root = (ns.repo_root or default_repo_root()).expanduser().resolve()
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"repo root invalid (HANDOFF_FORMAT.md missing): {fmt}", file=sys.stderr)
        sys.exit(2)

    rich_root = (ns.rich_root or default_rich_root()).expanduser().resolve()
    mempalace_root = (ns.mempalace_root or default_mempalace_root()).expanduser().resolve()

    model = collect_report(
        device=ns.device,
        repo_root=repo_root,
        rich_root=rich_root,
        mempalace_root=mempalace_root,
        handoff_rows=rows,
        no_syncthing=ns.no_syncthing,
        include_relay=ns.relay,
    )

    if ns.format == "json":
        body = render_json(model)
    else:
        body = render_markdown(model)

    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    sys.exit(0)


if __name__ == "__main__":
    main()