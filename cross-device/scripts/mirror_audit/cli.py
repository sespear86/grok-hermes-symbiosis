"""symbiosis-mirror-audit CLI (AUTON 9be206cf sym-build-04 starter)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collectors import collect_audit
from .paths import (
    CANONICAL_FROM,
    default_bin_dir,
    default_grok_root,
    default_repo_root,
    default_rich_root,
    mirror_kits_path,
)
from .render import render_json, render_markdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="symbiosis-mirror-audit",
        description="Compare git/rich/~/.grok/~/bin vs MIRROR_KITS checklist (read-only)",
    )
    p.add_argument("--device", required=True)
    p.add_argument("--repo-root", type=Path, default=None)
    p.add_argument("--rich-root", type=Path, default=None)
    p.add_argument("--grok-root", type=Path, default=None)
    p.add_argument("--bin-dir", type=Path, default=None)
    p.add_argument("--format", choices=("markdown", "json"), default="markdown")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit 3 if any component gaps detected",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    ns = parse_args(argv)
    if ns.device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        sys.exit(1)

    repo_root = (ns.repo_root or default_repo_root()).expanduser().resolve()
    mk = mirror_kits_path(repo_root)
    if not mk.is_file():
        print(f"repo root invalid (MIRROR_KITS missing): {mk}", file=sys.stderr)
        sys.exit(2)

    rich_root = (ns.rich_root or default_rich_root()).expanduser().resolve()
    grok_root = (ns.grok_root or default_grok_root()).expanduser().resolve()
    bin_dir = (ns.bin_dir or default_bin_dir()).expanduser().resolve()

    model = collect_audit(
        device=ns.device,
        repo_root=repo_root,
        rich_root=rich_root,
        grok_root=grok_root,
        bin_dir=bin_dir,
    )

    body = render_json(model) if ns.format == "json" else render_markdown(model)
    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)

    if ns.strict and model.gap_count > 0:
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()