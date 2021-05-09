"""Unit-tests for the _utils module."""
from pathlib import Path

import click
import pytest


from playlist_along._utils import _detect_file_encoding


def test_util_fails_on_encoding_detection_error() -> None:
    """It raises ClickException if the encoding detection fails."""
    with pytest.raises(click.ClickException) as exc_info:
        _ = _detect_file_encoding(Path('="WrongPath.m3u"'))
        assert True is True
    assert exc_info.typename == "ClickException"
