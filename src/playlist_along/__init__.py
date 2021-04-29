"""Playlist Along."""
from pathlib import Path

from single_source import get_version

__version__ = get_version("fake-package", Path(__file__).parent.parent.parent)
