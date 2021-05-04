"""Playlist Along."""
from pathlib import Path

from single_source import get_version

pyproject_name = "pyproject.toml"
path_to_project_dir = Path(__file__).parent.parent.parent
target_path = path_to_project_dir
target_path /= pyproject_name

if target_path.exists():
    __version__ = get_version("fake-package", path_to_project_dir)  # pragma: no cover
else:
    __version__ = get_version(__name__, Path(__file__).parent)
