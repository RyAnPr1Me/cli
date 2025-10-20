#!/usr/bin/env python3
"""Process management commands."""

import click
import psutil
import os
import signal


@click.group()
def process():
    """Process management and monitoring."""
    pass


@process.command()
@click.option('--sort', type=click.Choice(['cpu', 'memory', 'name']), default='cpu', 
              help='Sort by cpu, memory, or name')
@click.option('--limit', default=20, help='Number of processes to show')
def list(sort, limit):
    """List running processes with resource usage.
    
    Shows process ID, name, CPU usage, and memory usage.
    Sorted by CPU usage by default.
    """
    click.echo(f"Top {limit} Processes (sorted by {sort})\n" + "=" * 80)
    click.echo(f"{'PID':<8} {'Name':<30} {'CPU %':<10} {'Memory %':<10} {'Status':<10}")
    click.echo("-" * 80)
    
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort processes
    if sort == 'cpu':
        processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
    elif sort == 'memory':
        processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)
    elif sort == 'name':
        processes.sort(key=lambda x: x.get('name', '').lower())
    
    # Display top processes
    for proc in processes[:limit]:
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'N/A')[:29]
        cpu = proc.get('cpu_percent') or 0
        mem = proc.get('memory_percent') or 0
        status = proc.get('status', 'N/A')
        
        click.echo(f"{pid:<8} {name:<30} {cpu:<10.2f} {mem:<10.2f} {status:<10}")


@process.command()
@click.argument('name')
def find(name):
    """Find processes by name.
    
    Search for processes containing the specified name.
    Shows PID, full name, and resource usage.
    """
    click.echo(f"Searching for processes matching: {name}\n")
    click.echo(f"{'PID':<8} {'Name':<40} {'CPU %':<10} {'Memory %':<10}")
    click.echo("-" * 80)
    
    found = False
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if name.lower() in proc.info['name'].lower():
                found = True
                pid = proc.info['pid']
                pname = proc.info['name'][:39]
                cpu = proc.info.get('cpu_percent') or 0
                mem = proc.info.get('memory_percent') or 0
                
                click.echo(f"{pid:<8} {pname:<40} {cpu:<10.2f} {mem:<10.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if not found:
        click.echo(f"No processes found matching '{name}'")


@process.command()
@click.argument('pid', type=int)
def info(pid):
    """Get detailed information about a process.
    
    Shows comprehensive details about a specific process including
    CPU usage, memory, threads, files, and connections.
    """
    try:
        proc = psutil.Process(pid)
        
        click.echo(f"Process Information (PID: {pid})\n" + "=" * 80)
        
        # Basic info
        click.echo(f"\nBasic Information:")
        click.echo(f"  Name: {proc.name()}")
        click.echo(f"  Status: {proc.status()}")
        click.echo(f"  Created: {proc.create_time()}")
        
        try:
            click.echo(f"  User: {proc.username()}")
        except psutil.AccessDenied:
            click.echo(f"  User: (Access denied)")
        
        # Resource usage
        click.echo(f"\nResource Usage:")
        click.echo(f"  CPU: {proc.cpu_percent(interval=0.1)}%")
        
        mem_info = proc.memory_info()
        click.echo(f"  Memory (RSS): {mem_info.rss / (1024**2):.2f} MB")
        click.echo(f"  Memory (VMS): {mem_info.vms / (1024**2):.2f} MB")
        click.echo(f"  Memory %: {proc.memory_percent():.2f}%")
        
        # Threads
        click.echo(f"  Threads: {proc.num_threads()}")
        
        # Command line
        try:
            cmdline = ' '.join(proc.cmdline())
            if cmdline:
                click.echo(f"\nCommand Line:")
                click.echo(f"  {cmdline}")
        except psutil.AccessDenied:
            pass
        
        # Open files
        try:
            open_files = proc.open_files()
            if open_files:
                click.echo(f"\nOpen Files ({len(open_files)}):")
                for f in open_files[:10]:  # Show first 10
                    click.echo(f"  {f.path}")
                if len(open_files) > 10:
                    click.echo(f"  ... and {len(open_files) - 10} more")
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        
    except psutil.NoSuchProcess:
        click.echo(f"Error: No process found with PID {pid}", err=True)
        return 1
    except psutil.AccessDenied:
        click.echo(f"Error: Access denied for process {pid}", err=True)
        return 1


@process.command()
@click.argument('pid', type=int)
@click.option('--force', '-f', is_flag=True, help='Force kill (SIGKILL)')
def kill(pid, force):
    """Terminate a process by PID.
    
    Sends SIGTERM by default, or SIGKILL with --force flag.
    Only works for processes owned by the current user.
    """
    try:
        proc = psutil.Process(pid)
        pname = proc.name()
        
        if force:
            click.echo(f"Force killing process {pid} ({pname})...")
            proc.kill()  # SIGKILL
        else:
            click.echo(f"Terminating process {pid} ({pname})...")
            proc.terminate()  # SIGTERM
        
        # Wait for process to die
        try:
            proc.wait(timeout=3)
            click.echo(f"✓ Process {pid} terminated successfully")
        except psutil.TimeoutExpired:
            click.echo(f"⚠ Process {pid} did not terminate within 3 seconds", err=True)
            
    except psutil.NoSuchProcess:
        click.echo(f"Error: No process found with PID {pid}", err=True)
        return 1
    except psutil.AccessDenied:
        click.echo(f"Error: Access denied. Cannot kill process {pid}", err=True)
        click.echo(f"Note: You can only kill processes you own.", err=True)
        return 1


@process.command()
def stats():
    """Show overall process statistics.
    
    Displays total number of processes, threads, and overall resource usage.
    """
    click.echo("Process Statistics\n" + "=" * 50)
    
    total_procs = 0
    running_procs = 0
    sleeping_procs = 0
    total_threads = 0
    
    for proc in psutil.process_iter(['status']):
        try:
            total_procs += 1
            status = proc.info['status']
            
            if status == psutil.STATUS_RUNNING:
                running_procs += 1
            elif status == psutil.STATUS_SLEEPING:
                sleeping_procs += 1
            
            try:
                total_threads += proc.num_threads()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    click.echo(f"  Total Processes: {total_procs}")
    click.echo(f"  Running: {running_procs}")
    click.echo(f"  Sleeping: {sleeping_procs}")
    click.echo(f"  Total Threads: {total_threads}")
    click.echo(f"\n  CPU Count: {psutil.cpu_count()}")
    click.echo(f"  System CPU Usage: {psutil.cpu_percent(interval=1)}%")
