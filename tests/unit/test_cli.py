"""Unit-tests for the console module."""
from pathlib import Path
import platform
from textwrap import dedent
from unittest.mock import Mock

from click.testing import CliRunner, Result
import pytest
from pytest_mock import MockFixture

from playlist_along.cli import cli_main as cli


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
            cli,
            [
                "--file",
                "temp.m3u",
                "convert",
                "--dest",
                str(target_dest),
                "--copy",
                "--dir",
            ],
        )
        # Compare files in folders
        origin_dir = [
            child.name for child in temp_folder.iterdir() if not child.is_dir()
        ]
        converted_dir = [child.name for child in target_dest.iterdir()]
        assert origin_dir == converted_dir


def test_cli_injects_file_top_by_default(runner: CliRunner) -> None:
    """It injects file at the beginning of origin file by default."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            content = """\
            Track 01.mp3
            Track 02.flac"""
            f.write(dedent(content))

        temp_folder = Path("temp.m3u").resolve().parent
        # Create injection file
        Path(temp_folder / "inj.m3u").write_text(r"C:\temp\INJECTED Track 03.mp3")

        runner.invoke(cli, ["-f", "temp.m3u", "inject", "-f", "inj.m3u"])

        injected = Path("temp.m3u").read_text()
        expected = (
            "#EXTM3U\n"
            "C:\\temp\\INJECTED Track 03.mp3\n"
            "Track 01.mp3\n"
            "Track 02.flac\n"
        )
        assert expected == injected


def test_cli_injects_file_at_the_bottom(runner: CliRunner) -> None:
    """It injects file at the bottom of origin file."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            content = """\
            #EXTM3U
            Track 01.mp3
            Track 02.flac"""
            f.write(dedent(content))

        temp_folder = Path("temp.m3u").resolve().parent
        # Create injection file
        Path(temp_folder / "inj.m3u").write_text(r"C:\temp\INJECTED Track 03.mp3")

        runner.invoke(
            cli,
            ["--file", "temp.m3u", "inject", "--file", "inj.m3u", "--bottom"],
        )

        injected = Path("temp.m3u").read_text()
        expected = (
            "#EXTM3U\n"
            "Track 01.mp3\n"
            "Track 02.flac\n"
            "C:\\temp\\INJECTED Track 03.mp3\n"
        )
        assert expected == injected


def test_cli_exits_on_small_injection(runner: CliRunner) -> None:
    """It exits if injected file is too small."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            content = """\
            #EXTM3U
            Track 01.mp3
            Track 02.flac"""
            f.write(dedent(content))

        temp_folder = Path("temp.m3u").resolve().parent
        # Create injection file
        Path(temp_folder / "inj.m3u").write_text("")

        result = runner.invoke(
            cli,
            ["--file", "temp.m3u", "inject", "--file", "inj.m3u", "--bottom"],
        )

        injected = Path("temp.m3u").read_text()
        expected = "#EXTM3U\nTrack 01.mp3\nTrack 02.flac"
        assert expected == injected
        message = "Warning: Injected file is too small for playlist. Exit.\n"
        assert result.output == message
        assert result.exit_code == 0


def test_cli_injects_into_small_origin_playlist(runner: CliRunner) -> None:
    """It injects if origin file is too small."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write("")
        temp_folder = Path("temp.m3u").resolve().parent
        # Create injection file
        inj_content = """\
            #EXTM3U
            Track 01.mp3
            Track 02.flac"""
        Path(temp_folder / "inj.m3u").write_text(dedent(inj_content))

        runner.invoke(
            cli,
            ["-f", "temp.m3u", "inject", "--file", "inj.m3u"],
        )

        injected = Path("temp.m3u").read_text()
        expected = "#EXTM3U\nTrack 01.mp3\nTrack 02.flac\n"
        assert expected == injected


def test_cli_exists_when_small_playlist_to_display(runner: CliRunner) -> None:
    """It exists if playlist is too small to display."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write("")
        result = runner.invoke(
            cli,
            ["-f", "temp.m3u"],
        )
        message = "Warning: Playlist is too small to display. Exit.\n"
        assert result.output == message
        assert result.exit_code == 0


def test_cli_exists_when_small_playlist_to_convert(runner: CliRunner) -> None:
    """It exists if playlist is too small to convert."""
    with runner.isolated_filesystem():
        with open("temp.m3u", "w") as f:
            f.write("")
        result = runner.invoke(
            cli,
            ["-f", "temp.m3u", "convert", "-d", "C-temp.m3u"],
        )
        message = "Warning: Playlist is too small to convert. Exit.\n"
        assert result.output == message
        assert result.exit_code == 0


def test_cli_exists_on_create_from_nonexisting_folder(runner: CliRunner) -> None:
    """It exists if folder with audio files does not exist."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["-f", "temp.m3u", "create", "--from", "no_directory"],
        )
        message = "Error: This directory 'no_directory' does NOT exist.\n"
        assert result.output == message
        assert result.exit_code == 0


def test_cli_creates_empty_playlist_and_exists(runner: CliRunner) -> None:
    """It exists after creation an empty playlist."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            # Even if another options were passed
            ["-f", "new.m3u", "create", "-f", "no_directory", "--empty"],
        )
        content = Path("new.m3u").read_text()
        expected_content = ""

        assert expected_content == content
        assert result.exit_code == 0


def test_cli_exists_when_no_supported_audios_in_folder(runner: CliRunner) -> None:
    """It exists if there is no supported audio files in folder."""
    with runner.isolated_filesystem():
        # Create a couple of files
        Path("Track 01.mp4").write_text("Here Track 01.mp4")
        Path("Track 02.txt").write_text("Here Track 02.txt")
        temp_folder = Path("Track 01.mp4").resolve().parent

        result = runner.invoke(
            cli,
            ["-f", "new.m3u8", "create", "--from", str(temp_folder)],
        )
        message = "Warning: No supported audio files in folder"
        assert message in result.output
        assert result.exit_code == 0


def test_cli_creates_playlist_with_natural_sort_on_windows(
    runner: CliRunner,
) -> None:
    """It sorts files in playlist with natural order sorting.

    Note: this test only for Windows CI runners.
    """
    if platform.system() == "Windows":
        with runner.isolated_filesystem():
            # Create a couple of files
            Path(".wtf.mp3").write_text("")
            Path("1 Track 1.flac").write_text("")
            Path("10 Track 10.flac").write_text("")
            Path("01 Track 01.mp3").write_text("")
            Path("Track 01.mp3").write_text("")
            Path("!Star track.flac").write_text("")
            Path("04 Track 04.mp3").write_text("")
            temp_folder = Path("Track 01.mp3").resolve().parent

            result = runner.invoke(
                cli,
                ["-f", "new.m3u8", "create", "--from", str(temp_folder), "--nat-sort"],
            )
            content = Path("new.m3u8").read_text()
            expected = (
                "!Star track.flac\n"
                ".wtf.mp3\n"
                "01 Track 01.mp3\n"
                "1 Track 1.flac\n"
                "04 Track 04.mp3\n"
                "10 Track 10.flac\n"
                "Track 01.mp3\n"
            )
            assert expected == content
            assert result.exit_code == 0
    else:
        # Pass on other OS
        assert True


def test_cli_creates_playlist_with_natural_sort_on_linux(
    runner: CliRunner,
) -> None:
    """It sorts files in playlist with natural order sorting.

    Note: this test only for Linux CI runners.
    """
    if platform.system() == "Linux":
        with runner.isolated_filesystem():
            # Create a couple of files
            Path(".wtf.mp3").write_text("")
            Path("1 Track 1.flac").write_text("")
            Path("10 Track 10.flac").write_text("")
            Path("01 Track 01.mp3").write_text("")
            Path("Track 01.mp3").write_text("")
            Path("!Star track.flac").write_text("")
            temp_folder = Path("Track 01.mp3").resolve().parent

            result = runner.invoke(
                cli,
                ["-f", "new.m3u8", "create", "--from", str(temp_folder), "--nat-sort"],
            )
            content = Path("new.m3u8").read_text()
            # Output of 'ls -lA' on Ubuntu 20.04.2 LTS
            expected = (
                "01 Track 01.mp3\n"
                "10 Track 10.flac\n"
                "1 Track 1.flac\n"
                "!Star track.flac\n"
                "Track 01.mp3\n"
                ".wtf.mp3\n"
            )
            assert expected == content
            assert result.exit_code == 0
    else:
        # Pass on other OS
        assert True


def test_cli_creates_playlist_with_ordinary_sort(
    runner: CliRunner,
) -> None:
    """It sorts files in playlist with 'ordinary' sorting.

    Note: 'ordinary' here is Python sorted().
    """
    with runner.isolated_filesystem():
        # Create a couple of files
        Path(".wtf.mp3").write_text("")
        Path("1 Track 1.flac").write_text("")
        Path("10 Track 10.flac").write_text("")
        Path("01 Track 01.mp3").write_text("")
        Path("Track 01.mp3").write_text("")
        Path("!Star track.flac").write_text("")
        Path("04 Track 01.mp3").write_text("")
        temp_folder = Path("Track 01.mp3").resolve().parent
        result = runner.invoke(
            cli,
            ["-f", "new.m3u8", "create", "--from", str(temp_folder)],
        )
        content = Path("new.m3u8").read_text()
        expected = (
            "!Star track.flac\n"
            ".wtf.mp3\n"
            "01 Track 01.mp3\n"
            "04 Track 01.mp3\n"
            "1 Track 1.flac\n"
            "10 Track 10.flac\n"
            "Track 01.mp3\n"
        )
        assert expected == content
        assert result.exit_code == 0


def test_cli_creates_in_the_same_folder_with_here(runner: CliRunner) -> None:
    """It creates playlist in the same folder with audio files.

    If option '--here' was passed.
    """
    with runner.isolated_filesystem():
        temp_folder = Path().resolve()
        sub_temp = Path(temp_folder / "audios")
        sub_temp.mkdir()
        # Create a couple of files in sub-folder
        Path(sub_temp / "Track 01.mp3").write_text("")
        Path(sub_temp / "Track 02.flac").write_text("")

        result = runner.invoke(
            cli,
            ["-f", "news.m3u8", "create", "-f", str(sub_temp), "--here"],
        )
        content = Path(temp_folder / sub_temp / "news.m3u8").read_text()
        expected = "Track 01.mp3\nTrack 02.flac\n"
        assert expected == content
        assert result.exit_code == 0


def test_cli_creates_extended_m3u_with_abs_paths(runner: CliRunner) -> None:
    """It creates extended m3u (with basic tags).

    And with absolute paths.
    """
    with runner.isolated_filesystem():
        temp_folder = Path().resolve()
        # Create a couple of files in sub-folder
        Path(temp_folder / "Track 01.mp3").write_text("")
        Path(temp_folder / "Track 02.flac").write_text("")

        runner.invoke(
            cli,
            [
                "-f",
                "extended.m3u8",
                "create",
                "-f",
                str(temp_folder),
                "--ext-m3u",
                "--abs",
            ],
        )
        content = Path(temp_folder / "extended.m3u8").read_text()
        lines = content.splitlines()
        line_1 = "#EXTM3U"
        line_2 = "#EXTINF:" in lines[1] and ",Track 01" in lines[1]
        line_3 = str(Path(temp_folder / "Track 01.mp3"))
        line_4 = "#EXTINF:" in lines[3] and ",Track 02" in lines[3]
        line_5 = str(Path(temp_folder / "Track 02.flac"))
        assert line_1 == lines[0]
        assert line_2
        assert line_3 == lines[2]
        assert line_4
        assert line_5 == lines[4]
