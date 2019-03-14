#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Types and functions to manipulate packages and their content."""

import copy
import os
import shutil
import tarfile
import toml
import datetime
import stdlib.log
from typing import List, Dict
from termcolor import colored


class PackageID():
    """The unique identifier of a package: its repository, category, name and version.

    :param name: The name of the package. The name should be in ``snake-case``.
    :param repository: The name of the repository. The name should be in ``snake-case``.
        If ``None`` is given, the repository name is taken from the arguments given to Nest Build.
        The default value is ``None``.
    :param category: The name of the category. The name should be in ``snake-case``.
        If ``None`` is given, the category name is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param version: The version number. The version should follow `Semantic Versioning 2.0.0`_.
        If ``None`` is given, the version number is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.

    .. _Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html
    """
    def __init__(
        self,
        name: str,
        repository: str = None,
        category: str = None,
        version: str = None,
    ):
        build = stdlib.build.current_build()

        import core.args
        self.repository = repository if repository is not None else core.args.get_args().repository
        self.category = category if category is not None else build.manifest.metadata.category
        self.version = version if version is not None else build.semver
        self.name = name

    def full_name(self) -> str:
        """Return a string representing the full name of the package, which is the combination of its repository, category and name.

        :return: A string representing the full name of the package
        """
        return f'{self.repository}::{self.category}/{self.name}'

    def __str__(self) -> str:
        return f'{self.full_name()}#{self.version}'


class Package():
    """A package, the output of a :py:class:`~stdlib.build.Build`.

    :param id: The unique identifier of the package, including its name, category, repository and version.
    :param description: A description of the package. This description should start with an uppercase letter and finish with a dot.
        If ``None`` is given, the description is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param tags: A list of tags helping a user to find the built packages easily. Each tag should be in ``snake-case``.
        If ``None`` is given, the list of tags is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param maintainer: The email address of the maintainer of this build manifest.
        If ``None`` is given, the maintainer's email address is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param licenses: The licenses of the built software.
        If ``None`` is given, the licenses are taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param upstream_url: An URL pointing to the home page of the software.
        If ``None`` is given, the url is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
        The default value is ``None``.
    :param run_dependencies: A dictionary of runtime dependencies. The key is a package's full name, and the value is a version requirement.
        The default value is ``dict()``.

    :ivar id: The unique identifier of the package, including its name, category, repository and version.
    :vartype id: ``str``

    :ivar description: A description of the package.
    :vartype description: ``str``

    :ivar tags: A list of tags helping a user to find the built packages easily.
    :vartype tags: ``List`` [ ``str`` ]

    :ivar maintainer: The email address of the maintainer of this build manifest.
    :vartype maintainer: ``str``

    :ivar licenses: The licenses of the built software.
    :vartype licenses: ``List`` [ :py:class:`~stdlib.license.License` ]

    :ivar upstream_url: An URL pointing to the home page of the software.
    :vartype upstream_url: ``str``

    :ivar run_dependencies: A dictionary of runtime dependencies. The key is a package's full name, and the value is a version requirement.
    :vartype run_dependencies: ``Dict`` [ ``str``, ``str`` ]

    :ivar wrap_cache: The path pointing to the cache where the files that belong to this package should be placed before the package is wrapped.
    :vartype wrap_cache: ``str``

    :ivar package_cache: The path pointing to the folder where the resulting package is placed after being wrapped.
    :vartype package_cache: ``str``
    """
    def __init__(
        self,
        id: PackageID,
        description: str = None,
        tags: List[str] = None,
        maintainer: str = None,
        licenses: List[stdlib.License] = None,
        upstream_url: str = None,
        run_dependencies: Dict[str, str] = dict(),
    ):
        from core.cache import get_wrap_cache, get_package_cache

        build = stdlib.build.current_build()

        self.id = id
        self.description = description if description is not None else build.manifest.metadata.description
        self.description = self.description.replace('\n', ' ').strip()
        self.maintainer = maintainer if maintainer is not None else build.manifest.metadata.maintainer
        self.licenses = licenses if licenses is not None else build.manifest.metadata.licenses
        self.upstream_url = upstream_url if upstream_url is not None else build.manifest.metadata.upstream_url
        self.run_dependencies = copy.deepcopy(run_dependencies)

        self.wrap_cache = get_wrap_cache(self)
        self.package_cache = get_package_cache(self)

        if os.path.exists(self.wrap_cache):
            shutil.rmtree(self.wrap_cache)
        os.makedirs(self.wrap_cache)

        if os.path.exists(self.package_cache):
            shutil.rmtree(self.package_cache)
        os.makedirs(self.package_cache)

    def wrap(self):
        """Wrap the package by creating all the files needed by the repository (``nest-server``) to publish the package and putting
        them in the path referred to by ``self.package_cache``
        """
        stdlib.log.slog(f"Wrapping {self.id} ({self.wrap_cache})")

        with stdlib.pushd(self.wrap_cache):
            files_count = 0
            stdlib.log.ilog("Files added:")
            with stdlib.log.pushlog():
                for root, _, filenames in os.walk('.'):
                    for filename in filenames:
                        stdlib.log.ilog(__colored_path(os.path.join(root, filename)))
                        files_count += 1
            stdlib.log.ilog(f"(That's {files_count} files.)")

            stdlib.log.slog("Creating data.tar.gz")
            tarball_path = os.path.join(self.package_cache, 'data.tar.gz')
            with tarfile.open(tarball_path, mode='w:gz') as archive:
                archive.add('./')

        stdlib.log.slog("Creating manifest.toml")
        toml_path = os.path.join(self.package_cache, 'manifest.toml')
        with open(toml_path, "w") as filename:
            manifest = {
                'metadata': {
                    'name': self.id.name,
                    'category': self.id.category,
                    'version': self.id.version,
                    'description': self.description,
                    'created_at': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
                },
                'dependencies': self.run_dependencies,
            }
            toml.dump(manifest, filename)

    def __str__(self):
        return str(self.id)


def __colored_path(path, pretty_path=None):
    if pretty_path is None:
        pretty_path = path

    if os.path.islink(path):
        target_path = os.path.join(
            os.path.dirname(path),
            os.readlink(path),
        )
        if os.path.exists(target_path):
            return f"{colored(path, 'cyan', attrs=['bold'])} -> {__colored_path(target_path, os.readlink(path))}"
        else:
            return f"{colored(path, on_color='on_red', attrs=['bold'])} -> {colored(os.readlink(path), on_color='on_red', attrs=['bold'])}"
    elif os.path.isdir(path):
        return colored(pretty_path, 'blue', attrs=['bold'])
    elif os.access(path, os.X_OK):
        return colored(pretty_path, 'green', attrs=['bold'])
    else:
        return pretty_path
