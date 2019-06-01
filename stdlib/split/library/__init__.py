#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A collection of splitters destined to system libraries.
"""

import stdlib.build
import stdlib.package
from typing import Dict


def standard() -> Dict[str, stdlib.package.Package]:
    """
    A standard splitter for system libraries that will try to build the following packages given a build named ``xxx``:
      * ``xxx``, containing all the librairies, manuals (4, 5, 7, 8), configuration and relevant shared files.
      * ``sys-apps/xxx``, containing all the binaries, manuals (1, 6, 9) and relevant shared files.
      * ``xxx-dev``, containing all the headers, static libraries, symlinked shared object files and manuals (2, 3).
      * ``xxx-doc``, containing the offline documentation.

    Dependencies are as follow:
      * ``xxx`` has no pre-defined dependency.
      * ``sys-apps/xxx`` depends on the exact version of ``xxx``.
      * ``xxx-dev`` depends on the exact version of ``xxx``.
      * ``xxx-doc`` has no pre-defined dependency.
    """

    build = stdlib.build.current_build()

    library = stdlib.package.Package(
        stdlib.package.PackageID(build.manifest.metadata.name),
    )

    devel = stdlib.package.Package(
        stdlib.package.PackageID(f'{build.manifest.metadata.name}-dev'),
        description=f"Headers and manuals to compile or write a software using the {library.id.short_name()} library.",
    )

    binary = stdlib.package.Package(
        stdlib.package.PackageID(
            name=f'{build.manifest.metadata.name}',
            category='sys-apps',
        ),
        description=f"Binary and utilities related to the {library.id.short_name()} library.",
    )

    documentation = stdlib.package.Package(
        stdlib.package.PackageID(f'{build.manifest.metadata.name}-doc'),
        description=f"Offline documentation of {library.id.short_name()}."
    )

    # Library

    library.drain(
        '{,usr/{,local/}}lib{,32,64}/*.so.*',
        '{,usr/{,local/}}lib{,32,64}/pkgconfig/',
        '{,usr/{,local/}}lib{,32,64}/*.pc/',
        'usr/share/man/man{4,5,7,8}/',
        'usr/share/locale/',
        'usr/libexec/',
        'etc/',
    )

    library.move('{lib,/usr/local/lib}{,64}/*', 'usr/lib64/')
    library.move('{lib,/usr/local/lib}32/*', 'usr/lib32/')

    # Devel

    devel.drain(
        'usr/include/',
        '{,usr/{,local/}}lib{,32,64}/*.{a,so}',
        'usr/share/man/man{2,3}/',
    )

    devel.move('{lib,/usr/local/lib}{,64}/*', 'usr/lib64/')
    devel.move('{lib,/usr/local/lib}32/*', 'usr/lib32/')

    # Binary

    binary.drain(
        '{,usr/{,local/}}{,s}bin/*',
        'usr/share/man/man{1,6,9}/',
        'usr/share/bash-completion/',
    )

    binary.move('{,usr/local/}{,s}bin/*', 'usr/bin/')
    binary.move('usr/sbin/*', 'usr/bin/')

    # Documentation

    documentation.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    devel.depends_on(library)
    binary.depends_on(library)

    return {
        library.id.short_name(): library,
        devel.id.short_name(): devel,
        binary.id.short_name(): binary,
        documentation.id.short_name(): documentation,
    }
