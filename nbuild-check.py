#!/usr/bin/env python3

import argparse
import importlib.util
from nbuild.checks import check_package
from nbuild.manifest import load_manifest
from nbuild.stdenv.build import Build, current_build, set_current_build
from nbuild.args import set_args


def parse_args():
    parser = argparse.ArgumentParser(
        description="Checks package compiled with nbuild",
    )
    parser.add_argument(
        'manifests',
        nargs='*',
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        default='packages/',
        help="Output directory for built packages",
    )
    parser.add_argument(
        '-c',
        '--cache-dir',
        default='cache/',
        help="Cache directory used when downloading and building packages",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    set_args(args)

    for manifest_path in args.manifests:
        spec = load_manifest(manifest_path)
        set_current_build(Build())
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for pkg in current_build().packages:
            check_package(pkg)


if __name__ == '__main__':
    main()
