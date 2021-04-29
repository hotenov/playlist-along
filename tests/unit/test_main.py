"""Test cases for the __main__ module."""
from click.testing import CliRunner

from playlist_along.cli import cli


def test_main_succeeds_without_args(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli, prog_name="playlist-along")
    assert result.exit_code == 0
    assert "Usage: playlist-along [OPTIONS]" in result.output


def test_main_prints_version(runner: CliRunner) -> None:
    """It prints version."""
    result = runner.invoke(cli, ["--version"], prog_name="playlist-along")
    assert result.exit_code == 0
    assert "playlist-along, version 20" in result.output


def test_main_exits_when_no_file_pass(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli, ["display"])
    assert result.exit_code == 0
    assert "No file for script" in result.output


def test_main_prints_tracklist_itself(runner: CliRunner) -> None:
    """It prints tracklist of playlist without 'display' command."""
    with runner.isolated_filesystem():
        with open("tiny.m3u", "w") as f:
            f.write(
                """First track!
            Second Track!
            """
            )

        result = runner.invoke(cli, ["--file", "tiny.m3u"])
        assert result.output == "First track!\nSecond Track!\n\n"


def test_main_fails_unknown_command(runner: CliRunner) -> None:
    """It fails with incorrect command."""
    result = runner.invoke(cli, ["command.m3u"])
    assert "No such command 'command.m3u'" in result.output


def test_main_prints_tracklist_with_display(runner: CliRunner) -> None:
    """It prints tracklist of playlist with 'display' command."""
    with runner.isolated_filesystem():
        with open("tiny.m3u", "w") as f:
            f.write(
                """First track!
            Second Track!
            """
            )

        result = runner.invoke(cli, ["--file", "tiny.m3u", "display"])
        assert result.output == "First track!\nSecond Track!\n\n"
