#!/usr/bin/env python3
"""System information commands."""

import click
import psutil
import platform
import os


@click.group()
def system():
    """System information and monitoring."""
    pass


@system.command()
def info():
    """Display system information.
    
    Shows OS version, CPU, memory, and other system details.
    All information is gathered from user space without special privileges.
    """
    click.echo("System Information\n" + "=" * 50)
    
    # OS Information
    click.echo(f"\nOperating System:")
    click.echo(f"  System: {platform.system()}")
    click.echo(f"  Release: {platform.release()}")
    click.echo(f"  Version: {platform.version()}")
    click.echo(f"  Machine: {platform.machine()}")
    click.echo(f"  Processor: {platform.processor()}")
    
    # CPU Information
    click.echo(f"\nCPU:")
    click.echo(f"  Physical cores: {psutil.cpu_count(logical=False)}")
    click.echo(f"  Total cores: {psutil.cpu_count(logical=True)}")
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        click.echo(f"  Max Frequency: {cpu_freq.max:.2f} MHz")
        click.echo(f"  Current Frequency: {cpu_freq.current:.2f} MHz")
    
    # Memory Information
    memory = psutil.virtual_memory()
    click.echo(f"\nMemory:")
    click.echo(f"  Total: {memory.total / (1024**3):.2f} GB")
    click.echo(f"  Available: {memory.available / (1024**3):.2f} GB")
    click.echo(f"  Used: {memory.used / (1024**3):.2f} GB")
    click.echo(f"  Percentage: {memory.percent}%")
    
    # Disk Information
    click.echo(f"\nDisk:")
    disk = psutil.disk_usage('/')
    click.echo(f"  Total: {disk.total / (1024**3):.2f} GB")
    click.echo(f"  Used: {disk.used / (1024**3):.2f} GB")
    click.echo(f"  Free: {disk.free / (1024**3):.2f} GB")
    click.echo(f"  Percentage: {disk.percent}%")
    
    # Network
    click.echo(f"\nNetwork Interfaces:")
    net_if = psutil.net_if_addrs()
    for interface, addresses in net_if.items():
        click.echo(f"  {interface}:")
        for addr in addresses:
            click.echo(f"    {addr.family.name}: {addr.address}")


@system.command()
@click.option('--interval', default=1.0, help='Update interval in seconds')
@click.option('--count', default=10, help='Number of readings to take')
def monitor(interval, count):
    """Monitor system resources in real-time.
    
    Displays CPU usage, memory usage, and disk I/O statistics.
    Updates every 'interval' seconds for 'count' iterations.
    """
    click.echo("System Resource Monitor")
    click.echo("=" * 50)
    click.echo("Press Ctrl+C to stop\n")
    
    try:
        for i in range(count):
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=interval)
            
            # Memory
            memory = psutil.virtual_memory()
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            
            click.echo(f"\nReading {i+1}/{count}:")
            click.echo(f"  CPU Usage: {cpu_percent}%")
            click.echo(f"  Memory Usage: {memory.percent}% ({memory.used / (1024**3):.2f} GB / {memory.total / (1024**3):.2f} GB)")
            click.echo(f"  Disk Read: {disk_io.read_bytes / (1024**2):.2f} MB")
            click.echo(f"  Disk Write: {disk_io.write_bytes / (1024**2):.2f} MB")
            
    except KeyboardInterrupt:
        click.echo("\n\nMonitoring stopped.")


@system.command()
def battery():
    """Show battery status (for laptops).
    
    Displays battery percentage, charging status, and time remaining.
    """
    if not hasattr(psutil, "sensors_battery"):
        click.echo("Battery information not available on this system.")
        return
    
    battery = psutil.sensors_battery()
    
    if battery is None:
        click.echo("No battery detected (desktop system or battery info not available).")
        return
    
    click.echo("Battery Status\n" + "=" * 50)
    click.echo(f"  Percentage: {battery.percent}%")
    click.echo(f"  Plugged in: {'Yes' if battery.power_plugged else 'No'}")
    
    if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
        hours, remainder = divmod(battery.secsleft, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if battery.power_plugged:
            click.echo(f"  Time until full: {int(hours)}h {int(minutes)}m")
        else:
            click.echo(f"  Time remaining: {int(hours)}h {int(minutes)}m")


@system.command()
@click.option('--limit', default=10, help='Number of partitions to show')
def disks(limit):
    """List all disk partitions and their usage.
    
    Shows mount points, file systems, and space usage for all partitions.
    """
    click.echo("Disk Partitions\n" + "=" * 50)
    
    partitions = psutil.disk_partitions()
    count = 0
    
    for partition in partitions:
        if count >= limit:
            break
            
        click.echo(f"\nDevice: {partition.device}")
        click.echo(f"  Mountpoint: {partition.mountpoint}")
        click.echo(f"  File system: {partition.fstype}")
        
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            click.echo(f"  Total: {usage.total / (1024**3):.2f} GB")
            click.echo(f"  Used: {usage.used / (1024**3):.2f} GB")
            click.echo(f"  Free: {usage.free / (1024**3):.2f} GB")
            click.echo(f"  Usage: {usage.percent}%")
            count += 1
        except PermissionError:
            click.echo(f"  (Permission denied)")
            continue
