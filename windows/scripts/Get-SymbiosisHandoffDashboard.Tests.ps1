# Pester tests for Get-SymbiosisHandoffDashboard.ps1 (AUTON 3694a72b)
BeforeAll {
    $script:Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
    $script:Ps1 = Join-Path $PSScriptRoot "Get-SymbiosisHandoffDashboard.ps1"
    $script:Launcher = Join-Path $PSScriptRoot "start-handoff-dashboard.ps1"
    $script:Shim = Join-Path $script:Repo "cross-device\scripts\symbiosis-handoff-dashboard"
}

Describe "Get-SymbiosisHandoffDashboard parameter validation" {
    It "requires Device" {
        { & $script:Ps1 -RepoRoot $script:Repo -CheckOnly } | Should -Throw
    }

    It "rejects CompletedLimit out of range before invoking python" {
        { & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -CompletedLimit 0 -CheckOnly } | Should -Throw
        { & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -CompletedLimit 51 -CheckOnly } | Should -Throw
    }

    It "launcher script exists beside Get-" {
        Test-Path -LiteralPath $script:Launcher | Should -BeTrue
    }
}

Describe "Get-SymbiosisHandoffDashboard flag mapping" -Skip:( -not (Get-Command python3 -ErrorAction SilentlyContinue) ) {
    BeforeAll {
        $env:SYMBIOSIS_REPO_ROOT = $script:Repo
    }

    It "maps -CheckOnly to python CLI with success exit" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -CheckOnly -NoPresence
        $LASTEXITCODE | Should -Be 0
    }

    It "maps -BindAddress to --host on CLI" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -BindAddress "127.0.0.1" -CheckOnly -NoPresence
        $LASTEXITCODE | Should -Be 0
    }

    It "maps -NoPresence to python CLI" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Washington Linux" -NoPresence -CheckOnly
        $LASTEXITCODE | Should -Be 0
    }

    It "invalid Device returns non-zero (same as shim)" {
        & $script:Ps1 -RepoRoot $script:Repo -Device "Mars" -CheckOnly -NoPresence
        $LASTEXITCODE | Should -Be 1
    }

    It "delegates through symbiosis-handoff-dashboard shim path" {
        Test-Path -LiteralPath $script:Shim | Should -BeTrue
    }

    It "invalid repo returns exit 2 with -CheckOnly" {
        $bad = Join-Path $TestDrive "no-format-repo"
        New-Item -ItemType Directory -Path $bad -Force | Out-Null
        & $script:Ps1 -RepoRoot $bad -Device "Washington Linux" -CheckOnly -NoPresence
        $LASTEXITCODE | Should -Be 2
    }
}

Describe "Get-SymbiosisHandoffDashboard syntax" {
    It "parses without runtime errors (AST)" {
        $errors = $null
        $null = [System.Management.Automation.Language.Parser]::ParseFile(
            $script:Ps1, [ref]$null, [ref]$errors
        )
        $errors | Should -BeNullOrEmpty
    }

    It "launcher parses without AST errors" {
        $errors = $null
        $null = [System.Management.Automation.Language.Parser]::ParseFile(
            $script:Launcher, [ref]$null, [ref]$errors
        )
        $errors | Should -BeNullOrEmpty
    }
}

# <!-- Edited: 2026-06-04 | Device: Washington Linux | By: Grok (AUTON 3694a72b implementer batch3) -->