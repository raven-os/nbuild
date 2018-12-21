#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import shutil
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


def make_cp(*src, dest, root='', args=''):
    package = current_build().current_package
    for filename in src:
        path = f'{package.install_dir}/{root}/{filename}/'
        cmd(f'cp {args} {path} {dest}')


def make_mkdir(dir, args=''):
    package = current_build().current_package
    path = f'{package.install_dir}/{dir}/'
    cmd(f'mkdir {args} {path}')


def make_rm(*files, root='', args=''):
    package = current_build().current_package
    for filename in files:
        path = f'{package.install_dir}/{root}/{filename}/'
        cmd(f'rm {args} {path}')


def make_mv(*src, dest, root='', args=''):
    package = current_build().current_package
    for filename in src:
        path = f'{package.install_dir}/{root}/{filename}/'
        cmd(f'mv {args} {path} {dest}')


def make_chmod(dest, args):
    package = current_build().current_package
    path = f'{package.install_dir}/{dest}/'
    cmd(f'chmod {args} {path}')


def make_sed(regex, filename, args=''):
    package = current_build().current_package
    path = f'{package.install_dir}/{filename}/'
    cmd(f'sed {args} {regex} {path}')


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
