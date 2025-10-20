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


@utils.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--interpreter', '-i', help='Interpreter to use (e.g., python3, bash, node)')
@click.option('--args', '-a', multiple=True, help='Arguments to pass to the script')
def runscript(script_path, interpreter, args):
    """Run a script file with the appropriate interpreter.
    
    Automatically detects script type from extension or shebang line.
    Supports Python, Bash, Shell, Node.js, Ruby, Perl, and more.
    Use --interpreter to override automatic detection.
    """
    script_path = os.path.abspath(script_path)
    
    # Determine interpreter if not specified
    if not interpreter:
        # Try to detect from shebang
        try:
            with open(script_path, 'r') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#!'):
                    # Extract interpreter from shebang
                    shebang = first_line[2:].strip()
                    # Handle "#!/usr/bin/env python3" format
                    if 'env' in shebang:
                        interpreter = shebang.split()[-1]
                    else:
                        interpreter = os.path.basename(shebang)
                    click.echo(f"Detected interpreter from shebang: {interpreter}")
        except Exception:
            pass
        
        # If no shebang, try to detect from extension
        if not interpreter:
            ext = os.path.splitext(script_path)[1].lower()
            extension_map = {
                '.py': 'python3',
                '.sh': 'bash',
                '.bash': 'bash',
                '.js': 'node',
                '.rb': 'ruby',
                '.pl': 'perl',
                '.php': 'php',
            }
            interpreter = extension_map.get(ext, 'bash')
            click.echo(f"Detected interpreter from extension: {interpreter}")
    
    click.echo(f"Running: {script_path}")
    if args:
        click.echo(f"Arguments: {' '.join(args)}")
    click.echo("")
    
    # Build command
    cmd = [interpreter, script_path] + list(args)
    
    try:
        # Run the script
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode
    except FileNotFoundError:
        click.echo(f"Error: Interpreter '{interpreter}' not found", err=True)
        click.echo(f"Try specifying a different interpreter with --interpreter", err=True)
        return 1
    except KeyboardInterrupt:
        click.echo("\n\nScript execution interrupted by user.")
        return 130
    except Exception as e:
        click.echo(f"Error running script: {e}", err=True)
        return 1


@utils.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--pattern', '-p', default='*.sh', help='File pattern to match (default: *.sh)')
@click.option('--interpreter', '-i', help='Force specific interpreter for all scripts')
def runall(directory, pattern, interpreter):
    """Run all scripts matching pattern in a directory.
    
    Executes multiple scripts sequentially. Useful for batch processing
    or running test suites. Stops on first error unless continue flag is used.
    """
    import glob
    
    directory = os.path.abspath(directory)
    search_pattern = os.path.join(directory, pattern)
    scripts = sorted(glob.glob(search_pattern))
    
    if not scripts:
        click.echo(f"No scripts found matching pattern: {pattern} in {directory}")
        return 1
    
    click.echo(f"Found {len(scripts)} script(s) in {directory}\n")
    
    success_count = 0
    fail_count = 0
    
    for script in scripts:
        click.echo(f"{'='*60}")
        click.echo(f"Running: {os.path.basename(script)}")
        click.echo(f"{'='*60}")
        
        # Determine interpreter
        if not interpreter:
            ext = os.path.splitext(script)[1].lower()
            extension_map = {
                '.py': 'python3',
                '.sh': 'bash',
                '.bash': 'bash',
                '.js': 'node',
                '.rb': 'ruby',
                '.pl': 'perl',
            }
            script_interpreter = extension_map.get(ext, 'bash')
        else:
            script_interpreter = interpreter
        
        try:
            result = subprocess.run([script_interpreter, script], 
                                  capture_output=False, text=True)
            if result.returncode == 0:
                success_count += 1
                click.echo(f"✓ Success\n")
            else:
                fail_count += 1
                click.echo(f"✗ Failed with exit code {result.returncode}\n")
        except Exception as e:
            fail_count += 1
            click.echo(f"✗ Error: {e}\n")
    
    click.echo(f"{'='*60}")
    click.echo(f"Summary: {success_count} succeeded, {fail_count} failed")
    return 0 if fail_count == 0 else 1


@utils.command()
@click.argument('text')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--ignore-case', '-i', is_flag=True, help='Case-insensitive search')
@click.option('--count', '-c', is_flag=True, help='Only show count of matches')
@click.option('--line-numbers', '-n', is_flag=True, help='Show line numbers')
def grep(text, files, ignore_case, count, line_numbers):
    """Search for text in files (like grep).
    
    Simple text search utility for finding patterns in files.
    Supports multiple files and basic options.
    """
    if not files:
        click.echo("Error: No files specified", err=True)
        return 1
    
    search_text = text.lower() if ignore_case else text
    total_matches = 0
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                matches = 0
                for line_num, line in enumerate(f, 1):
                    compare_line = line.lower() if ignore_case else line
                    if search_text in compare_line:
                        matches += 1
                        total_matches += 1
                        if not count:
                            prefix = f"{filepath}:" if len(files) > 1 else ""
                            line_num_str = f"{line_num}:" if line_numbers else ""
                            click.echo(f"{prefix}{line_num_str}{line.rstrip()}")
                
                if count:
                    click.echo(f"{filepath}: {matches}")
                    
        except Exception as e:
            click.echo(f"Error reading {filepath}: {e}", err=True)
    
    if count and len(files) > 1:
        click.echo(f"Total: {total_matches}")


@utils.command()
@click.argument('url')
@click.argument('output', required=False)
@click.option('--show-progress', is_flag=True, help='Show download progress')
def download(url, output, show_progress):
    """Download a file from URL.
    
    Simple file downloader. Saves to current directory if no output specified.
    """
    import requests
    
    if not output:
        output = url.split('/')[-1] or 'downloaded_file'
    
    try:
        click.echo(f"Downloading: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output, 'wb') as f:
            if show_progress and total_size > 0:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100
                    click.echo(f"\rProgress: {percent:.1f}%", nl=False)
                click.echo()  # New line after progress
            else:
                f.write(response.content)
        
        size_mb = os.path.getsize(output) / (1024 * 1024)
        click.echo(f"✓ Downloaded to: {output} ({size_mb:.2f} MB)")
        
    except requests.exceptions.RequestException as e:
        click.echo(f"Error downloading file: {e}", err=True)
        return 1
    except IOError as e:
        click.echo(f"Error saving file: {e}", err=True)
        return 1


@utils.command()
@click.argument('text')
@click.option('--decode', is_flag=True, help='URL decode instead of encode')
def urlencode(text, decode):
    """URL encode or decode text.
    
    Encode text for use in URLs or decode URL-encoded text.
    """
    from urllib.parse import quote, unquote
    
    try:
        if decode:
            result = unquote(text)
            click.echo(f"Decoded: {result}")
        else:
            result = quote(text)
            click.echo(f"Encoded: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1


@utils.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@click.argument('archive', required=True)
@click.option('--compress', '-c', is_flag=True, help='Use compression')
def zip(files, archive, compress):
    """Create a zip archive from files.
    
    Combine multiple files into a single zip archive.
    Useful for packaging files or creating backups.
    """
    import zipfile
    
    if not archive.endswith('.zip'):
        archive += '.zip'
    
    try:
        compression = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
        
        with zipfile.ZipFile(archive, 'w', compression) as zf:
            for filepath in files:
                if os.path.isfile(filepath):
                    arcname = os.path.basename(filepath)
                    zf.write(filepath, arcname)
                    click.echo(f"Added: {filepath}")
                elif os.path.isdir(filepath):
                    # Add directory recursively
                    for root, dirs, dir_files in os.walk(filepath):
                        for file in dir_files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(filepath))
                            zf.write(file_path, arcname)
                            click.echo(f"Added: {file_path}")
        
        size_mb = os.path.getsize(archive) / (1024 * 1024)
        click.echo(f"\n✓ Created archive: {archive} ({size_mb:.2f} MB)")
        
    except Exception as e:
        click.echo(f"Error creating archive: {e}", err=True)
        return 1


@utils.command()
@click.argument('archive', type=click.Path(exists=True))
@click.argument('destination', default='.')
def unzip(archive, destination):
    """Extract a zip archive.
    
    Extract all files from a zip archive to specified directory.
    """
    import zipfile
    
    if not zipfile.is_zipfile(archive):
        click.echo(f"Error: {archive} is not a valid zip file", err=True)
        return 1
    
    try:
        os.makedirs(destination, exist_ok=True)
        
        with zipfile.ZipFile(archive, 'r') as zf:
            members = zf.namelist()
            click.echo(f"Extracting {len(members)} file(s) to {destination}...")
            
            for member in members:
                zf.extract(member, destination)
                click.echo(f"Extracted: {member}")
        
        click.echo(f"\n✓ Extracted to: {destination}")
        
    except Exception as e:
        click.echo(f"Error extracting archive: {e}", err=True)
        return 1


@utils.command()
@click.argument('json_file', type=click.Path(exists=True))
@click.option('--query', '-q', help='Query path (e.g., "data.items[0].name")')
@click.option('--pretty', '-p', is_flag=True, help='Pretty print output')
def json(json_file, query, pretty):
    """Parse and query JSON files.
    
    Read JSON files and optionally extract specific values using dot notation.
    """
    import json as json_lib
    
    try:
        with open(json_file, 'r') as f:
            data = json_lib.load(f)
        
        # Apply query if specified
        if query:
            parts = query.replace('[', '.').replace(']', '').split('.')
            result = data
            for part in parts:
                if part:
                    if part.isdigit():
                        result = result[int(part)]
                    else:
                        result = result[part]
            data = result
        
        # Output
        if pretty:
            output = json_lib.dumps(data, indent=2, sort_keys=True)
        else:
            output = json_lib.dumps(data)
        
        click.echo(output)
        
    except json_lib.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON - {e}", err=True)
        return 1
    except (KeyError, IndexError, TypeError) as e:
        click.echo(f"Error: Query failed - {e}", err=True)
        return 1
    except IOError as e:
        click.echo(f"Error reading file: {e}", err=True)
        return 1


@utils.command()
@click.argument('text')
@click.option('--reverse', '-r', is_flag=True, help='Reverse the text')
@click.option('--upper', '-u', is_flag=True, help='Convert to uppercase')
@click.option('--lower', '-l', is_flag=True, help='Convert to lowercase')
@click.option('--title', '-t', is_flag=True, help='Convert to title case')
def transform(text, reverse, upper, lower, title):
    """Transform text in various ways.
    
    Apply text transformations like reverse, case changes, etc.
    """
    result = text
    
    if reverse:
        result = result[::-1]
    if upper:
        result = result.upper()
    if lower:
        result = result.lower()
    if title:
        result = result.title()
    
    click.echo(result)
