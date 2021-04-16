"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Playlist Along."""


if __name__ == "__main__":
    main(prog_name="playlist-along")  # pragma: no cover
