"""Interation test cases for the utils module."""
import os
from pathlib import Path
from typing import Any

import pytest

from playlist_along._utils import detect_file_encoding


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "fixtures",
)


@pytest.mark.datafiles(
    # Order is important (must be like in folder)
    os.path.join(FIXTURE_DIR, "_test_ AIMPPL4 with cp1251 as UTF-16 LE.aimppl4"),
    os.path.join(FIXTURE_DIR, "_test_ M3U with cp1251 as UTF-8 with LF in TRAKTOR3.m3u"),
    os.path.join(FIXTURE_DIR, "_test_ M3U with cp1251 saved as UTF-8 BOM in KMPlayer.m3u"),
    os.path.join(FIXTURE_DIR, "_test_ M3U with cp1251 saved as UTF-8 in AIMP.m3u"),
    os.path.join(FIXTURE_DIR, "_test_ M3U8 with cp1251 saved as UTF-8 BOM in AIMP.m3u8"),
    os.path.join(FIXTURE_DIR, "_test_ M3U8 with cp1251 saved as UTF-8 in VLC.m3u8"),
)
def test_encoding_detection_for_files(datafiles: Any) -> None:
    """It detects correct encoding for prepared files."""
    expected = ["utf-16-le", "utf-8", "utf-8-sig", "cp1251", "utf-8-sig", "utf-8"]
    actual = []
    for playlist in sorted(datafiles.listdir()):
        actual.append(detect_file_encoding(Path(playlist)))
    assert actual == expected
