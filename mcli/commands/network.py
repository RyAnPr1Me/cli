#!/usr/bin/env python3
"""Network utilities commands."""

import socket
import click
import time
import requests
from urllib.parse import urlparse


@click.group()
def network():
    """Network diagnostics and utilities."""
    pass


@network.command()
@click.argument('host')
@click.argument('port', type=int)
@click.option('--timeout', default=3, help='Connection timeout in seconds')
def checkport(host, port, timeout):
    """Check if a port is open on a host.
    
    Tests TCP connectivity to the specified host and port.
    Useful for checking if services are running and accessible.
    """
    click.echo(f"Checking {host}:{port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            click.echo(f"✓ Port {port} is OPEN on {host}")
            return 0
        else:
            click.echo(f"✗ Port {port} is CLOSED on {host}")
            return 1
    except socket.gaierror:
        click.echo(f"✗ Could not resolve hostname: {host}", err=True)
        return 1
    except socket.timeout:
        click.echo(f"✗ Connection timed out", err=True)
        return 1
    finally:
        sock.close()


@network.command()
@click.option('--count', default=5, help='Number of requests to make')
@click.option('--url', default='https://www.google.com', help='URL to test')
def speedtest(count, url):
    """Simple network speed test.
    
    Makes multiple requests to a URL and measures response times.
    Provides min, max, and average latency statistics.
    """
    click.echo(f"Testing network speed to: {url}")
    click.echo(f"Making {count} requests...\n")
    
    times = []
    successful = 0
    
    for i in range(count):
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            
            if response.status_code == 200:
                times.append(elapsed)
                successful += 1
                click.echo(f"Request {i+1}: {elapsed:.2f} ms (status: {response.status_code})")
            else:
                click.echo(f"Request {i+1}: Failed (status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            click.echo(f"Request {i+1}: Failed ({str(e)})")
    
    if times:
        click.echo(f"\nResults:")
        click.echo(f"  Successful: {successful}/{count}")
        click.echo(f"  Min: {min(times):.2f} ms")
        click.echo(f"  Max: {max(times):.2f} ms")
        click.echo(f"  Avg: {sum(times)/len(times):.2f} ms")
    else:
        click.echo("\n✗ All requests failed")


@network.command()
@click.argument('hostname')
def lookup(hostname):
    """DNS lookup for a hostname.
    
    Resolves a hostname to its IP address(es).
    Works entirely in user space without special privileges.
    """
    click.echo(f"Looking up: {hostname}\n")
    
    try:
        # Get all IP addresses
        addresses = socket.getaddrinfo(hostname, None)
        
        ipv4_addresses = set()
        ipv6_addresses = set()
        
        for addr in addresses:
            ip = addr[4][0]
            if ':' in ip:
                ipv6_addresses.add(ip)
            else:
                ipv4_addresses.add(ip)
        
        if ipv4_addresses:
            click.echo("IPv4 addresses:")
            for ip in sorted(ipv4_addresses):
                click.echo(f"  {ip}")
        
        if ipv6_addresses:
            click.echo("\nIPv6 addresses:")
            for ip in sorted(ipv6_addresses):
                click.echo(f"  {ip}")
        
        if not ipv4_addresses and not ipv6_addresses:
            click.echo("No addresses found")
            
    except socket.gaierror as e:
        click.echo(f"✗ Failed to resolve {hostname}: {e}", err=True)
        return 1


@network.command()
@click.argument('start_port', type=int)
@click.argument('end_port', type=int)
@click.option('--host', default='127.0.0.1', help='Host to scan (default: localhost)')
def portscan(start_port, end_port, host):
    """Scan a range of ports on a host.
    
    Checks which ports are open in the specified range.
    Useful for local service discovery.
    """
    if start_port > end_port:
        click.echo("Error: start_port must be less than or equal to end_port", err=True)
        return 1
    
    if end_port > 65535:
        click.echo("Error: end_port must be less than or equal to 65535", err=True)
        return 1
    
    click.echo(f"Scanning ports {start_port}-{end_port} on {host}...\n")
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                click.echo(f"✓ Port {port} is OPEN")
        except:
            pass
        finally:
            sock.close()
    
    click.echo(f"\nScan complete. Found {len(open_ports)} open port(s).")
