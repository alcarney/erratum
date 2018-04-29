import logging
from inspect import isclass, getmembers


LOGGER = logging.getLogger(__name__)


class Error:
    """This is the definition of an error, it consists of

    - A url to point people in the direction to possibly fix their issue.
    - A description on how to fix it.
    - Methods for annotating exceptions with this info.
    """

    url = ""

    def __init__(self, f=None):

        parts = {}
        parts['url'] = self.url
        parts['name'] = self.__class__.__name__.lower()

        self._url = "More info --> {url}#{name}".format(**parts)

        if f is not None:
            self.__doc__ = f.__doc__
            self.__name__ = f.__name__

            def wrapper(*args, **kwargs):

                with self:
                    return f(*args, **kwargs)

            self._f = wrapper

    def __enter__(self):
        return self

    def __exit__(self, err_type, err, traceback):

        if err is None:
            return

        args = err.args

        if len(args) == 0:
            new_args = tuple([self._url])

        if len(args) == 1:
            new_args = tuple(["{}\n{}".format(args[0], self._url)])

        if len(args) > 1:
            new_args = tuple(args + (self._url,))

        err.args = new_args

    def __call__(self, *args, **kwargs):

        if self._f is not None:
            return self._f(*args, **kwargs)


def is_error(obj):
    """Given an object, return true if it is an Error."""
    return isclass(obj) and issubclass(obj, Error)


def find_errors(modules, include_base=False):
    """Given a module find all error definitions it contains.

    By default this will ignore the base Error class but you
    can enable it by setting include_base to be true.

    :param modules: The modules to search
    :param include_base: Flag to indicate if the base Error class
                         should be collected
    :type modules: list
    :type include_base: bool

    :rtype: dict
    :returns: Dictionary containing the error names as keys and the
              definitions as values
    """
    LOGGER.debug("Searching for Error definitions.")
    errors = {}

    for module in modules:
        LOGGER.debug("\t{}".format(module.__name__))

        for (name, definition) in getmembers(module, is_error):

            if name == "Error" and not include_base:
                continue

            if name not in errors:
                errors[name] = definition
                LOGGER.debug("\t\t-> {}".format(name))

    LOGGER.debug("Found {} Error Definitions.".format(len(errors)))
    return errors
