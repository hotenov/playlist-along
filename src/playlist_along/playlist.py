"""Playlist module."""
from pathlib import Path
import re
import shutil
from typing import Any, List, Optional, Tuple, Union

import click
from click import ClickException, Context, Option, Parameter

from ._utils import _detect_file_encoding


SUPPORTED_PLS_FILES: List[str] = [".m3u", ".m3u8"]
SONG_FORMATS: List[str] = [".mp3", ".flac"]


class Playlist(object):
    """Playlist object class."""

    def __init__(self, path: Optional[str] = None) -> None:
        """Initialization of class instance."""
        self.path: Path = Path(path or ".")


# Decorator for passing path to playlist file
pass_playlist = click.make_pass_decorator(Playlist, ensure=True)


def validate_file_callback(
    ctx: Context, param: Union[Option, Parameter], value: Any = None
) -> Any:
    """Validate supported playlist formats."""
    # For script running without parameters
    if not value or ctx.resilient_parsing:
        return
    supported_formats = SUPPORTED_PLS_FILES
    if Path(value).suffix in supported_formats:
        return value
    else:
        raise click.BadParameter(
            "currently we are supporting only these formats: %s" % supported_formats
        )


def get_only_track_paths_from_m3u(
    path: Path, encoding: Optional[str] = None
) -> List[str]:
    """Return list of paths (without #M3U tags)."""
    if encoding is None:
        encoding = _detect_file_encoding(path)
    playlist_content = path.read_text(encoding=encoding)
    only_paths = get_local_tracks_without_comment_lines(playlist_content)
    return only_paths


def get_local_tracks_without_comment_lines(playlist_content: str) -> List[str]:
    """Return list of tracks."""
    only_tracks: List[str] = [
        line.strip()
        for line in playlist_content.splitlines()
        if Path(line).suffix in SONG_FORMATS and "://" not in line
    ]
    return only_tracks


def get_full_content_of_playlist(
    path: Path, encoding: Optional[str] = None
) -> Tuple[str, str]:
    """Return full content (text) of a playlist."""
    if encoding is None:
        encoding = _detect_file_encoding(path)
    try:
        playlist_content = path.read_text(encoding=encoding)
    except (OSError) as error:
        message = str(error)
        raise ClickException(message)
    return playlist_content, encoding


def get_playlist_for_vlc_android(path: Path) -> Tuple[str, str]:
    """Return coverted playlist and its encoding."""
    playlist_content, encoding = get_full_content_of_playlist(path)
    playlist_content = clean_m3u_from_links(playlist_content)
    relative_playlist = make_relatives_paths_in_playlist(playlist_content)
    # VLC for Android player does NOT understand square brackets [] and # in filenames
    adapted_content = substitute_vlc_invalid_characters(relative_playlist)
    return adapted_content, encoding


def clean_m3u_from_links(content: str) -> str:
    """Delete lines with any links."""
    lines_without_links = [
        line.strip() for line in content.splitlines() if "://" not in line
    ]
    clean_content: str = "\n".join(lines_without_links)
    return clean_content


def clean_m3u_from_extended_tag(content: str) -> str:
    """Remove #EXTM3U and empty lines."""
    clean_content = content.strip()
    if clean_content[:8] == "#EXTM3U\n":
        clean_content = clean_content[len("#EXTM3U\n"):]
    return clean_content.strip()


def make_relatives_paths_in_playlist(content: str) -> str:
    """Remain only filenames from absolute paths."""
    # Pattern for matching line into two groups:
    # group 1 - all text before last backward or forward slash (including it)
    # group 2 - filename (with extension)
    regex_pattern = r"(.*[\\|\/])(.*)"
    relative_playlist = re.sub(regex_pattern, r"\2", content)
    return relative_playlist


def substitute_vlc_invalid_characters(content: str) -> str:
    """Substitute [ and ] and # in filenames."""
    adapted_content: str = ""
    for line in content.splitlines():
        # Replace characters only in filenames (not in comments)
        if Path(line).suffix in SONG_FORMATS:
            line = re.sub(r"[\[]", "%5B", line)
            line = re.sub(r"[\]]", "%5D", line)
            line = re.sub(r"[#]", "%23", line)
        adapted_content += line.strip() + "\n"

    return adapted_content


def save_playlist_content(
    content: str,
    dest: Path,
    encoding: Optional[str] = None,
    origin: Optional[Path] = None,
    yes_dir: Optional[bool] = None,
) -> None:
    """Save playlist content to new destination."""
    target_pls: Path
    if encoding is None:
        encoding = "utf-8"
    try:
        if (not dest.suffix or yes_dir) and origin:
            target_pls = dest / origin.name
        else:
            target_pls = dest
        if origin:
            if target_pls.resolve() == origin.resolve():
                suffix = target_pls.suffix
                new_name = str(target_pls.resolve().with_suffix("")) + "_vlc" + suffix
                target_pls = Path(new_name)

        target_pls.parent.mkdir(parents=True, exist_ok=True)
        target_pls.write_text(content, encoding)
    except (OSError) as error:
        message = str(error)
        raise ClickException(message)


def copy_local_tracks_to_folder(tracklist: List[str], dest: str) -> None:
    """Copy local files from list to a new destination."""
    destination: Path = Path(dest)
    missing_files: List[str] = []
    file_destination: Path
    if not destination.is_dir():
        destination = destination.parent
    with click.progressbar(
        tracklist,
        label="Copying from playlist:",
    ) as bar:
        for abs_path in bar:
            if not Path(abs_path).exists():
                missing_files.append(abs_path)
            else:
                name_only = Path(abs_path).name
                file_destination = destination / name_only
                if not file_destination.exists():
                    try:
                        shutil.copy2(Path(abs_path), destination)
                    except (OSError) as error:
                        message = str(error)
                        raise ClickException(message)
    if missing_files:
        click.echo("Missing files from playlist were NOT copied:")
        click.echo("\n".join(missing_files))


def is_file_too_small(file: Path) -> bool:
    """Return True if file is less than 7 bytes."""
    try:
        if file.stat().st_size > 7:
            return False
        else:
            return True
    except (OSError) as error:
        message = str(error)
        raise ClickException(message)
