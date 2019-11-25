#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A very basic and primitive splitter that drains all the output files of a build into a single package, named after the
:py:class:`.BuildManifest`.
"""

import os
import stdlib.build
from stdlib.package import Package, PackageID
from typing import Dict


def drain_all_into(target_package: Package) -> Dict[str, Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build into a given package.

    :param target_package: the :py:class:`.Package` to drain into

    :returns: A dictionary, with the given package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
        associated :py:class:`.Package` as the value.
    """
    target_package.drain('*')

    return {
        target_package.id.short_name(): target_package
    }


def drain_all() -> Dict[str, Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build into a single package, named after the
    :py:class:`.BuildManifest`.


    :returns: A dictionary, with the generated package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
        associated :py:class:`.Package` as the value.
    """

    build = stdlib.build.current_build()

    package = Package(PackageID(build.manifest.metadata.name))

    return drain_all_into(package)


def drain_all_with_doc_into(regular_package: Package, doc_package: Package) -> Dict[str, Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build but the documentation into a given package,
    and all the documentation in a second given package.

    :param regular_package: the :py:class:`.Package` to drain into
    :param doc_package: the :py:class:`.Package` to drain the documentation into

    :returns: A dictionary, with the given packages' :py:func:`~stdlib.package.PackageID.short_name` as keys, and the
        associated :py:class:`.Package` as values.
    """
    target = os.environ['TARGET']

    regular_package.move('{,usr/local/}{,s}bin/*', 'usr/bin/')
    regular_package.move('usr/sbin/*', 'usr/bin/')
    regular_package.move(f'usr/{target}/sbin/*', f'usr/{target}/bin/')

    regular_package.move('{lib,usr/local/lib}{,64}/*', 'usr/lib64/')
    regular_package.move('{lib,usr/local/lib}32/*', 'usr/lib32/')
    regular_package.move(f'usr/{target}/lib/*', f'usr/{target}/lib64/')

    doc_package.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    regular_package.drain('*')

    return {
        regular_package.id.short_name(): regular_package,
        doc_package.id.short_name(): doc_package,
    }


def drain_all_with_doc() -> Dict[str, Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build but the documentation into a single package,
    named after the :py:class:`.BuildManifest`, and all the documentation in a second package, named like the first one, except with
    a ``-doc`` suffix.


    :returns: A dictionary, with the generated package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
        associated :py:class:`.Package` as the value.
    """

    build = stdlib.build.current_build()

    package = Package(PackageID(build.manifest.metadata.name))

    documentation = Package(
        PackageID(f'{build.manifest.metadata.name}-doc'),
        description=f"Offline documentation of {package.id.short_name()}."
    )

    return drain_all_with_doc_into(package, documentation)
