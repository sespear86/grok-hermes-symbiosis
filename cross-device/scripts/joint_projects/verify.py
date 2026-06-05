"""Verify joint project directories (AUTON 61cdeb81 PR2)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .collectors import MANIFEST_NAME
from .paths import assert_under_projects_root, project_dir, validate_slug

AGENT_DIR_NAMES = frozenset({".grok", ".hermes"})


@dataclass
class VerifyResult:
    slug: str
    ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.ok = False
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def _list_project_slugs(projects_root: Path) -> list[str]:
    if not projects_root.is_dir():
        return []
    slugs: list[str] = []
    for child in sorted(projects_root.iterdir(), key=lambda p: p.name.casefold()):
        if child.is_dir() and not child.name.startswith("."):
            slugs.append(child.name)
    return slugs


def _find_agent_home_warnings(project_path: Path) -> list[str]:
    warnings: list[str] = []
    if not project_path.is_dir():
        return warnings
    for path in project_path.rglob("*"):
        if path.name in AGENT_DIR_NAMES and path.is_dir():
            warnings.append(f"agent home directory present: {path}")
    return warnings


def verify_project(root: Path, slug: str) -> VerifyResult:
    res = VerifyResult(slug=slug)
    projects_root = root.expanduser().resolve()

    try:
        validate_slug(slug)
        project_path = project_dir(projects_root, slug)
        assert_under_projects_root(project_path, projects_root)
    except ValueError as exc:
        res.fail(str(exc))
        return res

    if not project_path.is_dir():
        res.fail(f"project directory missing: {project_path}")
        return res

    if not (project_path / "README.md").is_file():
        res.fail("README.md missing")
    if not (project_path / ".stignore").is_file():
        res.fail(".stignore missing")

    manifest_path = project_path / MANIFEST_NAME
    if not manifest_path.is_file():
        res.warn(f"{MANIFEST_NAME} missing (legacy directory)")
    else:
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            res.warn(f"{MANIFEST_NAME} is not valid JSON")
        else:
            if not isinstance(data, dict):
                res.warn(f"{MANIFEST_NAME} must be a JSON object")
            elif data.get("slug") != slug:
                res.warn(
                    f"{MANIFEST_NAME} slug mismatch: "
                    f"expected {slug!r}, got {data.get('slug')!r}"
                )

    if (project_path / ".git").exists():
        res.warn(".git/ present at project root (ensure Syncthing ignores it)")

    for msg in _find_agent_home_warnings(project_path):
        res.warn(msg)

    return res


def verify_all(root: Path) -> list[VerifyResult]:
    projects_root = root.expanduser().resolve()
    return [verify_project(projects_root, slug) for slug in _list_project_slugs(projects_root)]


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR2) -->