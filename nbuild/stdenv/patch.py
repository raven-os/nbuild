#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from glob import glob
from nbuild.log import clog
from nbuild.cmd import cmd
from nbuild.stdenv.package import get_package


def apply_patches(
    patches=None,
):
    package = get_package()

    if patches is None:
        patches = glob(f'{package.download_dir}/*.patch')

    for patch_path in patches:
        cmd(f'patch -Np1 -i {patch_path}')
        clog(f"Applied patch {os.path.basename(patch_path)}")
