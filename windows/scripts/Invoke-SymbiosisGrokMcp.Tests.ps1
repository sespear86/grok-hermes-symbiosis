# Pester smoke tests for Invoke-SymbiosisGrokMcp.ps1 (AUTON b045169b)
BeforeAll {
    $script:Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
    $script:Ps1 = Join-Path $PSScriptRoot "Invoke-SymbiosisGrokMcp.ps1"
    $script:GrokMcp = Join-Path $script:Repo "cross-device\grok-mcp"
    $script:VenvPy = Join-Path $script:GrokMcp ".venv\Scripts\python.exe"
}

Describe "Invoke-SymbiosisGrokMcp package layout" {
    It "finds grok-mcp tree under repo" {
        Test-Path -LiteralPath $script:GrokMcp | Should -BeTrue
    }

    It "grok_mcp package is importable" -Skip:( -not (Test-Path -LiteralPath $script:VenvPy) ) {
        & $script:VenvPy -c "import grok_mcp; assert grok_mcp.__version__"
        $LASTEXITCODE | Should -Be 0
    }

    It "server module exposes FastMCP name grok" -Skip:( -not (Test-Path -LiteralPath $script:VenvPy) ) {
        $out = & $script:VenvPy -c "from grok_mcp.server import mcp; print(mcp.name)"
        $LASTEXITCODE | Should -Be 0
        ($out -join "`n") | Should -Match "grok"
    }
}

Describe "Invoke-SymbiosisGrokMcp.ps1" {
    It "-Help exits zero" {
        & $script:Ps1 -Help
        $LASTEXITCODE | Should -Be 0
    }

    It "errors when grok-mcp path missing" {
        { & $script:Ps1 -RepoRoot $env:TEMP } | Should -Throw
    }
}

# <!-- Edited: 2026-06-05 | Device: Washington Linux | By: Grok (AUTON b045169b PR6) -->