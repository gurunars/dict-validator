#!/usr/bin/env python

import sys

from pylint.checkers.base import DocStringChecker as OriginalDocStringChecker
from pylint.checkers import utils
from pylint.lint import Run as OriginalRun, PyLinter as OriginalPyLinter


class DocStringChecker(OriginalDocStringChecker):

    @utils.check_messages('missing-docstring', 'empty-docstring')
    def visit_module(self, node):
        """Do not enforce module docstrings."""


class PyLinter(OriginalPyLinter):

    def register_checker(self, checker):
        if checker.__class__ is OriginalDocStringChecker:
            checker = DocStringChecker(self)
        super(PyLinter, self).register_checker(checker)


class CustomRun(OriginalRun):
    LinterClass = PyLinter


def run_pylint():
    CustomRun(sys.argv[1:])
