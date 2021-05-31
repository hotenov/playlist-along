"""Interation test cases for the 'create' command."""
from pathlib import Path

from click.testing import CliRunner

from playlist_along.cli import cli_main as cli


FIXTURE_DIR = Path(
    Path(__file__).resolve().parent,
    "fixtures",
)


def test_cli_creates_extended_m3u_with_real_length(runner: CliRunner) -> None:
    """It creates extended m3u (with real audio length in seconds)."""
    with runner.isolated_filesystem():
        temp_folder = Path().resolve()

        runner.invoke(
            cli,
            [
                "-f",
                "extended.m3u8",
                "create",
                "-f",
                str(FIXTURE_DIR),
                "--ext-m3u",
                "--abs",
            ],
        )
        content = Path(temp_folder / "extended.m3u8").read_text()
        lines = content.splitlines()
        line_1 = "#EXTM3U"
        line_2 = "#EXTINF:22" in lines[1] and ",audio_test_file" in lines[1]
        line_3 = str(Path(FIXTURE_DIR / "audio_test_file.mp3"))
        assert line_1 == lines[0]
        assert line_2
        assert line_3 == lines[2]
