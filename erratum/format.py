from pathlib import Path
from string import Template
from inspect import getdoc


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


def build_entry(error):
    """Given an error object build the content definition.

    Fills out the content definintion required to document
    an error

    :param error: The error object to document
    :type error: erratum.Error

    :rtype: dict
    :returns: Content definition ready for use with a template.
    """

    name = error.__name__
    docstring = getdoc(error)

    content = {}
    content['title'] = format_header(name, '-')
    content['desc'] = docstring

    return content


def apply_template(template, content):
    """Apply a template to the given content

    :param template: The template to use
    :param content: The content to use with the template

    :type template: str
    :type content: dict

    :rtype: string
    :returns: The result of applying the content to the template.
    """

    template = Template(template)
    return template.substitute(**content)
