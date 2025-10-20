# Command Examples

This document provides detailed examples of using each command in the macOS CLI Tools.

## File Operations

### Find Duplicate Files

Find duplicate files in a directory, checking only files larger than 1MB:
```bash
mcli files duplicates ~/Downloads --min-size 1048576
```

Find duplicates in current directory:
```bash
mcli files duplicates .
```

### Disk Usage

Show disk usage with human-readable sizes:
```bash
mcli files diskusage ~/Documents --human
```

Show disk usage with deeper directory scanning:
```bash
mcli files diskusage ~/Projects --depth 3 --human
```

### Search for Files

Search for all Python files:
```bash
mcli files search "test" ~/Projects --extension .py
```

Case-sensitive search for files containing "Config":
```bash
mcli files search "Config" . --case-sensitive
```

Search for all image files:
```bash
mcli files search "image" ~/Pictures --extension .jpg
```

## Network Utilities

### Check Port

Check if web server is running:
```bash
mcli network checkport localhost 8080
```

Check HTTPS port on remote server:
```bash
mcli network checkport google.com 443
```

With custom timeout:
```bash
mcli network checkport example.com 80 --timeout 5
```

### Speed Test

Run a basic speed test:
```bash
mcli network speedtest
```

Test with more requests:
```bash
mcli network speedtest --count 10
```

Test with custom URL:
```bash
mcli network speedtest --url https://httpbin.org/get --count 5
```

### DNS Lookup

Lookup a hostname:
```bash
mcli network lookup google.com
```

Lookup local hostname:
```bash
mcli network lookup localhost
```

### Port Scan

Scan common web ports on localhost:
```bash
mcli network portscan 8000 8100 --host 127.0.0.1
```

Scan well-known ports:
```bash
mcli network portscan 20 80 --host localhost
```

## System Information

### System Info

Display complete system information:
```bash
mcli system info
```

### Monitor Resources

Monitor for 10 readings:
```bash
mcli system monitor --count 10
```

Monitor with faster updates:
```bash
mcli system monitor --interval 0.5 --count 20
```

### Battery Status

Check battery status (laptops only):
```bash
mcli system battery
```

### List Disks

Show all disk partitions:
```bash
mcli system disks
```

Limit to first 5 partitions:
```bash
mcli system disks --limit 5
```

## Process Management

### List Processes

List top 20 processes by CPU:
```bash
mcli process list
```

List by memory usage:
```bash
mcli process list --sort memory --limit 15
```

List alphabetically:
```bash
mcli process list --sort name --limit 30
```

### Find Process

Find all Python processes:
```bash
mcli process find python
```

Find Chrome processes:
```bash
mcli process find chrome
```

### Process Info

Get detailed info about a process:
```bash
mcli process info 1234
```

### Kill Process

Terminate a process gracefully:
```bash
mcli process kill 5678
```

Force kill a process:
```bash
mcli process kill 5678 --force
```

### Process Statistics

Show overall process stats:
```bash
mcli process stats
```

## Utilities

### Hash Text

Generate hashes of text:
```bash
mcli utils hash "Hello, World!"
```

### Hash File

Generate hashes of a file:
```bash
mcli utils hashfile ~/Documents/contract.pdf
```

### Directory Tree

Show directory structure:
```bash
mcli utils tree .
```

Show deeper tree:
```bash
mcli utils tree ~/Projects --depth 4
```

### Timer

Set a 5-minute timer:
```bash
mcli utils timer 300
```

Quick 1-minute timer:
```bash
mcli utils timer 60
```

### Compare Files

Compare two files:
```bash
mcli utils compare original.txt backup.txt
```

### Base64 Encoding

Encode text to base64:
```bash
mcli utils base64 "sensitive data"
```

Decode from base64:
```bash
mcli utils base64 "c2Vuc2l0aXZlIGRhdGE=" --decode
```

### Clipboard Operations (macOS only)

View clipboard contents:
```bash
mcli utils clipboard
```

Copy text to clipboard:
```bash
mcli utils setclipboard "Hello, World!"
```

### Run Scripts

Run a Python script:
```bash
mcli utils runscript myscript.py
```

Run a Bash script with arguments:
```bash
mcli utils runscript script.sh --args "input.txt" --args "output.txt"
```

Run script with explicit interpreter:
```bash
mcli utils runscript data.js --interpreter node
```

Run Ruby script:
```bash
mcli utils runscript process.rb --args "--verbose"
```

## Admin Workarounds

### View Hosts File

View /etc/hosts without sudo:
```bash
mcli admin hosts
```

### Flush DNS Cache

User space DNS cache flush:
```bash
mcli admin dnsflush
```

### Port Usage

Show which processes are using network ports:
```bash
mcli admin portusage
```

Show processes on specific port:
```bash
mcli admin portusage --port 8080
```

### Network Interfaces

Show all network interfaces (like ifconfig):
```bash
mcli admin interfaces
```

### Environment Variables

Display all environment variables:
```bash
mcli admin env
```

### System Preferences

Read system defaults/preferences:
```bash
mcli admin defaults NSGlobalDomain
```

Read specific key:
```bash
mcli admin defaults com.apple.finder AppleShowAllFiles
```

### LaunchAgents

List user LaunchAgents:
```bash
mcli admin launchagents
```

### Services

List running services (user accessible):
```bash
mcli admin services
```

Show all services including system:
```bash
mcli admin services --all
```

### Admin Command Reference

Show all admin command alternatives:
```bash
mcli admin sudocmds
```

## Combining Commands

### Find and Kill Process
```bash
# Find the process
mcli process find "myapp"
# Note the PID, then kill it
mcli process kill 12345
```

### Check Multiple Ports
```bash
mcli network checkport localhost 8000
mcli network checkport localhost 8080
mcli network checkport localhost 3000
```

### Monitor While Testing
```bash
# In one terminal
mcli system monitor --count 100

# In another terminal
# Run your application or tests
```

### Backup Verification
```bash
# Compare original and backup
mcli utils compare /path/to/original.txt /path/to/backup.txt

# Or hash them separately
mcli utils hashfile /path/to/original.txt
mcli utils hashfile /path/to/backup.txt
```

### Cleanup Duplicates Workflow
```bash
# First, find duplicates
mcli files duplicates ~/Downloads --min-size 1024

# Review the output, then manually delete unwanted duplicates
# Verify disk space freed
mcli files diskusage ~/Downloads --human
```

## Tips and Tricks

1. **Pipe output to files**:
   ```bash
   mcli system info > system-report.txt
   mcli process list > running-processes.txt
   ```

2. **Use with grep**:
   ```bash
   mcli process list | grep python
   mcli files search "config" . | grep -i json
   ```

3. **Combine with other tools**:
   ```bash
   mcli files duplicates . | tee duplicates.log
   mcli system monitor --count 5 | tee system-log.txt
   ```

4. **Create aliases** (add to ~/.zshrc or ~/.bash_profile):
   ```bash
   alias sysinfo='mcli system info'
   alias procs='mcli process list --sort memory'
   alias diskspace='mcli files diskusage ~ --human'
   ```

5. **Background monitoring**:
   ```bash
   mcli system monitor --count 100 --interval 5 > monitor.log &
   ```
