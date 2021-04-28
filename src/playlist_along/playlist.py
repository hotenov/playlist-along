"""Playlist module."""
from pathlib import Path
from typing import List, Optional

import click

from ._utils import detect_file_encoding


class PlsFile(object):
    """File object class."""

    def __init__(self, home: Optional[str] = None) -> None:
        """Initialization of class instance."""
        self.home: Path = Path(home or ".")


def display_tracks(file: Path, encoding: Optional[str] = None) -> None:
    """Display only tracks from playlist file."""
    only_paths = get_only_track_paths_from_m3u(file, encoding)
    click.echo("\n".join(only_paths))


def get_only_track_paths_from_m3u(
    path: Path, encoding: Optional[str] = None
) -> List[str]:
    """Return list of paths (without #M3U tags)."""
    if encoding is None:
        encoding = detect_file_encoding(path)
    playlist_content = path.read_text(encoding=encoding)
    only_paths = [
        line.strip() for line in playlist_content.splitlines() if line[0] != "#"
    ]
    return only_paths
