#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib.util
import os
from nbuild.args import parse_args, get_args, get_parser
from nbuild.log import flog
from nbuild.stdenv.build import Build, current_build, set_current_build


def main():
    parse_args()

    if len(get_args().manifests) == 0:
        get_parser().print_help()
        exit(0)

    cwd = os.getcwd()
    for manifest_path in get_args().manifests:
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

        set_current_build(Build())
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        current_build().build()

        os.chdir(cwd)


if __name__ == "__main__":
    main()
