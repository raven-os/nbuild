#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides functions to extract and manipulate tarballs."""

import os
import tarfile
import stdlib
import shutil
import itertools
from glob import glob
from braceexpand import braceexpand


def extract(
    path: str,
):
    """Extract the tarball pointed by ``path`` in the current directory.

    :param path: The path pointing to the tarball. It must be relative to the current directory.
    """
    stdlib.log.ilog(f"Extracting {os.path.basename(path)}")
    with tarfile.open(path, mode='r') as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)
    stdlib.log.slog(f"Extracted in {os.getcwd()}")


def extract_all():
    """Extract all tarballs of the current directory in the current directory."""
    for xtarball in braceexpand('*.{tar.{gz,xz,bz2},tgz}'):
        for tarball in itertools.chain(glob(xtarball)):
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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)

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
    for xtarball in braceexpand('*.{tar.{gz,xz,bz2},tgz}'):
        for tarball in itertools.chain(glob(xtarball)):
            flat_extract(tarball)
