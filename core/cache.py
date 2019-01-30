#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Functions to manipulate the different kind of caches.
"""

import os
import sys
import shutil
import random
from core.args import get_args
from stdlib.build import Build
from stdlib.package import Package


def get_install_cache(build: Build):
    """
    Returns the location of the cache where the files produced by the given build should be placed.
    The content of this cache mimics a Linux file system.
    """
    return os.path.join(
        get_args().cache_dir,
        'install',
        build.manifest.name,
        build.semver,
    )


def get_download_cache(build: Build):
    """
    Returns the location of the cache where the files downloaded by the given build should be placed.
    This cache is kept across build to avoid downloading the same files over and over.
    """
    return os.path.join(
        get_args().cache_dir,
        'download',
        build.manifest.name,
        build.semver,
    )


def get_build_cache(build: Build):
    """
    Returns the location of the cache where all the packages are built. It is also the place where the downloaded files
    are copied and extracted after download.
    """
    return os.path.join(
        get_args().cache_dir,
        'build',
        build.manifest.name,
        build.semver,
    )


def get_wrap_cache(package: Package):
    """
    Returns the location of the cache where the files composing of the given package should be placed.
    When calling Package.wrap(), the content of this cache is compressed into a tarball.
    The content of this cache mimics a Linux file system.
    """
    return os.path.join(
        get_args().cache_dir,
        'wrap',
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def get_package_cache(package: Package):
    """
    Returns the location of the cache where the final package, at the very end of the build process, should be placed.
    This cache is populated by Package.wrap() and contains the manifest and data of the package.
    """
    return os.path.join(
        get_args().output_dir,
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def purge_cache():
    """
    Purges the content of the `wrap`, `build`, `download` and `install` cache for all builds.
    """
    folder = get_args().cache_dir

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
        except Exception:
            pass
