#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A very basic and primitive splitter that drains all the output files of a build into a single package, named after the
:py:class:`.BuildManifest`.
"""

import os
import stdlib.build
import stdlib.package
from typing import Dict


def drain_all() -> Dict[str, stdlib.package.Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build into a single package, named after the
    :py:class:`.BuildManifest`.


    :returns: A dictionary, with the generated package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
        associated :py:class:`.Package` as the value.
    """

    build = stdlib.build.current_build()

    package = stdlib.package.Package(
        stdlib.package.PackageID(build.manifest.metadata.name),
    )

    package.drain('*')

    return {
        package.id.short_name(): package
    }


def drain_all_with_doc() -> Dict[str, stdlib.package.Package]:
    """
    A very basic and primitive splitter that drains all the output files of a build but the documentation into a single package,
    named after the :py:class:`.BuildManifest`, and all the documentation in a second package, named like the first one, except with
    a ``-doc`` suffix.


    :returns: A dictionary, with the generated package's :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
        associated :py:class:`.Package` as the value.
    """

    build = stdlib.build.current_build()
    target = os.environ['TARGET']

    package = stdlib.package.Package(
        stdlib.package.PackageID(build.manifest.metadata.name),
    )

    package.move('{,usr/local/}{,s}bin/*', 'usr/bin/')
    package.move('usr/sbin/*', 'usr/bin/')
    package.move(f'usr/{target}/sbin/*', f'usr/{target}/bin/')

    package.move('{lib,usr/local/lib}{,64}/*', 'usr/lib64/')
    package.move('{lib,usr/local/lib}32/*', 'usr/lib32/')
    package.move(f'usr/{target}/lib/*', f'usr/{target}/lib64/')

    documentation = stdlib.package.Package(
        stdlib.package.PackageID(
            f'{build.manifest.metadata.name}-doc',
        ),
        description=f"Offline documentation of {package.id.short_name()}."
    )

    documentation.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    package.drain('*')

    return {
        package.id.short_name(): package,
        documentation.id.short_name(): documentation,
    }
