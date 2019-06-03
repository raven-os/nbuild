#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides functions to extract and manipulate tarballs."""

import os
import tarfile
import stdlib
import glob
import shutil
import itertools


def extract(
    path: str,
):
    """Extract the tarball pointed by ``path`` in the current directory.

    :param path: The path pointing to the tarball. It must be relative to the current directory.
    """
    stdlib.log.ilog(f"Extracting {os.path.basename(path)}")
    with tarfile.open(path, mode='r') as tar:
        tar.extractall()
    stdlib.log.slog(f"Extracted in {os.getcwd()}")


def extract_all():
    """Extract all tarballs of the current directory in the current directory."""
    for tarball in itertools.chain(glob.glob('*.tar.gz'), glob.glob('*.tar.xz')):
        extract(tarball)


def flat_extract(
    path: str,
):
    """Extract the tarball pointed by ``path`` in the current directory.

    If the tarball recursively contains a single folder, the content of the folder is moved to the current directory
    The folder, now empty, is removed.

    :param path: The path pointing to the tarball. It must be relative to the current directory.
    """
    stdlib.log.ilog(f"Extracting {os.path.basename(path)}")

    main_dir = None

    with tarfile.open(path, mode='r') as tar:
        try:
            main_dir = os.path.commonpath(tar.getnames())
        except:
            pass
        tar.extractall()

    if main_dir is not None and os.path.exists(main_dir) and os.path.isdir(main_dir):
        for f in os.listdir(main_dir):
            shutil.move(
                os.path.join(main_dir, f),
                '.'
            )
        shutil.rmtree(main_dir)

    stdlib.log.slog(f"Extracted in {os.getcwd()}")


def flat_extract_all():
    """Extract all tarballs of the current directory in the current directory.

    If any tarball contains a single folder, the content of the folder is moved in the current directory
    and the folder, now empty, is removed.
    """
    for tarball in itertools.chain(glob.glob('*.tar.gz'), glob.glob('*.tar.xz')):
        flat_extract(tarball)
