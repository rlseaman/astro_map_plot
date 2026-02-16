#!/bin/bash
# Installation script for mapplot with BSC5 support

set -e

echo "Installing mapplot..."
echo "Includes Bright Star Catalogue (BSC5) support"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "Error: Python 3.7+ is required. Found version $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION ✓"

# Install required packages
echo "Installing required Python packages..."
echo "  - matplotlib (plotting)"
echo "  - cartopy (map projections)"
echo "  - numpy (numerical arrays)"
echo "  - astropy (celestial coordinates)"
echo ""

pip3 install --user matplotlib cartopy numpy astropy

# Locate project directories
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Make scripts executable
chmod +x "$SCRIPT_DIR/mapplot"

# Install directory
INSTALL_DIR="$HOME/.local/bin"
DATA_DIR="$HOME/.local/share/mapplot"

mkdir -p "$INSTALL_DIR"
mkdir -p "$DATA_DIR"

# Copy mapplot
if cp "$SCRIPT_DIR/mapplot" "$INSTALL_DIR/"; then
    echo "Installed mapplot to $INSTALL_DIR"
else
    echo "Could not install to $INSTALL_DIR"
    echo "You can run mapplot from the src directory: $SCRIPT_DIR/mapplot"
    exit 1
fi

# Copy BSC5 data
BSC5_FILE="$ROOT_DIR/data/bsc5_data.txt"
if [ -f "$BSC5_FILE" ]; then
    if cp "$BSC5_FILE" "$DATA_DIR/"; then
        echo "Installed bsc5_data.txt to $DATA_DIR"
    else
        echo "Warning: Could not copy bsc5_data.txt to $DATA_DIR"
        echo "  BSC5 catalog will be loaded from current directory"
    fi
else
    echo "Warning: bsc5_data.txt not found at $BSC5_FILE"
    echo "  Minimal built-in catalog will be used"
fi

# Check PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠ Note: $INSTALL_DIR is not in your PATH"
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then reload your shell with: source ~/.bashrc"
else
    echo "✓ $INSTALL_DIR is already in your PATH"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Try these commands:"
echo "  mapplot --sky --catalog -p mollweide -g    # Sky map with BSC5"
echo "  mapplot example_cities.txt                 # Earth map"
echo "  mapplot -h                                 # Full help"
echo ""
echo "For BSC5 info: http://tdc-www.harvard.edu/catalogs/bsc5.html"
