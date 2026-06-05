param([string]$Action, [string]$TaskId)
$Shared = $env:SYMBIOSIS_SHARED
if (-not $Shared) { $Shared = "$env:USERPROFILE\Synced\grok-mempalace-integration" }
$PresenceDir = Join-Path $Shared "device-presence"
$PresenceFile = Join-Path $PresenceDir "oregon-grok-build-presence.json"
New-Item -ItemType Directory -Force -Path $PresenceDir | Out-Null
$now = (Get-Date).ToUniversalTime().ToString("o")
$bust = ($Action -eq "bust_a_nut_start")
$data = @{
  grok_build_active = $true
  last_seen = $now
  task_id = $TaskId
  bust_a_nut = $bust
  source = "Set-OregonGrokBuildBeacon"
} | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($PresenceFile, $data, [System.Text.UTF8Encoding]::new($false))
Write-Host "Set-OregonGrokBuildBeacon: wrote presence active=true bust=$bust for $TaskId"
exit 0
