#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import toml
import shutil
import tarfile
from os import makedirs
from datetime import datetime
from multiprocessing import cpu_count
from nbuild.log import ilog, dlog
from nbuild.args import get_args
from nbuild.pushd import pushd
from nbuild.pushenv import pushenv
import nbuild.stdenv.build


class Package():
    def __init__(
        self,
        package_id: str,
        description: str,
        builder,
        run_dependencies={},
    ):
        self.id = package_id
        self.description = description.replace('\n', ' ').strip()
        self.repository = package_id.split('::')[0]
        self.category = package_id.split('::')[1].split('/')[0]
        self.name = package_id.split('/')[1].split('#')[0]
        self.version = package_id.split('#')[1]
        self.builder = builder

        self.run_dependencies = run_dependencies

        dir = os.path.join(
            self.repository,
            self.category,
            self.name,
            self.version,
        )

        cwd = os.getcwd()
        cache_dir = get_args().cache_dir
        output_dir = get_args().output_dir
        self.build_dir = nbuild.stdenv.build.current_build().build_dir
        self.download_dir = os.path.join(cwd, cache_dir, 'downloads/', dir)
        self.install_dir = os.path.join(cwd, cache_dir, 'installs/', dir)
        self.package_dir = os.path.join(cwd, output_dir, dir)

    def __str__(self):
        return self.id

    def build(self):
        # Erase old content of previous builds
        if os.path.exists(self.package_dir):
            shutil.rmtree(self.package_dir)
        if os.path.exists(self.install_dir):
            shutil.rmtree(self.install_dir)

        # (Re)create directories
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.install_dir, exist_ok=True)
        os.makedirs(self.package_dir, exist_ok=True)

        if get_args().verbose >= 1:
            dlog(f"Download dir: {self.download_dir}", indent=False)
            dlog(f"Build dir: {self.build_dir}", indent=False)
            dlog(f"Install dir: {self.install_dir}", indent=False)
            dlog(f"Package dir: {self.package_dir}", indent=False)

        with pushenv():
            # Setup default env
            os.environ.clear()

            # Target & host architecture
            # TODO FIXME Set as parameter
            os.environ['TARGET'] = 'x86_64-linux-gnu'
            os.environ['HOST'] = 'x86_64-linux-gnu'

            # Common flags for the gnu toolchain (cpp, cc, cxx, as, ld)
            gnuflags = '-O -s -m64 -mtune=generic'

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
            with pushd(self.build_dir):
                self.builder()

        ilog("Creating data.tar.gz", indent=False)
        with pushd(self.install_dir):
            files_count = 0
            if get_args().verbose >= 1:
                for root, _, filenames in os.walk('.'):
                    for filename in filenames:
                        dlog("Adding", os.path.join(root, filename))
                        files_count += 1
                dlog(f"(That's {files_count} files.)")

            tarball_path = os.path.join(self.package_dir, 'data.tar.gz')
            with tarfile.open(tarball_path, mode='w:gz') as archive:
                archive.add('./')

        ilog("Creating manifest.toml", indent=False)
        toml_path = os.path.join(self.package_dir, 'manifest.toml')
        with open(toml_path, 'w') as filename:
            manifest = {
                'metadata': {
                    'name': self.name,
                    'category': self.category,
                    'version': self.version,
                    'description': self.description,
                    'created_at': datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
                },
                'dependencies': self.run_dependencies,
            }
            toml.dump(manifest, filename)

        ilog(f"Finished building {self.id}.")
        ilog(f"Output placed in {self.package_dir}")


def package(id: str, description: str, build_dependencies={}, run_dependencies={}):

    def register_package(builder):
        package = Package(id, description, builder, run_dependencies)
        nbuild.stdenv.build.current_build().queue_package(package)

    return register_package
