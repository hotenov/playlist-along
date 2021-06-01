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
    "--top/--bottom",
    default=True,
    help=(
        "Insert a content of injected file at the begining "
        "OR at the end of the origin playlist."
    ),
)
@pass_playlist
def inject_cmd(pls_obj: Playlist, file: str, top: bool) -> None:
    """Injects one playlist into another."""
    origin_file: Path = pls_obj.path
    inj_file: Path = Path(file)

    if playlist.is_file_too_small(inj_file):
        click.echo("Warning: Injected file is too small for playlist. Exit.")
        click.get_current_context().exit()
    else:
        inj_content, inj_enc = playlist.get_full_content_of_playlist(inj_file)

    if playlist.is_file_too_small(origin_file):
        origin_content = ""
        origin_enc = "utf-8"
    else:
        origin_content, origin_enc = playlist.get_full_content_of_playlist(origin_file)

    inj_result = inject_content(origin_content, inj_content, top)
    playlist.save_playlist_content(inj_result, origin_file, origin_enc)


def inject_content(origin: str, injection: str, top: bool) -> str:
    """Concatenates incoming contents."""
    origin_clean: str = playlist.clean_m3u_from_extended_tag(origin)
    inj_clean: str = playlist.clean_m3u_from_extended_tag(injection)
    concatenation: str = "#EXTM3U\n"
    if top:
        paste_origin_after = "\n" + origin_clean
        concatenation += f"{inj_clean + paste_origin_after if origin else inj_clean}"
    else:
        paste_origin_before = origin_clean + "\n"
        concatenation += f"{paste_origin_before + inj_clean if origin else inj_clean}"
    concatenation += "\n"
    return concatenation
