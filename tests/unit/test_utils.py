"""Unit-tests for the _utils module."""
from pathlib import Path
from unittest.mock import Mock

from click import ClickException
import pytest
from pytest_mock import MockFixture

from playlist_along._utils import _detect_file_encoding


@pytest.fixture
def mock__detect_file_encoding(mocker: MockFixture) -> Mock:
    """Fixture for mocking _detect_file_encoding called from tests."""
    detect_file_encoding: Mock = mocker.patch(
        "playlist_along._utils._detect_file_encoding"
    )
    return detect_file_encoding


def test_util_fails_on_encoding_detection_error(
    mock__detect_file_encoding: Mock,
) -> None:
    """It raises ClickException if the encoding detection fails."""
    mock__detect_file_encoding.side_effect = OSError
    with pytest.raises(ClickException) as exc_info:
        _ = _detect_file_encoding(Path("AnyPath.m3u"))
    assert exc_info.typename == "ClickException"

    mock__detect_file_encoding.side_effect = AttributeError
    with pytest.raises(ClickException) as exc_info:
        _ = _detect_file_encoding(Path("AnyPath.m3u"))
    assert exc_info.typename == "ClickException"
