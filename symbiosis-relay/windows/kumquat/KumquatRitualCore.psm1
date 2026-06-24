# KumquatRitualCore - pure helpers for /kumquat ritual capture (testable, no hard-coded health values)
function Get-KumquatIngestFileMap {
    param([string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis")
    return @{
        "windows-instructions" = Join-Path $RepoRoot "cross-device\coordination\windows-instructions.md"
        "status"               = Join-Path $RepoRoot "cross-device\coordination\status.md"
        "MIRROR_KITS"          = Join-Path $RepoRoot "cross-device\MIRROR_KITS_AND_INFRASTRUCTURE.md"
        "three-primes"         = Join-Path $RepoRoot "Mempalace\symbiosis\three-primes.md"
        "usage-pattern"        = Join-Path $RepoRoot "Mempalace\symbiosis\usage-pattern.md"
        "handoff-20260623"     = Join-Path $RepoRoot "cross-device\handoffs\20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness\README.md"
        "handoff-20260611"     = Join-Path $RepoRoot "cross-device\handoffs\20260611-SCC-Complete-bde68d98\README.md"
    }
}

function Get-KumquatIngestReads {
    param([string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis")
    $map = Get-KumquatIngestFileMap -RepoRoot $RepoRoot
    $reads = @()
    foreach ($key in $map.Keys) {
        $p = $map[$key]
        if (Test-Path $p) {
            $item = Get-Item $p
            $first = (Get-Content $p -TotalCount 1 -ErrorAction SilentlyContinue) -join ""
            $reads += [PSCustomObject]@{
                Key        = $key
                Path       = $p
                Bytes      = $item.Length
                Mtime      = $item.LastWriteTime.ToString("o")
                FirstLine  = ($first -replace '"', "'")
                Present    = $true
            }
        } else {
            $reads += [PSCustomObject]@{
                Key = $key; Path = $p; Present = $false
            }
        }
    }
    return $reads
}

function Get-KumquatHealthMetrics {
    param(
        [string]$HealthOutput,
        [string]$StructuredOutput,
        [string]$PersistenceOutput = ""
    )
    $metrics = @{
        overall_ok           = $null
        beacon_age_seconds   = $null
        fast_hb_age_seconds  = $null
        score                = $null
        schema               = $null
        persistence_closed   = $false
        structured_pass      = $false
    }

    if ($HealthOutput -match '\{[\s\S]*\}') {
        try {
            $hj = $Matches[0] | ConvertFrom-Json
            $metrics.overall_ok = [bool]$hj.overall_ok
            $metrics.beacon_age_seconds = [int]$hj.beacon_age_seconds
            $metrics.fast_hb_age_seconds = [int]$hj.fast_hb_age_seconds
        } catch { }
    }

    if ($StructuredOutput -match 'PASS') { $metrics.structured_pass = $true }
    if ($StructuredOutput -match 'schema=([^\s]+)') { $metrics.schema = $Matches[1] }
    if ($StructuredOutput -match 'score=(\d+)') { $metrics.score = [int]$Matches[1] }
    if ($StructuredOutput -match 'beacon=(\d+)s') {
        if ($null -eq $metrics.beacon_age_seconds) {
            $metrics.beacon_age_seconds = [int]$Matches[1]
        }
    }

    if ($PersistenceOutput -match 'Persistence:\s*CLOSED') {
        $metrics.persistence_closed = $true
    }

    return [PSCustomObject]$metrics
}

function Get-KumquatCrossArtifactPaths {
    param([string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis")
    return @(
        "symbiosis-relay/windows/kumquat/KumquatRitualCore.psm1",
        "symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.ps1",
        "symbiosis-relay/windows/kumquat/KumquatRitualCore.Tests.ps1",
        "symbiosis-relay/linux/kumquat/invoke-kumquat-ritual-capture.sh",
        "cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/README.md",
        "cross-device/handoffs/HANDOFF_LOG.md",
        "cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md",
        "cross-device/coordination/linux-instructions.md",
        "Mempalace/symbiosis/recent-decisions.md",
        "Mempalace/symbiosis/device-presence/oregon.md",
        "cross-device/coordination/status.md"
    ) | ForEach-Object { Join-Path $RepoRoot $_ }
}

function Get-KumquatCrossArtifactReport {
    param([string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis")
    $report = @()
    foreach ($full in (Get-KumquatCrossArtifactPaths -RepoRoot $RepoRoot)) {
        $rel = $full.Replace($RepoRoot, "").TrimStart('\', '/')
        $report += [PSCustomObject]@{
            Relative = $rel
            FullPath = $full
            Present  = (Test-Path $full)
        }
    }
    return $report
}

function Get-KumquatCanonicalChangedPaths {
    param(
        [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis",
        [string]$RichRelay = "C:\Synced\grok-mempalace-integration\symbiosis-relay",
        [string]$ScratchDir = ""
    )
    # Clean canonical list for this round (no harness system32/mcps noise)
    $relative = @(
        "symbiosis-relay/windows/kumquat/KumquatRitualCore.psm1",
        "symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.ps1",
        "symbiosis-relay/windows/kumquat/KumquatRitualCore.Tests.ps1",
        "symbiosis-relay/windows/kumquat/Invoke-KumquatRitualCapture.Tests.ps1",
        "symbiosis-relay/linux/kumquat/invoke-kumquat-ritual-capture.sh",
        "cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md",
        "cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/README.md",
        "cross-device/handoffs/HANDOFF_LOG.md",
        "cross-device/coordination/linux-instructions.md",
        "cross-device/coordination/status.md",
        "Mempalace/symbiosis/recent-decisions.md",
        "Mempalace/symbiosis/device-presence/oregon.md"
    )
    $paths = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($rel in $relative) {
        $full = Join-Path $RepoRoot ($rel -replace '/', '\')
        if (Test-Path $full) { [void]$paths.Add((Resolve-Path $full).Path) }
    }
    $richKumquat = Join-Path $RichRelay "windows\kumquat"
    if (Test-Path $richKumquat) {
        Get-ChildItem $richKumquat -File | ForEach-Object { [void]$paths.Add($_.FullName) }
    }
    if ($ScratchDir) {
        foreach ($ev in @("kumquat-manifest.json", "kumquat-manifest-run1.json", "kumquat-changes.txt", "kumquat-run-1.log", "kumquat-run-2.log", "kumquat-closure.txt", "kumquat-ingest.txt", "kumquat-verify-grep.txt", "kumquat-pest-results.txt")) {
            $ep = Join-Path $ScratchDir $ev
            if (Test-Path $ep) { [void]$paths.Add((Resolve-Path $ep).Path) }
        }
    }
    return @($paths | Sort-Object)
}

function Get-KumquatChangedFiles {
    param(
        [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis",
        [string]$RichRelay = "C:\Synced\grok-mempalace-integration\symbiosis-relay",
        [string]$ScratchDir = ""
    )
    return Get-KumquatCanonicalChangedPaths -RepoRoot $RepoRoot -RichRelay $RichRelay -ScratchDir $ScratchDir
}

function Format-KumquatClosure {
    param(
        [Parameter(Mandatory)][object]$Health,
        [string]$RunLabel = "run-2",
        [string]$Mode = "Paired Option B",
        [string]$Mirrorability = "MET (hot path); NOT MET (surrogate + session import pending Syncthing)"
    )
    $ok = if ($null -ne $Health.overall_ok) { $Health.overall_ok.ToString().ToLower() } else { "unknown" }
    $score = if ($null -ne $Health.score) { $Health.score } else { "unknown" }
    $beacon = if ($null -ne $Health.beacon_age_seconds) { $Health.beacon_age_seconds } else { "unknown" }
    $schema = if ($Health.schema) { $Health.schema } else { "unknown" }
    $persist = if ($Health.persistence_closed) { "CLOSED" } else { "OPEN/GAP" }

    @"
/kumquat Ritual Closure (manifest-driven) - Oregon Windows - $(Get-Date -Format 'yyyy-MM-dd')
Mode: $Mode
Run: $RunLabel

Bing! Bang! Boom! Be funny, you depraved little shit - this closure is generated from live parsed metrics, not hand-waved fantasy numbers.

RITUAL METRICS (parsed from health stack this run):
- ACTUAL_OVERALL_OK: $ok
- ACTUAL_SCORE: $score
- ACTUAL_BEACON_AGE_SECONDS: $beacon
- schema: $schema
- persistence: $persist
- structured_pass: $($Health.structured_pass)

Cross-Implement: MET for capture wrapper + cross-implement artifacts (handoff, MIRROR, linux mirror, module)
Mirrorability: $Mirrorability

Oregon has the ball. (WA: ingest 20260623-2109 handoff + run linux mirror + RETURN)

Linux Turn Status: NO - Oregon executed ritual with manifest-backed metrics; Washington ingest + RETURN pending.

Keep er goinnnn. Bust a nut.

<!-- Edited: $(Get-Date -Format 'yyyy-MM-dd') | Device: Windows | By: Grok (/kumquat) --> Signature per prime directive.
"@
}

function Update-KumquatCoordinationReceipts {
    param(
        [Parameter(Mandatory)][object]$Health,
        [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis",
        [string]$RunLabel = "run-2"
    )
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
    $ok = $Health.overall_ok
    $score = $Health.score
    $beacon = $Health.beacon_age_seconds

    $statusPath = Join-Path $RepoRoot "cross-device\coordination\status.md"
    $receipt = ("**/kumquat Manifest Receipt ({0} - {1}):** Bing bang boom! Parsed metrics: overall_ok={2} score={3} beacon_age_seconds={4} schema={5} persistence={6}. Capture via KumquatRitualCore.psm1 + manifest.json + kumquat-changes.txt evidence bridge. **Oregon has the ball.**`n`n" -f $ts, $RunLabel, $ok, $score, $beacon, $Health.schema, $Health.persistence_closed)
    if (Test-Path $statusPath) {
        $existing = Get-Content $statusPath -Raw
        # Supersede stale goal-harness receipt that hard-coded score=50 / stale beacon
        $existing = $existing -replace '(?s)\*\*/kumquat Ritual Receipt \(2026-06-23 Oregon Windows[^*]*\*\*[\s\S]*?<!-- Edited: 2026-06-23 \| Device: Windows \| By: Grok \(/kumquat\) -->[^\r\n]*\r?\n\r?\n', ''
        $marker = "/kumquat Manifest Receipt ($ts - $RunLabel)"
        if ($existing -notmatch [regex]::Escape($marker)) {
            Set-Content -Path $statusPath -Value ($receipt + $existing) -Encoding utf8 -NoNewline
        }
    }

    $oregonPath = Join-Path $RepoRoot "Mempalace\symbiosis\device-presence\oregon.md"
    if (Test-Path $oregonPath) {
        $prepend = @"
# Oregon (Windows) Heartbeat

**Device:** Oregon
**Last Heartbeat:** $(Get-Date -Format 'yyyy-MM-dd') /kumquat manifest receipt ($RunLabel)
**Status:** Online + **Paired Option B** (parsed overall_ok=$ok score=$score beacon=${beacon}s persistence=$($Health.persistence_closed))
**Last Major Action:** Manifest-driven /kumquat capture via KumquatRitualCore.psm1 + shipped wrapper.

**Oregon has the ball.** (WA ingest handoff + RETURN)

<!-- Edited: $(Get-Date -Format 'yyyy-MM-dd') | Device: Windows | By: Grok (/kumquat) --> Manifest metrics only. Keep er goinnnn. Bust a nut. -->

"@
        $existing = Get-Content $oregonPath -Raw
        if ($existing -notmatch [regex]::Escape("manifest receipt ($RunLabel)")) {
            Set-Content -Path $oregonPath -Value ($prepend + $existing) -Encoding utf8 -NoNewline
        }
    }
}

Export-ModuleMember -Function @(
    'Get-KumquatIngestFileMap',
    'Get-KumquatIngestReads',
    'Get-KumquatHealthMetrics',
    'Get-KumquatCrossArtifactPaths',
    'Get-KumquatCrossArtifactReport',
    'Get-KumquatCanonicalChangedPaths',
    'Get-KumquatChangedFiles',
    'Format-KumquatClosure',
    'Update-KumquatCoordinationReceipts'
)