"""Test cases for the __main__ module."""
from click.testing import CliRunner
import pytest

from playlist_along import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds_without_args(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS]" in result.output
