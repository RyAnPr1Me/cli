#!/usr/bin/env python3
"""Utility commands."""

import click
import os
import subprocess
import hashlib
import time
from pathlib import Path


@click.group()
def utils():
    """Miscellaneous utility commands."""
    pass


@utils.command()
@click.argument('text')
def hash(text):
    """Generate hash of text.
    
    Computes MD5, SHA1, and SHA256 hashes of the provided text.
    Useful for verifying data integrity or generating checksums.
    """
    click.echo(f"Hashing: {text}\n")
    
    # MD5
    md5 = hashlib.md5(text.encode()).hexdigest()
    click.echo(f"MD5:    {md5}")
    
    # SHA1
    sha1 = hashlib.sha1(text.encode()).hexdigest()
    click.echo(f"SHA1:   {sha1}")
    
    # SHA256
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    click.echo(f"SHA256: {sha256}")


@utils.command()
@click.argument('filepath', type=click.Path(exists=True))
def hashfile(filepath):
    """Generate hash of a file.
    
    Computes MD5, SHA1, and SHA256 hashes of a file.
    Useful for file integrity verification.
    """
    click.echo(f"Hashing file: {filepath}\n")
    
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            
        # MD5
        md5 = hashlib.md5(data).hexdigest()
        click.echo(f"MD5:    {md5}")
        
        # SHA1
        sha1 = hashlib.sha1(data).hexdigest()
        click.echo(f"SHA1:   {sha1}")
        
        # SHA256
        sha256 = hashlib.sha256(data).hexdigest()
        click.echo(f"SHA256: {sha256}")
        
    except IOError as e:
        click.echo(f"Error reading file: {e}", err=True)
        return 1


@utils.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--depth', default=2, help='Directory depth (default: 2)')
def tree(path, depth):
    """Display directory tree structure.
    
    Shows a tree view of directories and files up to the specified depth.
    Similar to the 'tree' command but works in pure user space.
    """
    def print_tree(directory, prefix="", current_depth=0):
        if current_depth >= depth:
            return
            
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            click.echo(f"{prefix}[Permission Denied]")
            return
        
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            entry_path = os.path.join(directory, entry)
            
            # Skip hidden files in root
            if current_depth == 0 and entry.startswith('.'):
                continue
            
            connector = "└── " if is_last else "├── "
            click.echo(f"{prefix}{connector}{entry}")
            
            if os.path.isdir(entry_path):
                extension = "    " if is_last else "│   "
                print_tree(entry_path, prefix + extension, current_depth + 1)
    
    click.echo(f"{path}")
    print_tree(path)


@utils.command()
@click.argument('seconds', type=int)
def timer(seconds):
    """Simple countdown timer.
    
    Counts down from the specified number of seconds.
    Displays remaining time and beeps when complete.
    """
    if seconds <= 0:
        click.echo("Error: seconds must be positive", err=True)
        return 1
    
    click.echo(f"Timer started for {seconds} seconds...")
    click.echo("Press Ctrl+C to cancel\n")
    
    try:
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            timeformat = f"{mins:02d}:{secs:02d}"
            click.echo(f"\r{timeformat} remaining", nl=False)
            time.sleep(1)
        
        click.echo("\r00:00 - Time's up! \a")  # \a is the bell character
        
    except KeyboardInterrupt:
        click.echo("\n\nTimer cancelled.")


@utils.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
def compare(file1, file2):
    """Compare two files for equality.
    
    Compares files byte-by-byte using hash comparison.
    Much faster than reading entire files for large files.
    """
    click.echo(f"Comparing files:\n  {file1}\n  {file2}\n")
    
    # First check file sizes
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    
    if size1 != size2:
        click.echo(f"✗ Files are DIFFERENT (sizes: {size1} vs {size2} bytes)")
        return
    
    # Compare using hash
    try:
        with open(file1, 'rb') as f:
            hash1 = hashlib.sha256(f.read()).hexdigest()
        
        with open(file2, 'rb') as f:
            hash2 = hashlib.sha256(f.read()).hexdigest()
        
        if hash1 == hash2:
            click.echo(f"✓ Files are IDENTICAL ({size1} bytes)")
        else:
            click.echo(f"✗ Files are DIFFERENT (same size but different content)")
            
    except IOError as e:
        click.echo(f"Error reading files: {e}", err=True)
        return 1


@utils.command()
@click.argument('text')
@click.option('--decode', is_flag=True, help='Decode from base64 instead of encoding')
def base64(text, decode):
    """Encode or decode base64.
    
    Encode text to base64 by default, or decode with --decode flag.
    """
    import base64 as b64
    
    try:
        if decode:
            decoded = b64.b64decode(text).decode('utf-8')
            click.echo(f"Decoded: {decoded}")
        else:
            encoded = b64.b64encode(text.encode()).decode('utf-8')
            click.echo(f"Encoded: {encoded}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1


@utils.command()
def clipboard():
    """Display clipboard contents (macOS).
    
    Shows the current clipboard text using pbpaste.
    macOS only - uses native pbpaste command.
    """
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
        content = result.stdout
        
        if content:
            click.echo("Clipboard contents:")
            click.echo("-" * 50)
            click.echo(content)
        else:
            click.echo("Clipboard is empty")
            
    except FileNotFoundError:
        click.echo("Error: pbpaste not found (are you on macOS?)", err=True)
        return 1
    except subprocess.CalledProcessError as e:
        click.echo(f"Error accessing clipboard: {e}", err=True)
        return 1


@utils.command()
@click.argument('text')
def setclipboard(text):
    """Copy text to clipboard (macOS).
    
    Copies the provided text to the system clipboard using pbcopy.
    macOS only - uses native pbcopy command.
    """
    try:
        subprocess.run(['pbcopy'], input=text, text=True, check=True)
        click.echo(f"✓ Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}")
        
    except FileNotFoundError:
        click.echo("Error: pbcopy not found (are you on macOS?)", err=True)
        return 1
    except subprocess.CalledProcessError as e:
        click.echo(f"Error setting clipboard: {e}", err=True)
        return 1
