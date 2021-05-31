"""Create command."""
from pathlib import Path
from typing import Iterator, List, Tuple


import click
import mutagen
from natsort import os_sorted

from .. import playlist
from ..playlist import pass_playlist, Playlist, SONG_FORMATS


@click.command(name="create")
@click.option(
    "--from",
    "-f",
    "from_",
    type=str,
    help="Folder with audio files.",
    metavar="<string>",
)
@click.option(
    "--nat-sort",
    "nat_sort",
    is_flag=True,
    help="Use 'natural sort order' for list of audio files.",
)
@click.option(
    "--rel/--abs",
    default=True,
    help="Paths in playlist are relative or absolute.",
)
@click.option(
    "--ext-m3u",
    "extended",
    is_flag=True,
    help="Generate extended M3U playlist.",
)
@click.option(
    "--here",
    "is_here",
    is_flag=True,
    help=(
        "Save playlist in folder with audio files, "
        "taking only name from main '--file' option."
    ),
)
@click.option(
    "--empty",
    "is_empty",
    is_flag=True,
    help="Create an empty playlist file and exit.",
)
@click.option(
    "--reverse",
    "-REV",
    "is_reversed",
    is_flag=True,
    help="Reverse the order of playlist.",
)
@pass_playlist
def create_cmd(
    pls_obj: Playlist,
    from_: str,
    rel: bool,
    extended: bool,
    nat_sort: bool,
    is_here: bool,
    is_empty: bool,
    is_reversed: bool,
) -> None:
    """Creates playlist from folder or from scratch."""
    pls_path: Path = pls_obj.path

    if is_empty:
        # Create an empty playlist file and exit.
        pls_path.write_text("")
        click.get_current_context().exit()

    dir: Path = Path(from_)
    playlist_as_text: str = ""

    try:
        if dir.is_dir():
            valid_files: List[Path] = []
            valid_files = get_supported_audios_in_folder(dir)

            if not valid_files:
                click.echo(f"Warning: No supported audio files in folder '{str(dir)}'.")
                click.get_current_context().exit()

            sorted_rel: List[str] = []
            sorted_abs: List[str] = []
            rel_paths = [f.name for f in valid_files]
            abs_paths = [str(f.resolve()) for f in valid_files]

            if nat_sort:
                sorted_rel, sorted_abs = os_sorted(rel_paths), os_sorted(abs_paths)
            else:
                sorted_rel, sorted_abs = sorted(rel_paths), sorted(abs_paths)

            if is_reversed:
                sorted_rel.reverse()
                sorted_abs.reverse()

            zipped_paths = zip(sorted_rel, sorted_abs)

            playlist_as_text = generate_playlist_content_from_zipped(
                zipped_paths, extended, rel
            )

            target_file: Path = Path()
            if is_here:
                playlist_name = pls_path.name
                target_file = Path(dir, Path(playlist_name))
            else:
                target_file = pls_path
            playlist.save_playlist_content(playlist_as_text, target_file)

        else:
            click.echo(f"Error: This directory '{str(dir)}' does NOT exist.")
            click.get_current_context().exit()
    except (OSError) as error:
        message = str(error)
        raise click.ClickException(message)


def get_supported_audios_in_folder(dir: Path) -> List[Path]:
    """Explore folder and pick up supported audios."""
    valid_files_in_dir: List[Path] = []
    valid_files_in_dir = [
        p.resolve() for p in dir.glob("*") if p.suffix.lower() in set(SONG_FORMATS)
    ]
    return valid_files_in_dir


def generate_playlist_content_from_zipped(
    zip_rel_abs: Iterator[Tuple[str, str]],
    extended: bool,
    rel: bool,
) -> str:
    """Return string content for playlist.

    From zip(relative, absolute).
    """
    content: str = ""
    for i, (rel_p, abs_p) in enumerate(zip_rel_abs, start=1):
        if extended:
            # Add header tag at the beginning
            if i == 1:
                content += "#EXTM3U" + "\n"
            length_sec: int = 0
            try:
                length_sec = get_seconds_from_file_info(abs_p)
            except Exception:
                length_sec = 0
            content += "#EXTINF:" + str(length_sec) + "," + Path(abs_p).stem + "\n"
        if rel:
            content += rel_p + "\n"
        else:
            content += abs_p + "\n"
    return content


def get_seconds_from_file_info(path: str) -> int:
    """Get audio length in seconds (rounded)."""
    audio = mutagen.File(path)
    length = audio.info.length
    seconds = round(length)
    return seconds
