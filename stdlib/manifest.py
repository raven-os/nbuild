#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides types and functions to create and manipulate a build manifest and all its components.

A build manifest is a set of instructions that fetches, compiles, and splits a software into one or more packages.
It is typically made of three main parts:

  * A set of metadata used as a reference for the metadata of the built packages
  * A list of versions and a corresponding set of data, one per version, called the versionized arguments of a build
  * A list of instructions (taking the form of a python function) that builds the packages

The build manifest can then generate a list of :py:class:`.Build` for each version in the versionized arguments.
Those :py:class:`.Build` s will take as parameter (among other things) the set of data associated with this version.

For example, it may have a field named ``url`` holding a URL pointing to the source code of the software.
Therefore, this field will hold the correct URL for all versions and is easily accessible in a uniform, version-independent way.

*Example of an illustrated versionized list of arguments:*

+---------+-----------------------------------------------+----------------------------------------------+
| Version | Value of the field ``url``                    | Value of the field ``sha256``                |
+=========+===============================================+==============================================+
| 1.0.0   | ``https://example.com/software_1.0.0.tar.gz`` | ``5891b5b522d5df086d0ff0b110fbd9d21bb4f...`` |
+---------+-----------------------------------------------+----------------------------------------------+
| 1.1.0   | ``https://example.com/software_1.1.0.tar.gz`` | ``e258d248fda94c63753607f7c4494ee0fcbe9...`` |
+---------+-----------------------------------------------+----------------------------------------------+
| 1.2.0   | ``https://example.com/software_1.2.0.tar.gz`` | ``fc7c46367a4ef38398cdfd30b56885357e86b...`` |
+---------+-----------------------------------------------+----------------------------------------------+
"""

import os
import core
import stdlib.log
from typing import List, Dict


class BuildManifestMetadata():
    """A set of values used as a reference when filling the metadata of the built packages

    Built packages will reuse this information to build their own metadata.
    For example, the developer version of a package might reuse the name provided and append ``-dev`` at the end.

    :info: The information provided here can be overriden on a per-package basis. They are only here as a default option.

    :param name: The name of the software being built. The name should be in ``snake-case``.
    :param category: The category the built packages belong to. The category should be in ``snake-case``.
    :param description: A description of the software being built. This description should start with an uppercase letter and finish with a dot.
    :param tags: A list of tags helping a user to find the built packages easily. Each tag should be in ``snake-case``.
    :param maintainer: The email address of the maintainer of this build manifest.
    :param licenses: The licenses of the built software.
    :type licenses: ``List`` [ :py:class:`.License` ]
    :param upstream_url: The URL pointing to the home page of the software.

    :ivar name: The name of the software being built.
    :vartype name: ``str``

    :ivar category: The category the built packages belong to.
    :vartype category: ``str``

    :ivar description: A description of the software being built.
    :vartype description: ``str``

    :ivar tags: A list of tags helping a user to find the built packages easily.
    :vartype tags: ``List`` [ ``str`` ]

    :ivar maintainer: The email address of the maintainer of this build manifest.
    :vartype maintainer: ``str``

    :ivar licenses: The licenses of the built software.
    :vartype licenses: ``List`` [ :py:class:`~stdlib.license.License` ]

    :ivar upstream_url: The URL pointing to the home page of the software.
    :vartype upstream_url: ``str``
    """
    def __init__(
        self,
        name: str,
        category: str,
        description: str,
        tags: List[str],
        maintainer: str,
        licenses,
        upstream_url: str,
    ):
        self.name = name
        self.category = category
        self.description = description.replace('\n', ' ').strip()
        self.tags = tags
        self.maintainer = maintainer
        self.licenses = licenses
        self.upstream_url = upstream_url


class BuildManifest():
    """A build manifest is a set of instructions that fetches, compiles, and splits a software into one or more packages.

    It is made of three components:

      * A set of metadata used as a reference for the metadata of the built packages
      * A list of versions and a corresponding set of data, one per version, called the versionized arguments of a build
      * A list of instructions (taking the form of a python function) that builds the packages

    **Versionized Arguments:**

    The field ``versionized_args`` is a list. Each entry in this list represents a new version of the software.
    The entries are a dictionary holding the build's arguments for each version.

    It must have a key named ``semver`` that holds the version number, following `Semantic Versioning 2.0.0`_.

    All the remaining pairs of key/value can be used freely. Some functions of the standard compilation library (:py:mod:`stdlib`)
    may use them as generic, version-agnostic arguments. To ensure future compatibility, the standard compilation library reserves
    all key names that don't start with an underscore (``_``).

    For example, the function :py:func:`stdlib.fetch.fetch` is used to download files (like the source code) before building a software.
    It looks for an entry named ``fetch`` in ``versionized_args`` that contains the elements needed to download a file (like its URL, its hash etc.)
    (See the documentation of :py:func:`stdlib.fetch.fetch` for more informations.)

    Here is an example of ``versionized_args`` for a build manifest supporting two versions (``1.0.0`` and ``1.1.0``) of the software
    and uses the function :py:func:`stdlib.fetch.fetch` to download the source code::

        [
            {
                'semver': '1.0.0',
                'fetch': [{
                        'url': 'http://example.com/dl/hello_world_1.0.0.tar.gz',
                        'sha256': '5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
                    }
                ],
            },
            {
                'semver': '1.1.0',
                'fetch': [{
                        'url': 'http://example.com/dl/hello_world_1.1.0.tar.gz',
                        'sha256': 'e258d248fda94c63753607f7c4494ee0fcbe92f1a76bfdac795c9d84101eb317',
                    },
                ]
            }
        ]

    .. _Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html

    :param path: The path where the build manifest is stored
    :param metadata: A set of values used as a reference when filling the metadata of the built packages
    :param versionized_args: A list of dictionaries used as a generic way to give arguments to each versions of the build.
        See the above explanations for its exact structure and limitations.
    :param instructions: A callable (usually a python function) that builds the packages. It takes a :py:class:`~stdlib.build.Build` as parameter
        and returns an iterable collection of :py:class:`~stdlib.package.Package` (usually a list).
    :type instructions: fn (:py:class:`~stdlib.build.Build`) -> ``Iterable`` [ :py:class:`~stdlib.package.Package` ]

    :ivar path: The path where the build manifest is stored
    :vartype path: ``str``

    :ivar metadata: A set of values used as a reference when filling the metadata of the built packages
    :vartype metadata: :py:class:`~BuildManifestMetadata`

    :ivar versionized_args: A list of dictionaries used as a generic way to give arguments to each versions of the build.
    :vartype versionized_args: ``List`` [ ``Dict`` [ ``str``, ``str`` ] ]

    :ivar instructions: A callable that builds the package.
    :vartype instructions: fn (:py:class:`~stdlib.build.Build`) -> ``Iterable`` [ :py:class:`~stdlib.package.Package` ]
    """
    def __init__(
        self,
        path: str,
        metadata: BuildManifestMetadata,
        versionized_args: List[Dict[str, str]],
        instructions,
    ):
        self.metadata = metadata
        self.versionized_args = versionized_args
        self.instructions = instructions
        self.path = path

    def builds(self):
        """Aggregate all the builds for this manifest into a list, one per version.

        :returns: A list of all the builds for this manifest, one per version.
        :returntype: ``List`` [ :py:class:`.Build` ]
        """
        from stdlib.build import Build
        return list(map(
            lambda args: Build(self, args),
            self.versionized_args,
        ))


def manifest(
    versions_data: List[Dict[str, str]],
    build_dependencies: List[str] = [],
    **kwargs,
):
    """Create a :py:class:`.BuildManifest` and execute all the builds generated.

    First, this function will create an instance of :py:class:`.BuildManifest` with the given metadata.
    Then it will install the build dependencies needed to compile the software.
    For all versions in the build manifest, a :py:class:`.Build` instance is
    created and executed (using :py:func:`stdlib.build.Build.build`).
    At the end, all the retrieved packages are wrapped using :py:func:`stdlib.package.Package.wrap`.

    :info: The environment and current working directory are saved before each build, limiting the impact of one build on another.
    :info: See the constructor of :py:class:`~stdlib.manifest.BuildManifest` and :py:class:`.BuildManifestMetadata`
        for the exact meaning and limitation of ``kwargs`` and ``versions_data``.
    :info: The packages ``stable::raven-os/essentials`` and ``stable::raven-os/essentials-dev`` are guaranteed to be installed.
        There is no need to include them in ``build_dependencies``.

    :param kwargs: Arguments transferred to the constructor of :py:class:`.BuildManifestMetadata`
    :param versions_data: Versionized arguments of the build manifest.
    :param build_dependencies: A list of package requirements that must be installed (using ``nest``) before building anything.
    """
    def exec_manifest(builder):
        metadata = BuildManifestMetadata(**kwargs)
        manifest = BuildManifest(
            core.args.get_args().manifest,
            metadata,
            versions_data,
            builder,
        )

        # Install build dependencies
        for build_dep in build_dependencies:
            stdlib.log.slog(f"Installing build dependency \"{build_dep}\"")

        for build in manifest.builds():
            stdlib.log.slog(f"Building {build}")

            # Save state before building
            with stdlib.pushd(), stdlib.pushenv(), stdlib.log.pushlog():
                pkgs = build.build()

                # Wrap packages
                for pkg in pkgs:
                    pkg.wrap()

    return exec_manifest
