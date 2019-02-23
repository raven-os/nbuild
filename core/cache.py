#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Functions to manipulate the different kinds of caches.
"""

import os
import sys
import shutil
import random
import core.args
import stdlib.build


def get_install_cache(build) -> str:
    """Get the path pointing to the cache where the files produced by the given build should be stored.

    :info: The content of this cache mimics a Linux file system
    :param build: The build associated with the cache
    :type build: :py:class:`.Build`

    :returns: The path pointing to the cache where the produced files should be stored
    """
    return os.path.join(
        core.args.get_args().cache_dir,
        'install',
        build.manifest.metadata.name,
        build.semver,
    )


def get_download_cache(build) -> str:
    """Get the path pointing to the cache where the files downloaded by the given build should be stored.

    :info: This cache is kept across builds to avoid downloading the same files over and over
    :param build: The build associated with the cache
    :type build: :py:class:`.Build`

    :returns: The path pointing to the cache where the downloaded files should be stored
    """
    return os.path.join(
        core.args.get_args().cache_dir,
        'download',
        build.manifest.metadata.name,
        build.semver,
    )


def get_build_cache(build) -> str:
    """Get the path pointing to the cache where the given build should be built.

    :param build: The build associated with the cache
    :type build: :py:class:`.Build`

    :returns: The path pointing to the cache where the build is built
    """
    return os.path.join(
        core.args.get_args().cache_dir,
        'build',
        build.manifest.metadata.name,
        build.semver,
    )


def get_wrap_cache(package) -> str:
    """Get the path pointing to the cache where the files belonging to the given package should be stored.

    When the build is over, all files in the cache will be wrapped to form the package's content.

    :info: The content of this cache mimics a Linux file system
    :param package: The package associated with the cache
    :type package: :py:class:`.Package`

    :returns: The path pointing to the cache where the files belonging to the given package should be stored
    """
    return os.path.join(
        core.args.get_args().cache_dir,
        'wrap',
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def get_package_cache(package) -> str:
    """Get the path pointing to the cache where the final package, at the very end of the build process, should be stored.

    This cache is populated automatically at the end of the build process. A build manifest should not have to write anything to it.

    :info: This cache is populated by Package.wrap() and contains the manifest and data of the package
    :param package: The package associated with the cache
    :type package: :py:class:`.Package`

    :returns: The path pointing to the cache where the files belonging to the given package should be stored
    """
    return os.path.join(
        core.args.get_args().output_dir,
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def purge_cache():
    """Purge the content of the `wrap`, `build`, `download` and `install` cache for all builds."""
    folder = core.args.get_args().cache_dir

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
        except Exception:
            pass
