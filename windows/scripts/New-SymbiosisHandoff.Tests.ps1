# Pester smoke tests for New-SymbiosisHandoff.ps1 (AUTON f41d2ff4)
BeforeAll {
    $script:Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
    $script:Ps1 = Join-Path $PSScriptRoot "New-SymbiosisHandoff.ps1"
}

Describe "New-SymbiosisHandoff" {
    It "requires Slug when not validating" {
        { & $script:Ps1 -RepoRoot $script:Repo } | Should -Throw
    }

    It "DryRun maps to python CLI without error" -Skip:( -not (Get-Command python3 -ErrorAction SilentlyContinue) ) {
        & $script:Ps1 -RepoRoot $script:Repo -Slug "PS-Parity-Test" -DryRun -Context "bing" -Task "bang"
        $LASTEXITCODE | Should -Be 0
    }

    It "ValidateOnly returns non-zero for legacy incomplete package" -Skip:( -not (Get-Command python3 -ErrorAction SilentlyContinue) ) {
        $legacy = Join-Path $script:Repo "cross-device\handoffs\20260527-0200-Mempalace-Usage-Formalization"
        & $script:Ps1 -RepoRoot $script:Repo -ValidateOnly $legacy
        $LASTEXITCODE | Should -Not -Be 0
    }
}