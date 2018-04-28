Erratum
=======

.. list-table::
    :stub-columns: 1

    * - code
      - |travis| |coveralls|
    * - pypi
      - |version| |py-supported|

.. |version| image:: https://img.shields.io/pypi/v/erratum.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/erratum

.. |py-supported| image:: https://img.shields.io/pypi/pyversions/erratum.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/erratum

.. |travis| image:: https://travis-ci.org/alcarney/erratum.svg?branch=dev
    :target: https://travis-ci.org/alcarney/erratum

.. |coveralls| image:: https://coveralls.io/repos/github/alcarney/erratum/badge.svg?branch=dev
    :target: https://coveralls.io/github/alcarney/erratum?branch=dev

Erratum is a python package that aims to make it easy to build in user friendly
error messages into your project. Let's look at the following example:

.. code-block:: python

    >>> my_square_root(-1)
    <ipython-input-3-a8d1f1b285c7> in my_square_root(n)
          5
          6     if n < 0:
    ----> 7         raise ValueError("You can only take the square root of a positive number")
          8
          9     return math.sqrt(n)

    ValueError: You can only take the square root of a positive number
    More info --> https://github.com/alcarney/erratum

As you can see we get the error message as passed to the exception but we also get
a link to a webpage where we can find more information about the error and what
we need to do to fix it.

How? Well let's look at the implementation of :code:`my_square_root`

.. code-block:: python

    import math
    from erratum import Error

    class SqrtError(Error):
        url = "https://github.com/alcarney/erratum"

    @SqrtError
    def my_square_root(n):

        if n < 0:
            raise ValueError("You can only take the square root of a positive number")

        return math.sqrt(n)

Here we declare our error :code:`SqrtError` by subclassing the :code:`Error` class
which allows us to set the url the user gets sent to find out more about the error.
Then it is simply of decorating any function we want the function to apply to with
the :code:`annotate` method. This will cause any exception that is thrown from within
the function to be tagged with the more info link.
