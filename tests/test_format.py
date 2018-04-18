import pytest
from unittest import TestCase
from hypothesis import given, assume
from hypothesis.strategies import text


from erratum.format import format_header


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
