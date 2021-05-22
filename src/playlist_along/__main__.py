"""Script entry point."""
import sys

from .cli import cli_main as cli


def main() -> None:
    """Calls 'cli_main' click group."""
    cli()  # pragma: no cover


if __name__ == "__main__":
    if len(sys.argv) == 1:  # pragma: no cover
        cli(prog_name="playlist-along")  # pragma: no cover
    else:  # pragma: no cover
        main()  # pragma: no cover
