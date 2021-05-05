"""Unit-tests for the console module."""
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
