#!/usr/bin/env bash
# Test script for install.sh
# Tests basic installer functionality

set -e

echo "=================================="
echo "Testing Installer Script"
echo "=================================="
echo ""

# Test 1: Check if install.sh exists and is executable
echo "Test 1: Check if install.sh exists and is executable"
if [ -x "./install.sh" ]; then
    echo "✓ install.sh exists and is executable"
else
    echo "✗ install.sh not found or not executable"
    exit 1
fi

# Test 2: Syntax check
echo ""
echo "Test 2: Bash syntax check"
if bash -n ./install.sh; then
    echo "✓ install.sh has valid bash syntax"
else
    echo "✗ install.sh has syntax errors"
    exit 1
fi

# Test 3: Check for required commands in script
echo ""
echo "Test 3: Check for required features in script"
required_features=(
    "venv"  # Virtual environment creation
    "INSTALL_DIR"  # Installation directory variable
    "VENV_DIR"  # Virtual environment directory
    "BIN_WRAPPER"  # Wrapper script
    "SHELL_NAME"  # Shell detection
    "SHELL_RC"  # Shell config file
    "PATH_ENTRY"  # PATH configuration
    "ALIAS_ENTRY"  # Alias configuration
)

all_found=true
for feature in "${required_features[@]}"; do
    if grep -q "$feature" ./install.sh; then
        echo "  ✓ Found: $feature"
    else
        echo "  ✗ Missing: $feature"
        all_found=false
    fi
done

if [ "$all_found" = true ]; then
    echo "✓ All required features found in install.sh"
else
    echo "✗ Some required features missing"
    exit 1
fi

# Test 4: Check that script doesn't use --user flag
echo ""
echo "Test 4: Verify no system-wide installation (--user flag)"
if grep -q "pip install --user" ./install.sh; then
    echo "✗ Script still uses 'pip install --user' which installs system-wide"
    exit 1
else
    echo "✓ Script does not use --user flag (good - using isolated venv)"
fi

# Test 5: Check for shell configuration options
echo ""
echo "Test 5: Check for automatic shell configuration"
if grep -q "Would you like to automatically configure" ./install.sh; then
    echo "✓ Script prompts for automatic configuration"
else
    echo "✗ Script doesn't prompt for automatic configuration"
    exit 1
fi

if grep -q "Choose configuration method" ./install.sh; then
    echo "✓ Script offers choice between PATH and alias"
else
    echo "✗ Script doesn't offer configuration method choice"
    exit 1
fi

# Test 6: Check for zsh and bash detection
echo ""
echo "Test 6: Check for shell detection (zsh/bash)"
if grep -q ".zshrc" ./install.sh && grep -q ".bash_profile" ./install.sh; then
    echo "✓ Script detects both zsh and bash shells"
else
    echo "✗ Script doesn't properly detect both zsh and bash"
    exit 1
fi

# Test 7: Verify wrapper script template
echo ""
echo "Test 7: Check wrapper script template"
if grep -q "VENV_DIR/bin/python" ./install.sh; then
    echo "✓ Wrapper script uses virtual environment Python"
else
    echo "✗ Wrapper script doesn't use virtual environment Python"
    exit 1
fi

echo ""
echo "=================================="
echo "All installer tests passed! ✓"
echo "=================================="
