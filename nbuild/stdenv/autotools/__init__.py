#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from nbuild.log import ilog
from nbuild.pushd import pushd
from nbuild.stdenv.package import Package, get_package
from nbuild.stdenv.extract import extract_tarballs
from nbuild.stdenv.autotools.make import do_make
from nbuild.stdenv.patch import apply_patches
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
    package = get_package()

    ilog("Step 1/7: Fetch", indent=False)
    fetch()

    ilog("Step 2/7: Extract", indent=False)
    extract()

    ilog("Step 3/7: Patch", indent=False)
    patch()

    os.makedirs('build')
    with pushd('build'):
        ilog("Step 4/7: Configure", indent=False)
        configure()

        ilog("Step 5/7: Compile", indent=False)
        compile()

        ilog("Step 6/7: Check", indent=False)
        check()

        os.environ['DESTDIR'] = package.install_dir
        ilog("Step 7/7: Install", indent=False)
        install()
