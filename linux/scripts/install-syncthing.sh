#!/bin/bash
# Syncthing Installation Script for this Linux machine (Fedora)
# Run this in a normal terminal.

set -e

echo "=== Installing Syncthing (Portable Binary) ==="

INSTALL_DIR="$HOME/Tools/syncthing"

mkdir -p "$HOME/Tools"

cd "$HOME/Tools"

echo "Fetching latest version..."
VERSION=$(curl -s https://api.github.com/repos/syncthing/syncthing/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$VERSION" ]; then
    echo "Could not determine latest version. Using fallback v1.27.10"
    VERSION="v1.27.10"
fi

echo "Downloading Syncthing $VERSION..."
curl -LO "https://github.com/syncthing/syncthing/releases/download/${VERSION}/syncthing-linux-amd64.tar.gz"

echo "Extracting..."
tar -xzf syncthing-linux-amd64.tar.gz
rm -f syncthing-linux-amd64.tar.gz

if [ -d syncthing-linux-amd64 ]; then
    mv syncthing-linux-amd64 syncthing
fi

echo "Syncthing installed to: $INSTALL_DIR"

echo ""
echo "To run Syncthing:"
echo "  $INSTALL_DIR/syncthing"
echo ""
echo "Recommended first run (with GUI on localhost):"
echo "  $INSTALL_DIR/syncthing --gui-address=127.0.0.1:8384"
