#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib.util
import os
from nbuild.args import parse_args, get_args, get_parser
from nbuild.log import flog, elog
from nbuild.stdenv.build import Build, current_build, set_current_build
from nbuild.checks import check_package


def load_manifest(manifest_path):
    spec = importlib.util.spec_from_file_location(
        "build_manifest",
        manifest_path
    )

    if not spec:
        flog(
            "Failed to load Build Manifest "
            f"located at path \"{manifest_path}\""
        )
        exit(1)
    return spec


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

    if args.check is not None:
        if len(args.check) == 0:
            elog("You need to provide a manifest to a package to be checked.")
        else:
            for manifest_path in args.check:
                spec = load_manifest(manifest_path)
                set_current_build(Build())
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for pkg in current_build().packages:
                    check_package(pkg)


if __name__ == "__main__":
    main()
