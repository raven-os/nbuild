#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import toml
import shutil
import tarfile
from os import makedirs
from copy import deepcopy
from multiprocessing import cpu_count
from nbuild.log import ilog, dlog
from nbuild.args import get_args
from nbuild.cmd import cmd
from nbuild.pushd import pushd
from nbuild.pushenv import pushenv

_current_package = None


class Package():
    def __init__(self, package_id: str, run_dependencies={}):
        self.id = package_id
        self.repository = package_id.split('::')[0]
        self.category = package_id.split('::')[1].split('/')[0]
        self.name = package_id.split('/')[1].split('#')[0]
        self.version = package_id.split('#')[1]

        self.run_dependencies = run_dependencies

        dir = os.path.join(
            self.repository,
            self.category,
            self.name,
            self.version,
        )

        self.download_dir = os.path.join('/usr/nbuild/downloads/', dir)
        self.source_dir = os.path.join('/usr/nbuild/sources/', dir)
        self.install_dir = os.path.join('/usr/nbuild/installs/', dir)
        self.package_dir = os.path.join('/usr/nbuild/packages/', dir)

        # Erase old content of previous builds
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        if os.path.exists(self.package_dir):
            shutil.rmtree(self.package_dir)
        if os.path.exists(self.install_dir):
            shutil.rmtree(self.install_dir)

        # (Re)Create directories
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.install_dir, exist_ok=True)
        os.makedirs(self.package_dir, exist_ok=True)

    def __str__(self):
        return self.id


def package(id: str, build_dependencies={}, run_dependencies={}):
    package = Package(id, run_dependencies)

    global _current_package
    _current_package = package

    def do_package(builder):

        # Print welcome message
        ilog(f"Building {package.id}", indent=False)
        if get_args().verbose >= 1:
            dlog(f"Download dir: {package.download_dir}", indent=False)
            dlog(f"Source dir: {package.source_dir}", indent=False)
            dlog(f"Install dir: {package.install_dir}", indent=False)
            dlog(f"Package dir: {package.package_dir}", indent=False)

        with pushenv():
            # Setup default env
            os.environ.clear()

            # Target & host architecture
            # TODO FIXME Set as parameter
            os.environ['TARGET'] = 'x86_64-pc-linux-gnu'
            os.environ['HOST'] = 'x86_64-pc-linux-gnu'

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

            # Archiver
            os.environ['AR'] = f'{os.environ["TARGET"]}-ar'
            os.environ['HOSTAR'] = f'{os.environ["HOST"]}-ar'

            # Linker
            os.environ['LD'] = f'{os.environ["TARGET"]}-ld'
            os.environ['HOSTLD'] = f'{os.environ["HOST"]}-ld'
            os.environ['LDFLAGS'] = gnuflags

            # Misc
            # FIXME: remove /tools/bin from PATH
            os.environ['TERM'] = 'xterm'
            os.environ['PATH'] = '/bin:/sbin/:/usr/bin:/usr/sbin:/tools/bin'
            os.environ['MAKEFLAGS'] = f'-j{cpu_count() + 1}'

            # Call builder
            with pushd(package.source_dir):
                builder()

        ilog("Creating data.tar.gz", indent=False)
        with pushd(package.install_dir):
            files_count = 0
            if get_args().verbose >= 1:
                for root, _, filenames in os.walk('.'):
                    for filename in filenames:
                        dlog("Adding", os.path.join(root, filename))
                        files_count += 1
                dlog(f"(That's {files_count} files.)")

            tarball_path = os.path.join(package.package_dir, 'data.tar.gz')
            with tarfile.open(tarball_path, mode='w:gz') as archive:
                archive.add('./')

        ilog("Creating manifest.toml", indent=False)
        toml_path = os.path.join(package.package_dir, 'manifest.toml')
        with open(toml_path, "w") as filename:
            manifest = {
                "metadata": {
                    "name": package.name,
                    "category": package.category,
                    "version": package.version
                },
                "dependencies": package.run_dependencies,
            }
            toml.dump(manifest, filename)

        ilog(f"Finished building {package.id}.")
        ilog(f"Output placed in {package.package_dir}")
    return do_package


def get_package():
    global _current_package
    return _current_package
