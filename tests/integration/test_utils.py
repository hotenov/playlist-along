"""Integration test cases for the utils module."""
from pathlib import Path
from typing import Any

import pytest

from playlist_along._utils import _detect_file_encoding


FIXTURE_DIR = Path(__file__).parent.resolve() / "fixtures"


@pytest.mark.datafiles(
    # Order is important (must be like in folder)
    FIXTURE_DIR / "_test_ AIMPPL4 with cp1251 as UTF-16 LE.aimppl4",
    FIXTURE_DIR / "_test_ M3U with cp1251 as UTF-8 with LF in TRAKTOR3.m3u",
    FIXTURE_DIR / "_test_ M3U with cp1251 saved as UTF-8 BOM in KMPlayer.m3u",
    FIXTURE_DIR / "_test_ M3U with cp1251 saved as UTF-8 in AIMP.m3u",
    FIXTURE_DIR / "_test_ M3U8 with cp1251 saved as UTF-8 BOM in AIMP.m3u8",
    FIXTURE_DIR / "_test_ M3U8 with cp1251 saved as UTF-8 in VLC.m3u8",
)
def test_encoding_detection_for_files(datafiles: Any) -> None:
    """It detects correct encoding for prepared files."""
    expected = ["utf-16-le", "utf-8", "utf-8-sig", "cp1251", "utf-8-sig", "utf-8"]
    actual = []
    for playlist in sorted(datafiles.iterdir()):
        actual.append(_detect_file_encoding(Path(playlist)))
    assert actual == expected
