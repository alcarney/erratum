"""This module defines a script that can be run against a project, it will
detect any :code:`Error` definitions and automatically write the
troubleshooting page for you.
"""
import sys
import logging
import argparse

from string import Template
from importlib import import_module
from pkgutil import iter_modules

from .format import format_header, get_title, build_entry, apply_template
from .error import find_errors


LOGGER = logging.getLogger(__name__)


ENTRY_TEMPLATE = """
$title

$desc
"""


def write_documentation(errors, path):
    """Given error definitions, write the documentation."""

    LOGGER.debug("Writing documentation to: {}".format(path))
    title = get_title(path)

    with open(path, 'w') as f:

        # Write the title
        f.write(format_header(title, "=") + "\n\n")

        for definition in errors.values():

            entry = build_entry(definition)
            f.write(apply_template(ENTRY_TEMPLATE, entry))


def find_modules(package):
    """Given the package name, find all submodules."""

    LOGGER.debug("Importing {}.".format(package))

    try:
        parent_module = import_module(package)
    except ModuleNotFoundError:
        LOGGER.error("Fatal: module [{}] not found.".format(package))
        sys.exit(1)

    LOGGER.debug("Looking for submodules.")
    path, name = parent_module.__path__, parent_module.__name__

    modules = [parent_module]
    mod_names = []

    for p in iter_modules(path, name + '.'):
        mod_name = "{}".format(p.name)
        mod_names.append(mod_name)
        LOGGER.debug("\t-> {}".format(mod_name))

    LOGGER.debug("Found {} submodules.".format(len(mod_names)))
    modules += import_modules(mod_names)
    return modules


def import_modules(names):
    """Given a list of module names, import them."""

    modules = []
    LOGGER.debug("Importing modules")

    for mname in names:

        try:
            modules.append(import_module(mname))
            LOGGER.debug("\t-> {}".format(mname))
        except ModuleNotFoundError:
            LOGGER.error("Unable to import [{}]".format(mname))
            sys.exit(1)

    return modules


def run(package, path, inc_err):
    """Given the python package to document find all the error definitions
    and write the documentation.

    :param package: The package to document.
    :param path: The path to write the documentation to.
    :param inc_err: Flag to indicate if the base Error class should be
                    included in the output.

    :type package: str
    :type path: str:
    :type inc_err: bool
    """
    LOGGER.debug("Documenting errors declared " +
                 "in [{}] and all submodules.".format(package))

    modules = find_modules(package)
    errors = find_errors(modules, inc_err)
    write_documentation(errors, path)


def configure_logging(debug=False):
    """Configure console logging depending on verbosity setting."""

    fmtstr = "%(name)s :: %(message)s"
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(format=fmtstr, level=level)


def configure_args():
    """Configure the argument parser."""

    description = "Document the errors defined in a python package"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("package",
                        help="The name of the package to document.")

    parser.add_argument('-v --verbose', dest='debug', action='store_true',
                        help="Enable verbose output (for debugging purposes)")

    parser.add_argument("-i, --include-error", action="store_true",
                        dest="inc_err",
                        help="Include the base Error class in the output.")

    parser.add_argument("-o, --output", type=str, dest="output",
                        help="The file to write the documentation to")

    return parser


def main():

    args = configure_args().parse_args()
    path = "troubleshooting.rst" if not args.output else args.output

    configure_logging(args.debug)
    LOGGER.debug("Starting.")

    run(args.package, path, args.inc_err)


if __name__ == '__main__':
    main()
