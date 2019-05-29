#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Types and functions to manipulate packages and their content."""

import copy
import os
import shutil
import tarfile
import toml
import datetime
import braceexpand
import glob
import core.config
import stdlib.log
import stdlib.kind
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

        self.repository = repository or core.config.get_config()['global']['target']
        self.category = category if category is not None else build.manifest.metadata.category
        self.version = version if version is not None else build.semver
        self.name = name

    def short_name(self) -> str:
        """Return a string representing the short name of the package, which is the combination of its category and name.

        :return: A string representing the short name of the package
        """
        return f'{self.category}/{self.name}'

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
    :param kind: The kind of the package. Effective means the package has data to install, while Virtual means the package has no data to install.
        If ``None`` is given, the kind is taken from the current :py:class:`~stdlib.manifest.BuildManifestMetadata`.
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

    :ivar kind: The kind of the package. Effective means the package has data to install, while Virtual means the package has no data to install.
    :vartype kind: :py:class:`~stdlib.kind.Kind`

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
        kind: stdlib.kind.Kind = None,
        run_dependencies: Dict[str, str]={},
    ):
        from core.cache import get_wrap_cache, get_package_cache

        build = stdlib.build.current_build()

        self.id = id
        self.description = description if description is not None else build.manifest.metadata.description
        self.description = self.description.replace('\n', ' ').strip()
        self.tags = tags if tags is not None else build.manifest.metadata.tags
        self.maintainer = maintainer if maintainer is not None else build.manifest.metadata.maintainer
        self.licenses = licenses if licenses is not None else build.manifest.metadata.licenses
        self.upstream_url = upstream_url if upstream_url is not None else build.manifest.metadata.upstream_url
        self.kind = kind if kind is not None else build.manifest.metadata.kind
        self.run_dependencies = copy.deepcopy(run_dependencies)

        self.wrap_cache = get_wrap_cache(self)
        self.package_cache = get_package_cache(self)

        if os.path.exists(self.wrap_cache):
            shutil.rmtree(self.wrap_cache)
        os.makedirs(self.wrap_cache)

        if os.path.exists(self.package_cache):
            shutil.rmtree(self.package_cache)
        os.makedirs(self.package_cache)

    def is_empty(self) -> bool:
        """Test whether the ``wrap_cache`` of this :py:class:`.Package` contains at least a single file.

        :note: If the wrap cache contains only empty directories, this function returns ``False``.

        :returns: ``True`` if the cache contains at least a single file, ``False`` otherwise.
        """
        for _, _, filenames in os.walk(self.wrap_cache):
            if len(filenames):
                return False
        return True

    def drain(self, *paths: str):
        """Drain the current :py:class:`.Build`, moving files from their ``install_cache`` to this
        :py:class:`.Package`'s ``wrap_cache``.

        This function is mostly used to grab the files that weren't automatically picked up by the package splitter.

        *Example:* ::

            package.drain(
                'usr/{lib,bin}',
                'usr/lib64/lib*.so',
            )

        :note: Files are moved and not copied

        :param paths: The paths pointing to the files to move, relative to the ``install_cache`` of the current :py:class:`.Build`.
            This argument supports the globbing and braces syntax of common shells.
        """
        build = stdlib.build.current_build()

        # Move to source directory
        with stdlib.pushd(build.install_cache):
            for rglob in paths:
                for rglob in braceexpand.braceexpand(paths):  # Expand braces

                    if os.path.isabs(rglob):
                        raise RuntimeError("Package.drain() received an absolute path as parameter, but it expects a relative one")

                    for rpath in glob.glob(rglob):  # Expand globbing
                        dstpath = os.path.join(
                            self.wrap_cache,
                            os.path.relpath(
                                rpath,
                                build.install_cache
                            ),
                        )

                        os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                        shutil.move(rpath, dstpath)

    def drain_package(self, source, *paths: str):
        """Drain a :py:class:`.Package`, moving files from its ``wrap_cache`` to this :py:class:`.Package`'s ``wrap_cache``.

        This function is mostly used to grab the files that were wrongly assigned to another package by the package splitter.

        *Example:* ::

            lib_pkg.drain_package(
                bin_pkg,
                'usr/lib{32,64}/',
                'usr/lib/lib*.so',
            )

        :note: Files are moved and not copied

        :param source: The source package containing the files to drain from.
        :type source: :py:class:`.Package`
        :param paths: The paths pointing to the files to move, relative to the ``wrap_cache`` of the given :py:class:`.Package`.
            This argument supports the globbing and braces syntax of common shells.
        """
        with stdlib.pushd(source.wrap_cache):
            for rglob in paths:
                for rglob in braceexpand.braceexpand(rglob):  # Expand braces

                    if os.path.isabs(rglob):
                        raise RuntimeError("Package.drain_package() received an absolute path as parameter, but it expects a relative one")

                    for rpath in glob.glob(rglob):  # Expand globbing
                        dstpath = os.path.join(
                            self.wrap_cache,
                            os.path.relpath(
                                rpath,
                                source.wrap_cache,
                            ),
                        )

                        os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                        shutil.move(rpath, dstpath)

    def drain_build_cache(self, src, dst):
        """Drain the current :py:class:`.Build`, moving files from its ``build_cache`` to this package's ``wrap_cache``.

        This function is mostly used to grab files that are given with the software's source code but aren't
        automatically installed, like the documentation or some code examples.

        *Example*: ::

            package.drain_build_cache(
                'doc/*',
                'usr/share/doc/my_package_0.1.1/'
            )

        :note: Files are moved and not copied

        :param src: A path pointing to the files to move, relative to the ``build_cache`` of the current :py:class:`.Build`,
            This argument supports the globbing and braces syntax of common shells.
        :param dst: A path pointing to the directory where the files should be moved, relative to the ``wrap_cache`` of this :py:class:`.Package`,

        """
        build = stdlib.build.current_build()

        if os.path.isabs(src) or os.path.isabs(dst):
            raise RuntimeError("Package.drain_build_cache() received an absolute path as parameter, but it expects a relative one")

        # Move to source directory
        with stdlib.pushd(build.build_cache):

            for rglob in braceexpand.braceexpand(src):  # Expand braces
                for rpath in glob.glob(rglob):  # Expand globbing
                    dstpath = os.path.join(
                        self.wrap_cache,
                        dst,
                    )

                    os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                    shutil.move(rpath, dstpath)

    def move(self, srcs: str, dst: str):
        """Move the files pointed to by ``srcs`` to ``dst``.

        :param srcs: The paths pointing to the files to move, relative to the ``wrap_cache`` of this :py:class:`.Package`.
            This argument supports the globbing and braces syntax of common shells.
        :param dst: A path pointing to the destination folder, relative to the ``wrap_cache`` of this :py:class:`.Package`.
        """

        if os.path.isabs(srcs) or os.path.isabs(dst):
            raise RuntimeError("Package.move() received an absolute path as parameter, but it expects a relative one")

        if not os.path.isdir(dst):
            raise RuntimeError("Package.move() did not receive a path pointing to a directory as paramter")

        with stdlib.pushd(self.wrap_cache):
            for srcs in braceexpand.braceexpand(srcs):  # Expand braces
                for src in glob.glob(srcs):  # Expand globbing
                    os.makedirs(os.path.dirname(dst), exist_ok=True)  # Create parent directories (if any)
                    shutil.move(src, dst)

    def remove(self, *files: str):
        """Remove the files pointed to by ``files``.

        :param files: The paths pointing to the files to remove, relative to the ``wrap_cache`` of this :py:class:`.Package`.
            This argument supports the globbing and braces syntax of common shells.
        """

        with stdlib.pushd(self.wrap_cache):
            for file in files:

                if os.path.isabs(file):
                    raise RuntimeError("Package.remove() received an absolute path as parameter, but it expects a relative one")

                for srcs in braceexpand.braceexpand(file):  # Expand braces
                    for src in glob.glob(srcs):  # Expand globbing
                        if os.path.isdir(src):
                            shutil.rmtree(src)
                        else:
                            os.remove(src)

    def wrap(self):
        """Wrap the package by creating all the files needed by the repository (``nest-server``) to publish the package and putting
        them in the path referred to by ``self.package_cache``
        """
        stdlib.log.slog(f"Wrapping {self.id} ({self.wrap_cache})")

        stdlib.log.slog(f"Manifest:")
        with stdlib.log.pushlog():
            stdlib.log.slog(f"name: {self.id.name}")
            stdlib.log.slog(f"category: {self.id.category}")
            stdlib.log.slog(f"version: {self.id.version}")
            stdlib.log.slog(f"description: {self.description}")
            stdlib.log.slog(f"tags: {', '.join(self.tags)}")
            stdlib.log.slog(f"maintainer: {self.maintainer}")
            stdlib.log.slog(f"licenses: {', '.join(map(lambda l: l.value, self.licenses))}")
            stdlib.log.slog(f"upstream_url: {self.upstream_url}")
            stdlib.log.slog(f"kind: {self.kind.value}")
            stdlib.log.slog(f"wrap_date: {datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'}")
            stdlib.log.slog(f"dependencies:")
            with stdlib.log.pushlog():
                for (full_name, version_req) in self.run_dependencies.items():
                    stdlib.log.slog(f"{full_name}#{version_req}")

        if self.kind == stdlib.kind.Kind.EFFECTIVE:
            with stdlib.pushd(self.wrap_cache):
                files_count = 0
                stdlib.log.slog("Files added:")
                with stdlib.log.pushlog():
                    for root, _, filenames in os.walk('.'):
                        for filename in filenames:
                            stdlib.log.slog(_colored_path(os.path.join(root, filename)))
                            files_count += 1
                stdlib.log.slog(f"(That's {files_count} files.)")

                stdlib.log.slog("Creating data.tar.gz")
                tarball_path = os.path.join(self.package_cache, 'data.tar.gz')
                with tarfile.open(tarball_path, mode='w:gz') as archive:
                    archive.add('./')
        elif self.kind == stdlib.kind.Kind.VIRTUAL:
            stdlib.log.ilog("Package is virtual, no data is wrapped.")

        stdlib.log.slog("Creating manifest.toml")
        toml_path = os.path.join(self.package_cache, 'manifest.toml')
        with open(toml_path, "w") as filename:
            manifest = {
                'name': self.id.name,
                'category': self.id.category,
                'version': self.id.version,
                'metadata': {
                    'description': self.description,
                    'tags': self.tags,
                    'maintainer': self.maintainer,
                    'licenses': list(map(lambda l: l.value, self.licenses)),
                    'upstream_url': self.upstream_url,
                },
                'kind': self.kind.value,
                'wrap_date': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
                'dependencies': self.run_dependencies,
            }
            toml.dump(manifest, filename)

        stdlib.log.slog("Creating package.nest")
        with stdlib.pushd(self.package_cache):
            nest_file = os.path.join(self.package_cache, f'{self.id.name}-{self.id.version}.nest')
            with tarfile.open(nest_file, mode='w') as archive:
                archive.add('./manifest.toml')
                if self.kind == stdlib.kind.Kind.EFFECTIVE:
                    archive.add('./data.tar.gz')

            # Remove temporary manifest.toml and data.tar.gz
            os.remove('./manifest.toml')
            if self.kind == stdlib.kind.Kind.EFFECTIVE:
                os.remove('./data.tar.gz')

    def __str__(self):
        return str(self.id)


def _colored_path(path, pretty_path=None):
    if pretty_path is None:
        pretty_path = path

    if os.path.islink(path):
        target_path = os.path.join(
            os.path.dirname(path),
            os.readlink(path),
        )
        if os.path.exists(target_path):
            return f"{colored(path, 'cyan', attrs=['bold'])} -> {_colored_path(target_path, os.readlink(path))}"
        else:
            return f"{colored(path, on_color='on_red', attrs=['bold'])} -> {colored(os.readlink(path), on_color='on_red', attrs=['bold'])}"
    elif os.path.isdir(path):
        return colored(pretty_path, 'blue', attrs=['bold'])
    elif os.access(path, os.X_OK):
        return colored(pretty_path, 'green', attrs=['bold'])
    else:
        return pretty_path
