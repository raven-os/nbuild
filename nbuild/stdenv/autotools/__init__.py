#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from nbuild.log import ilog
from nbuild.pushd import pushd
from nbuild.stdenv.patch import apply_patches
from nbuild.stdenv.build import current_build
from nbuild.stdenv.extract import extract_tarballs
from nbuild.stdenv.autotools.make import do_make
from nbuild.stdenv.install import exclude_dirs, keep_only
from nbuild.stdenv.autotools.autoconf import do_configure


def build_autotools_package(
    fetch=lambda: None,
    extract=extract_tarballs,
    patch=apply_patches,
    configure=do_configure,
    compile=do_make,
    check=lambda: do_make(target = "check", fail_ok = True),
    install=lambda: do_make(target = "install"),
):
    package = current_build().current_package

    ilog("Step 1/7: Fetch", indent=False)
    if fetch is not None:
        fetch()

    ilog("Step 2/7: Extract", indent=False)
    if extract is not None:
        extract()

    ilog("Step 3/7: Patch", indent=False)
    if patch is not None:
        patch()

    os.makedirs('build', exist_ok=True)
    with pushd('build'):
        ilog("Step 4/7: Configure", indent=False)
        if configure is not None:
            configure()

        ilog("Step 5/7: Compile", indent=False)
        if compile is not None:
            compile()

        ilog("Step 6/7: Check", indent=False)
        if check is not None:
            check()

        os.environ['DESTDIR'] = package.install_dir
        ilog("Step 7/7: Install", indent=False)
        if install is not None:
            install()
