# Pester smoke tests for Get-SymbiosisSyncReport.ps1 (AUTON 355e3993)
BeforeAll {
    $script:Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
    $script:Ps1 = Join-Path $PSScriptRoot "Get-SymbiosisSyncReport.ps1"
    $script:Shim = Join-Path $script:Repo "cross-device\scripts\symbiosis-sync-report"
}

Describe "Get-SymbiosisSyncReport parameter validation" {
    It "requires Device" {
        { & $script:Ps1 -RepoRoot $script:Repo -NoSyncthing } | Should -Throw
    }

    It "rejects HandoffRows out of range before invoking python" {
        { & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -HandoffRows 0 -NoSyncthing } | Should -Throw
        { & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -HandoffRows 11 -NoSyncthing } | Should -Throw
    }
}

Describe "Get-SymbiosisSyncReport flag mapping" -Skip:( -not (Get-Command python3 -ErrorAction SilentlyContinue) ) {
    It "maps -NoSyncthing to python CLI (dry invoke) with success exit" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -NoSyncthing
        $LASTEXITCODE | Should -Be 0
    }

    It "maps -Format json to python CLI" {
        $out = & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -NoSyncthing -Format json 2>&1
        $LASTEXITCODE | Should -Be 0
        ($out -join "`n") | Should -Match '"syncthing"'
        ($out -join "`n") | Should -Match '"available"\s*:\s*false'
    }

    It "invalid Device returns non-zero (same as shim)" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Mars" -NoSyncthing
        $LASTEXITCODE | Should -Be 1
    }

    It "delegates through symbiosis-sync-report shim path" {
        Test-Path -LiteralPath $script:Shim | Should -BeTrue
    }
}