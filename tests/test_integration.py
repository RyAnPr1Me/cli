#!/usr/bin/env python3
"""Basic integration tests for the CLI."""

import subprocess
import sys


def run_command(cmd):
    """Run a CLI command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_cli():
    """Test basic CLI functionality."""
    tests = [
        # Basic help commands
        ("python3 -m mcli.cli --help", "Test main help"),
        ("python3 -m mcli.cli --version", "Test version"),
        
        # File operations
        ("python3 -m mcli.cli files --help", "Test files help"),
        ("python3 -m mcli.cli files duplicates --help", "Test duplicates help"),
        ("python3 -m mcli.cli files diskusage /tmp", "Test disk usage"),
        
        # System commands
        ("python3 -m mcli.cli system --help", "Test system help"),
        ("python3 -m mcli.cli system info", "Test system info"),
        ("python3 -m mcli.cli process stats", "Test process stats"),
        
        # Utilities
        ("python3 -m mcli.cli utils --help", "Test utils help"),
        ("python3 -m mcli.cli utils hash 'test'", "Test hash"),
        ("python3 -m mcli.cli utils tree /tmp --depth 1", "Test tree"),
        
        # Network (basic checks)
        ("python3 -m mcli.cli network --help", "Test network help"),
    ]
    
    passed = 0
    failed = 0
    
    print("Running integration tests...\n")
    print("=" * 70)
    
    for cmd, description in tests:
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print(f"✓ PASS: {description}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Command: {cmd}")
            if stderr:
                print(f"  Error: {stderr[:100]}")
            failed += 1
    
    print("=" * 70)
    print(f"\nResults: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = test_cli()
    sys.exit(0 if success else 1)
