# -*- coding: utf-8 -*-
"""
@file
@brief Command line for this module.
"""
import sys


def main(args, fLOG=print):
    """
    Implements ``python -m manydataapi <command> <args>``.

    @param      args        command line arguments
    @param      fLOG        logging function
    """
    try:
        from .parsers.folders import read_folder
    except ImportError:  # pragma: no cover
        from manydataapi.parsers.folders import read_folder

    fcts = dict(read_folder=read_folder)
    from pyquickhelper.cli import cli_main_helper
    return cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
