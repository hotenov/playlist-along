"""Command-line interface."""
from playlist_along.console import cli


def main() -> None:
    """Playlist Along."""
    cli(obj={})


if __name__ == "__main__":
    main(prog_name="playlist-along")  # pragma: no cover
