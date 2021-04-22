"""CLI commands."""
from pathlib import Path

import click

from playlist_along import playlist


def display_tracks(file: Path, encoding: str = None) -> None:
    """Display only tracks from playlist file."""
    only_paths = playlist.get_only_paths_from_m3u(Path(file), encoding)
    click.echo("\n".join(only_paths))


def validate_formats(ctx, param, value):
    """Validate supported playlist formats."""
    supported_formats = [".m3u", ".m3u8"]
    if Path(value).suffix not in supported_formats:
        raise click.BadParameter(
            "currently we supported only these formats: %s" % supported_formats
        )
    else:
        return value


@click.group(invoke_without_command=True)
@click.option(
    "--file",
    "-f",
    callback=validate_formats,
)
@click.pass_context
def cli(ctx, file):
    """Group of commands."""
    ctx.ensure_object(dict)
    ctx.obj["FILE"] = file
    if ctx.invoked_subcommand is None:
        display_tracks(Path(file))


@cli.command()
@click.pass_context
def display(ctx):
    """Display command."""
    display_tracks(Path(ctx.obj["FILE"]))
