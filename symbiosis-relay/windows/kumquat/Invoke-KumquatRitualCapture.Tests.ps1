# Pester 3.x tests - drives SHIPPED symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.ps1
Describe "Invoke-KumquatRitualCapture (shipped)" {
    $CaptureScript = Join-Path $PSScriptRoot "Invoke-KumquatRitualCapture.ps1"
    $ScratchLog = Join-Path $env:TEMP "kumquat-pest-shipped.log"

    It "invokes oregon_ensure_symbiosis_latest.ps1 with full ingest/presence/surrogate/cross logging" {
        if (Test-Path $ScratchLog) { Remove-Item $ScratchLog -Force }
        & powershell -ExecutionPolicy Bypass -File $CaptureScript -RunLabel "pest-shipped" -LogPath $ScratchLog
        $LASTEXITCODE | Should Be 0
        $log = Get-Content $ScratchLog -Raw
        $log | Should Match "oregon_ensure_symbiosis_latest\.ps1"
        $log | Should Match "ENSURE_SCRIPT_INVOKED"
        $log | Should Match "ENSURE_HARNESS_NOTE"
        $log | Should Match "INGEST_READ:.*mtime="
        $log | Should Match "WA_BEACON:"
        $log | Should Match "SURROGATE_GAP|SURROGATE_FOUND"
        $log | Should Match "CROSS_ARTIFACT_OK:"
        $log | Should Match "PASS - structured Oregon relay status"
        $log | Should Match "Linux Turn Status"
        $log | Should Match "Keep er goinnnn\. Bust a nut\."
    }
}