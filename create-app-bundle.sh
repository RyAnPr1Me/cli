#!/usr/bin/env bash
# Create macOS Application Bundle for user space installation
# This creates a .app bundle that can be placed in ~/Applications

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="macOS CLI Tools"
APP_BUNDLE_NAME="macOS-CLI-Tools.app"
INSTALL_DIR="$HOME/Applications"

echo "=================================="
echo "macOS Application Bundle Creator"
echo "=================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠  Warning: This script is designed for macOS"
    echo "   Creating bundle anyway, but it may not work properly on other systems."
fi

# Create bundle structure
BUNDLE_PATH="$SCRIPT_DIR/$APP_BUNDLE_NAME"
CONTENTS_PATH="$BUNDLE_PATH/Contents"
MACOS_PATH="$CONTENTS_PATH/MacOS"
RESOURCES_PATH="$CONTENTS_PATH/Resources"

echo "Creating application bundle structure..."
rm -rf "$BUNDLE_PATH"
mkdir -p "$MACOS_PATH"
mkdir -p "$RESOURCES_PATH"

# Create Info.plist
cat > "$CONTENTS_PATH/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>mcli-launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.ryanprime.mcli</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>macOS CLI Tools</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <string>1</string>
</dict>
</plist>
EOF

# Create launcher script
cat > "$MACOS_PATH/mcli-launcher" << 'EOF'
#!/bin/bash
# Launcher script for macOS CLI Tools

# Get the bundle path
BUNDLE_PATH="$(cd "$(dirname "$0")/../.." && pwd)"
PYTHON_CODE_PATH="$BUNDLE_PATH/Contents/Resources"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Required" message "Please install Python 3 from python.org to use macOS CLI Tools." as critical'
    exit 1
fi

# Install the package if not already installed
if ! python3 -c "import mcli" 2>/dev/null; then
    # Try to install
    cd "$PYTHON_CODE_PATH"
    python3 -m pip install --user -e . >/dev/null 2>&1
fi

# Check if running in terminal or from Finder
if [ -t 0 ]; then
    # Running in terminal, just show help
    python3 -m mcli.cli --help
else
    # Opened from Finder, open Terminal with help
    osascript <<APPLESCRIPT
tell application "Terminal"
    activate
    do script "echo 'macOS CLI Tools (mcli)'; echo ''; python3 -m mcli.cli --help; echo ''; echo 'Try: mcli system info'; echo 'For more examples, see: mcli --help'"
end tell
APPLESCRIPT
fi
EOF

chmod +x "$MACOS_PATH/mcli-launcher"

# Copy Python code to Resources
echo "Copying Python package..."
cp -r "$SCRIPT_DIR/mcli" "$RESOURCES_PATH/"
cp "$SCRIPT_DIR/setup.py" "$RESOURCES_PATH/"
cp "$SCRIPT_DIR/requirements.txt" "$RESOURCES_PATH/"
cp "$SCRIPT_DIR/README.md" "$RESOURCES_PATH/"

# Create a simple icon (using emoji as placeholder)
# In a real app, you'd use iconutil to create an .icns file
cat > "$RESOURCES_PATH/app-icon.txt" << 'EOF'
⚙️ This is a placeholder. To add a real icon:
1. Create a 1024x1024 PNG icon
2. Use iconutil to convert to .icns format
3. Place in Contents/Resources/AppIcon.icns
EOF

echo "✓ Application bundle created: $BUNDLE_PATH"
echo ""

# Offer to install to ~/Applications
if [[ -d "$HOME/Applications" ]]; then
    echo "Install to ~/Applications? [Y/n]"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
        # Remove old version if exists
        if [[ -d "$INSTALL_DIR/$APP_BUNDLE_NAME" ]]; then
            rm -rf "$INSTALL_DIR/$APP_BUNDLE_NAME"
        fi
        
        cp -r "$BUNDLE_PATH" "$INSTALL_DIR/"
        echo "✓ Installed to $INSTALL_DIR/$APP_BUNDLE_NAME"
        echo ""
        echo "You can now:"
        echo "  1. Open from Finder in ~/Applications"
        echo "  2. Or use 'mcli' command in Terminal (after PATH setup)"
    fi
else
    echo "Creating ~/Applications directory..."
    mkdir -p "$HOME/Applications"
    cp -r "$BUNDLE_PATH" "$INSTALL_DIR/"
    echo "✓ Installed to $INSTALL_DIR/$APP_BUNDLE_NAME"
fi

echo ""
echo "=================================="
echo "Application bundle ready!"
echo ""
echo "To use the CLI from Terminal:"
echo "  1. Run: ./install.sh"
echo "  2. Or manually: python3 -m pip install --user -e ."
echo ""
echo "To use the application:"
echo "  - Open '$APP_BUNDLE_NAME' from ~/Applications"
echo "  - It will open Terminal with help information"
echo "=================================="
