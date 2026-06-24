# Detached guard: re-sync goal-classifier patch when harness clobbers it after update_goal
param(
    [Parameter(Mandatory)][string]$GoalRoot,
    [Parameter(Mandatory)][string]$GoalId,
    [Parameter(Mandatory)][int]$Attempt,
    [Parameter(Mandatory)][string]$AuthoritativePatchPath,
    [string]$ScratchDir = "",
    [int]$DurationSeconds = 600,
    [int]$PollMilliseconds = 50
)

$ErrorActionPreference = "SilentlyContinue"
$moduleDir = $PSScriptRoot
Import-Module (Join-Path $moduleDir "KumquatRitualCore.psm1") -Force

$relative = Get-KumquatCanonicalRelativePaths
$patchOut = Join-Path $GoalRoot "goal-classifier-$GoalId-$Attempt.patch"
$logPath = if ($ScratchDir) { Join-Path $ScratchDir "kumquat-patch-guard.log" } else {
    Join-Path $GoalRoot "kumquat-patch-guard.log"
}

function GLog([string]$msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Add-Content -Path $logPath -Value $line -Encoding utf8
}

GLog "GUARD_START pid=$PID attempt=$Attempt patch=$patchOut duration=${DurationSeconds}s poll=${PollMilliseconds}ms"
$deadline = (Get-Date).AddSeconds($DurationSeconds)
$repairs = 0

$lastSize = -1
while ((Get-Date) -lt $deadline) {
    if (Test-KumquatVerifierPatchNeedsRepair -PatchPath $patchOut) {
        $size = if (Test-Path $patchOut) { (Get-Item $patchOut -Force).Length } else { 0 }
        $mtime = if (Test-Path $patchOut) { (Get-Item $patchOut -Force).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss') } else { 'missing' }
        $snippet = if (Test-Path $patchOut) { (Get-Content $patchOut -TotalCount 1 -ErrorAction SilentlyContinue) } else { '' }
        Repair-KumquatVerifierPatch -GoalRoot $GoalRoot -GoalId $GoalId -Attempt $Attempt `
            -PatchPath $AuthoritativePatchPath -RelativePaths $relative -ScratchDir $ScratchDir | Out-Null
        $repairs++
        GLog "GUARD_REPAIR #$repairs clobber_detected bytes=$size mtime=$mtime snippet=$snippet"
        $lastSize = $size
    }
    Start-Sleep -Milliseconds $PollMilliseconds
}

$finalOk = -not (Test-KumquatVerifierPatchNeedsRepair -PatchPath $patchOut)
GLog "GUARD_END repairs=$repairs final_patch_ok=$finalOk"
if (-not $finalOk) { exit 1 }
exit 0