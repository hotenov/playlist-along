"""Unit-tests for the playlist module."""
from pathlib import Path
from unittest.mock import Mock

from click import ClickException
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
    """Fixture for mocking pathlib.Path.write_text."""
    pathlib_write_text: Mock = mocker.patch("pathlib.Path.write_text")
    return pathlib_write_text


def test_saving_playlist_with_default_encoding(
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


def test_playlist_fails_on_writing_with_wrong_path_error() -> None:
    """It raises ClickException if the playlist writing fails with wrong path."""
    content = "ClickException if The filename, directory name, or volume label syntax is incorrect."
    dest = Path("/::WrongPath.m3u")
    with pytest.raises(ClickException) as exc_info:
        playlist.save_playlist_content(content, dest)
    assert exc_info.typename == "ClickException"


def test_playlist_fails_on_writing_with_permission_error(runner: CliRunner) -> None:
    """It raises ClickException if the playlist writing fails with 'Permission denied'."""
    content = "ClickException if Permission denied:"
    with runner.isolated_filesystem():
        temp_folder = Path("folder.m3u").resolve()
        # Create a folder, not a file
        temp_folder.mkdir(parents=True, exist_ok=True)

        with pytest.raises(ClickException) as exc_info:
            # Try to write to a folder
            playlist.save_playlist_content(content, temp_folder)
        assert exc_info.typename == "ClickException"


@pytest.fixture
def mock_playlist_detect_file_encoding(mocker: MockFixture) -> Mock:
    """Fixture for mocking _detect_file_encoding called from playlist."""
    detect_file_encoding: Mock = mocker.patch(
        "playlist_along.playlist._detect_file_encoding"
    )
    return detect_file_encoding


def test_playlist_fails_on_reading_error(
    runner: CliRunner,
    mock_playlist_detect_file_encoding: Mock,
) -> None:
    """It raises ClickException if the playlist reading fails.

    Even after successful encoding detection.
    """
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """D:\\tmp\\tmp_flack\\First [track!].flac
            /home/user/Downloads/#Second Track!.mp3
            """
            )
        temp_file = Path("temp.m3u").resolve()
        mock_playlist_detect_file_encoding.return_value = "utf-8"
        # Delete file
        temp_file.unlink()
        with pytest.raises(ClickException) as exc_info:
            playlist.get_full_content_of_playlist(temp_file)
        assert exc_info.typename == "ClickException"


def test_playlist_substitutes_invalid_characters() -> None:
    """It substitutes [ and ] and # in passed text."""
    text = """Track - [01].mp3
    #Track# - 02].flac
    """
    substituted = playlist.substitute_vlc_invalid_characters(text)
    expected = "Track - %5B01%5D.mp3\n%23Track%23 - 02%5D.flac\n\n"
    assert expected == substituted


def test_removing_extended_tag_from_playlist() -> None:
    """It removes #EXTM3U tag from playlist content."""
    content = "\n\n#EXTM3U\nExpected Line\n\n"
    cleaned = playlist.clean_m3u_from_extended_tag(content)
    expected = "Expected Line"
    assert expected == cleaned

    content_without = "\n\nC:\\temp\\Expected Line.mp3\n\n"
    cleaned = playlist.clean_m3u_from_extended_tag(content_without)
    expected = r"C:\temp\Expected Line.mp3"
    assert expected == cleaned


@pytest.fixture
def mock_pathlib_read_text(mocker: MockFixture) -> Mock:
    """Fixture for mocking pathlib.Path.read_text."""
    pathlib_read_text: Mock = mocker.patch("pathlib.Path.read_text")
    return pathlib_read_text


def test_read_playlist_with_passed_encoding(
    mock_pathlib_read_text: Mock,
) -> None:
    """It applies encoding to read text if it was passed."""
    file = Path("temp.m3u")
    playlist.get_full_content_of_playlist(file, "utf-8")
    mock_pathlib_read_text.assert_called_once_with(encoding="utf-8")


@pytest.fixture
def mock_playlist_path_stat(mocker: MockFixture) -> Mock:
    """Fixture for mocking Path.stat() called from playlist."""
    path_stat_mock: Mock = mocker.patch("pathlib.Path.stat")
    return path_stat_mock


def test_playlist_fails_on_retreving_file_stat(
    mock_playlist_path_stat: Mock,
) -> None:
    """It raises ClickException if the file stat retreving fails."""
    mock_playlist_path_stat.side_effect = OSError
    with pytest.raises(ClickException) as exc_info:
        _ = playlist.is_file_too_small(Path("AnyPath.m3u"))
    assert exc_info.typename == "ClickException"
