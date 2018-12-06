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


def install_file(source, dest, chmod=0o644):
    package = current_build().current_package
    dest = f'{package.install_dir}/{dest}'

    # Create parent directory
    parent = os.path.dirname(dest)
    os.makedirs(parent, exist_ok=True)

    # Copy and chmod the target
    shutil.copyfile(source, dest)
    os.chmod(dest, chmod)
