"""Unit-tests for the playlist module."""
from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture

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


@pytest.fixture
def mock_pathlib_write_text(mocker: MockFixture) -> Mock:
    """Fixture for mocking wikipedia.random_page."""
    pathlib_write_text: Mock = mocker.patch("pathlib.Path.write_text")
    return pathlib_write_text


def test_saving_playlist_with__default_encoding(
    runner: CliRunner,
    mock_pathlib_write_text: Mock,
) -> None:
    """It returns default encoding if it was not passed."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """D:\\tmp\\tmp_flack\\First [track!].flac
            /home/user/Downloads/#Second Track!.mp3
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        target_file = temp_folder / "temp_converted.m3u"
        temp_content = Path("temp.m3u").read_text()
        playlist.save_playlist_content(temp_content, target_file)
        mock_pathlib_write_text.assert_called_once_with(temp_content, "utf-8")
