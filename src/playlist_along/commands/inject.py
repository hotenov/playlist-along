"""Inject command."""
from pathlib import Path

import click

from .. import playlist
from ..playlist import pass_playlist, Playlist, validate_file_callback


@click.command(name="inject")
@click.option(
    "--file",
    "-f",
    type=str,
    callback=validate_file_callback,
    is_eager=True,
    help="Full path to injected playlist file.",
    metavar="<string>",
)
@click.option(
    "--top/--no-top",
    " /--bottom",
    default=True,
)
@pass_playlist
def inject_cmd(pls_obj: Playlist, file: str, top: bool) -> None:
    """Injects one playlist into another."""
    origin_file: Path = pls_obj.path
    inj_file: Path = Path(file)

    origin_content, origin_enc = playlist.get_full_content_of_playlist(origin_file)
    inj_content, inj_enc = playlist.get_full_content_of_playlist(inj_file)

    inj_result = inject_content(origin_content, inj_content, top)
    playlist.save_playlist_content(inj_result, origin_file, origin_enc)


def inject_content(origin: str, injection: str, top: bool) -> str:
    """Concatenates incoming contents."""
    origin_clean: str = playlist.clean_m3u_from_extended_tag(origin)
    inj_clean: str = playlist.clean_m3u_from_extended_tag(injection)
    concatenation: str = "#EXTM3U\n"
    if top:
        concatenation += inj_clean + "\n" + origin_clean
    else:
        concatenation += origin_clean + "\n" + inj_clean
    concatenation += "\n"
    return concatenation
