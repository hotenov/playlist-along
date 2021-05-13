"""Playlist module."""
from pathlib import Path
import re
import shutil
from typing import List, Optional, Tuple

import click
from click.exceptions import ClickException

from ._utils import _detect_file_encoding


SONG_FORMATS: List[str] = [".mp3", ".flac"]


class Playlist(object):
    """Playlist object class."""

    def __init__(self, path: Optional[str] = None) -> None:
        """Initialization of class instance."""
        self.path: Path = Path(path or ".")


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


def get_full_content_of_playlist(path: Path) -> Tuple[str, str]:
    """Return full content (text) of a playlist."""
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
    with click.termui.progressbar(
        tracklist,
        label="Copying from playlist:",
    ) as bar:
        for abs_path in bar:  # type: ignore[attr-defined]
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
        click.utils.echo("Missing files from playlist were NOT copied:")
        click.utils.echo("\n".join(missing_files))
