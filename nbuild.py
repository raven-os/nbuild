#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import importlib.util
from nbuild.args import parse_args, get_args, get_parser
from nbuild.stdenv.build import Build, current_build, set_current_build
from nbuild.manifest import load_manifest


def main():
    parse_args()
    args = get_args()

    if len(args.manifests) == 0 and args.check is None:
        get_parser().print_help()
        exit(0)

    cwd = os.getcwd()
    for manifest_path in args.manifests:

        spec = load_manifest(manifest_path)

        set_current_build(Build())

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        current_build().build()

        os.chdir(cwd)


if __name__ == "__main__":
    main()
