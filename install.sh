#!/usr/bin/env bash
# Installation script for macOS CLI Tools
# Installs in user space without requiring sudo/root privileges

set -e

echo "=================================="
echo "macOS CLI Tools - User Space Installer"
echo "=================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is required but not found."
    echo "Please install pip: python3 -m ensurepip --upgrade"
    exit 1
fi

echo "✓ Found pip"
echo ""

# Determine installation directory
USER_BIN="$HOME/.local/bin"
USER_LIB="$HOME/.local/lib/python${PYTHON_VERSION}/site-packages"

# Create directories if they don't exist
mkdir -p "$USER_BIN"
echo "✓ Installation directory: $USER_BIN"

# Install the package in user space
echo ""
echo "Installing macOS CLI Tools..."
python3 -m pip install --user -e . || {
    echo "Error: Installation failed"
    exit 1
}

echo ""
echo "✓ Installation complete!"
echo ""

# Check if user bin is in PATH
if [[ ":$PATH:" == *":$USER_BIN:"* ]]; then
    echo "✓ $USER_BIN is in your PATH"
else
    echo "⚠  Warning: $USER_BIN is not in your PATH"
    echo ""
    echo "To use the 'mcli' command, add this line to your ~/.zshrc or ~/.bash_profile:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then restart your terminal or run: source ~/.zshrc"
fi

echo ""
echo "=================================="
echo "You can now use the 'mcli' command!"
echo "Try: mcli --help"
echo "=================================="
