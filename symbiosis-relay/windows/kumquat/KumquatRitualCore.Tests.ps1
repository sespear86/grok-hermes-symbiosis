# Pester 3.x - unit tests for KumquatRitualCore.psm1 pure functions
$modulePath = Join-Path $PSScriptRoot "KumquatRitualCore.psm1"
Import-Module $modulePath -Force

Describe "Get-KumquatHealthMetrics" {
    It "parses overall_ok=false and score=50 from sample health output" {
        $healthJson = @'
=== Oregon Relay Health Complete ===
{
    "beacon_age_seconds":  235,
    "fast_hb_age_seconds":  235,
    "intent_active":  true,
    "pending_tasks":  0,
    "timestamp":  "2026-06-24T04:17:27Z",
    "overall_ok":  false
}
'@
        $structured = "PASS - structured Oregon relay status`nschema=0.3.0-structured-status score=50 beacon=239s fast=239s"
        $persist = "Persistence: CLOSED - admin-registration"
        $m = Get-KumquatHealthMetrics -HealthOutput $healthJson -StructuredOutput $structured -PersistenceOutput $persist
        $m.overall_ok | Should Be $false
        $m.score | Should Be 50
        $m.beacon_age_seconds | Should Be 235
        $m.persistence_closed | Should Be $true
        $m.structured_pass | Should Be $true
    }
}

Describe "Get-KumquatCanonicalChangedPaths" {
    It "returns relative repo paths only (no absolute paths)" {
        $paths = Get-KumquatCanonicalChangedPaths
        $paths.Count | Should BeGreaterThan 10
        ($paths -join "`n") | Should Match "KumquatRitualCore\.psm1"
        ($paths -join "`n") | Should Not Match "C:\\\\"
        ($paths -join "`n") | Should Not Match "implementer"
    }
}

Describe "Set-KumquatManifestBlock" {
    It "replaces metrics when run label already exists (symmetric overwrite)" {
        $tmp = Join-Path $env:TEMP "kumquat-test-$(Get-Random).md"
        $health1 = [PSCustomObject]@{ overall_ok = $true; score = 75; beacon_age_seconds = 39; schema = "0.3.0"; persistence_closed = $true }
        $health2 = [PSCustomObject]@{ overall_ok = $false; score = 50; beacon_age_seconds = 505; schema = "0.3.0"; persistence_closed = $true }
        $content1 = Format-KumquatOregonHB -Health $health1 -RunLabel "run-2"
        Set-KumquatManifestBlock -FilePath $tmp -BlockName "oregon-hb" -NewContent $content1 | Out-Null
        $content2 = Format-KumquatOregonHB -Health $health2 -RunLabel "run-2"
        Set-KumquatManifestBlock -FilePath $tmp -BlockName "oregon-hb" -NewContent $content2 | Out-Null
        $final = Get-Content $tmp -Raw
        $final | Should Match "overall_ok=False"
        $final | Should Match "score=50"
        $final | Should Match "beacon=505s"
        $final | Should Not Match "score=75"
        Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    }
}

Describe "Format-KumquatClosure" {
    It "emits all required style phrases with parameterized metrics" {
        $health = [PSCustomObject]@{
            overall_ok = $false
            score = 50
            beacon_age_seconds = 235
            schema = "0.3.0-structured-status"
            persistence_closed = $true
            structured_pass = $true
        }
        $closure = Format-KumquatClosure -Health $health -RunLabel "test"
        $closure | Should Match "ACTUAL_OVERALL_OK:\s*false"
        $closure | Should Match "ACTUAL_SCORE:\s*50"
        $closure | Should Match "Linux Turn Status"
        $closure | Should Match "Keep er goinnnn\. Bust a nut\."
        $closure | Should Match "Oregon has the ball"
        $closure | Should Match "Be funny, you depraved little shit"
        $closure | Should Match "Cross-Implement"
        $closure | Should Match "Mirrorability"
        $closure | Should Match "Edited:"
    }
}