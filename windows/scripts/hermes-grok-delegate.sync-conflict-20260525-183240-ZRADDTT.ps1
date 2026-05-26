<#
.SYNOPSIS
    Hermes to Grok Build Delegate (Windows)
    Escalate specialist SE, design, verification, or professional doc work from Hermes to Grok Build.
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Task,

    [string]$Extra = ""
)

$Cwd = Get-Location
$GitInfo = (git branch --show-current 2>$null; git status --short 2>$null | Select-Object -First 5) ?? "no-git"

$Prompt = @"
SYMBIOSIS ESCALATION from Hermes Agent (Windows) to Grok Build TUI (xAI grok-4.3 SE specialist).

Working directory: $Cwd
Git context:
$GitInfo

Task for Grok specialist:
$Task

Additional context:
$Extra

[CROSS-DEVICE / OREGON COLLAB]
This may be part of joint work with the Linux machine.
Coordinate status via the shared chat + Hermes gateway.

Recommended Grok workflows:
- implement (with reviewers) for coding
- design for architecture
- check for verification
- best-of-n for exploration
- pptx/xlsx/docx for polished output
- plan mode for ambiguity

After completion, provide clear summary + file paths. Hand long-running or gateway delivery work back to Hermes.

Begin using the most appropriate Grok capability.
"@

Write-Host ">>> [Symbiosis] Delegating to Grok Build from Hermes (Windows)..." -ForegroundColor Cyan
grok -z $Prompt
