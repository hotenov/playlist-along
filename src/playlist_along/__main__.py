"""Command-line interface."""
import sys
from typing import Any

from .cli import cli


def main() -> Any:
    """Return CLI click group."""
    return cli()  # pragma: no cover


if __name__ == "__main__":
    if len(sys.argv) == 1:  # pragma: no cover
        cli(prog_name="playlist-along")  # pragma: no cover
    else:  # pragma: no cover
        main()  # pragma: no cover
