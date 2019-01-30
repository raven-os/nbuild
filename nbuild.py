#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module of Nest Build: Raven-OS's automated build system for lazy maintainers.
"""

import os
import re
import importlib.util
import core
from core.log import slog, flog
from dotenv import load_dotenv
from multiprocessing import cpu_count


def main():
    core.args.parse_args()

    if core.args.get_args().purge:
        from core.cache import purge_cache

        print("Purging cache... ", end='')
        purge_cache()
        print("Done!")
        exit(0)

    if core.args.get_args().manifest is None:
        flog("No path to a build manifest given.")
        exit(1)

    # Clear environment, inflate a default one
    os.environ.clear()

    # Target & host architecture
    # TODO FIXME Set as parameter
    os.environ['TARGET'] = 'x86_64-linux-gnu'
    os.environ['HOST'] = 'x86_64-linux-gnu'

    # Common flags for the gnu toolchain (cpp, cc, cxx, as, ld)
    gnuflags = '-O2 -s -m64 -mtune=generic'

    # Pre-processor
    os.environ['CPP'] = f'{os.environ["TARGET"]}-cpp'
    os.environ['HOSTCPP'] = f'{os.environ["HOST"]}-cpp'
    os.environ['CPPFLAGS'] = gnuflags

    # C Compilers
    os.environ['CC'] = f'{os.environ["TARGET"]}-gcc'
    os.environ['HOSTCC'] = f'{os.environ["HOST"]}-gcc'
    os.environ['CFLAGS'] = gnuflags

    # C++ Compilers
    os.environ['CXX'] = f'{os.environ["TARGET"]}-g++'
    os.environ['HOSTCXX'] = f'{os.environ["HOST"]}-g++'
    os.environ['CXXFLAGS'] = gnuflags

    # Assembler
    os.environ['AS'] = f'{os.environ["TARGET"]}-as'
    os.environ['HOSTAS'] = f'{os.environ["HOST"]}-as'
    os.environ['ASFLAGS'] = gnuflags

    # Linker
    os.environ['LD'] = f'{os.environ["TARGET"]}-ld'
    os.environ['HOSTLD'] = f'{os.environ["HOST"]}-ld'
    os.environ['LDFLAGS'] = gnuflags

    # Archiver
    os.environ['AR'] = f'{os.environ["TARGET"]}-ar'
    os.environ['HOSTAR'] = f'{os.environ["HOST"]}-ar'

    # Misc
    os.environ['TERM'] = 'xterm'
    os.environ['PATH'] = '/bin:/sbin/:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/opt/bin'
    os.environ['MAKEFLAGS'] = f'-j{cpu_count() + 1}'

    # Override those with the ones within the .env file.
    load_dotenv(dotenv_path='.env', override=True)

    manifest_path = core.args.get_args().manifest
    spec = importlib.util.spec_from_file_location('build_manifest', manifest_path)
    if not spec:
        flog(f"Failed to load Build Manifest located at path \"{manifest_path}\"")
        exit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


if __name__ == "__main__":
    main()
