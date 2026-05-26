#!/bin/bash
# Syncthing Installation Script (Improved for v2.x naming)

set -e

echo "=== Installing Syncthing (Portable Binary) ==="

INSTALL_DIR="$HOME/Tools/syncthing"

mkdir -p "$HOME/Tools"
cd "$HOME/Tools"

echo "Using known good version v2.1.0 (current latest as of this setup)"
VERSION="v2.1.0"

echo "Downloading syncthing-linux-amd64-${VERSION}.tar.gz ..."
curl -LO "https://github.com/syncthing/syncthing/releases/download/${VERSION}/syncthing-linux-amd64-${VERSION}.tar.gz"

echo "Extracting..."
tar -xzf "syncthing-linux-amd64-${VERSION}.tar.gz"
rm -f "syncthing-linux-amd64-${VERSION}.tar.gz"

if [ -d "syncthing-linux-amd64-${VERSION}" ]; then
    mv "syncthing-linux-amd64-${VERSION}" syncthing
fi

echo ""
echo "✅ Syncthing installed to: $INSTALL_DIR"
echo ""
echo "To start it with the web UI:"
echo "  $INSTALL_DIR/syncthing --gui-address=127.0.0.1:8384"
