<#
.SYNOPSIS
Oregon (Windows) mirror for symbiosis-handoff-dashboard (AUTON 3694a72b).

Maps PascalCase flags to the canonical Python CLI (same behavior as WA shim).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Device,
    [string]$RepoRoot,
    [string]$MempalaceRoot,
    [int]$Port = 8766,
    [string]$BindAddress = "127.0.0.1",
    [switch]$Open,
    [switch]$NoPresence,
    [int]$CompletedLimit = 5,
    [switch]$CheckOnly,
    [switch]$AllowLan
)

$ErrorActionPreference = "Stop"

function Find-DashboardShim {
    param([string]$Root)
    $candidates = @(
        (Join-Path $Root "cross-device\scripts\symbiosis-handoff-dashboard"),
        (Join-Path $Root "cross-device\scripts\handoff_dashboard\cli.py")
    )
    foreach ($c in $candidates) {
        if (Test-Path -LiteralPath $c) { return $c }
    }
    return $null
}

function Resolve-RepoRoot {
    if ($RepoRoot) { return (Resolve-Path $RepoRoot).Path }
    $here = Split-Path -Parent $MyInvocation.MyCommand.Path
    $guess = Resolve-Path (Join-Path $here "..\..") -ErrorAction SilentlyContinue
    if ($guess) { return $guess.Path }
    if ($env:SYMBIOSIS_REPO_ROOT) { return $env:SYMBIOSIS_REPO_ROOT }
    throw "Cannot resolve repo root; pass -RepoRoot or set SYMBIOSIS_REPO_ROOT"
}

if ($CompletedLimit -lt 1 -or $CompletedLimit -gt 50) {
    Write-Error "CompletedLimit must be between 1 and 50"
    exit 1
}

$root = Resolve-RepoRoot
$shim = Find-DashboardShim -Root $root
if (-not $shim) { Write-Error "symbiosis-handoff-dashboard shim not found under repo"; exit 1 }
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }

$cli = @(
    $shim,
    "--device", $Device,
    "--repo-root", $root,
    "--port", "$Port",
    "--host", $BindAddress,
    "--completed-limit", "$CompletedLimit"
)
if ($MempalaceRoot) { $cli += @("--mempalace-root", $MempalaceRoot) }
if ($NoPresence) { $cli += "--no-presence" }
if ($Open) { $cli += "--open" }
if ($CheckOnly) { $cli += "--check-only" }
if ($AllowLan) { $cli += "--allow-lan" }

& $py.Source @cli
exit $LASTEXITCODE

# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch3) -->