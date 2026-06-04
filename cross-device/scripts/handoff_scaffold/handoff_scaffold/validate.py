"""Handoff package validation (--validate-only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .paths import assert_under_handoffs, handoff_format_path
from .render import REQUIRED_FORMAT_H2, parse_required_h2_from_format

FOLDER_RE = re.compile(r"^\d{8}-\d{4}-[A-Za-z0-9][A-Za-z0-9-]+$")
ID_LINE_RE = re.compile(r"^\*\*ID:\*\*\s*(.+)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
MEM_BULLET_RE = re.compile(r"^-\s+`.+`", re.MULTILINE)


@dataclass
class ValidationResult:
    ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.ok = False
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def required_sections_from_repo(repo_root: Path) -> list[str]:
    fmt = handoff_format_path(repo_root)
    if not fmt.is_file():
        return list(REQUIRED_FORMAT_H2)
    return parse_required_h2_from_format(fmt.read_text(encoding="utf-8"))


def validate_package(
    package_path: Path,
    repo_root: Path,
    *,
    log_path: Path | None = None,
) -> ValidationResult:
    res = ValidationResult()
    try:
        pkg = assert_under_handoffs(package_path, repo_root)
    except ValueError as e:
        res.fail(str(e))
        return res

    if ".sync-conflict" in str(pkg):
        res.warn("path contains .sync-conflict — resolve Syncthing conflict")

    name = pkg.name
    if not FOLDER_RE.match(name):
        res.fail(f"folder name must match YYYYMMDD-HHMM-Slug: {name}")

    readme = pkg / "README.md"
    if not readme.is_file():
        res.fail("README.md missing")
        return res

    text = readme.read_text(encoding="utf-8")
    m = ID_LINE_RE.search(text)
    if not m:
        res.fail("README missing **ID:** line")
    elif m.group(1).strip() != name:
        res.fail(f"**ID:** {m.group(1).strip()} does not match folder {name}")

    found_h2 = {h.strip() for h in H2_RE.findall(text)}
    for sec in required_sections_from_repo(repo_root):
        if sec not in found_h2:
            res.fail(f"missing required section: ## {sec}")

    mem_section = re.search(
        r"## Relevant Memory \(Mempalace\)(.*?)(?:\n## |\Z)",
        text,
        re.DOTALL,
    )
    if mem_section:
        bullets = MEM_BULLET_RE.findall(mem_section.group(1))
        if len(bullets) < 6:
            res.fail(
                f"Mempalace section needs ≥6 bullet paths; found {len(bullets)}"
            )
    else:
        res.fail("## Relevant Memory (Mempalace) section not found")

    if log_path and log_path.is_file():
        if name not in log_path.read_text(encoding="utf-8"):
            res.warn(f"HANDOFF_LOG has no row for {name}")

    return res


def validate_format_drift(repo_root: Path, template_h2: list[str]) -> ValidationResult:
    res = ValidationResult()
    live = required_sections_from_repo(repo_root)
    missing_in_template = [s for s in live if s not in template_h2]
    extra_in_template = [s for s in template_h2 if s not in live]
    if missing_in_template:
        res.fail(f"template missing FORMAT sections: {missing_in_template}")
    if extra_in_template:
        res.warn(f"template has extra sections vs FORMAT: {extra_in_template}")
    return res