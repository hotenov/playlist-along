"""Test cases for the __main__ module."""
from click.testing import CliRunner

from playlist_along.cli import cli


def test_main_succeeds_without_args(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli, prog_name="playlist-along")
    assert result.exit_code == 0
    assert "Usage: playlist-along [OPTIONS]" in result.output
