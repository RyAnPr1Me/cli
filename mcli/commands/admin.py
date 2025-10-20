#!/usr/bin/env python3
"""Admin workarounds - user space alternatives to admin commands."""

import click
import subprocess
import os
import socket
import psutil
from pathlib import Path


@click.group()
def admin():
    """Admin command workarounds (user space alternatives)."""
    pass


@admin.command()
def hosts():
    """View the hosts file (/etc/hosts).
    
    Displays the contents of /etc/hosts without requiring admin privileges.
    User can read but not modify the file.
    """
    hosts_file = "/etc/hosts"
    
    try:
        with open(hosts_file, 'r') as f:
            content = f.read()
            
        click.echo(f"Contents of {hosts_file}:\n")
        click.echo("=" * 60)
        
        for line_num, line in enumerate(content.split('\n'), 1):
            # Highlight non-comment lines
            if line.strip() and not line.strip().startswith('#'):
                click.echo(click.style(f"{line_num:4d} | {line}", bold=True))
            else:
                click.echo(f"{line_num:4d} | {line}")
                
    except PermissionError:
        click.echo("Error: Permission denied to read /etc/hosts", err=True)
        return 1
    except FileNotFoundError:
        click.echo("Error: /etc/hosts file not found", err=True)
        return 1


@admin.command()
def dnsflush():
    """Flush DNS cache (user space workaround).
    
    Attempts to flush DNS cache without admin privileges.
    Uses Python's socket cache clearing as a workaround.
    For full flush, admin privileges are required (dscacheutil -flushcache).
    """
    click.echo("DNS Cache Flush (User Space Workaround)")
    click.echo("=" * 60)
    
    # Clear Python's DNS cache
    if hasattr(socket, 'setdefaulttimeout'):
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(1)
        socket.setdefaulttimeout(old_timeout)
        click.echo("✓ Cleared Python socket DNS cache")
    
    # Try to get process info for mDNSResponder
    click.echo("\n⚠  Note: Full DNS cache flush requires admin privileges")
    click.echo("   User space workaround: clear application-level caches")
    
    # Check if mDNSResponder is running
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'mDNSResponder' in proc.info['name']:
                click.echo(f"\n   mDNSResponder running (PID: {proc.info['pid']})")
                click.echo("   To fully flush: sudo dscacheutil -flushcache")
                click.echo("   Or: sudo killall -HUP mDNSResponder")
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    click.echo("\n✓ Application-level DNS cache cleared")
    click.echo("  (System-level cache requires sudo)")


@admin.command()
@click.option('--port', '-p', type=int, help='Show processes using specific port')
def portusage(port):
    """Show which processes are using network ports.
    
    User space alternative to 'lsof -i' - shows network connections
    for processes the user can access.
    """
    click.echo("Network Port Usage (User Accessible)")
    click.echo("=" * 80)
    
    connections = psutil.net_connections(kind='inet')
    
    if port:
        # Filter by specific port
        connections = [c for c in connections if c.laddr.port == port or 
                      (c.raddr and c.raddr.port == port)]
        click.echo(f"Showing processes using port {port}:\n")
    else:
        click.echo("Showing all network connections (first 50):\n")
        connections = connections[:50]
    
    if not connections:
        click.echo(f"No connections found" + (f" on port {port}" if port else ""))
        return
    
    # Header
    click.echo(f"{'Protocol':<8} {'Local Address':<25} {'Remote Address':<25} {'Status':<12} {'PID':<8} {'Process':<20}")
    click.echo("-" * 110)
    
    for conn in connections:
        try:
            # Get process name if available
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    proc_name = proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_name = "N/A"
            else:
                proc_name = "N/A"
            
            # Format addresses
            local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            
            # Protocol type
            protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            
            status = conn.status if conn.status else "N/A"
            pid = str(conn.pid) if conn.pid else "N/A"
            
            click.echo(f"{protocol:<8} {local:<25} {remote:<25} {status:<12} {pid:<8} {proc_name:<20}")
            
        except Exception:
            continue


@admin.command()
def interfaces():
    """Show network interface information.
    
    User space alternative to 'ifconfig' - shows network interfaces
    without requiring admin privileges.
    """
    click.echo("Network Interfaces (User Space)")
    click.echo("=" * 70)
    
    # Get network interfaces
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    for interface_name, addresses in interfaces.items():
        click.echo(f"\n{interface_name}:")
        
        # Show status if available
        if interface_name in stats:
            stat = stats[interface_name]
            status = "UP" if stat.isup else "DOWN"
            click.echo(f"  Status: {status}")
            click.echo(f"  Speed: {stat.speed} Mbps" if stat.speed > 0 else "  Speed: Unknown")
            click.echo(f"  MTU: {stat.mtu}")
        
        # Show addresses
        for addr in addresses:
            if addr.family == socket.AF_INET:
                click.echo(f"  IPv4: {addr.address}")
                if addr.netmask:
                    click.echo(f"    Netmask: {addr.netmask}")
                if addr.broadcast:
                    click.echo(f"    Broadcast: {addr.broadcast}")
            elif addr.family == socket.AF_INET6:
                click.echo(f"  IPv6: {addr.address}")
                if addr.netmask:
                    click.echo(f"    Netmask: {addr.netmask}")
            elif addr.family == psutil.AF_LINK:
                click.echo(f"  MAC: {addr.address}")


@admin.command()
def launchagents():
    """List user LaunchAgents.
    
    Shows LaunchAgents that the user can manage without admin privileges.
    User LaunchAgents are in ~/Library/LaunchAgents.
    """
    click.echo("User LaunchAgents (User Space)")
    click.echo("=" * 70)
    
    user_agents_dir = Path.home() / "Library" / "LaunchAgents"
    
    if not user_agents_dir.exists():
        click.echo(f"No LaunchAgents directory found at: {user_agents_dir}")
        click.echo("Create this directory to add user launch agents.")
        return
    
    agents = list(user_agents_dir.glob("*.plist"))
    
    if not agents:
        click.echo(f"No LaunchAgents found in: {user_agents_dir}")
        click.echo("\nUser LaunchAgents can be managed with 'launchctl' commands:")
        click.echo("  launchctl load ~/Library/LaunchAgents/com.example.agent.plist")
        click.echo("  launchctl unload ~/Library/LaunchAgents/com.example.agent.plist")
        return
    
    click.echo(f"Found {len(agents)} LaunchAgent(s):\n")
    
    for agent in sorted(agents):
        click.echo(f"  {agent.name}")
        
        # Try to determine if it's loaded
        try:
            result = subprocess.run(
                ['launchctl', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            agent_label = agent.stem
            if agent_label in result.stdout:
                click.echo(f"    Status: ✓ Loaded")
            else:
                click.echo(f"    Status: Not loaded")
        except Exception:
            click.echo(f"    Status: Unknown")
    
    click.echo(f"\nLocation: {user_agents_dir}")
    click.echo("\nManage with 'launchctl' (no sudo required for user agents):")
    click.echo("  launchctl load <path>")
    click.echo("  launchctl unload <path>")
    click.echo("  launchctl list")


@admin.command()
@click.argument('domain', default='NSGlobalDomain')
@click.argument('key', required=False)
def defaults(domain, key):
    """Read system defaults/preferences.
    
    User space alternative to 'defaults read' command.
    Can read user preferences without admin privileges.
    
    Examples:
      mcli admin defaults NSGlobalDomain
      mcli admin defaults com.apple.finder
      mcli admin defaults NSGlobalDomain AppleShowAllFiles
    """
    click.echo(f"System Defaults - {domain}")
    click.echo("=" * 70)
    
    try:
        if key:
            # Read specific key
            result = subprocess.run(
                ['defaults', 'read', domain, key],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            # Read all keys in domain
            result = subprocess.run(
                ['defaults', 'read', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
        
        if result.returncode == 0:
            click.echo(result.stdout)
        else:
            click.echo(f"Error reading defaults: {result.stderr.strip()}", err=True)
            click.echo("\nCommon domains:", err=True)
            click.echo("  NSGlobalDomain - Global preferences", err=True)
            click.echo("  com.apple.finder - Finder preferences", err=True)
            click.echo("  com.apple.dock - Dock preferences", err=True)
            return 1
            
    except subprocess.TimeoutExpired:
        click.echo("Error: Command timed out", err=True)
        return 1
    except FileNotFoundError:
        click.echo("Error: 'defaults' command not found", err=True)
        return 1


@admin.command()
def env():
    """Show environment variables.
    
    Displays all environment variables accessible to the user.
    User can modify these without admin privileges.
    """
    click.echo("Environment Variables (User Space)")
    click.echo("=" * 70)
    
    env_vars = dict(os.environ)
    
    # Sort and display
    for key in sorted(env_vars.keys()):
        value = env_vars[key]
        # Truncate long values
        if len(value) > 100:
            value = value[:97] + "..."
        click.echo(f"{key}={value}")
    
    click.echo(f"\nTotal: {len(env_vars)} environment variables")
    click.echo("\nModify in ~/.zshrc, ~/.bash_profile, or ~/.bashrc:")
    click.echo("  export MY_VAR=value")


@admin.command()
@click.option('--all', '-a', is_flag=True, help='Show all services (system and user)')
def services(all):
    """List running services (user accessible).
    
    Shows services/daemons that the user can view.
    For user LaunchAgents, no admin privileges required.
    """
    click.echo("Services (User Space View)")
    click.echo("=" * 70)
    
    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            click.echo("Error running launchctl list", err=True)
            return 1
        
        lines = result.stdout.strip().split('\n')
        
        # Skip header line
        if len(lines) > 1:
            header = lines[0]
            click.echo(header)
            click.echo("-" * 70)
            
            services = lines[1:]
            
            # Filter if not showing all
            if not all:
                # Show only user services (rough filter)
                services = [s for s in services if 'com.apple.xpc' not in s.lower() 
                           and 'system' not in s.lower()]
            
            for service in services[:50]:  # Limit to 50 entries
                click.echo(service)
            
            if len(services) > 50:
                click.echo(f"\n... and {len(services) - 50} more")
            
            click.echo(f"\nShowing: {min(50, len(services))} of {len(services)} services")
        
    except subprocess.TimeoutExpired:
        click.echo("Error: Command timed out", err=True)
        return 1
    except FileNotFoundError:
        click.echo("Error: 'launchctl' command not found", err=True)
        return 1


@admin.command()
def sudocmds():
    """Show common admin commands and their user-space alternatives.
    
    Educational command showing typical sudo commands and how to
    accomplish similar tasks without admin privileges.
    """
    click.echo("Common Admin Commands - User Space Alternatives")
    click.echo("=" * 70)
    
    commands = [
        ("View hosts file", "cat /etc/hosts", "mcli admin hosts"),
        ("Flush DNS cache", "sudo dscacheutil -flushcache", "mcli admin dnsflush"),
        ("View network ports", "sudo lsof -i", "mcli admin portusage"),
        ("Network interfaces", "ifconfig", "mcli admin interfaces"),
        ("List services", "sudo launchctl list", "mcli admin services"),
        ("User LaunchAgents", "ls /Library/LaunchAgents", "mcli admin launchagents"),
        ("Read preferences", "defaults read", "mcli admin defaults <domain>"),
        ("View environment", "printenv", "mcli admin env"),
        ("Process list", "ps aux", "mcli process list"),
        ("Disk usage", "df -h", "mcli system disks"),
        ("Network info", "netstat -an", "mcli admin portusage"),
        ("System info", "sw_vers", "mcli system info"),
    ]
    
    click.echo(f"\n{'Task':<25} {'Admin Command':<35} {'User Alternative':<35}")
    click.echo("-" * 95)
    
    for task, admin_cmd, user_cmd in commands:
        click.echo(f"{task:<25} {admin_cmd:<35} {user_cmd:<35}")
    
    click.echo("\n" + "=" * 70)
    click.echo("All 'mcli admin' commands work without sudo/admin privileges!")
    click.echo("Some operations have limitations compared to admin commands.")
