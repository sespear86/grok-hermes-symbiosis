<#
.SYNOPSIS
    Grok-Hermes Symbiosis Delegate (Windows PowerShell)
    Hands rich context from a Grok Build session to Hermes, with cross-device awareness.
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Task,

    [string]$Extra = "",

    [switch]$OneShot
)

$Cwd = Get-Location
$GitBranch = (git branch --show-current 2>$null) ?? "no-git"
$GitStatus = (git status --short 2>$null | Select-Object -First 8) ?? @("no-git-or-clean")

$CrossDeviceNote = @"
[CROSS-DEVICE / OREGON COLLAB]
This task may involve handoff to or from the Linux machine in Oregon.
Mark progress clearly in the shared chat (Discord/Telegram/etc.).
Use the shared grok-hermes-symbiosis repo for skills/scripts.
Prefer Hermes gateway in the joint channel for notifications and coordination.
"@

$Prompt = @"
SYMBIOSIS DELEGATION from Grok Build (Windows 11) to Hermes Agent.

Working directory: $Cwd
Git branch: $GitBranch
Git status (truncated):
$GitStatus

Task / Goal:
$Task

Additional context:
$Extra

$CrossDeviceNote

Instructions:
- Execute using Hermes full capabilities (skills, tools, memory, kanban, gateway).
- If heavy architecture, multi-reviewer coding, professional docs, verification, or best-of-n exploration is needed, escalate back using the 'grok-build' skill.
- For cross-device work with Oregon/Linux: keep the shared chat updated and reference the symbiosis repo.
- Report session ID or key outcomes.

Begin.
"@

Write-Host ">>> [Symbiosis] Launching Hermes with cross-device context from Windows Grok..." -ForegroundColor Cyan
Write-Host ">>> Task: $Task" -ForegroundColor Gray

if ($OneShot) {
    hermes -z $Prompt --skills grok-build,github,devops
} else {
    hermes --skills grok-build,github,devops -z $Prompt
}
