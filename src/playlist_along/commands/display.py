"""Display command."""
from pathlib import Path
from typing import Optional

import click

from .. import playlist
from ..playlist import pass_playlist, Playlist


@click.command(name="display")
@pass_playlist
def display_cmd(pls_obj: Playlist) -> None:
    """Displays tracks from playlist."""
    file: Path = pls_obj.path
    if playlist.is_file_too_small(file):
        click.echo("Warning: Playlist is too small to display. Exit.")
        click.get_current_context().exit()
    else:
        echo_tracks_with_click(file)


def echo_tracks_with_click(file: Path, encoding: Optional[str] = None) -> None:
    """Display only tracks from playlist file via click.echo()."""
    only_paths = playlist.get_only_track_paths_from_m3u(file, encoding)
    click.echo("\n".join(only_paths))
