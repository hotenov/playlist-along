"""Unit-tests for the console module."""
from click.testing import CliRunner, Result

from playlist_along import __main__


def test_console_fails_for_unsupported_format(runner: CliRunner) -> None:
    """It warns if format validation is failed."""
    result: Result
    result = runner.invoke(
        __main__.main, args=["-f", "hello.txt"], prog_name="playlist-along"
    )
    assert "currently we are supporting only" in result.output


def test_console_fails_without_file_argument(runner: CliRunner) -> None:
    """It fails if -f option has no argument."""
    result = runner.invoke(__main__.main, ["-f"])
    assert "Error: -f option requires an argument" in result.output
