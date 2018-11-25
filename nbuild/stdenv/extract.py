#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import tarfile
import shutil
from glob import glob
from nbuild.log import ilog, clog
from nbuild.stdenv.build import current_build


def extract_tarballs(
    files=None,
    move_subdir=True,
    subdir=None,
):
    package = current_build().current_package

    if files is None:
        files = glob(f'{package.download_dir}/*.tar*')

    for tarball_path in files:
        ilog(f"Extracting {os.path.basename(tarball_path)}")
        with tarfile.open(tarball_path) as tar:
            tar.extractall(path=package.build_dir)

        if move_subdir:
            if subdir is None:
                # If sources are contained in a sub directory,
                # move the content one folder up
                subdir = os.path.join(
                    package.build_dir,
                    os.path.basename(tarball_path).split('.tar')[0],
                )

            if os.path.exists(subdir):
                for filename in os.listdir(subdir):
                    shutil.move(
                        os.path.join(subdir, filename),
                        package.build_dir,
                    )

        clog(f"Extracted in {package.build_dir}")
