"""CLI commands and functions."""
from pathlib import Path
from typing import Any, List, Optional, Union

import click
from click.core import Context, Option, Parameter

from playlist_along import __version__
from . import playlist
from .playlist import Playlist


# Decorator for passing path to playlist file
pass_playlist = click.decorators.make_pass_decorator(Playlist, ensure=True)


def echo_tracks_with_click(file: Path, encoding: Optional[str] = None) -> None:
    """Display only tracks from playlist file via click.echo()."""
    only_paths = playlist.get_only_track_paths_from_m3u(file, encoding)
    click.utils.echo("\n".join(only_paths))


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
        raise click.exceptions.BadParameter(
            "currently we are supporting only these formats: %s" % supported_formats
        )


@click.decorators.group(
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.decorators.version_option(version=__version__)
@click.decorators.option(
    "--file",
    "-f",
    type=str,
    callback=validate_file_callback,
    is_eager=True,
    help="Full path to playlist file.",
    metavar="<string>",
)
@click.decorators.pass_context
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


@cli.command()
@click.decorators.option(
    "--dest",
    "-d",
    type=str,
    help="Directory or full path to playlist destination.",
    metavar="<string>",
)
@click.decorators.option(
    "--copy",
    is_flag=True,
    help="Copy files from playlist.",
)
@click.decorators.option(
    "--dir",
    "yes_dir",
    is_flag=True,
    help="Tells script that destination is a dir, not a file (for directory name with '.' dot).",
)
@pass_playlist
def convert(pls_obj: Playlist, dest: str, yes_dir: bool, copy: bool) -> None:
    """Converts playlist from one player to another."""
    file: Path = pls_obj.path
    convert_from_aimp_to_vlc_android(file, dest, yes_dir)
    if copy:
        copy_files_from_playlist_to_destination_folder(file, dest)


def convert_from_aimp_to_vlc_android(file: Path, dest: str, yes_dir: bool) -> None:
    """Converts AIMP playlist to VLC for Android."""
    converted_pls, encoding = playlist.get_playlist_for_vlc_android(file)
    playlist.save_playlist_content(converted_pls, Path(dest), encoding, file, yes_dir)


def copy_files_from_playlist_to_destination_folder(file: Path, dest: str) -> None:
    """Copy tracks from playlist to folder with converted playlist."""
    content, encoding = playlist.get_full_content_of_playlist(file)
    only_tracks: List[str] = playlist.get_local_tracks_without_comment_lines(content)
    playlist.copy_local_tracks_to_folder(only_tracks, dest)


if __name__ == "__main__":
    cli()  # pragma: no cover
