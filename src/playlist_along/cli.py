"""CLI main click group."""
import click

from playlist_along import __version__
from .commands import convert, create, display, inject
from .playlist import Playlist, validate_file_callback


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.version_option(version=__version__)
@click.option(
    "--file",
    "-f",
    type=str,
    callback=validate_file_callback,
    is_eager=True,
    help="Full path to playlist file.",
    metavar="<string>",
)
@click.pass_context
def cli_main(ctx: click.Context, file: str) -> None:
    """Playlist Along - a CLI for playlist processing."""
    ctx.obj = Playlist(file)

    if file is None:
        click.echo("No file for script. Try 'playlist-along --help' for help.")
        ctx.exit()
    else:
        if ctx.invoked_subcommand is None:
            ctx.invoke(display.display_cmd)


cli_main.add_command(display.display_cmd)
cli_main.add_command(convert.convert_cmd)
cli_main.add_command(inject.inject_cmd)
cli_main.add_command(create.create_cmd)


if __name__ == "__main__":
    cli_main()  # pragma: no cover
