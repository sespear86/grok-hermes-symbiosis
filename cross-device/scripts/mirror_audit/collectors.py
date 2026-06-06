"""Collect mirror parity signals across git, rich, grok, bin."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .checklist import CHECKLIST, ComponentSpec, LocationKind
from .paths import mirror_kits_path

_SECTION_RE = re.compile(r"^##\s+(\d+(?:\.\d+)?)\.\s+(.+)$", re.MULTILINE)


@dataclass
class PathCheck:
    rel: str
    kind: LocationKind
    exists: bool
    resolved: str


@dataclass
class ComponentReport:
    spec: ComponentSpec
    checks: list[PathCheck] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.gaps) == 0


@dataclass
class AuditModel:
    device: str
    repo_root: str
    rich_root: str
    grok_root: str
    bin_dir: str
    mirror_kits_present: bool
    mirror_sections: list[str]
    components: list[ComponentReport]
    health: dict[str, str | bool | None]

    @property
    def gap_count(self) -> int:
        return sum(len(c.gaps) for c in self.components)


def _root_for(kind: LocationKind, repo: Path, rich: Path, grok: Path, bin_dir: Path) -> Path:
    if kind == "git":
        return repo
    if kind == "rich":
        return rich
    if kind == "grok":
        return grok
    return bin_dir


def _check_paths(
    spec: ComponentSpec,
    repo: Path,
    rich: Path,
    grok: Path,
    bin_dir: Path,
) -> ComponentReport:
    report = ComponentReport(spec=spec)
    for kind, rels in spec.locations.items():
        root = _root_for(kind, repo, rich, grok, bin_dir)
        for rel in rels:
            target = (root / rel).resolve()
            exists = target.exists()
            report.checks.append(
                PathCheck(rel=rel, kind=kind, exists=exists, resolved=str(target))
            )
            if not exists:
                report.gaps.append(f"missing {kind}:{rel}")
    return report


def parse_mirror_sections(mirror_doc: Path) -> list[str]:
    if not mirror_doc.is_file():
        return []
    text = mirror_doc.read_text(encoding="utf-8", errors="replace")
    return [f"§{num} {title.strip()}" for num, title in _SECTION_RE.findall(text)]


def run_health_probes(repo_root: Path, rich_root: Path) -> dict[str, str | bool | None]:
    out: dict[str, str | bool | None] = {
        "check_primes": None,
        "relay_health": None,
        "memory_sync_shim": None,
    }
    primes = Path("~/bin/check-primes.sh").expanduser()
    if primes.is_file():
        try:
            proc = subprocess.run(
                [str(primes)],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            out["check_primes"] = proc.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            out["check_primes"] = False
    relay = rich_root / "symbiosis-relay" / "tools" / "relay-health.sh"
    if relay.is_file():
        out["relay_health"] = str(relay)
    shim = repo_root / "cross-device" / "scripts" / "symbiosis-memory-sync"
    out["memory_sync_shim"] = shim.is_file()
    return out


def collect_audit(
    *,
    device: str,
    repo_root: Path,
    rich_root: Path,
    grok_root: Path,
    bin_dir: Path,
) -> AuditModel:
    mk = mirror_kits_path(repo_root)
    sections = parse_mirror_sections(mk)
    components = [
        _check_paths(spec, repo_root, rich_root, grok_root, bin_dir) for spec in CHECKLIST
    ]
    health = run_health_probes(repo_root, rich_root)
    return AuditModel(
        device=device,
        repo_root=str(repo_root),
        rich_root=str(rich_root),
        grok_root=str(grok_root),
        bin_dir=str(bin_dir),
        mirror_kits_present=mk.is_file(),
        mirror_sections=sections,
        components=components,
        health=health,
    )