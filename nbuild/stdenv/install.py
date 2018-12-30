#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import shutil
import re
from nbuild.stdenv.build import current_build
from nbuild.cmd import cmd


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


def make_cp(*files, dest, root=''):
    package = current_build().current_package
    for filename in files:
        path = f'{package.install_dir}/{root}/{filename}'
        shutil.copy2(path, dest)


def make_mkdir(dir):
    package = current_build().current_package
    path = f'{package.install_dir}/{dir}/'
    if not os.path.exists(path):
        os.makedirs(path)


def make_rm_file(*files, root=''):
    package = current_build().current_package
    for filename in files:
        path = f'{package.install_dir}/{root}/{filename}'
        os.remove(path)


def make_mv(*files, dest, root=''):
    package = current_build().current_package
    for filename in files:
        path = f'{package.install_dir}/{root}/{filename}'
        shutil.move(path, dest)


def make_chmod(dest, mode, root=''):
    package = current_build().current_package
    path = f'{package.install_dir}/{root}/{dest}'
    octal_mode = "0o" + mode
    os.chmod(path, octal_mode)


def make_sed(regex, replacement, filename, root=''):
    package = current_build().current_package
    path = f'{package.install_dir}/{root}/{filename}'
    input = open(path, 'r')
    content = input.read()
    input.close()
    f = open(path, 'w')
    f.write(re.sub(regex, replacement, content))
    f.close()


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
