"""symbiosis-new-handoff CLI (AUTON f41d2ff4)."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from . import log as log_mod
from .paths import (
    CANONICAL_FROM,
    CANONICAL_TO,
    default_repo_root,
    handoff_format_path,
    handoff_log_path,
    package_dir,
)
from .render import folder_id, render_readme, signature_boilerplate
from .validate import validate_package

SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{2,80}$")
MAX_CONTEXT = 2000
MAX_TASK = 2000


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="symbiosis-new-handoff",
        description="Create or validate symbiosis handoff packages per HANDOFF_FORMAT.md",
    )
    p.add_argument("--from", dest="from_device", required=False)
    p.add_argument("--to", dest="to_device", required=False)
    p.add_argument("--slug", required=False)
    p.add_argument("--context", default="", help="Handoff context narrative")
    p.add_argument("--task", default="", help="Task / request narrative")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-log", action="store_true")
    p.add_argument("--return-stub", action="store_true")
    p.add_argument("--validate-only", metavar="PATH")
    p.add_argument("--repo-root", type=Path, default=None)
    p.add_argument("--date", metavar="YYYY-MM-DD")
    p.add_argument("--time", metavar="HHMM")
    p.add_argument(
        "--mempalace-extra",
        action="append",
        default=[],
        help="Extra Mempalace path (repeatable)",
    )
    p.add_argument(
        "--log-status",
        default="In Progress",
        help="Status column for new LOG row",
    )
    return p.parse_args(argv)


def _device_label(from_device: str) -> str:
    return "Windows" if "Windows" in from_device else "Linux"


def cmd_validate_only(path: Path, repo_root: Path) -> int:
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"HANDOFF_FORMAT.md missing: {fmt}", file=sys.stderr)
        return 1
    res = validate_package(
        path, repo_root, log_path=handoff_log_path(repo_root)
    )
    for w in res.warnings:
        print(f"WARN: {w}")
    for e in res.errors:
        print(f"ERROR: {e}", file=sys.stderr)
    return 0 if res.ok else 1


def cmd_create(ns: argparse.Namespace) -> int:
    if not ns.from_device or not ns.to_device or not ns.slug:
        print("--from, --to, and --slug are required to create a handoff", file=sys.stderr)
        return 1
    if ns.from_device not in CANONICAL_FROM:
        print(
            f"invalid --from; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        return 1
    if ns.to_device not in CANONICAL_TO:
        print(
            f"invalid --to; use one of: {', '.join(sorted(CANONICAL_TO))}",
            file=sys.stderr,
        )
        return 1
    if not SLUG_RE.match(ns.slug):
        print("invalid --slug; must match ^[A-Za-z0-9][A-Za-z0-9-]{2,80}$", file=sys.stderr)
        return 1
    if len(ns.context) > MAX_CONTEXT or len(ns.task) > MAX_TASK:
        print("context/task exceed max length 2000", file=sys.stderr)
        return 1

    repo_root = (ns.repo_root or default_repo_root()).resolve()
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"HANDOFF_FORMAT.md missing: {fmt}", file=sys.stderr)
        return 1

    now = datetime.now()
    if ns.date:
        date_iso = ns.date
        yyyymmdd = ns.date.replace("-", "")
    else:
        date_iso = now.strftime("%Y-%m-%d")
        yyyymmdd = now.strftime("%Y%m%d")
    time_hhmm = ns.time if ns.time else now.strftime("%H%M")

    fid = folder_id(yyyymmdd, time_hhmm, ns.slug)
    dest = package_dir(repo_root, fid)
    if dest.exists():
        print(f"collision: {dest} already exists (no overwrite)", file=sys.stderr)
        return 1

    readme = render_readme(
        from_device=ns.from_device,
        to_device=ns.to_device,
        slug=ns.slug,
        date_iso=date_iso,
        time_hhmm=time_hhmm,
        context=ns.context or "TBD — fill context after scaffold.",
        task=ns.task or "TBD — fill task after scaffold.",
        mempalace_extra=ns.mempalace_extra,
        include_return_stub=ns.return_stub,
    )

    print(f"Package ID: {fid}")
    print(f"Path: {dest}")
    print(signature_boilerplate(_device_label(ns.from_device)))
    print(
        "Reminder: add Agent Context block from HANDOFF_FORMAT if delegating to Hermes sub-agents."
    )

    if ns.dry_run:
        print("[dry-run] no files written")
        return 0

    dest.mkdir(parents=True, exist_ok=False)
    (dest / "README.md").write_text(readme, encoding="utf-8")

    if not ns.no_log:
        log_p = handoff_log_path(repo_root)
        row = log_mod.build_row(
            date_display=date_iso,
            folder_id=fid,
            from_device=ns.from_device,
            to_device=ns.to_device,
            description=ns.slug.replace("-", " "),
            status=ns.log_status,
        )
        log_mod.insert_log_row(log_p, row, dry_run=False)

    print("Created handoff package. Kumquat the receiver with bing/bang/boom when you summarize.")
    return 0


def main(argv: list[str] | None = None) -> None:
    ns = parse_args(argv)
    repo_root = (ns.repo_root or default_repo_root()).resolve()

    if ns.validate_only:
        code = cmd_validate_only(Path(ns.validate_only).expanduser(), repo_root)
        sys.exit(code)

    code = cmd_create(ns)
    sys.exit(code)


if __name__ == "__main__":
    main()