# fix-git-remote.ps1
# Quick helper to ensure the symbiosis repo uses the SSH remote.
# Run this from your normal PowerShell when you want to push from your real identity.

$RepoPath = "C:\Users\spear\grok-hermes-symbiosis"   # Adjust if your path differs
$DesiredRemote = "git@github.com:sespear86/grok-hermes-symbiosis.git"

if (-not (Test-Path $RepoPath)) {
    Write-Error "Repo not found at $RepoPath. Update the path in this script."
    exit 1
}

Set-Location $RepoPath

$current = git remote get-url origin 2>$null

if ($current -ne $DesiredRemote) {
    Write-Host "Current remote: $current"
    Write-Host "Switching to SSH remote: $DesiredRemote"
    git remote set-url origin $DesiredRemote
    git remote -v
    Write-Host ""
    Write-Host "Done. Make sure your SSH key for GitHub is loaded (ssh-add or Pageant/1Password/etc)."
    Write-Host "If you still get permission issues, you are probably still inside the harness environment."
} else {
    Write-Host "Remote is already set correctly to SSH."
    git remote -v
}

Write-Host ""
Write-Host "Reminder: The harness often runs as a different GitHub account and will 403 on push."
Write-Host "Do final pushes from your normal terminal for best results."