<#
.SYNOPSIS
Oregon (Windows) launcher for symbiosis-grok-mcp (AUTON b045169b).

Runs the FastMCP stdio server via package venv or python -m grok_mcp (same as Hermes registration).
#>
[CmdletBinding()]
param(
    [string]$RepoRoot,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

function Show-Usage {
    @"
Invoke-SymbiosisGrokMcp.ps1 — Grok Build MCP stdio (AUTON b045169b)

  .\Invoke-SymbiosisGrokMcp.ps1          Start MCP stdio server
  .\Invoke-SymbiosisGrokMcp.ps1 -Help    This message

Hermes: hermes mcp add grok --command <venv>\Scripts\python.exe --args -m grok_mcp
"@
}

if ($Help) {
    Show-Usage
    exit 0
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
$grokMcp = Join-Path $root "cross-device\grok-mcp"
if (-not (Test-Path -LiteralPath $grokMcp)) {
    Write-Error "grok-mcp package not found: $grokMcp"
    exit 1
}

$venvPy = Join-Path $grokMcp ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPy) {
    Push-Location $grokMcp
    try {
        & $venvPy -m grok_mcp
        exit $LASTEXITCODE
    } finally {
        Pop-Location
    }
}

$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) {
    Push-Location $grokMcp
    try {
        & py -3.11 -m grok_mcp
        exit $LASTEXITCODE
    } finally {
        Pop-Location
    }
}

$py3 = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py3) { $py3 = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py3) {
    Write-Error "python not found; create .venv under cross-device\grok-mcp"
    exit 127
}

Push-Location $grokMcp
try {
    & $py3.Source -m grok_mcp
    exit $LASTEXITCODE
} finally {
    Pop-Location
}

# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON b045169b PR6) -->