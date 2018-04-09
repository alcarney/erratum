"""This module defines a script that can be run against a project, it will detect
any :code:`Error` definitions and automatically write the troubleshooting page
for you.
"""
import sys
import logging
import argparse

from string import Template
from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules

from .error import Error


class DocumentErrors:

    def __init__(self, logger, entry_template):
        self.logger = logger
        self.entry_template = entry_template

    def format_entry(self, err_name, err_def):

        fragments = {}
        fragments['title'] = err_name + "\n" + "="*len(err_name)
        fragments['desc'] = err_def.__doc__

        return self.entry_template.substitute(**fragments)

    def write_documentation(self, errors, path):
        """Given error definitions, write the documentation."""

        self.logger.debug("Writing documentation to: {}".format(path))
        with open(path, 'w') as f:

            for err_name, err_def in errors.items():
                f.write(self.format_entry(err_name, err_def))

    def find_errors(self, modules):
        """Given a module, find all the error definitions inside."""

        errors = {}
        self.logger.debug("Searching for Error definitions.")

        # This is what defines an error definition
        error_filter = lambda o: isclass(o) and issubclass(o, (Error,))

        for module in modules:
            self.logger.debug("\t{}".format(module.__name__))

            for err in getmembers(module, error_filter):
                err_name = err[0]
                err_def = err[1]

                if err_name not in errors:
                    errors[err_name] = err_def
                    self.logger.debug("\t\t-> {}".format(err_name))

        self.logger.debug("Found {} Error Definitions.".format(len(errors)))
        return errors

    def find_modules(self, package):
        """Given the package name, find all submodules."""

        self.logger.debug("Importing {}.".format(package))

        try:
            parent_module = import_module(package)
        except ModuleNotFoundError:
            self.logger.info("Fatal: module [{}] not found.".format(package))
            sys.exit(1)

        self.logger.debug("Looking for submodules.")
        path, name = parent_module.__path__, parent_module.__name__

        modules = [parent_module]
        mod_names = []

        for p in iter_modules(path, name + '.'):
            mod_name = "{}".format(p.name)
            mod_names.append(mod_name)
            self.logger.debug("\t-> {}".format(mod_name))

        self.logger.debug("Found {} submodules.".format(len(mod_names)))
        self.logger.debug("Importing modules")

        for mname in mod_names:

            try:
                modules.append(import_module(mname))
                self.logger.debug("\t-> {}".format(mname))
            except ModuleNotFoundError:
                self.logger.info("Unable to import [{}]".format(mname))
                sys.exit(1)

        return modules

    def run(self, package, path):
        """Given the python package to document find all the error definitions
        and write the documentation.

        :param package:
        :type package: str
        """
        self.logger.debug("Documenting errors declared " +
                          "in [{}] and all submodules.".format(package))

        modules = self.find_modules(package)
        errors = self.find_errors(modules)
        self.write_documentation(errors, path)


def configure_logging(debug=False):
    """Configure console logging depending on verbosity setting."""

    fmtstr = "%(name)s :: %(message)s"
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(format=fmtstr, level=level)
    return logging.getLogger("errors.document")


def configure_argparser():
    """Configure the argument parser."""

    description = "Document the errors defined in a python package"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("package",
                        help="The name of the package to document.")
    parser.add_argument('-v --verbose', dest='debug', action='store_true',
                        help="Enable verbose output (for debugging purposes)")
    parser.add_argument("-o, --output", type=str, dest="output",
                        help="The file to write the documentation to")

    return parser


ENTRY_TEMPLATE="""
$title

$desc
"""


def main():

    parser = configure_argparser()
    args = parser.parse_args()

    if args.output is None:
        path = "troubleshooting.rst"
    else:
        path = args.output

    logger = configure_logging(args.debug)
    logger.debug("Starting.")

    entry_template = Template(ENTRY_TEMPLATE)

    command = DocumentErrors(logger, entry_template)
    command.run(args.package, path)


if __name__ == '__main__':
    main()

