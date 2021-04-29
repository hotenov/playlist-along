"""CLI commands and functions."""
from pathlib import Path
from typing import Any, Optional, Union

import click
from click import Context, Option, Parameter

from playlist_along import __version__
from . import playlist
from .playlist import Playlist


# Decorator for passing path to playlist file
pass_playlist = click.make_pass_decorator(Playlist, ensure=True)


def echo_tracks_with_click(file: Path, encoding: Optional[str] = None) -> None:
    """Display only tracks from playlist file via click.echo()."""
    only_paths = playlist.get_only_track_paths_from_m3u(file, encoding)
    click.echo("\n".join(only_paths))


def validate_file_callback(
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


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.version_option(version=__version__)
@click.option(
    "--file",
    "-f",
    type=str,
    callback=validate_file_callback,
    is_eager=True,
    help="Full path to playlist file.",
    metavar="<string>",
)
@click.pass_context
def cli(ctx: Context, file: str) -> None:
    """Playlist Along - a CLI for playlist processing."""
    ctx.obj = Playlist(file)

    if file is None:
        click.echo("No file for script. Try 'playlist-along --help' for help.")
        ctx.exit()
    else:
        if ctx.invoked_subcommand is None:
            echo_tracks_with_click(Path(file))


@cli.command()
@pass_playlist
def display(pls_obj: Playlist) -> None:
    """Displays tracks from playlist."""
    file: Path = pls_obj.path
    echo_tracks_with_click(file)
