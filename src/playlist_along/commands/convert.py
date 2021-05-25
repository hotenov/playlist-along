"""Convert command."""
from pathlib import Path
from typing import List

import click

from .. import playlist
from ..playlist import pass_playlist, Playlist


@click.command(name="convert")
@click.option(
    "--dest",
    "-d",
    type=str,
    help="Directory or full path to playlist destination.",
    metavar="<string>",
)
@click.option(
    "--copy",
    is_flag=True,
    help="Copy files from playlist.",
)
@click.option(
    "--dir",
    "yes_dir",
    is_flag=True,
    help="Tells script that destination is a dir, not a file (for directory name with '.' dot).",
)
@pass_playlist
def convert_cmd(pls_obj: Playlist, dest: str, yes_dir: bool, copy: bool) -> None:
    """Converts playlist from one player to another."""
    file: Path = pls_obj.path
    if playlist.is_file_too_small(file):
        click.echo("Warning: Playlist is too small to convert. Exit.")
        click.get_current_context().exit()
    else:
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
