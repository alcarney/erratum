import pytest
from unittest import TestCase
from hypothesis import given, assume
from hypothesis.strategies import text

from erratum.error import Error
from erratum.format import format_header, build_entry, apply_template, get_title


@pytest.mark.format
class TestFormat(TestCase):
    """Tests around the formatting of error documentation"""

    @given(header=text())
    def test_format_header(self, header):
        """Formatting of the title."""

        assume("\n" not in header)

        htext, under = format_header(header, "=").split("\n")

        assert len(htext) == len(under)
        assert len(htext) == len(header)
        assert header == htext

    def test_build_error(self):
        """Check that build_entry builds the required fields"""

        content = build_entry(Error)

        assert 'title' in content
        assert 'desc' in content

        assert content['title'] == "Error\n-----"

    @given(content=text(), title=text())
    def test_apply_template(self, content, title):

        template = "$title <-> $content"
        d = {'title': title, 'content': content}

        result = apply_template(template, d)

        assert result == "{} <-> {}".format(title, content)

    def test_get_title(self):
        """Check that the title is extracted from the filepath correctly."""

        title = get_title("/file/path/to/my/awesome/title.png")
        assert title == "Title"
