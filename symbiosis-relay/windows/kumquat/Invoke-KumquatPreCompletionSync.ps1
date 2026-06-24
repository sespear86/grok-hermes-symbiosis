# Pre-completion verifier sync - run immediately before update_goal(completed:true)
param(
    [string]$ScratchDir = "",
    [string]$RepoRoot = "C:\Users\spear\grok-hermes-symbiosis",
    [string]$SessionDir = "",
    [int]$Attempt = 0
)

$ErrorActionPreference = "Stop"
$moduleDir = $PSScriptRoot
Import-Module (Join-Path $moduleDir "KumquatRitualCore.psm1") -Force

if (-not $ScratchDir) { $ScratchDir = $env:KUMQUAT_SCRATCH }
if (-not $ScratchDir) { throw "KUMQUAT_SCRATCH or -ScratchDir required" }

$goalRoot = Split-Path $ScratchDir -Parent
$goalId = Get-KumquatGoalIdFromRoot -GoalRoot $goalRoot
if (-not $goalId) { throw "Could not parse goal id from goal root: $goalRoot" }

if (-not $SessionDir) {
    $SessionDir = $env:KUMQUAT_SESSION_DIR
}
if (-not $SessionDir) {
    $SessionDir = "C:\Users\spear\.grok\sessions\C%3A%5CWINDOWS%5Csystem32\019ef7c5-ad0b-7513-9573-1e969798b050"
}

$patchPath = Join-Path $ScratchDir "kumquat-git-diff.patch"
if (-not (Test-Path $patchPath)) { throw "kumquat-git-diff.patch missing in scratch: $ScratchDir" }

$relative = Get-KumquatCanonicalRelativePaths
$currentRound = Get-KumquatClassifierRound -GoalRoot $goalRoot -GoalId $goalId
if ($Attempt -le 0) {
    $Attempt = Get-KumquatVerifierAttempt -GoalRoot $goalRoot -GoalId $goalId
}

$workspace = Publish-KumquatWorkspaceDeliverables -RepoRoot $RepoRoot -RelativePaths $relative
$sync = Sync-KumquatVerifierInputs -GoalRoot $goalRoot -GoalId $goalId -Attempt $Attempt `
    -PatchPath $patchPath -RelativePaths $relative -ScratchDir $ScratchDir
$stubs = Copy-KumquatDeliverableStubs -RepoRoot $RepoRoot -SessionDir $SessionDir `
    -ScratchDir $ScratchDir -RelativePaths $relative
$guard = Start-KumquatVerifierPatchGuard -GoalRoot $goalRoot -GoalId $goalId -Attempt $Attempt `
    -AuthoritativePatchPath $patchPath -ScratchDir $ScratchDir -DurationSeconds 120

$logPath = Join-Path $ScratchDir "kumquat-precompletion-sync.log"
@(
    "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] PRECOMPLETION_SYNC",
    "goal_root: $goalRoot",
    "goal_id: $goalId",
    "classifier_round: $currentRound",
    "verifier_attempt: $Attempt",
    "patch_ok: $($sync.patch_ok)",
    "patch: $($sync.patch_path)",
    "changed: $($sync.changed_path)",
    "patch_guard_pid: $($guard.pid)",
    "workspace_published: $($workspace.copied)/$($workspace.expected)",
    "deliverables: $($stubs.deliverables_root)",
    "stubs_copied: $($stubs.copied)/$($stubs.expected)"
) | Set-Content -Path $logPath -Encoding utf8

if (-not $sync.patch_ok) { exit 1 }
if ($stubs.copied -lt $relative.Count) { exit 1 }
if ($workspace.copied -lt $relative.Count) { exit 1 }
exit 0