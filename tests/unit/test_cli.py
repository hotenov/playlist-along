"""Unit-tests for the console module."""
from pathlib import Path

from click.testing import CliRunner, Result

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
    assert "Error: -f option requires an argument" in result.output


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
