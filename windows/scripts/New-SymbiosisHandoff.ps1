<#
.SYNOPSIS
Oregon (Windows) mirror for symbiosis-handoff-scaffold (AUTON f41d2ff4).

Maps PascalCase flags to the canonical Python CLI (same behavior as WA symbiosis-new-handoff).
#>
[CmdletBinding()]
param(
    [string]$From = "Washington Linux",
    [string]$To = "Oregon Windows",
    [Parameter(Mandatory = $false)]
    [string]$Slug,
    [string]$Context = "",
    [string]$Task = "",
    [switch]$DryRun,
    [switch]$NoLog,
    [switch]$ReturnStub,
    [string]$ValidateOnly,
    [string]$RepoRoot,
    [string]$Date,
    [string]$Time,
    [string[]]$MempalaceExtra = @(),
    [switch]$Crlf
)

$ErrorActionPreference = "Stop"

function Find-Shim {
    param([string]$Root)
    $candidates = @(
        (Join-Path $Root "cross-device\scripts\symbiosis-new-handoff"),
        (Join-Path $Root "cross-device\scripts\handoff_scaffold\handoff_scaffold\cli.py")
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

if ($ValidateOnly) {
    $root = Resolve-RepoRoot
    $shim = Find-Shim -Root $root
    if (-not $shim) { Write-Error "symbiosis-new-handoff shim not found under repo"; exit 1 }
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
    if (-not $py) { Write-Error "python not found for validate-only"; exit 1 }
    $args = @($shim, "--validate-only", $ValidateOnly, "--repo-root", $root)
    & $py.Source @args
    exit $LASTEXITCODE
}

if (-not $Slug) {
    Write-Host "Usage: .\New-SymbiosisHandoff.ps1 -Slug 'My-Handoff' [-DryRun] [-From ...] [-To ...]"
    exit 1
}

$root = Resolve-RepoRoot
$shim = Find-Shim -Root $root
if (-not $shim) { Write-Error "symbiosis-new-handoff shim not found"; exit 1 }
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }

$cli = @(
    $shim,
    "--from", $From,
    "--to", $To,
    "--slug", $Slug,
    "--repo-root", $root
)
if ($Context) { $cli += @("--context", $Context) }
if ($Task) { $cli += @("--task", $Task) }
if ($DryRun) { $cli += "--dry-run" }
if ($NoLog) { $cli += "--no-log" }
if ($ReturnStub) { $cli += "--return-stub" }
if ($Date) { $cli += @("--date", $Date) }
if ($Time) { $cli += @("--time", $Time) }
foreach ($m in $MempalaceExtra) { $cli += @("--mempalace-extra", $m) }

& $py.Source @cli
if ($Crlf) { Write-Host "(Note: README uses LF; re-normalize with git if needed on Windows.)" }
exit $LASTEXITCODE