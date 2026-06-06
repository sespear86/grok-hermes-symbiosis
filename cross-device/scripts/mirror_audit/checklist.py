"""Expected symbiosis components vs MIRROR_KITS (starter inventory)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

LocationKind = Literal["git", "rich", "grok", "bin"]


@dataclass(frozen=True)
class ComponentSpec:
    component_id: str
    title: str
    mirror_section: str
    locations: dict[LocationKind, list[str]] = field(default_factory=dict)
    provision_hint: str = ""


# Paths are relative to each root (git repo, rich, ~/.grok, ~/bin).
CHECKLIST: tuple[ComponentSpec, ...] = (
    ComponentSpec(
        "symbiosis-sync-report",
        "Sync report emitter",
        "§11",
        {
            "git": ["cross-device/scripts/symbiosis-sync-report", "cross-device/scripts/sync_report"],
            "rich": ["symbiosis-relay/scripts/symbiosis-sync-report"],
            "bin": ["symbiosis-sync-report"],
        },
        "ln -sf ~/grok-hermes-symbiosis/cross-device/scripts/symbiosis-sync-report ~/bin/",
    ),
    ComponentSpec(
        "symbiosis-kanban",
        "Handoff kanban",
        "§13",
        {
            "git": ["cross-device/scripts/symbiosis-kanban", "cross-device/scripts/kanban"],
            "rich": ["symbiosis-relay/scripts/symbiosis-kanban"],
            "bin": ["symbiosis-kanban"],
        },
        "cp -a cross-device/scripts to rich; ln -sf shim to ~/bin",
    ),
    ComponentSpec(
        "symbiosis-memory-sync",
        "Bidirectional memory sync",
        "§17",
        {
            "git": ["cross-device/scripts/symbiosis-memory-sync", "cross-device/scripts/memory_sync"],
            "rich": ["symbiosis-relay/scripts/memory_sync"],
            "bin": ["symbiosis-memory-sync"],
        },
        "cp -a memory_sync to rich; see PRODUCTION_READY 7eb7d1b7/9be206cf",
    ),
    ComponentSpec(
        "symbiosis-mirror-audit",
        "Mirror parity audit (this tool)",
        "§20",
        {
            "git": ["cross-device/scripts/symbiosis-mirror-audit", "cross-device/scripts/mirror_audit"],
            "rich": ["symbiosis-relay/scripts/symbiosis-mirror-audit"],
            "bin": ["symbiosis-mirror-audit"],
        },
        "pytest -k mirror_audit; rich cp scripts subtree",
    ),
    ComponentSpec(
        "toolbox-docker-gateway",
        "Docker MCP gateway wrapper",
        "§19",
        {
            "grok": [
                "toolbox/scripts/run-mcp-docker-gateway.sh",
                "toolbox/registry/toolbox-registry.json",
            ],
        },
        "~/.grok/toolbox/scripts/run-mcp-docker-gateway.sh recipe; install Docker on OR",
    ),
    ComponentSpec(
        "toolbox-mcp-wrappers",
        "Docker catalog MCP wrappers",
        "§19",
        {
            "grok": [
                "toolbox/scripts/run-mcp-docker-docs.sh",
                "toolbox/scripts/run-mcp-fetch.sh",
                "toolbox/scripts/run-mcp-playwright.sh",
            ],
        },
        "Mirror ~/.grok/toolbox via Kumquat; re-vet with vet-tool.sh",
    ),
    ComponentSpec(
        "auton-gate-shim",
        "Production readiness gate shim",
        "§18",
        {"bin": ["auton-gate"]},
        "pip install -e ~/auton-gate; ln -sf ~/.local/bin/auton-gate ~/bin/",
    ),
    ComponentSpec(
        "mirror-kits-doc",
        "Master mirror inventory",
        "§5",
        {
            "git": ["cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md"],
        },
        "git pull grok-hermes-symbiosis; keep Syncthing coordination in sync",
    ),
    ComponentSpec(
        "handoff-dashboard",
        "Handoff dashboard",
        "§1.5",
        {
            "git": [
                "cross-device/scripts/symbiosis-handoff-dashboard",
                "cross-device/scripts/handoff_dashboard",
            ],
            "bin": ["symbiosis-handoff-dashboard", "symbiosis-dashboard"],
        },
        "rich tools/multi-device-dashboard when present; see MIRROR §1.5",
    ),
)