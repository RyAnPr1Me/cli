# Features and User Space Design

## Overview

macOS CLI Tools is designed to be a powerful command-line utility that operates entirely in user space, without requiring root or sudo privileges. This document explains the features and how the tool works around macOS user space restrictions.

## User Space Architecture

### What is User Space?

User space refers to the portion of system memory and resources that are accessible to regular user applications without elevated privileges. This tool is designed to:

1. **Run without sudo/root** - All operations work with normal user permissions
2. **Fail gracefully** - When access is denied, commands skip those resources and continue
3. **Use standard APIs** - Leverages Python's cross-platform libraries that work within user constraints
4. **Install locally** - Goes into `~/.local/bin` instead of system directories

### Working Around Restrictions

#### File System Access
- **Challenge**: Can't access files owned by other users or system files
- **Solution**: Commands that scan directories skip files with permission errors and continue
- **Example**: `duplicates` command processes only accessible files

#### Process Management
- **Challenge**: Can't kill or inspect processes owned by other users
- **Solution**: Only show and manage processes the user owns
- **Example**: `process kill` only works on user's own processes

#### Network Operations
- **Challenge**: Can't bind to privileged ports (<1024) or use raw sockets
- **Solution**: Use standard network APIs for port checking and DNS lookup
- **Example**: `network checkport` uses standard socket connections

#### System Information
- **Challenge**: Some system metrics require root access
- **Solution**: Use psutil library which provides user-accessible system information
- **Example**: `system info` shows CPU, memory, disk without requiring root

## Feature Categories

### 1. File Operations

#### Find Duplicates
- Scans directories recursively
- Uses MD5 hashing for content comparison
- Optimizes by grouping files by size first
- Skips inaccessible files gracefully

**User Space Benefits:**
- Works on any directory the user can read
- No need for root to scan most personal directories
- Safe to run - read-only operation

#### Disk Usage
- Calculates total space used by directories
- Human-readable output (KB, MB, GB)
- Configurable depth for subdirectories

**User Space Benefits:**
- Uses standard `os.scandir()` which works in user space
- Automatically handles permission errors

#### File Search
- Pattern-based file searching
- Extension filtering
- Case-sensitive/insensitive options

**User Space Benefits:**
- Leverages OS file system APIs
- Works on entire accessible file system

### 2. Network Utilities

#### Port Checking
- Tests TCP connectivity to any host:port
- Configurable timeout
- Clear success/failure reporting

**User Space Benefits:**
- Uses standard socket API
- No raw sockets needed
- Can test any remote port

#### Speed Test
- Measures HTTP request latency
- Multiple request averaging
- Min/max/average statistics

**User Space Benefits:**
- Uses standard HTTP library (requests)
- No special network privileges required

#### DNS Lookup
- Resolves hostnames to IP addresses
- Shows both IPv4 and IPv6
- Uses system DNS resolver

**User Space Benefits:**
- Standard DNS resolution API
- No need for dig/nslookup privileges

#### Port Scanner
- Scans ranges of ports
- Great for checking local services
- Fast scanning with timeout

**User Space Benefits:**
- Connection-based scanning (not raw packets)
- Perfect for checking your own services

### 3. System Information

#### System Info
- OS version and details
- CPU information and frequency
- Memory statistics
- Disk usage
- Network interfaces

**User Space Benefits:**
- Uses psutil library (user-space system library)
- No /proc reading needed
- Cross-platform compatible

#### Resource Monitor
- Real-time CPU usage
- Memory consumption
- Disk I/O statistics
- Configurable update interval

**User Space Benefits:**
- All metrics available via psutil
- No kernel access required
- Safe continuous monitoring

#### Battery Status
- Percentage and charging status
- Time remaining/until full
- Laptop detection

**User Space Benefits:**
- Uses system power management API
- No IOKit access needed directly

#### Disk List
- All mounted partitions
- File system types
- Space usage per partition

**User Space Benefits:**
- Uses standard disk APIs
- Shows user-accessible partitions

### 4. Process Management

#### Process List
- Shows all visible processes
- CPU and memory usage
- Sortable by different metrics
- Status information

**User Space Benefits:**
- Shows processes user can see
- Uses psutil for safe access
- No /proc parsing needed

#### Find Process
- Search by process name
- Shows matching processes
- Resource usage per process

**User Space Benefits:**
- Filters user-visible processes
- Safe searching without root

#### Process Info
- Detailed process information
- Command line arguments
- Open files (when accessible)
- Thread count
- Memory breakdown

**User Space Benefits:**
- Shows maximum available info
- Gracefully handles access denied
- Clear error messages

#### Process Kill
- Terminate processes gracefully (SIGTERM)
- Force kill option (SIGKILL)
- Only works on owned processes

**User Space Benefits:**
- Safety: can't kill system processes
- Can only affect user's processes
- Prevents accidental system damage

### 5. Utilities

#### Hashing
- MD5, SHA1, SHA256 support
- Text and file hashing
- Fast computation

**User Space Benefits:**
- Pure Python implementation
- No system utilities needed
- Cross-platform

#### Directory Tree
- Visual directory structure
- Configurable depth
- Skips hidden files by default

**User Space Benefits:**
- Pure Python implementation
- Graceful permission handling
- No 'tree' command required

#### Timer
- Countdown functionality
- Visual feedback
- Bell on completion

**User Space Benefits:**
- Pure Python time management
- No system timer needed

#### File Compare
- Fast hash-based comparison
- Size check optimization
- Clear output

**User Space Benefits:**
- Works on any readable files
- No 'diff' command needed

#### Base64 Operations
- Encode and decode
- Text processing
- Error handling

**User Space Benefits:**
- Built-in Python functionality
- No external tools needed

#### Clipboard (macOS)
- Read clipboard contents
- Write to clipboard
- Uses native macOS commands

**User Space Benefits:**
- Uses pbcopy/pbpaste (user accessible)
- No accessibility permissions needed

## Security Considerations

### What This Tool Can Do
- Access files and directories the user can read
- Monitor and kill processes owned by the user
- Make network connections (outbound)
- Read system information available to user space
- Modify files the user owns

### What This Tool Cannot Do
- Access files owned by other users without permission
- Kill processes owned by other users or root
- Bind to privileged ports (<1024)
- Access raw system hardware
- Modify system configuration
- Install system-wide without sudo

### Safety Features
1. **Permission Checking**: All operations check permissions first
2. **Error Handling**: Graceful failure with clear messages
3. **Read-Only by Default**: Most commands are read-only
4. **User Confirmation**: Destructive operations (like kill) are explicit
5. **No Privilege Escalation**: Never attempts to gain root access

## Performance

### Optimizations
- **Duplicate Finding**: Groups by size before hashing
- **Process Listing**: Caches process information
- **Network Testing**: Configurable timeouts
- **Disk Scanning**: Efficient directory traversal

### Resource Usage
- **Memory**: Minimal, except when hashing large files
- **CPU**: Low, uses efficient algorithms
- **Disk I/O**: Only reads what's necessary
- **Network**: Only when using network commands

## Compatibility

### macOS Versions
- Tested on macOS 10.14+
- Should work on all modern macOS versions
- Uses standard Python APIs

### Python Versions
- Requires Python 3.7+
- Usually pre-installed on macOS
- Dependencies are minimal

### Cross-Platform
While designed for macOS, most features work on:
- Linux
- Unix-like systems
- WSL on Windows (some features)

**macOS-specific features:**
- Clipboard operations (pbcopy/pbpaste)
- Some system information details

## Installation Methods

### User Space (Recommended)
```bash
./install.sh
```
Installs to `~/.local/bin` - no root needed!

### System Wide (Requires sudo)
```bash
sudo python3 -m pip install -e .
```
Installs to `/usr/local/bin` - available to all users

### Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```
Isolated installation - great for development

## Future Enhancements

Potential additions that maintain user-space operation:
- File encryption/decryption
- Backup and sync utilities
- Text processing commands
- Image manipulation (with PIL)
- JSON/YAML processing
- Git repository helpers
- Log file analysis
- Configuration file management

All future features will maintain the user-space philosophy!
