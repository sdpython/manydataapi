# -*- coding: utf-8 -*-
"""
@file
@brief Module *manypi*.
Many pieces of code to access and process various API
mostly used for teaching purpose.
"""
import sys


__version__ = "0.2"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/manydataapi"
__url__ = "http://www.xavierdupre.fr/app/manydataapi/helpsphinx/index.html"
__license__ = "MIT License"


def _setup_hook(add_print=False, unit_test=False):
    """
    if this function is added to the module,
    the help automation and unit tests call it first before
    anything goes on as an initialization step.
    It should be run in a separate process.

    @param      add_print       print *Success: _setup_hook*
    @param      unit_test       used only for unit testing purpose
    """
    # we can check many things, needed module
    # any others things before unit tests are started
    if add_print:
        print("Success: _setup_hook")


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True
