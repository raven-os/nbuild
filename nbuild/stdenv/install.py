#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import shutil
from nbuild.stdenv.build import current_build


def make_keeper(dest):
    package = current_build().current_package
    dest = f'{package.install_dir}/{dest}/'
    keeper = f'{dest}/.nestkeep'
    os.makedirs(dest, exist_ok=True)
    open(keeper, 'w+')


def make_symlink(src, dst):
    package = current_build().current_package
    dst = f'{package.install_dir}/{dst}'
    os.symlink(src, dst)


def install_file(source, dest, chmod=0o644):
    package = current_build().current_package
    dest = f'{package.install_dir}/{dest}'

    # Create parent directory
    parent = os.path.dirname(dest)
    os.makedirs(parent, exist_ok=True)

    # Copy and chmod the target
    shutil.copyfile(source, dest)
    os.chmod(dest, chmod)


def exclude_dirs(*directories):
    package = current_build().current_package
    for directory in directories:
        dest = f'{package.install_dir}/{directory}/'
        shutil.rmtree(dest)


def keep_only(*directories, base='/'):
    package = current_build().current_package
    base = f'{package.install_dir}/{base}/'
    for entry in os.listdir(base):
        if entry not in directories:
            shutil.rmtree(f'{base}/{entry}')
