from pathlib import Path
from string import Template


def format_header(header, tchar):
    """Given a string and title char return a reStructuredText style section
    header.

    :param header: The header text to format
    :param tchar: The character to use.

    :type header: str
    :type tchar: str

    :rtype: str
    :returns: The formatted title.
    """

    return header + "\n" + tchar*len(header)


def get_title(path):
    """Given a path, find the filename to use as the title."""

    filepath = Path(path)
    return filepath.stem.capitalize()


