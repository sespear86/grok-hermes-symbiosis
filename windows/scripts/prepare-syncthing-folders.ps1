# prepare-syncthing-folders.ps1
# Windows helper for initial Syncthing folder preparation in the Grok-Hermes symbiosis.
# Run this in a normal PowerShell as your regular user.

$ErrorActionPreference = "Stop"

$SyncedRoot = "C:\Synced"  # Recommended location outside OneDrive / Documents
$SymbiosisRepo = "$env:USERPROFILE\grok-hermes-symbiosis"
$HandoffsDir = "$SymbiosisRepo\cross-device\handoffs"

Write-Host "=== Preparing Syncthing folder structure ===" -ForegroundColor Cyan

# 1. Create dedicated synced root (outside OneDrive)
if (-not (Test-Path $SyncedRoot)) {
    New-Item -ItemType Directory -Path $SyncedRoot -Force | Out-Null
    Write-Host "Created: $SyncedRoot" -ForegroundColor Green
} else {
    Write-Host "Exists: $SyncedRoot"
}

# 2. Ensure the symbiosis repo is in a good place (it already should be)
if (Test-Path $SymbiosisRepo) {
    Write-Host "Symbiosis repo found at: $SymbiosisRepo"
} else {
    Write-Warning "Symbiosis repo not found at expected location. Clone it first."
}

# 3. Create handoffs directory if it doesn't exist
if (-not (Test-Path $HandoffsDir)) {
    New-Item -ItemType Directory -Path $HandoffsDir -Force | Out-Null
    Write-Host "Created handoffs directory: $HandoffsDir" -ForegroundColor Green
}

# 4. Create a starter .stignore in the symbiosis repo root (if not present)
$StIgnorePath = Join-Path $SymbiosisRepo ".stignore"
if (-not (Test-Path $StIgnorePath)) {
    $stIgnoreContent = @"
# Grok-Hermes Symbiosis - Windows .stignore
# Edit as needed. These patterns are applied recursively.

# Build / cache artifacts
node_modules/
.venv/
__pycache__/
dist/
build/
*.log
.cache/

# Secrets & machine-specific (CRITICAL - never sync these)
.env*
secrets/
**/.git/
**/.ssh/
**/.grok/
**/.hermes/
**/%LOCALAPPDATA%/hermes/
**/%APPDATA%/hermes/

# Large / unnecessary files
*.mp4
*.iso
*.zip
models/
downloads/
"@
    Set-Content -Path $StIgnorePath -Value $stIgnoreContent -Encoding UTF8
    Write-Host "Created starter .stignore at $StIgnorePath" -ForegroundColor Green
} else {
    Write-Host ".stignore already exists at $StIgnorePath (not overwriting)"
}

# 5. Create an example .stignore for a generic joint projects folder
$ProjectsStIgnore = Join-Path $SyncedRoot "Projects\.stignore"
if (-not (Test-Path (Split-Path $ProjectsStIgnore))) {
    New-Item -ItemType Directory -Path (Split-Path $ProjectsStIgnore) -Force | Out-Null
}
if (-not (Test-Path $ProjectsStIgnore)) {
    $projectIgnore = @"
# Example .stignore for joint project folders
node_modules/
.venv/
__pycache__/
dist/
build/
.env*
secrets/
.git/
*.log
.cache/
"@
    Set-Content -Path $ProjectsStIgnore -Value $projectIgnore -Encoding UTF8
    Write-Host "Created example Projects .stignore"
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Download Syncthing portable from https://syncthing.net/downloads/"
Write-Host "2. Extract and run syncthing.exe"
Write-Host "3. In the web UI (http://127.0.0.1:8384), add these folders:"
Write-Host "   - $SymbiosisRepo"
Write-Host "   - Any joint project folders under $SyncedRoot"
Write-Host "4. Copy the Device ID from Actions > Show ID and send it to your brother."
Write-Host "5. See windows/syncthing-setup.md for the full Windows checklist."

Write-Host ""
Write-Host "Preparation complete." -ForegroundColor Green