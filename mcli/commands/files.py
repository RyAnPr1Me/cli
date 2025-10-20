#!/usr/bin/env python3
"""File operations commands."""

import os
import hashlib
import click
from pathlib import Path
from collections import defaultdict


@click.group()
def files():
    """File and directory operations."""
    pass


@files.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--min-size', default=1024, help='Minimum file size in bytes (default: 1KB)')
def duplicates(path, min_size):
    """Find duplicate files in a directory.
    
    Scans the specified path recursively and identifies files with identical content
    based on MD5 hash comparison. Only files larger than min-size are checked.
    """
    click.echo(f"Scanning for duplicates in: {path}")
    click.echo(f"Minimum file size: {min_size} bytes\n")
    
    files_by_size = defaultdict(list)
    
    # Group files by size first (optimization)
    for root, dirs, files_list in os.walk(path):
        for filename in files_list:
            filepath = os.path.join(root, filename)
            try:
                size = os.path.getsize(filepath)
                if size >= min_size:
                    files_by_size[size].append(filepath)
            except (OSError, IOError) as e:
                click.echo(f"Warning: Cannot access {filepath}: {e}", err=True)
    
    # Check for duplicates among files with same size
    duplicates_found = False
    files_by_hash = defaultdict(list)
    
    for size, file_list in files_by_size.items():
        if len(file_list) > 1:
            for filepath in file_list:
                try:
                    with open(filepath, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        files_by_hash[file_hash].append(filepath)
                except (OSError, IOError) as e:
                    click.echo(f"Warning: Cannot read {filepath}: {e}", err=True)
    
    # Report duplicates
    for file_hash, file_list in files_by_hash.items():
        if len(file_list) > 1:
            duplicates_found = True
            click.echo(f"Duplicate files (hash: {file_hash[:8]}...):")
            for filepath in file_list:
                size = os.path.getsize(filepath)
                click.echo(f"  - {filepath} ({size} bytes)")
            click.echo()
    
    if not duplicates_found:
        click.echo("No duplicate files found.")


@files.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--depth', default=1, help='Directory depth to display (default: 1)')
@click.option('--human', is_flag=True, help='Display sizes in human-readable format')
def diskusage(path, depth, human):
    """Show disk usage for directories.
    
    Displays the disk space used by directories at the specified depth.
    Use --human flag for human-readable sizes (KB, MB, GB).
    """
    def get_size(path):
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_size(entry.path)
        except PermissionError:
            pass
        return total
    
    def format_size(size):
        if not human:
            return f"{size} bytes"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    click.echo(f"Disk usage for: {path}\n")
    
    if os.path.isfile(path):
        size = os.path.getsize(path)
        click.echo(f"{format_size(size)}: {path}")
        return
    
    # Get sizes for subdirectories
    items = []
    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                size = get_size(entry.path)
                items.append((size, entry.name))
        except PermissionError:
            click.echo(f"Warning: Permission denied for {entry.name}", err=True)
    
    # Sort by size (descending)
    items.sort(reverse=True)
    
    for size, name in items:
        click.echo(f"{format_size(size):>12} - {name}")


@files.command()
@click.argument('pattern')
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--extension', '-e', help='Filter by file extension (e.g., .py, .txt)')
@click.option('--case-sensitive', is_flag=True, help='Make search case-sensitive')
def search(pattern, path, extension, case_sensitive):
    """Search for files by name pattern.
    
    Searches recursively for files matching the given pattern.
    Supports filtering by file extension.
    """
    import fnmatch
    
    if not case_sensitive:
        pattern = pattern.lower()
    
    click.echo(f"Searching for '{pattern}' in: {path}\n")
    found_count = 0
    
    for root, dirs, files_list in os.walk(path):
        for filename in files_list:
            # Apply extension filter if specified
            if extension and not filename.endswith(extension):
                continue
            
            # Match pattern
            search_name = filename if case_sensitive else filename.lower()
            if pattern in search_name or fnmatch.fnmatch(search_name, f"*{pattern}*"):
                filepath = os.path.join(root, filename)
                size = os.path.getsize(filepath)
                click.echo(f"{filepath} ({size} bytes)")
                found_count += 1
    
    click.echo(f"\nFound {found_count} matching file(s).")
