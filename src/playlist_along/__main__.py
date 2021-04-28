"""Command-line interface."""
from pathlib import Path
import sys

import click
from click import Context

from . import console, playlist


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.version_option()
@click.option(
    "--file",
    "-f",
    type=str,
    callback=console.validate_formats,
    is_eager=True,
)
@click.pass_context
def main(ctx: Context, file: str) -> None:
    """Playlist Along."""
    ctx.obj = playlist.PlsFile(file)

    if file is None:
        click.echo("No file for script. Try 'playlist-along --help' for help.")
        ctx.exit()
    else:
        if ctx.invoked_subcommand is None:
            playlist.display_tracks(Path(file))


main.add_command(console.display)

if __name__ == "__main__":
    if len(sys.argv) == 1:  # pragma: no cover
        main(prog_name="playlist-along")  # pragma: no cover
    else:  # pragma: no cover
        main()  # pragma: no cover
