# Pester 3.x - thin smoke test for shipped capture wrapper (core logic tested in KumquatRitualCore.Tests.ps1)
Describe "Invoke-KumquatRitualCapture (smoke)" {
    $CaptureScript = Join-Path $PSScriptRoot "Invoke-KumquatRitualCapture.ps1"
    $ScratchLog = Join-Path $env:TEMP "kumquat-smoke.log"
    $Manifest = Join-Path $env:TEMP "kumquat-smoke-manifest.json"

    It "runs shipped wrapper and writes manifest with ACTUAL_* metrics" {
        if (Test-Path $ScratchLog) { Remove-Item $ScratchLog -Force }
        if (Test-Path $Manifest) { Remove-Item $Manifest -Force }
        & powershell -ExecutionPolicy Bypass -File $CaptureScript -RunLabel "smoke" -LogPath $ScratchLog -ManifestPath $Manifest -ScratchDir $env:TEMP
        $LASTEXITCODE | Should Be 0
        Test-Path $Manifest | Should Be $true
        $log = Get-Content $ScratchLog -Raw
        $log | Should Match "oregon_ensure_symbiosis_latest\.ps1"
        $log | Should Match "ACTUAL_OVERALL_OK:"
        $log | Should Match "ACTUAL_SCORE:"
        $log | Should Match "MANIFEST_WRITTEN:"
        $m = Get-Content $Manifest -Raw | ConvertFrom-Json
        $m.health.score | Should Not BeNullOrEmpty
    }
}