#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Types and functions to create and manipulate a :py:class:`.Build`, an instance of a
:py:class:`.BuildManifest` for a specific version.
"""

import os
import shutil
from typing import Dict

_current_build = None


class Build():
    """An instance of a :py:class:`.BuildManifest` for a specific version.

    :param manifest: The :py:class:`.BuildManifest` this :py:class:`.Build` belongs to.
    :type manifest: :py:class:`~.BuildManifest`

    :param args: The arguments of this build. This is a subset of ``BuildManifest.versionized_args``,
        the one corresponding to the version of this build.
    """
    def __init__(
        self,
        manifest,
        args: Dict[str, str],
    ):
        self.manifest = manifest
        self.args = args

        self.semver = self.args['semver']
        self.major, self.minor, self.patch = self.args['semver'].split('.')

        from core.cache import get_download_cache, get_build_cache, get_install_cache
        self.download_cache = get_download_cache(self)
        self.build_cache = get_build_cache(self)
        self.install_cache = get_install_cache(self)

    def __str__(self):
        return f'''{self.manifest.metadata.name} ({self.semver})'''

    def build(self):
        """Set the current build to ``self`` and execute the instructions contained in the :py:class:`.BuildManifest`.

        :returns: A dictionary, with a package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
            associated :py:class:`.Package` as the value.
            It forwards the return value of the instructions contained in the :py:class:`.BuildManifest`.
        :returntype: ``Dict`` [ ``str`` , :py:class:`.Package` ]
        """
        _set_current_build(self)

        # Create the caches
        os.makedirs(self.download_cache, exist_ok=True)

        if os.path.exists(self.build_cache):
            shutil.rmtree(self.build_cache)
        os.makedirs(self.build_cache)

        if os.path.exists(self.install_cache):
            shutil.rmtree(self.install_cache)
        os.makedirs(self.install_cache)

        # Call the parent's manifest instructions
        os.chdir(self.build_cache)
        return self.manifest.instructions(self)


def current_build() -> Build:
    """Return the :py:class:`.Build` currently being executed.

    :info: This function is mainly used by the :py:mod:`stdlib` functions to avoid explictly taking
        the current :py:class:`.Build` as a parameter.
    :returns: The :py:class:`.Build` currently being executed.
    """
    global _current_build
    return _current_build


def _set_current_build(build: Build):
    global _current_build
    _current_build = build
