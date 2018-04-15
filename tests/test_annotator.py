import pytest
from pytest import raises
from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import text

from erratum.error import Annotator


@pytest.mark.annotater
class TestAnnotator(TestCase):
    """Tests that check that the annotator works correctly."""

    @given(url=text())
    def test_init(self, url):
        """On creation the annotator should store the correct url."""

        annotator = Annotator(url)
        assert annotator.url == "More info --> " + url

    def test_context_enter(self):
        """On entering a new context the annotator should return itself."""

        annotator = Annotator('')
        assert annotator.__enter__() is annotator

    def test_context_exit_no_error(self):
        """If there was not an error, __exit__ should be a no op."""

        annotator = Annotator('')
        assert annotator.__exit__(None, None, None) is None

    @given(url=text())
    def test_context_exit_no_args(self, url):
        """If the error has no args, then simply the url should be added."""

        annotator = Annotator(url)

        with raises(TypeError) as err:

            with annotator:

                raise TypeError()

        args = err.value.args
        assert url in args[0]

    @given(msg=text(), url=text())
    def test_context_exit_one_arg(self, url, msg):
        """If the error has a single argument, tack on the url at the end."""

        annotator = Annotator(url)

        with raises(TypeError) as err:

            with annotator:
                raise TypeError(msg)

        args = err.value.args

        assert msg in args[0]
        assert url in args[0]

    @given(msg=text(), url=text())
    def text_context_multiple_args(self, url, msg):
        """If the error has multiple arguments, just add the url as another
        argument."""

        annotator = Annotator(url)

        with raises(TypeError) as err:

            with annotator:
                raise TypeError(msg, "other", "arguments")

        args = err.value.args
        assert url in args[-1]
