"""CLI commands and functions."""
from pathlib import Path
from typing import Any, Union

import click
from click import Context, Option, Parameter

from . import playlist


def validate_formats(
    ctx: Context, param: Union[Option, Parameter], value: Any = None
) -> Any:
    """Validate supported playlist formats."""
    # For script running without parameters
    if not value or ctx.resilient_parsing:
        return
    supported_formats = [".m3u", ".m3u8"]
    if Path(value).suffix in supported_formats:
        return value
    else:
        raise click.BadParameter(
            "currently we supported only these formats: %s" % supported_formats
        )


# Decorator for passing path to playlist file
pass_file = click.make_pass_decorator(playlist.PlsFile, ensure=True)


@click.command()
# @click.pass_context
@pass_file
def display(pls_file: playlist.PlsFile) -> None:
    """Display command."""
    # display_tracks(Path(ctx.obj["FILE"]))
    playlist.display_tracks(pls_file)
