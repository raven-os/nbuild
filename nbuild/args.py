#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import argparse


nbuild_args = None
nbuild_parser = None


def parse_args():
    global nbuild_parser
    global nbuild_args

    nbuild_parser = argparse.ArgumentParser(
        description="Compiles packages from a Build Manifest.",
    )
    nbuild_parser.add_argument(
        '-o',
        '--output-dir',
        default='packages/',
        help="Output directory for built packages",
    )
    nbuild_parser.add_argument(
        '-c',
        '--cache-dir',
        default='cache/',
        help="Cache directory used when downloading and building packages",
    )
    nbuild_parser.add_argument(
        'manifests',
        nargs='*',
    )
    nbuild_parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help="Make the operation more talkative",
    )
    nbuild_parser.add_argument(
        '-C',
        '--check',
        nargs='*',
        help="Check the validity of an already built package",
    )
    nbuild_parser.add_argument(
        '--no-sanity-checks',
        action='store_true',
        help="Don't run the sanity checks.",
    )
    nbuild_args = nbuild_parser.parse_args()


def set_args(args):
    global nbuild_args
    nbuild_args = args


def get_args():
    global nbuild_args
    return nbuild_args


def get_parser():
    global nbuild_parser
    return nbuild_parser
