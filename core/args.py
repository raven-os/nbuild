#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Functions to parse and retrieve command line arguments."""

import os
import sys
import argparse

nbuild_args = None
nbuild_parser = None


def parse_args():
    """Parse the command line arguments.

    :note: Exit if the command line arguments are invalid.
    """
    global nbuild_parser
    global nbuild_args

    nbuild_parser = argparse.ArgumentParser(
        description="Compiles packages from a build Manifest."
    )
    nbuild_parser.add_argument(
        '-o',
        '--output-dir',
        default=os.path.join(  # Default path is script_dir/packages
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'packages',
        ),
        help="Output directory for built packages. Default: packages/",
    )
    nbuild_parser.add_argument(
        '-c',
        '--cache-dir',
        default=os.path.join(  # Default path is script_dir/cache
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'cache',
        ),
        help="Cache directory used when downloading and building packages. Default: cache/",
    )
    nbuild_parser.add_argument(
        '--purge',
        action='store_true',
        help="Remove all cached data.",
    )
    nbuild_parser.add_argument(
        '-r',
        '--repository',
        default='stable',
        metavar='REPOSITORY',
        help="Name of the repository the built packages will be a part of. Default: stable",
    )
    nbuild_parser.add_argument(
        'manifest',
        metavar='MANIFEST_PATH',
        nargs='?',
    )
    nbuild_parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help="Make the operation more talkative. Append it multiple times to make it even more talkative."
    )
    nbuild_args = nbuild_parser.parse_args()


def get_args():
    """Return an object holding the values of each command line argument.

    :returns: The return value of :py:func:`argparse.ArgumentParser.parse_args()`, so refer to :py:mod:`argparse`'s
        documentation for its exact content and behaviour.
    """
    return nbuild_args


def print_usage():
    """Print the usage to the standard output."""
    nbuild_parser.print_help()
