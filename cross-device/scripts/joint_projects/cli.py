"""symbiosis-projects CLI (AUTON 61cdeb81)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from handoff_scaffold.paths import handoff_format_path

from .collectors import collect_list
from .init import init_project
from .paths import CANONICAL_FROM, default_projects_root, default_repo_root
from .render import render_json, render_md
from .verify import verify_all, verify_project


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="symbiosis-projects",
        description="Symbiosis shared joint projects workspace (list / init / verify)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List project directories under projects root")
    list_p.add_argument("--device", required=True)
    list_p.add_argument("--projects-root", type=Path, default=None)
    list_p.add_argument("--repo-root", type=Path, default=None)
    list_p.add_argument("--format", choices=("md", "json", "markdown"), default="md")
    list_p.add_argument("--no-coord", action="store_true")
    list_p.add_argument("--strict-coord", action="store_true")

    init_p = sub.add_parser("init", help="Initialize a new project under projects root")
    init_p.add_argument("--slug", required=True)
    init_p.add_argument("--device", required=True)
    init_p.add_argument("--projects-root", type=Path, default=None)
    init_p.add_argument("--dry-run", action="store_true")
    init_p.add_argument("--template", choices=("minimal", "app"), default="minimal")

    verify_p = sub.add_parser("verify", help="Verify project layout and hygiene")
    verify_p.add_argument("--slug", default=None)
    verify_p.add_argument("--device", required=True)
    verify_p.add_argument("--projects-root", type=Path, default=None)

    return p.parse_args(argv)


def _validate_repo_for_coord(repo_root: Path, *, strict: bool) -> int | None:
    """Return exit code if invalid under strict/explicit repo rules, else None."""
    fmt = handoff_format_path(repo_root)
    if fmt.is_file():
        return None
    if strict:
        print(
            f"repo root invalid (HANDOFF_FORMAT.md missing): {fmt}",
            file=sys.stderr,
        )
        return 2
    return None


def cmd_list(ns: argparse.Namespace) -> int:
    if ns.device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        return 1

    projects_root = (ns.projects_root or default_projects_root()).expanduser().resolve()

    include_coord = not ns.no_coord
    repo_for_collect: Path | None = None

    if ns.no_coord:
        repo_for_collect = None
    elif ns.repo_root is not None:
        repo_for_collect = ns.repo_root.expanduser().resolve()
        code = _validate_repo_for_coord(repo_for_collect, strict=True)
        if code is not None:
            return code
    elif ns.strict_coord:
        repo_for_collect = default_repo_root().expanduser().resolve()
        code = _validate_repo_for_coord(repo_for_collect, strict=True)
        if code is not None:
            return code
    else:
        candidate = default_repo_root().expanduser().resolve()
        if handoff_format_path(candidate).is_file():
            repo_for_collect = candidate

    try:
        model = collect_list(
            device=ns.device,
            projects_root=projects_root,
            repo_root=repo_for_collect,
            include_coord=include_coord,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    fmt_name = "md" if ns.format == "markdown" else ns.format
    model["meta"]["format"] = fmt_name
    if fmt_name == "json":
        body = render_json(model)
    else:
        body = render_md(model)
    sys.stdout.write(body)
    return 0


def cmd_init(ns: argparse.Namespace) -> int:
    if ns.device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        return 1

    projects_root = (ns.projects_root or default_projects_root()).expanduser().resolve()
    result = init_project(
        slug=ns.slug,
        root=projects_root,
        device=ns.device,
        template=ns.template,
        dry_run=ns.dry_run,
    )
    if result.project_path:
        print(f"Project path: {result.project_path}")
    for path in result.planned_paths:
        print(f"  {path}")
    if ns.dry_run:
        print("[dry-run] no files written")
    for err in result.errors:
        print(f"ERROR: {err}", file=sys.stderr)
    if not result.ok:
        return 1
    if not ns.dry_run:
        print(f"Initialized project {ns.slug!r} (template={ns.template})")
    return 0


def cmd_verify(ns: argparse.Namespace) -> int:
    if ns.device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        return 1

    projects_root = (ns.projects_root or default_projects_root()).expanduser().resolve()
    if ns.slug:
        results = [verify_project(projects_root, ns.slug)]
    else:
        results = verify_all(projects_root)

    if not results and ns.slug is None:
        print(f"No project directories under {projects_root}")
        return 0

    exit_code = 0
    for res in results:
        print(f"=== {res.slug} ===")
        for w in res.warnings:
            print(f"WARN: {w}")
        for e in res.errors:
            print(f"ERROR: {e}", file=sys.stderr)
            exit_code = 1
        if res.ok and not res.warnings:
            print("OK")
        elif res.ok:
            print("OK (with warnings)")
    return exit_code


def main(argv: list[str] | None = None) -> None:
    ns = parse_args(argv)
    if ns.command == "list":
        sys.exit(cmd_list(ns))
    if ns.command == "init":
        sys.exit(cmd_init(ns))
    if ns.command == "verify":
        sys.exit(cmd_verify(ns))
    print(f"unknown command: {ns.command}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR2) -->