"""symbiosis-memory-sync CLI (AUTON 7eb7d1b7 / c7d73093 completion)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from memory_sync._pathbootstrap import ensure_scripts_path

ensure_scripts_path()

from handoff_scaffold.paths import CANONICAL_FROM, handoff_format_path

from memory_sync import merge, palace_io, render
from memory_sync.build import build_bundle_dict
from memory_sync.paths import (
    DEFAULT_PROJECT_SLUG,
    default_mempalace_root,
    default_palace_path,
    default_repo_root,
    validate_project_slug,
)


def _parse_global(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Symbiosis repo root (HANDOFF_FORMAT guard)",
    )
    p.add_argument(
        "--project",
        default=None,
        help=f"Project slug (default env SYMBIOSIS_MEMORY_PROJECT or {DEFAULT_PROJECT_SLUG})",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    import os

    ap = argparse.ArgumentParser(prog="symbiosis-memory-sync")
    sub = ap.add_subparsers(dest="cmd", required=True)

    bp = sub.add_parser("bundle", help="Build bundle JSON (no palace)")
    _parse_global(bp)
    bp.add_argument("--agent", choices=["grok", "hermes"], required=True)
    bp.add_argument("--device", required=True)
    bp.add_argument("--session", type=Path, default=None)
    bp.add_argument("--cwd", type=Path, default=None)
    bp.add_argument("--dry-run", action="store_true")

    pp = sub.add_parser("push", help="Push bundle to Mempalace")
    _parse_global(pp)
    pp.add_argument("--agent", choices=["grok", "hermes"], required=True)
    pp.add_argument("--device", required=True)
    pp.add_argument("--session", type=Path, default=None)
    pp.add_argument("--cwd", type=Path, default=None)
    pp.add_argument("--dry-run", action="store_true")
    pp.add_argument("--force", action="store_true")

    pl = sub.add_parser("pull", help="Pull and render inject")
    _parse_global(pl)
    pl.add_argument("--agent", choices=["grok", "hermes"], required=True)
    pl.add_argument("--device", required=True)
    pl.add_argument("--format", choices=["markdown", "json"], default="markdown")
    pl.add_argument("--out", type=Path, default=None)
    pl.add_argument("--merge", action=argparse.BooleanOptionalAction, default=True)
    pl.add_argument("--dry-run", action="store_true")

    sp = sub.add_parser("status", help="Local + brother sync status")
    _parse_global(sp)
    sp.add_argument("--device", required=True)
    sp.add_argument("--format", choices=["markdown", "json"], default="markdown")
    sp.add_argument("--no-repo", action="store_true")

    ns = ap.parse_args(argv)
    if ns.project is None:
        ns.project = os.environ.get("SYMBIOSIS_MEMORY_PROJECT", DEFAULT_PROJECT_SLUG)
    return ns


def _validate_device(device: str) -> int | None:
    if device not in CANONICAL_FROM:
        print(
            f"invalid --device; use one of: {', '.join(sorted(CANONICAL_FROM))}",
            file=sys.stderr,
        )
        return 1
    return None


def _validate_repo(repo_root: Path, *, skip: bool = False) -> int | None:
    if skip:
        return None
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        print(f"repo root invalid (HANDOFF_FORMAT.md missing): {fmt}", file=sys.stderr)
        return 2
    return None


def cmd_bundle(ns: argparse.Namespace, repo_root: Path) -> int:
    try:
        validate_project_slug(ns.project)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    try:
        b, _ = build_bundle_dict(
            agent=ns.agent,
            device=ns.device,
            project_slug=ns.project,
            repo_root=repo_root,
            cwd=ns.cwd,
            session_path=ns.session,
        )
    except ValueError:
        print("bundle oversize after truncation", file=sys.stderr)
        return 4
    print(json.dumps(b, indent=2, sort_keys=True))
    return 0


def cmd_push(ns: argparse.Namespace, repo_root: Path, palace: Path) -> int:
    try:
        validate_project_slug(ns.project)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    try:
        b, _ = build_bundle_dict(
            agent=ns.agent,
            device=ns.device,
            project_slug=ns.project,
            repo_root=repo_root,
            cwd=ns.cwd,
            session_path=ns.session,
        )
    except ValueError:
        print("bundle oversize after truncation", file=sys.stderr)
        return 4
    if ns.dry_run:
        print(json.dumps({"dry_run": True, "would_push": b}, indent=2))
        return 0
    try:
        res = palace_io.push_bundle(
            palace, b, ns.project, force=ns.force
        )
    except OSError as e:
        print(f"palace unavailable: {e}", file=sys.stderr)
        return 3
    if res.deduped:
        print("dedup_skipped")
        print(
            json.dumps(
                {
                    "deduped": True,
                    "bundle_id": res.bundle_id,
                    "content_hash": res.content_hash,
                },
                indent=2,
            )
        )
        return 0
    print(
        json.dumps(
            {
                "pushed": True,
                "bundle_id": res.bundle_id,
                "drawer": res.drawer_ref,
                "content_hash": res.content_hash,
            },
            indent=2,
        )
    )
    return 0


def cmd_pull(ns: argparse.Namespace, repo_root: Path, mem_root: Path) -> int:
    palace = default_palace_path()
    parsed = palace_io.pull_bundles(palace, ns.project, limit=100)
    if not parsed:
        print("no parseable bundles in palace", file=sys.stderr)
        return 5
    latest = merge.select_latest_per_agent(parsed)
    if ns.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "would_pull": [x.get("bundle_id") for x in latest],
                },
                indent=2,
            )
        )
        return 0
    if not ns.merge and latest:
        merged = latest[0] if len(latest) == 1 else merge.latest_for_agent(
            latest, ns.agent
        ) or latest[0]
    else:
        merged = merge.merge_bundles(latest) if len(latest) > 1 else (latest[0] if latest else {})
    if ns.format == "json":
        body = json.dumps(merged, indent=2, sort_keys=True)
    else:
        body = render.render_inject(merged, latest_for_labels=latest)
    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    return 0


def cmd_status(
    ns: argparse.Namespace, repo_root: Path, mem_root: Path
) -> int:
    from memory_sync.collectors import coordination
    from memory_sync import paths as mpaths

    warnings: list[str] = []
    palace = default_palace_path()
    pushes = palace_io.get_local_pushes(ns.project, ns.device)
    parsed = palace_io.pull_bundles(palace, ns.project, limit=100)
    latest = merge.select_latest_per_agent(parsed)
    palace_latest = [
        {
            "agent": b.get("agent"),
            "bundle_id": b.get("bundle_id"),
            "exported_at": b.get("exported_at"),
        }
        for b in latest
    ]
    pres, pw = coordination.collect_presence_staleness(ns.device, mem_root)
    warnings.extend(pw)
    brother_push, bw = palace_io.brother_last_push(
        ns.project, ns.device, palace
    )
    warnings.extend(bw)
    brother_pres = pres.get("brother") or {}
    data = {
        "project_slug": ns.project,
        "local": {"device": ns.device, "pushes": pushes},
        "palace": {"latest_drawers": palace_latest},
        "brother": {
            "source_tag": mpaths.device_to_source_tag(
                mpaths.brother_device(ns.device)
            ),
            "last_push": brother_push,
            "heartbeat_age_seconds": brother_pres.get("age_seconds"),
            "paired_hint": brother_pres.get("paired_hint"),
        },
        "warnings": warnings,
    }
    body = render.render_status(data, fmt=ns.format)
    sys.stdout.write(body)
    return 0


def main(argv: list[str] | None = None) -> int:
    ns = parse_args(argv)
    rc = _validate_device(ns.device)
    if rc is not None:
        return rc
    repo_root = (ns.repo_root or default_repo_root()).expanduser().resolve()
    skip_repo = ns.cmd == "status" and getattr(ns, "no_repo", False)
    rc = _validate_repo(repo_root, skip=skip_repo)
    if rc is not None:
        return rc
    mem_root = default_mempalace_root()
    palace = default_palace_path()

    if ns.cmd == "bundle":
        return cmd_bundle(ns, repo_root)
    if ns.cmd == "push":
        return cmd_push(ns, repo_root, palace)
    if ns.cmd == "pull":
        return cmd_pull(ns, repo_root, mem_root)
    if ns.cmd == "status":
        return cmd_status(ns, repo_root, mem_root)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


# <!-- Edited: 2026-06-06 | Device: Washington Linux | By: Grok (AUTON 9be206cf) --> -m bootstrap + pull --no-merge fix. Sig per prime. Boom.