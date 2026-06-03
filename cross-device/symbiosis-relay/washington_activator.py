#!/usr/bin/env python3
"""
Washington (Linux) Grok Build Activator / Listener

Thin CLI: delegates to activator_core (PR1, AUTON 19557e65).
Run persistently via systemd or use --once / --health for operations.

19557e65 + oregon-support: --device flag (or SYMBIOSIS_DEVICE env) sets the device for paths
(default "washington"). Oregon receiver sets env=oregon then invokes this same script
(name kept for zero friction on shared nervous source).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import activator_core as core


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Washington Symbiosis Relay activator (19557e65 + oregon-support via --device)")
    p.add_argument("--once", action="store_true", help="Process inbox once and exit")
    p.add_argument("--health", action="store_true", help="Run health check and exit")
    p.add_argument("--status", action="store_true", help="Print status.json and exit")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and claim flow without hermes/inject",
    )
    p.add_argument(
        "--device",
        default=None,
        help="Device name (default from SYMBIOSIS_DEVICE env or 'washington'). Sets env before core import for path generalization.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.device:
        os.environ["SYMBIOSIS_DEVICE"] = args.device
    core.configure_logging()
    core.ensure_directories()

    if args.health:
        report = core.health_check()
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1

    if args.status:
        print(json.dumps(core.read_status(), indent=2))
        return 0

    if args.once:
        core.run_once(dry_run=args.dry_run)
        return 0

    core.run_loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())