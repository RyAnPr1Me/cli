# Installation Script Improvements

## Problem Statement
The original installer had several issues:
1. Used `pip install --user` which installs packages system-wide in user's Python site-packages
2. Only suggested adding PATH to shell config but didn't do it automatically
3. Didn't provide an alias option as fallback
4. May not work consistently across different macOS versions and shells

## Solution Implemented

### 1. Isolated Virtual Environment Installation
**Before:**
```bash
python3 -m pip install --user -e .
```

**After:**
```bash
python3 -m venv "$HOME/.mcli/venv"
"$HOME/.mcli/venv/bin/pip" install -e .
```

**Benefits:**
- No system-wide package pollution
- Completely isolated Python environment
- Each tool has its own dependencies
- No conflicts with other Python packages

### 2. Wrapper Script
Created a wrapper script at `~/.mcli/bin/mcli` that:
- Automatically activates the virtual environment
- Calls the Python module with proper environment
- Makes it transparent to the user

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/../venv"
exec "$VENV_DIR/bin/python" -m mcli.cli "$@"
```

### 3. Automatic Shell Configuration
**Interactive Options:**
1. Asks user if they want automatic configuration
2. Offers two configuration methods:
   - **Option 1 (Recommended):** Add to PATH
   - **Option 2 (Fallback):** Create alias

**Shell Detection:**
- Detects zsh → uses `~/.zshrc`
- Detects bash → prefers `~/.bash_profile`, falls back to `~/.bashrc`
- Creates config file if it doesn't exist

### 4. PATH vs Alias Configuration

**PATH Configuration (Option 1):**
```bash
export PATH="$HOME/.mcli/bin:$PATH"
```
- Allows `mcli` to be called from anywhere
- Standard Unix approach
- Works with tab completion

**Alias Configuration (Option 2):**
```bash
alias mcli="$HOME/.mcli/bin/mcli"
```
- Simple shortcut approach
- Useful if PATH modifications are problematic
- Works in interactive shells

### 5. Duplicate Configuration Prevention
The script checks if:
- PATH entry already exists in shell config
- Alias already exists in shell config
- The bin directory is already in current PATH

Prevents duplicate entries on repeated installations.

## Testing

### Automated Tests
1. **test_installer.sh** - Validates installer script structure and features
2. **Wrapper script tests** - Ensures wrapper correctly invokes venv Python
3. **Shell detection tests** - Verifies zsh/bash detection logic

### Manual Testing Results
✓ Creates isolated virtual environment at `~/.mcli/venv`
✓ Installs packages only in virtual environment (no system-wide installation)
✓ Creates functional wrapper script at `~/.mcli/bin/mcli`
✓ Correctly detects user's shell (bash/zsh)
✓ Offers interactive configuration with PATH or alias
✓ Prevents duplicate configuration entries

## Compatibility

### macOS Versions
- Works on all macOS versions with Python 3.7+
- Compatible with both Intel and Apple Silicon Macs
- Tested on macOS 10.14+

### Shell Support
- **zsh** (default on macOS 10.15+)
- **bash** (older macOS versions)
- Falls back to zsh config for other shells

### Python Versions
- Python 3.7+
- Automatically uses system Python 3
- No specific Python version requirements

## Usage

### Standard Installation
```bash
git clone https://github.com/RyAnPr1Me/cli.git
cd cli
./install.sh
```

### Interactive Prompts
1. **Configuration prompt:**
   ```
   Would you like to automatically configure mcli in your shell? (y/n)
   ```
   - Answer `y` to proceed with automatic configuration
   - Answer `n` to configure manually later

2. **Method selection:**
   ```
   Choose configuration method:
     1) Add to PATH (recommended)
     2) Create alias
   Enter choice (1 or 2, default: 1):
   ```
   - Press `1` or Enter for PATH configuration
   - Press `2` for alias configuration

### Post-Installation
Restart your terminal or run:
```bash
source ~/.zshrc    # for zsh
source ~/.bash_profile  # for bash
```

## Verification

Check installation:
```bash
# Verify directory structure
ls -la ~/.mcli/
# Should show: bin/ and venv/

# Verify wrapper script
cat ~/.mcli/bin/mcli
# Should contain venv activation logic

# Test command
mcli --help
# Should display help text
```

Verify no system-wide packages:
```bash
pip3 list --user | grep macos-cli
# Should show no results
```

## Troubleshooting

### Command not found: mcli
Either add to PATH:
```bash
export PATH="$HOME/.mcli/bin:$PATH"
```

Or create alias:
```bash
alias mcli="$HOME/.mcli/bin/mcli"
```

Then add to your shell config file permanently.

### Re-running installer
The installer:
- Removes old virtual environment if exists
- Creates fresh installation
- Detects existing configuration to prevent duplicates

### Uninstallation
```bash
# Remove installation
rm -rf ~/.mcli

# Remove configuration from shell config
# Edit ~/.zshrc or ~/.bash_profile and remove:
# - export PATH="$HOME/.mcli/bin:$PATH"
# OR
# - alias mcli="$HOME/.mcli/bin/mcli"
```

## Benefits Summary

1. ✓ **No system-wide pollution** - Completely isolated installation
2. ✓ **Works on all macOS systems** - Compatible with all versions and shells
3. ✓ **Automatic configuration** - Interactive shell setup
4. ✓ **Flexible options** - PATH or alias configuration
5. ✓ **No sudo required** - Fully user-space installation
6. ✓ **Clean uninstall** - Simple directory removal
7. ✓ **Prevents conflicts** - Virtual environment isolation
8. ✓ **Easy to maintain** - All files in one location
