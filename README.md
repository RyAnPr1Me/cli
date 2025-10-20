# macOS CLI Tools

A powerful macOS compatible user space CLI with many useful features. Install and run entirely in user space without requiring root/sudo privileges.

## Features

This CLI tool provides multiple categories of commands:

### 📁 File Operations
- **duplicates** - Find duplicate files by content hash
- **diskusage** - Display disk usage for directories
- **search** - Search for files by name pattern

### 🌐 Network Utilities
- **checkport** - Check if a port is open on a host
- **speedtest** - Simple network speed test
- **lookup** - DNS lookup for hostnames
- **portscan** - Scan a range of ports

### 💻 System Information
- **info** - Display comprehensive system information
- **monitor** - Real-time system resource monitoring
- **battery** - Show battery status (for laptops)
- **disks** - List all disk partitions and usage

### 🔧 Process Management
- **list** - List running processes with resource usage
- **find** - Find processes by name
- **info** - Get detailed process information
- **kill** - Terminate a process (user processes only)
- **stats** - Show overall process statistics

### 🛠️ Utilities
- **hash** - Generate MD5/SHA1/SHA256 hashes of text
- **hashfile** - Generate hashes of files
- **tree** - Display directory tree structure
- **timer** - Simple countdown timer
- **compare** - Compare two files for equality
- **base64** - Encode/decode base64
- **clipboard** - Display clipboard contents (macOS)
- **setclipboard** - Copy text to clipboard (macOS)
- **runscript** - Run scripts with automatic interpreter detection
- **runall** - Run all scripts in a directory (batch execution)
- **grep** - Search for text in files (like grep command)
- **download** - Download files from URLs
- **urlencode** - URL encode/decode text
- **zip** - Create zip archives
- **unzip** - Extract zip archives
- **json** - Parse and query JSON files
- **transform** - Transform text (reverse, case changes)

### 🔐 Admin Workarounds
- **hosts** - View /etc/hosts file without sudo
- **dnsflush** - Flush DNS cache (user space alternative)
- **portusage** - Show processes using network ports (like lsof -i)
- **interfaces** - Show network interface info (like ifconfig)
- **launchagents** - List user LaunchAgents
- **defaults** - Read system preferences/defaults
- **env** - Show environment variables
- **services** - List running services (user accessible)
- **sudocmds** - Show admin command alternatives

## Installation

### User Space Installation (No sudo required!)

```bash
# Clone the repository
git clone https://github.com/RyAnPr1Me/cli.git
cd cli

# Run the user space installer
./install.sh
```

The installer will:
1. Install the package in `~/.local` (user space)
2. Add the `mcli` command to your PATH
3. No root/sudo privileges required!

### macOS Application Bundle (Alternative)

You can also create a macOS application bundle for installation to ~/Applications:

```bash
# Create and install the .app bundle
./create-app-bundle.sh
```

This creates a `macOS-CLI-Tools.app` that can be:
- Placed in ~/Applications folder (no admin rights needed)
- Opened from Finder (launches Terminal with CLI help)
- Used alongside the command-line installation

### Manual Installation

```bash
# Install in user space with pip
python3 -m pip install --user -e .

# Make sure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

Add the PATH export to your `~/.zshrc` or `~/.bash_profile` to make it permanent.

## Usage

After installation, use the `mcli` command:

```bash
# Get help
mcli --help

# Get help for a specific command group
mcli files --help
mcli network --help

# Example commands
mcli files duplicates ~/Documents          # Find duplicate files
mcli files diskusage ~/Downloads --human   # Show disk usage
mcli network checkport google.com 443      # Check if port is open
mcli network speedtest                     # Test network speed
mcli system info                           # Show system information
mcli system monitor --count 5              # Monitor resources
mcli process list --sort memory            # List processes by memory
mcli utils hash "my text"                  # Generate hashes
mcli utils tree . --depth 3                # Display directory tree
```

### Run a script
```bash
mcli utils runscript myscript.py
```

### Run a script with arguments
```bash
mcli utils runscript script.sh --args "arg1" --args "arg2"
```

### Run with specific interpreter
```bash
mcli utils runscript myfile.txt --interpreter python3
```

## Examples

### Find duplicate files in your Downloads folder
```bash
mcli files duplicates ~/Downloads --min-size 10240
```

### Check which ports are open locally
```bash
mcli network portscan 8000 8100 --host 127.0.0.1
```

### Monitor system resources
```bash
mcli system monitor --interval 2 --count 10
```

### Find all Python processes
```bash
mcli process find python
```

### Compare two files
```bash
mcli utils compare file1.txt file2.txt
```

### Display directory structure
```bash
mcli utils tree ~/Projects --depth 3
```

### View hosts file without sudo
```bash
mcli admin hosts
```

### Check which processes are using port 8080
```bash
mcli admin portusage --port 8080
```

### Show network interfaces (like ifconfig)
```bash
mcli admin interfaces
```

### Flush DNS cache (user space workaround)
```bash
mcli admin dnsflush
```

## Working Around User Space Restrictions

This tool is designed to work entirely in user space and handle common macOS restrictions:

1. **No root required** - All commands run with user privileges
2. **Graceful permission handling** - Commands skip files/directories when permission is denied
3. **User process management** - Can only manage processes owned by the current user
4. **Network operations** - Uses unprivileged ports and standard network APIs
5. **File system access** - Works within user's accessible directories
6. **System information** - Gathers data from user-accessible APIs (psutil)

### Admin Command Workarounds

The `mcli admin` command group provides user-space alternatives to common admin commands:

| Admin Command | User Space Alternative | Description |
|---------------|----------------------|-------------|
| `sudo cat /etc/hosts` | `mcli admin hosts` | View hosts file |
| `sudo dscacheutil -flushcache` | `mcli admin dnsflush` | Flush DNS cache |
| `sudo lsof -i` | `mcli admin portusage` | Show port usage |
| `ifconfig` | `mcli admin interfaces` | Network interfaces |
| `sudo launchctl list` | `mcli admin services` | List services |
| `ls /Library/LaunchAgents` | `mcli admin launchagents` | User agents |
| `defaults read <domain>` | `mcli admin defaults <domain>` | Read preferences |

Run `mcli admin sudocmds` to see a complete list of admin command alternatives.

## Requirements

- macOS 10.14 or later
- Python 3.7 or later (usually pre-installed on macOS)
- pip (Python package manager)

## Dependencies

The tool uses these Python packages (automatically installed):
- `click` - Command-line interface framework
- `psutil` - System and process utilities
- `requests` - HTTP library for network testing

## Development

```bash
# Install in development mode
python3 -m pip install --user -e .

# Run tests (if available)
python3 -m pytest

# Uninstall
python3 -m pip uninstall macos-cli-tools
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

### Command not found: mcli
Make sure `~/.local/bin` is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission denied errors
Some commands may not be able to access all files/processes due to macOS security restrictions. This is normal and expected in user space.

### Python version issues
Make sure you're using Python 3.7 or later:
```bash
python3 --version
```

## Platform Support

While optimized for macOS, most commands will work on Linux and other Unix-like systems. macOS-specific features (clipboard operations) gracefully fail on other platforms.