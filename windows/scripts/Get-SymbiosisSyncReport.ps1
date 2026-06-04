<#
.SYNOPSIS
Oregon (Windows) mirror for symbiosis-sync-report (AUTON 355e3993).

Maps PascalCase flags to the canonical Python CLI (same behavior as WA symbiosis-sync-report).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Device,
    [string]$RepoRoot,
    [string]$RichRoot,
    [string]$MempalaceRoot,
    [ValidateSet("markdown", "json")]
    [string]$Format = "markdown",
    [string]$Out,
    [switch]$NoSyncthing,
    [switch]$Relay,
    [int]$HandoffRows = 3
)

$ErrorActionPreference = "Stop"

function Find-Shim {
    param([string]$Root)
    $candidates = @(
        (Join-Path $Root "cross-device\scripts\symbiosis-sync-report"),
        (Join-Path $Root "cross-device\scripts\sync_report\cli.py")
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

if ($HandoffRows -lt 1 -or $HandoffRows -gt 10) {
    Write-Error "--handoff-rows must be between 1 and 10"
    exit 1
}

$root = Resolve-RepoRoot
$shim = Find-Shim -Root $root
if (-not $shim) { Write-Error "symbiosis-sync-report shim not found under repo"; exit 1 }
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }

$cli = @(
    $shim,
    "--device", $Device,
    "--repo-root", $root,
    "--format", $Format,
    "--handoff-rows", "$HandoffRows"
)
if ($RichRoot) { $cli += @("--rich-root", $RichRoot) }
if ($MempalaceRoot) { $cli += @("--mempalace-root", $MempalaceRoot) }
if ($Out) { $cli += @("--out", $Out) }
if ($NoSyncthing) { $cli += "--no-syncthing" }
if ($Relay) { $cli += "--relay" }

& $py.Source @cli
exit $LASTEXITCODE