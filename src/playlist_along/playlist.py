"""Playlist module."""
from pathlib import Path
from typing import List, Optional

from ._utils import _detect_file_encoding


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
    only_paths = [
        line.strip() for line in playlist_content.splitlines() if line[0] != "#"
    ]
    return only_paths
