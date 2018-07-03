#!/usr/bin/env python3

import argparse


nbuild_args = None
nbuild_parser = None


def parse_args():
    global nbuild_parser
    global nbuild_args

    parser = argparse.ArgumentParser(
        description='Compile packages from a Build Manifest.'
    )
    parser.add_argument(
        'manifests',
        nargs='*'
    )
    parser.add_argument(
        '--build-dir',
        type=str,
        metavar='<directory>',
        default='build',
        help='Build the packages into <directory>'
    )
    parser.add_argument(
        '--pkg-dir',
        type=str,
        metavar='<directory>',
        default='packages',
        help='Place the output files into <directory>'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Make the operation more talkative'
    )
    nbuild_args = parser.parse_args()


def get_args():
    global nbuild_args
    return nbuild_args


def print_help():
    global nbuild_parser
    nbuild_parser.print_help()
