"""CLI commands and functions."""
from pathlib import Path

import click
from click import Context, Option

from . import playlist


def display_tracks(file: Path, encoding: str = None) -> None:
    """Display only tracks from playlist file."""
    only_paths = playlist.get_only_paths_from_m3u(Path(file), encoding)
    click.echo("\n".join(only_paths))


def validate_formats(ctx: Context, param: Option, value: str) -> str:
    """Validate supported playlist formats."""
    # For script running without parameters
    if not value:
        return
    supported_formats = [".m3u", ".m3u8"]
    if Path(value).suffix in supported_formats:
        return value
    else:
        raise click.BadParameter(
            "currently we supported only these formats: %s" % supported_formats
        )


@click.command()
@click.pass_context
def display(ctx: Context) -> None:
    """Display command."""
    display_tracks(Path(ctx.obj["FILE"]))
