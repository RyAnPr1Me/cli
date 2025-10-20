# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/RyAnPr1Me/cli.git
cd cli

# Run the installer (no sudo needed!)
./install.sh
```

## First Commands to Try

### 1. Check System Information
```bash
mcli system info
```
Displays your macOS system details including CPU, memory, disk, and network information.

### 2. List Running Processes
```bash
mcli process list --sort memory --limit 10
```
Shows the top 10 processes sorted by memory usage.

### 3. Find Duplicate Files
```bash
mcli files duplicates ~/Downloads --min-size 10240
```
Finds duplicate files in your Downloads folder (minimum 10KB).

### 4. Check Network Connectivity
```bash
mcli network checkport google.com 443
```
Tests if port 443 (HTTPS) is open on google.com.

### 5. Monitor System Resources
```bash
mcli system monitor --count 5 --interval 2
```
Monitors CPU, memory, and disk usage for 5 readings, 2 seconds apart.

### 6. Display Directory Tree
```bash
mcli utils tree ~/Projects --depth 3
```
Shows a tree view of your Projects directory up to 3 levels deep.

### 7. Generate File Hash
```bash
mcli utils hashfile ~/Documents/important.pdf
```
Computes MD5, SHA1, and SHA256 hashes of a file.

### 8. Search for Files
```bash
mcli files search "*.py" ~/Projects --extension .py
```
Searches for Python files in your Projects directory.

### 9. Compare Two Files
```bash
mcli utils compare file1.txt file2.txt
```
Quickly checks if two files are identical.

### 10. Show Disk Usage
```bash
mcli files diskusage ~/Documents --human --depth 2
```
Shows disk space used by subdirectories in human-readable format.

## Getting Help

For any command, add `--help` to see detailed information:

```bash
mcli --help                    # Main help
mcli files --help              # File operations help
mcli network checkport --help  # Specific command help
```

## Tips

1. **User Space Only**: All commands run without root/sudo privileges
2. **Permission Errors**: Commands gracefully skip files/directories you can't access
3. **Clipboard Operations**: Use `mcli utils clipboard` and `mcli utils setclipboard` (macOS only)
4. **Process Management**: You can only manage processes you own
5. **Network Tools**: Port scanning works best on localhost for security scanning

## Common Use Cases

### Finding Large Files
```bash
mcli files diskusage ~/Downloads --human | head -20
```

### Monitoring a Specific Process
```bash
mcli process find "python"
mcli process info <PID>
```

### Testing Local Services
```bash
mcli network portscan 8000 8100
```

### Quick File Comparison
```bash
mcli utils compare backup/file.txt current/file.txt
```

## Next Steps

Explore all available commands:
- `mcli files --help` - File operations
- `mcli network --help` - Network utilities
- `mcli system --help` - System information
- `mcli process --help` - Process management
- `mcli utils --help` - Miscellaneous utilities

Happy command-line exploring!
