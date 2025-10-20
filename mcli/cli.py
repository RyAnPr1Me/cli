#!/usr/bin/env python3
"""Main CLI interface for macOS CLI Tools."""

import click
from mcli.commands import files, network, system, process, utils, admin


@click.group()
@click.version_option(version="1.0.0")
@click.pass_context
def main(ctx):
    """macOS CLI Tools - A powerful user space CLI with useful features.
    
    This tool provides various utilities for file operations, network diagnostics,
    system information, process management, and more - all running in user space
    without requiring root privileges.
    """
    ctx.ensure_object(dict)


# Register command groups
main.add_command(admin.admin)
main.add_command(files.files)
main.add_command(network.network)
main.add_command(system.system)
main.add_command(process.process)
main.add_command(utils.utils)


if __name__ == "__main__":
    main()
