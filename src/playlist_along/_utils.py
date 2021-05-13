"""Module with utilities (helpers)."""
from pathlib import Path

from charset_normalizer import CharsetNormalizerMatches as CnM
from click.exceptions import ClickException


def _detect_file_encoding(path: Path) -> str:
    """Return an approximate encoding of text file.

    Performs an encoding detection and BOM check.

    Args:
        path: The path to playlist file

    Returns:
        A string with "best" encoding from following:
        'utf-8', 'utf-8-sig', 'cp1251', 'cp1252', 'utf_16_le'.

    Raises:
        ClickException: The file was no found or
            the encoding was not retrieved from 'charset_normalizer'
    """
    try:
        detection_result = (
            CnM.from_path(path, cp_isolation=["utf_8", "cp1252", "cp1251", "utf_16_le"])
            .best()
            .first()
        )

        encoding = "utf-8"
        if path.suffix == ".aimppl4":
            encoding = "utf-16-le"
        elif detection_result.encoding == "utf_8":
            if detection_result.byte_order_mark:
                encoding = "utf-8-sig"
        else:
            encoding = detection_result.encoding

        return encoding
    except (OSError, AttributeError) as error:
        message = str(error)
        raise ClickException(message)
