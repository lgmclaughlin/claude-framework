#!/bin/bash
set -e

# Detect platform and set paths
case "$(uname -s)" in
    Darwin)
        INSTALL_BIN="/usr/local/bin"
        INSTALL_DATA="$HOME/Library/Application Support/cframe"
        NEEDS_SUDO=true
        ;;
    *)
        INSTALL_BIN="$HOME/.local/bin"
        INSTALL_DATA="$HOME/.local/share/cframe"
        NEEDS_SUDO=false
        ;;
esac

echo "Installing cframe..."

# Create directories
mkdir -p "$INSTALL_DATA"

# Copy script (sudo if needed for bin dir)
if [ "$NEEDS_SUDO" = true ]; then
    echo "Note: Installing to $INSTALL_BIN requires sudo"
    sudo cp cli/cframe.py "$INSTALL_BIN/cframe"
    sudo chmod +x "$INSTALL_BIN/cframe"
else
    mkdir -p "$INSTALL_BIN"
    cp cli/cframe.py "$INSTALL_BIN/cframe"
    chmod +x "$INSTALL_BIN/cframe"
fi

# Copy templates (remove old first for clean install)
rm -rf "$INSTALL_DATA/templates"
cp -r templates "$INSTALL_DATA/templates"

echo "Installed to:"
echo "  $INSTALL_BIN/cframe"
echo "  $INSTALL_DATA/templates/"

# Check if cframe is findable from user's shell
if ! bash -lc 'command -v cframe' &>/dev/null; then
    echo ""
    if [ "$NEEDS_SUDO" = true ]; then
        echo "Note: cframe is not in your PATH. $INSTALL_BIN should be in PATH by default."
        echo "Try restarting your terminal."
    else
        echo "Note: cframe is not in your PATH. Add this to your shell config:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi
