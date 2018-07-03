#!/usr/bin/env python3

import sys
import importlib.util
import os
import nbuild.args


def main():
    nbuild.args.parse_args()

    if len(nbuild.args.get_args().manifests) == 0:
        nbuild.args.print_help()
        exit(0)

    exec_path = os.getcwd()
    for manifest_path in nbuild.args.get_args().manifests:
        spec = importlib.util.spec_from_file_location(
            "build_manifest",
            manifest_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        os.chdir(exec_path)


if __name__ == "__main__":
    main()
