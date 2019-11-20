#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NBuild: Raven-OS's automated package builder for lazy maintainers"""

import sys
import os
import re
import importlib.util
import core.args
import core.config
import stdlib.log
from multiprocessing import cpu_count


def main():
    core.args.parse_args()

    if core.args.get_args().purge:
        from core.cache import purge_cache

        stdlib.log.ilog("Purging caches... ")
        purge_cache()
        stdlib.log.slog("Caches purged!")
        exit(0)

    if core.args.get_args().manifest is None:
        stdlib.log.flog("No path to a build manifest given.")
        exit(1)

    try:
        core.config.load_config()
    except Exception as e:
        stdlib.log.flog(str(e))
        exit(1)

    # Clear environment, inflate a default one
    os.environ.clear()

    # Target and host architecture
    # TODO FIXME Set as parameter
    os.environ['TARGET'] = 'x86_64-raven-linux-gnu'

    # Common flags for the gnu toolchain (cpp, cc, cxx, as, ld)
    gnuflags = '-O2 -s -m64 -mtune=generic '

    # Compilator flags
    os.environ['CFLAGS'] = gnuflags
    os.environ['CXXFLAGS'] = gnuflags
    os.environ['LDFLAGS'] = gnuflags

    # Misc
    os.environ['TERM'] = 'xterm-256color'
    os.environ['PATH'] = '/bin:/sbin/:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/opt/bin'
    os.environ['MAKEFLAGS'] = f'-j{cpu_count() + 1}'

    # Override environment with the content of the config file
    if 'env' in core.config.get_config():
        os.environ.update(core.config.get_config()['env'])

    manifest_path = core.args.get_args().manifest
    spec = importlib.util.spec_from_file_location('build_manifest', manifest_path)
    if not spec:
        stdlib.log.flog(f"Failed to load Build Manifest located at path \"{manifest_path}\"")
        exit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


if __name__ == "__main__":
    main()
