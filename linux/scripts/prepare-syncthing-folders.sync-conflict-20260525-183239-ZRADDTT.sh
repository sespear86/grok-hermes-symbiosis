#!/bin/bash
# Linux equivalent of prepare-syncthing-folders.ps1

set -e

SYNC_ROOT="${HOME}/Synced"
SYMBIOSIS_DIR="${HOME}/grok-hermes-symbiosis"

echo "=== Linux Syncthing Preparation ==="
echo "Creating sync root at: $SYNC_ROOT"

mkdir -p "$SYNC_ROOT/Projects"
mkdir -p "$SYNC_ROOT/handoffs"
mkdir -p "$SYNC_ROOT/grok-hermes-symbiosis"

echo "Ensuring symbiosis repo link..."
if [ ! -e "$SYNC_ROOT/grok-hermes-symbiosis" ]; then
    ln -s "$SYMBIOSIS_DIR" "$SYNC_ROOT/grok-hermes-symbiosis" 2>/dev/null || echo "Symbiosis folder already linked or exists"
fi

# Create a good .stignore if it doesn't exist in the symbiosis repo
STIGNORE="$SYMBIOSIS_DIR/.stignore"
if [ ! -f "$STIGNORE" ]; then
    echo "Creating default .stignore..."
    cat > "$STIGNORE" << 'STIGNORE_EOF'
# Grok-Hermes Symbiosis - Default .stignore (Linux)
.git
.env*
**/.env
**/secrets/
**/*.key
**/*.pem
**/*token*
**/*secret*
**/.hermes/
**/.grok/
node_modules/
.venv/
__pycache__/
dist/
build/
*.log
logs/
.synt*
STIGNORE_EOF
fi

echo "Preparation complete."
echo "Recommended sync root: $SYNC_ROOT"
echo "Next: Install Syncthing and add folders."
