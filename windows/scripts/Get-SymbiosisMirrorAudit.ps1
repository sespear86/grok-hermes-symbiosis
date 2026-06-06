<#
.SYNOPSIS
Oregon (Windows) mirror for symbiosis-mirror-audit (AUTON 9be206cf sym-build-04 starter).

Maps PascalCase flags to the canonical Python CLI. Full Pester suite planned (skeleton:
copy Get-SymbiosisSyncReport.Tests.ps1 pattern when sym-build-04 expands).
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Device,
    [string]$RepoRoot,
    [string]$RichRoot,
    [string]$GrokRoot,
    [string]$BinDir,
    [ValidateSet("markdown", "json")]
    [string]$Format = "markdown",
    [string]$Out,
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

function Find-Shim {
    param([string]$Root)
    $c = Join-Path $Root "cross-device\scripts\symbiosis-mirror-audit"
    if (Test-Path -LiteralPath $c) { return $c }
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

$root = Resolve-RepoRoot
$shim = Find-Shim -Root $root
if (-not $shim) { Write-Error "symbiosis-mirror-audit shim not found under repo"; exit 1 }
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 1 }

$cli = @($shim, "--device", $Device, "--repo-root", $root, "--format", $Format)
if ($RichRoot) { $cli += @("--rich-root", $RichRoot) }
if ($GrokRoot) { $cli += @("--grok-root", $GrokRoot) }
if ($BinDir) { $cli += @("--bin-dir", $BinDir) }
if ($Out) { $cli += @("--out", $Out) }
if ($Strict) { $cli += "--strict" }

& $py.Source @cli
exit $LASTEXITCODE