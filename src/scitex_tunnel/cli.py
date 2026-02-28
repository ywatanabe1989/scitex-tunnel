#!/usr/bin/env python3
"""SciTeX Tunnel CLI - Manage persistent SSH reverse tunnels."""

import click

from . import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """Persistent SSH reverse tunnel for SciTeX (NAT traversal).

    Manage autossh-based reverse SSH tunnels for accessing machines
    behind NAT/firewalls via a bastion server.
    """


@main.command()
@click.option("-p", "--port", required=True, type=int, help="Remote port to forward.")
@click.option("-b", "--bastion", required=True, help="Bastion server hostname or IP.")
@click.option(
    "-s",
    "--secret-key",
    required=True,
    help="Path to SSH private key.",
    type=click.Path(exists=True),
)
def setup(port, bastion, secret_key):
    """Set up a persistent SSH reverse tunnel."""
    from . import setup as _setup

    result = _setup(port, bastion, secret_key)
    if result["success"]:
        click.secho(f"Tunnel on port {port} set up successfully.", fg="green")
        if result["stdout"]:
            click.echo(result["stdout"])
    else:
        click.secho(f"Failed to set up tunnel on port {port}.", fg="red", err=True)
        if result["stderr"]:
            click.echo(result["stderr"], err=True)
        raise SystemExit(1)


@main.command()
@click.option("-p", "--port", required=True, type=int, help="Port of tunnel to remove.")
def remove(port):
    """Remove a persistent SSH reverse tunnel."""
    from . import remove as _remove

    result = _remove(port)
    if result["success"]:
        click.secho(f"Tunnel on port {port} removed.", fg="green")
        if result["stdout"]:
            click.echo(result["stdout"])
    else:
        click.secho(f"Failed to remove tunnel on port {port}.", fg="red", err=True)
        if result["stderr"]:
            click.echo(result["stderr"], err=True)
        raise SystemExit(1)


@main.command()
@click.option(
    "-p",
    "--port",
    type=int,
    default=None,
    help="Specific port to check (default: all).",
)
def status(port):
    """Check status of SSH reverse tunnels."""
    from . import status as _status

    result = _status(port)
    click.echo(result["stdout"])
    if result["stderr"]:
        click.echo(result["stderr"], err=True)


# EOF
