import pytest
from pytest import raises
from unittest import TestCase

from erratum.error import Error


@pytest.mark.error
class TestError(TestCase):
    """Tests relating to the Error class."""

    def test_annotate_wraps(self):
        """Check that the annotate method wraps functions."""

        class MyError(Error):
            pass

        @MyError.annotate()
        def my_function(a, b, c):
            """A docstring."""
            return a + b + c

        assert my_function.__doc__ == "A docstring."
        assert my_function.__name__ == "my_function"
        assert my_function(1, 2, 3) == 6

    def test_annotate_errs(self):
        """Check that the annotate method annotates error messages."""

        class MyError(Error):
            url = "https://my-docs.com"

        @MyError.annotate()
        def my_function(a, b, c):
            raise TypeError("This is wrong.")

        with raises(TypeError) as err:
            my_function(1, 2, 3)

        assert "This is wrong" in err.value.args[0]
        assert "https://my-docs.com" in err.value.args[0]
