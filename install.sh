#!/usr/bin/env bash
# Installation script for macOS CLI Tools
# Installs in user space without requiring sudo/root privileges
# Creates isolated installation without system-wide package pollution

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

# Determine installation directory - use a dedicated location for this tool
INSTALL_DIR="$HOME/.mcli"
VENV_DIR="$INSTALL_DIR/venv"
BIN_WRAPPER="$INSTALL_DIR/bin/mcli"

# Create directories if they don't exist
mkdir -p "$INSTALL_DIR/bin"
echo "✓ Installation directory: $INSTALL_DIR"

# Create a virtual environment for isolated installation
echo ""
echo "Creating isolated Python environment..."
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR" || {
    echo "Error: Failed to create virtual environment"
    exit 1
}

echo "✓ Virtual environment created"

# Install the package in the virtual environment (no system-wide packages)
echo ""
echo "Installing macOS CLI Tools (isolated, no system-wide packages)..."
"$VENV_DIR/bin/pip" install -e . || {
    echo "Error: Installation failed"
    exit 1
}

echo "✓ Package installed in isolated environment"

# Create a wrapper script that activates the venv and runs mcli
echo ""
echo "Creating launcher script..."
cat > "$BIN_WRAPPER" << 'EOF'
#!/usr/bin/env bash
# Wrapper script for mcli - activates virtual environment and runs command

# Resolve the actual script location, handling symlinks
SOURCE="$0"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"

VENV_DIR="$SCRIPT_DIR/../venv"
exec "$VENV_DIR/bin/python" -m mcli.cli "$@"
EOF

chmod +x "$BIN_WRAPPER"
echo "✓ Launcher script created at $BIN_WRAPPER"

echo ""
echo "✓ Installation complete!"
echo ""

# Detect the user's shell
SHELL_NAME=$(basename "$SHELL")
SHELL_RC=""

if [ "$SHELL_NAME" = "zsh" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    # On macOS, prefer .bash_profile for login shells
    if [ -f "$HOME/.bash_profile" ]; then
        SHELL_RC="$HOME/.bash_profile"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
else
    # Default to .zshrc for other shells (zsh is default on modern macOS)
    SHELL_RC="$HOME/.zshrc"
fi

echo "Detected shell: $SHELL_NAME"
echo "Shell configuration file: $SHELL_RC"
echo ""

# Check if PATH already contains our bin directory or if alias exists
PATH_ENTRY="export PATH=\"\$HOME/.mcli/bin:\$PATH\""
ALIAS_ENTRY="alias mcli=\"\$HOME/.mcli/bin/mcli\""
PATH_EXISTS=false
ALIAS_EXISTS=false

if [ -f "$SHELL_RC" ]; then
    if grep -q "/.mcli/bin" "$SHELL_RC" 2>/dev/null; then
        PATH_EXISTS=true
    fi
    if grep -q "alias mcli=" "$SHELL_RC" 2>/dev/null; then
        ALIAS_EXISTS=true
    fi
fi

# Determine what to add to shell configuration
if [ "$PATH_EXISTS" = true ] || [ "$ALIAS_EXISTS" = true ]; then
    echo "✓ mcli is already configured in $SHELL_RC"
elif [[ ":$PATH:" == *":$HOME/.mcli/bin:"* ]]; then
    echo "✓ $HOME/.mcli/bin is already in your PATH"
else
    # Ask user if they want to automatically configure the shell
    echo "Would you like to automatically configure mcli in your shell? (y/n)"
    echo "This will add an entry to $SHELL_RC"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Try to add to PATH first, but if that seems problematic, use alias instead
        echo ""
        echo "Choose configuration method:"
        echo "  1) Add to PATH (recommended) - adds $HOME/.mcli/bin to PATH"
        echo "  2) Create alias - creates 'alias mcli=...' shortcut"
        echo ""
        echo "Enter choice (1 or 2, default: 1):"
        read -r config_choice
        
        # Create shell RC file if it doesn't exist
        if [ ! -f "$SHELL_RC" ]; then
            touch "$SHELL_RC"
            echo "Created $SHELL_RC"
        fi
        
        if [ "$config_choice" = "2" ]; then
            # User prefers alias
            echo "" >> "$SHELL_RC"
            echo "# macOS CLI Tools - mcli command alias" >> "$SHELL_RC"
            echo "$ALIAS_ENTRY" >> "$SHELL_RC"
            echo "✓ Added alias to $SHELL_RC"
            echo ""
            echo "Alias added: mcli"
            echo "Restart your terminal or run: source $SHELL_RC"
        else
            # Default: add to PATH
            echo "" >> "$SHELL_RC"
            echo "# macOS CLI Tools - add mcli to PATH" >> "$SHELL_RC"
            echo "$PATH_ENTRY" >> "$SHELL_RC"
            echo "✓ Added PATH entry to $SHELL_RC"
            echo ""
            echo "PATH updated!"
            echo "Restart your terminal or run: source $SHELL_RC"
        fi
    else
        echo ""
        echo "⚠  Skipping automatic configuration."
        echo ""
        echo "To use the 'mcli' command, add one of these to your $SHELL_RC:"
        echo ""
        echo "Option 1 (PATH - recommended):"
        echo "    $PATH_ENTRY"
        echo ""
        echo "Option 2 (Alias):"
        echo "    $ALIAS_ENTRY"
        echo ""
        echo "Then restart your terminal or run: source $SHELL_RC"
    fi
fi

echo ""
echo "=================================="
echo "Installation Summary:"
echo "  - Installed to: $INSTALL_DIR"
echo "  - No system-wide packages installed"
echo "  - Isolated Python virtual environment"
echo "  - Shell: $SHELL_NAME ($SHELL_RC)"
echo ""
echo "You can now use the 'mcli' command!"
echo "Try: mcli --help"
echo "=================================="
