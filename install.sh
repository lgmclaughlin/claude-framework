#!/bin/bash
set -e

# Detect platform and set paths
case "$(uname -s)" in
    Darwin)
        INSTALL_BIN="$HOME/.local/bin"
        INSTALL_DATA="$HOME/Library/Application Support/cframe"
        ;;
    *)
        INSTALL_BIN="$HOME/.local/bin"
        INSTALL_DATA="$HOME/.local/share/cframe"
        ;;
esac

echo "Installing cframe..."

# Create directories
mkdir -p "$INSTALL_BIN"
mkdir -p "$INSTALL_DATA"

# Copy script
cp cli/cframe.py "$INSTALL_BIN/cframe"
chmod +x "$INSTALL_BIN/cframe"

# Copy templates (remove old first for clean install)
rm -rf "$INSTALL_DATA/templates"
cp -r templates "$INSTALL_DATA/templates"

echo "Installed to:"
echo "  $INSTALL_BIN/cframe"
echo "  $INSTALL_DATA/templates/"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$INSTALL_BIN:"* ]]; then
    echo ""
    echo "Warning: $INSTALL_BIN is not in your PATH"
    echo "Add this to your shell config:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
