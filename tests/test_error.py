import pytest
from pytest import raises
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
