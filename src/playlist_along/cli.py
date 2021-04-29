"""CLI commands and functions."""
from pathlib import Path
from typing import Any, Union

import click
from click import Context, Option, Parameter

from playlist_along import __version__
from . import playlist


def validate_formats(
    ctx: Context, param: Union[Option, Parameter], value: Any = None
) -> Any:
    """Validate supported playlist formats."""
    # For script running without parameters
    if not value or ctx.resilient_parsing:
        return
    supported_formats = [".m3u", ".m3u8"]
    if Path(value).suffix in supported_formats:
        return value
    else:
        raise click.BadParameter(
            "currently we are supporting only these formats: %s" % supported_formats
        )


# Decorator for passing path to playlist file
pass_file = click.make_pass_decorator(playlist.PlsFile, ensure=True)


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.version_option(version=__version__)
@click.option(
    "--file",
    "-f",
    type=str,
    callback=validate_formats,
    is_eager=True,
)
@click.pass_context
def cli(ctx: Context, file: str) -> None:
    """Playlist Along."""
    ctx.obj = playlist.PlsFile(file)

    if file is None:
        click.echo("No file for script. Try 'playlist-along --help' for help.")
        ctx.exit()
    else:
        if ctx.invoked_subcommand is None:
            playlist.display_tracks(Path(file))


@cli.command()
@pass_file
def display(pls_file: playlist.PlsFile) -> None:
    """Display command."""
    file: Path = pls_file.home
    playlist.display_tracks(file)
