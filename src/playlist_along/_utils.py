from pathlib import Path

from charset_normalizer import CharsetNormalizerMatches as CnM


def detect_file_encoding(path: Path) -> str:
    """Return a approximate encoding of text file.

    Performs an encoding detection and BOM check.

    Args:
        path: The path to playlist file

    Returns:
        A string with encoding ('utf-8', 'utf-8-sig', 'cp1251', etc.).

    Raises:
        TO DO.
    """
    with open(path, "rb") as playlist_file:
        textdata = playlist_file.read()

    detection_result = CnM.from_bytes(textdata).best().first()

    encoding = "utf-8"
    if detection_result.byte_order_mark and detection_result.encoding == "utf_8":
        encoding = "utf-8-sig"
    elif detection_result.encoding == "cp1251":
        encoding = "cp1251"
    elif detection_result.encoding == "gb18030":  # VLC playlist
        encoding = "utf-8"
    elif detection_result.encoding == "utf_16":  # .aimppl4 playlist
        encoding = "utf-16-le"
    elif detection_result.encoding == "utf_8":
        encoding = "utf-8"
    else:
        encoding = detection_result.encoding

    return encoding
