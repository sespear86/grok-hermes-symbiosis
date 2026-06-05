"""Initialize joint project directories under projects root (AUTON 61cdeb81 PR2)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .paths import (
    assert_under_projects_root,
    project_dir,
    validate_slug,
)

AUTON_ID = "61cdeb81"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
MANIFEST_NAME = ".symbiosis-project.json"
VALID_TEMPLATES = frozenset({"minimal", "app"})


@dataclass
class InitResult:
    ok: bool = True
    slug: str = ""
    project_path: Path | None = None
    planned_paths: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.ok = False
        self.errors.append(msg)


def _template_path(name: str) -> Path:
    return TEMPLATES_DIR / name


def _load_stignore() -> str:
    return _template_path("stignore.txt").read_text(encoding="utf-8")


def _render_readme(
    *,
    slug: str,
    device: str,
    template: str,
    created_utc: str,
) -> str:
    tmpl = _template_path("README.md.tmpl").read_text(encoding="utf-8")
    body = tmpl.format(
        slug=slug,
        created_by_device=device,
        template=template,
        created_utc=created_utc,
    )
    if template == "app":
        body += "\n## Suggested layout\n\n- `src/` — application source\n"
    return body


def _manifest_payload(
    *,
    slug: str,
    device: str,
    template: str,
    created_utc: str,
) -> dict[str, str]:
    return {
        "slug": slug,
        "created_utc": created_utc,
        "created_by_device": device,
        "auton_id": AUTON_ID,
        "template": template,
    }


def init_project(
    *,
    slug: str,
    root: Path,
    device: str,
    template: str = "minimal",
    dry_run: bool = False,
) -> InitResult:
    res = InitResult(slug=slug)
    try:
        validate_slug(slug)
    except ValueError as exc:
        res.fail(str(exc))
        return res

    if template not in VALID_TEMPLATES:
        res.fail(f"invalid template {template!r}; use minimal or app")
        return res

    projects_root = root.expanduser().resolve()
    try:
        target = project_dir(projects_root, slug)
        assert_under_projects_root(target, projects_root)
    except ValueError as exc:
        res.fail(str(exc))
        return res

    res.project_path = target
    created_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    rel_paths = [
        "README.md",
        ".stignore",
        MANIFEST_NAME,
    ]
    if template == "app":
        rel_paths.append("src/.gitkeep")

    res.planned_paths = [str(target / p) for p in rel_paths]

    if target.exists():
        res.fail(f"project directory already exists: {target}")
        return res

    if dry_run:
        return res

    if not projects_root.is_dir():
        projects_root.mkdir(parents=True, exist_ok=True)
        assert_under_projects_root(projects_root, projects_root)

    target.mkdir(parents=False, exist_ok=False)
    assert_under_projects_root(target, projects_root)

    (target / "README.md").write_text(
        _render_readme(
            slug=slug,
            device=device,
            template=template,
            created_utc=created_utc,
        ),
        encoding="utf-8",
    )
    (target / ".stignore").write_text(_load_stignore(), encoding="utf-8")
    (target / MANIFEST_NAME).write_text(
        json.dumps(
            _manifest_payload(
                slug=slug,
                device=device,
                template=template,
                created_utc=created_utc,
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if template == "app":
        src = target / "src"
        src.mkdir(parents=False, exist_ok=False)
        assert_under_projects_root(src, projects_root)
        (src / ".gitkeep").write_text("", encoding="utf-8")

    return res


# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON 61cdeb81 PR2) -->