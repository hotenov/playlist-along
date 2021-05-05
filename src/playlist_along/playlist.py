"""Playlist module."""
from pathlib import Path
import re
from typing import List, Optional, Tuple

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
    only_paths = get_tracks_without_comment_lines(playlist_content)
    return only_paths


def get_tracks_without_comment_lines(playlist_content: str) -> List[str]:
    """Return list of tracks."""
    only_tracks: List[str] = [
        line.strip()
        for line in playlist_content.splitlines()
        if Path(line).suffix in SONG_FORMATS
    ]
    return only_tracks


def get_playlist_for_vlc_android(path: Path) -> Tuple[str, str]:
    """Return coverted playlist and its encoding."""
    encoding = _detect_file_encoding(path)
    playlist_content = path.read_text(encoding=encoding)

    # Pattern for matching line into two groups:
    # group 1 - all text before last backward or forward slash (including it)
    # group 2 - filename (with extension)
    regex_pattern = r"(.*[\\|\/])(.*)"

    relative_playlist = re.sub(regex_pattern, r"\2", playlist_content)

    # VLC for Android player does NOT understand square brackets [] and # in filenames
    adapted_content = substitute_vlc_invalid_characters(relative_playlist)

    return adapted_content, encoding


def substitute_vlc_invalid_characters(content: str) -> str:
    """Substitute [ and ] and # in filenames."""
    adapted_content: str = ""
    for line in content.splitlines():
        # Replace characters only in filenames (not in comments)
        if Path(line).suffix in SONG_FORMATS:
            line = re.sub(r"[\[]", "%5B", line)
            line = re.sub(r"[\]]", "%5D", line)
            line = re.sub(r"[#]", "%23", line)
        adapted_content += line + "\n"

    return adapted_content
