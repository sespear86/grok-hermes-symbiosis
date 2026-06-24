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

Describe "Archive-KumquatOregonTail" {
    It "removes stale duplicate HB content below manifest block" {
        $repo = Join-Path $env:TEMP "kumquat-repo-$(Get-Random)"
        $oregonDir = Join-Path $repo "Mempalace\symbiosis\device-presence"
        New-Item -ItemType Directory -Path $oregonDir -Force | Out-Null
        $oregonPath = Join-Path $oregonDir "oregon.md"
        $m = Get-KumquatManifestBlockMarkers -BlockName "oregon-hb"
        $stale = "# Oregon (Windows) Heartbeat`n**Status:** overall_ok=True score=75`n"
        Set-Content -Path $oregonPath -Value ($m.Start + "`nhb`n" + $m.End + "`n`n" + $stale) -Encoding utf8
        Archive-KumquatOregonTail -RepoRoot $repo | Out-Null
        $final = Get-Content $oregonPath -Raw
        $final | Should Not Match "score=75"
        $final.TrimEnd() | Should Match ([regex]::Escape($m.End))
        Remove-Item $repo -Recurse -Force -ErrorAction SilentlyContinue
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

Describe "Sync-KumquatVerifierInputs" {
    It "overwrites attempt-indexed patch with authoritative repo diff header" {
        $goalId = "testid123abc"
        $goalRoot = Join-Path $env:TEMP "grok-goal-$goalId"
        $impl = Join-Path $goalRoot "implementer"
        New-Item -ItemType Directory -Path $impl -Force | Out-Null
        $stalePatch = Join-Path $goalRoot "goal-classifier-$goalId-3.patch"
        Set-Content -Path $stalePatch -Value "STALE_JUNK agent-tools" -Encoding utf8
        $authPatch = Join-Path $impl "kumquat-git-diff.patch"
        Set-Content -Path $authPatch -Value "# Kumquat git diff anchor`nAUTHORITATIVE KumquatRitualCore.psm1 diff" -Encoding utf8
        $relative = Get-KumquatCanonicalRelativePaths
        $result = Sync-KumquatVerifierInputs -GoalRoot $goalRoot -GoalId $goalId -Attempt 3 `
            -PatchPath $authPatch -RelativePaths $relative -ScratchDir $impl
        (Get-Content $stalePatch -TotalCount 1) | Should Match "# Kumquat git diff anchor"
        (Get-Content $stalePatch -Raw) | Should Not Match "STALE_JUNK"
        $result.patch_ok | Should Be $true
        Test-Path (Join-Path $goalRoot "goal-classifier-$goalId-3-CHANGED_FILES.txt") | Should Be $true
        Remove-Item $goalRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Describe "Copy-KumquatDeliverableStubs" {
    It "copies canonical repo files into session goal deliverables" {
        $repo = "C:\Users\spear\grok-hermes-symbiosis"
        $session = Join-Path $env:TEMP "kumquat-session-$(Get-Random)"
        $relative = Get-KumquatCanonicalRelativePaths
        $result = Copy-KumquatDeliverableStubs -RepoRoot $repo -SessionDir $session -RelativePaths $relative
        $result.copied | Should Be $relative.Count
        Test-Path (Join-Path $session "goal\deliverables\symbiosis-relay\windows\kumquat\KumquatRitualCore.psm1") | Should Be $true
        Remove-Item $session -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Describe "Write-KumquatEvidenceVerification" {
    It "writes evidence index with mirror match count and CHANGED_FILES_ANCHOR note" {
        $repo = "C:\Users\spear\grok-hermes-symbiosis"
        $scratch = Join-Path $env:TEMP "kumquat-ev-test-$(Get-Random)"
        New-Item -ItemType Directory -Path $scratch -Force | Out-Null
        $relative = Get-KumquatCanonicalRelativePaths
        $relative | Set-Content -Path (Join-Path $scratch "CHANGED_FILES_ANCHOR.txt") -Encoding utf8
        $evidenceDir = Join-Path $scratch "evidence"
        foreach ($rel in $relative) {
            $src = Join-Path $repo ($rel -replace '/', '\')
            if (-not (Test-Path $src)) { continue }
            $dst = Join-Path $evidenceDir ($rel -replace '/', '\')
            $dstDir = Split-Path $dst -Parent
            if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
            Copy-Item $src $dst -Force
        }
        $result = Write-KumquatEvidenceVerification -RepoRoot $repo -ScratchDir $scratch -RelativePaths $relative
        $index = Get-Content (Join-Path $scratch "kumquat-evidence-index.txt") -Raw
        $index | Should Match "CHANGED_FILES_ANCHOR"
        $index | Should Match "evidence_mirror_match: $($relative.Count)/$($relative.Count)"
        $index | Should Match "KumquatRitualCore\.psm1_in_evidence: YES"
        $result.mirror_ok | Should Be $relative.Count
        Remove-Item $scratch -Recurse -Force -ErrorAction SilentlyContinue
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