"""Unit-tests for the playlist module."""
from pathlib import Path

from click.testing import CliRunner

from playlist_along import playlist


def test_playlist_passing_cyrillic_encoding(runner: CliRunner) -> None:
    """It prints tracklist with 'cp1251' encoding."""
    with runner.isolated_filesystem():
        with open("tiny.m3u", "w", encoding="cp1251") as f:
            f.write(
                """Кирилл - Track_01!.mp3
            Мефодий - Track_02!.mp3
            """
            )
        only_paths = playlist.get_only_track_paths_from_m3u(Path("tiny.m3u"), "cp1251")
        result = "\n".join(only_paths)
        assert result == "Кирилл - Track_01!.mp3\nМефодий - Track_02!.mp3"
