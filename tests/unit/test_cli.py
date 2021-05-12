"""Unit-tests for the console module."""
from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner, Result
import pytest
from pytest_mock import MockFixture

from playlist_along.cli import cli


def test_cli_prints_version(runner: CliRunner) -> None:
    """It prints version."""
    result = runner.invoke(cli, ["--version"], prog_name="playlist-along")
    assert result.exit_code == 0
    assert "playlist-along, version 20" in result.output


def test_cli_fails_for_unsupported_format(runner: CliRunner) -> None:
    """It warns if format validation is failed."""
    result: Result
    result = runner.invoke(cli, args=["-f", "hello.txt"], prog_name="playlist-along")
    assert "currently we are supporting only" in result.output


def test_cli_fails_without_file_argument(runner: CliRunner) -> None:
    """It fails if -f option has no argument."""
    result = runner.invoke(cli, ["-f"])
    assert "Error: Option '-f' requires an argument" in result.output


def test_cli_exits_when_no_file_pass(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli, ["display"])
    assert result.exit_code == 0
    assert "No file for script" in result.output


def test_cli_prints_tracklist_itself(runner: CliRunner) -> None:
    """It prints tracklist of playlist without 'display' command."""
    with runner.isolated_filesystem():
        with open("tiny.m3u", "w") as f:
            f.write(
                """First track!.mp3
            Second Track!.flac
            """
            )

        result = runner.invoke(cli, ["--file", "tiny.m3u"])
        assert result.output == "First track!.mp3\nSecond Track!.flac\n"


def test_cli_fails_unknown_command(runner: CliRunner) -> None:
    """It fails with incorrect command."""
    result = runner.invoke(cli, ["command.m3u"])
    assert "No such command 'command.m3u'" in result.output


def test_cli_prints_tracklist_with_display(runner: CliRunner) -> None:
    """It prints tracklist of playlist with 'display' command."""
    with runner.isolated_filesystem():
        with open("tiny.m3u", "w") as f:
            f.write(
                """First track!.flac
            Second Track!.mp3
            """
            )

        result = runner.invoke(cli, ["--file", "tiny.m3u", "display"])
        assert result.output == "First track!.flac\nSecond Track!.mp3\n"


def test_cli_converts_tracklist_for_vlc(runner: CliRunner) -> None:
    """It saves converted playlist with relative paths and with valid characters."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """D:\\tmp\\tmp_flack\\First [track!].flac
            /home/user/Downloads/#Second Track!.mp3
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        target_file = temp_folder / "coverted.m3u"
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_file)]
        )
        result = runner.invoke(cli, ["--file", str(target_file), "display"])
        assert result.output == "First %5Btrack!%5D.flac\n%23Second Track!.mp3\n"


def test_cli_saves_playlist_with_same_name_for_folder(runner: CliRunner) -> None:
    """It saves converted playlist with the same filename.

    If destination option was passed as folder.
    """
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """D:\\tmp\\tmp_flack\\First [track!].flac
            /home/user/Downloads/#Second Track!.mp3
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent

        target_dest = temp_folder / "sub"
        target_dest.mkdir()
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest)]
        )
        saved_file = temp_folder / "sub" / "temp.m3u"
        result = runner.invoke(cli, ["--file", str(saved_file), "display"])
        assert result.output == "First %5Btrack!%5D.flac\n%23Second Track!.mp3\n"


def test_cli_saves_playlist_with_different_name(runner: CliRunner) -> None:
    """It saves converted playlist with auto added '_vlc'.

    If destination file and origin playlist are the same.
    """
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """D:\\tmp\\tmp_flack\\First [track!].flac
            /home/user/Downloads/#Second Track!.mp3
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent

        target_file = temp_folder / "temp.m3u"
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_file)]
        )
        saved_file = temp_folder / "temp_vlc.m3u"
        result = runner.invoke(cli, ["--file", str(saved_file), "display"])
        assert result.output == "First %5Btrack!%5D.flac\n%23Second Track!.mp3\n"


def test_cli_copies_files_from_playlist(runner: CliRunner) -> None:
    """It copies files to destination of converted playlist."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        # Create these files
        Path(temp_folder / "Track 01.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 02.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 03.flac").write_text("Here are music bytes")
        target_dest = temp_folder / "sub"
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy"]
        )
        # Compare files in folders
        origin_dir = [
            child.name for child in temp_folder.iterdir() if not child.is_dir()
        ]
        converted_dir = [child.name for child in target_dest.iterdir()]
        assert origin_dir == converted_dir


def test_cli_prints_missing_files_after_coping(runner: CliRunner) -> None:
    """It prints missing files in playlist after coping action."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        # Create these files
        Path(temp_folder / "Track 01.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 03.flac").write_text("Here are music bytes")
        target_dest = temp_folder / "sub"
        result = runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy"]
        )
        result_lines = str(result.output).splitlines()
        line_1 = "Missing files from playlist were NOT copied:"
        missing_name = "Track 02.mp3"
        assert line_1 == result_lines[1]
        assert missing_name == result_lines[2]


def test_cli_copies_only_absent_files_by_default(runner: CliRunner) -> None:
    """It copies only new files to destination folder.

    Without overriding by default.
    """
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        # Create these files
        Path(temp_folder / "Track 01.mp3").write_text(
            "Here are music bytes from origin"
        )
        Path(temp_folder / "Track 02.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 03.flac").write_text("Here are music bytes")
        target_dest = temp_folder / "sub"
        target_dest.mkdir()
        Path(temp_folder / "sub" / "Track 01.mp3").write_text(
            "Here are music bytes UPDATED"
        )
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy"]
        )
        # Compare content of 'Track 01.mp3'
        existing_in_sub = Path(temp_folder / "sub" / "Track 01.mp3").read_text()
        expected = "Here are music bytes UPDATED"
        assert expected == existing_in_sub


def test_cli_dest_with_dot_is_file_by_default(runner: CliRunner) -> None:
    """It processes path with dot as file of converted playlist."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        # Create these files
        Path(temp_folder / "Track 01.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 02.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 03.flac").write_text("Here are music bytes")
        target_dest = temp_folder / "sub" / "file.txt"
        target_dest.parent.mkdir()
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy"]
        )
        # Check that copying is successful
        converted_dir = [child.name for child in target_dest.parent.iterdir()]
        assert len(converted_dir) == 4
        # Check if destination file is created (not a folder)
        target_playlist = Path(temp_folder / "sub" / "file.txt").read_text()
        expected = "Track 01.mp3\nTrack 02.mp3\nTrack 03.flac\n"
        assert expected == target_playlist


@pytest.fixture
def mock_shutil_copy2(mocker: MockFixture) -> Mock:
    """Fixture for mocking shutil.copy2."""
    shutil_copy2: Mock = mocker.patch("shutil.copy2")
    return shutil_copy2


def test_cli_fails_on_copy_error(
    runner: CliRunner,
    mock_shutil_copy2: Mock,
) -> None:
    """It exits with a non-zero status code if the copying fails."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        Path(temp_folder / "Track 01.mp3").write_text("Here are music bytes")
        target_dest = temp_folder / "sub"

        mock_shutil_copy2.side_effect = OSError
        result = runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy"]
        )
        assert result.exit_code == 1
        assert "Error" in result.output


def test_cli_copies_files_into_folder_with_dot(runner: CliRunner) -> None:
    """It copies files to destination folder with dot.

    Test how is '--dir' option work.
    """
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write(
                """Track 01.mp3
            Track 02.mp3
            Track 03.flac
            """
            )
        temp_folder = Path("temp.m3u").resolve().parent
        # Create these files
        Path(temp_folder / "Track 01.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 02.mp3").write_text("Here are music bytes")
        Path(temp_folder / "Track 03.flac").write_text("Here are music bytes")
        target_dest = temp_folder / "sub.m3u"
        runner.invoke(
            cli, ["--file", "temp.m3u", "convert", "--dest", str(target_dest), "--copy", "--dir"]
        )
        # Compare files in folders
        origin_dir = [
            child.name for child in temp_folder.iterdir() if not child.is_dir()
        ]
        converted_dir = [child.name for child in target_dest.iterdir()]
        assert origin_dir == converted_dir
