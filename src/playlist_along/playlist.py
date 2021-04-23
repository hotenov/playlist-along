"""Playlist module."""
from pathlib import Path
from typing import List, Optional

from playlist_along._utils import detect_file_encoding


def get_only_paths_from_m3u(path: Path, encoding: Optional[str] = None) -> List[str]:
    """Return list of paths (without #M3U tags)."""
    if encoding is None:
        encoding = detect_file_encoding(path)
    playlist_content = path.read_text(encoding=encoding)
    only_paths = [
        line.strip() for line in playlist_content.splitlines() if line[0] != "#"
    ]
    return only_paths
