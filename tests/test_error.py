import pytest
from pytest import raises
from hypothesis import given
from hypothesis.strategies import text
from unittest import TestCase

from erratum.error import Error, is_error


@pytest.mark.error
class TestError(TestCase):
    """Tests relating to the Error class."""

    def test_wraps(self):
        """Check that an error wraps functions."""

        class MyError(Error):
            pass

        @MyError
        def my_function(a, b, c):
            """A docstring."""
            return a + b + c

        assert my_function.__doc__ == "A docstring."
        assert my_function.__name__ == "my_function"
        assert my_function(1, 2, 3) == 6

    def test_annotate_errs(self):
        """Check that an error annotates error messages."""

        class MyError(Error):
            url = "https://my-docs.com"

        @MyError
        def my_function(a, b, c):
            raise TypeError("This is wrong.")

        with raises(TypeError) as err:
            my_function(1, 2, 3)

        assert "This is wrong" in err.value.args[0]
        assert "https://my-docs.com" in err.value.args[0]

    def test_context_enter(self):
        """On entering a context the error should return itself."""

        error = Error()
        assert error.__enter__() is error

    def test_context_exit_no_error(self):
        """If there was no error, exit should return None."""

        error = Error()
        assert error.__exit__(None, None, None) is None

    @given(URL=text())
    def test_context_exit_no_args(self, URL):

        class MyError(Error):
            url = URL

        with raises(TypeError) as err:
            with MyError():
                raise TypeError()

        args = err.value.args
        assert URL in args[0]

    @given(msg=text(), URL=text())
    def test_context_exit_one_arg(self, URL, msg):
        """If the error has a single argument, tack on the url at the end."""

        class MyError(Error):
            url = URL

        with raises(TypeError) as err:
            with MyError():
                raise TypeError(msg)

        args = err.value.args

        assert msg in args[0]
        assert URL in args[0]

    @given(URL=text(), msg=text())
    def test_context_multiple_args(self, URL, msg):
        """If the error has multiple arguments, just add the url as another
        argument."""

        class MyError(Error):
            url = URL

        with raises(TypeError) as err:
            with MyError():
                raise TypeError(msg, 'other', 'arguments')

        args = err.value.args
        assert URL in args[-1]

    def test_is_error(self):
        """Check that is_error only identfies the error definitions"""

        class MyError(Error):
            pass

        @MyError
        def func(x):
            return x + 1

        assert is_error(Error)
        assert is_error(MyError)
        assert not is_error(func)
