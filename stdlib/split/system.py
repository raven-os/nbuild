#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A standard splitter for system applications and libraries.
"""

import os
import stdlib.build
import stdlib.package
from typing import Dict


def system() -> Dict[str, stdlib.package.Package]:
    """
    A standard splitter for system application and libraries that will try to build the following packages given a build named ``xxx``:

      * ``xxx``, containing all the applications, librairies, manuals (1, 4, 5, 6, 7, 8, 9), configuration and shared files.
      * ``xxx-dev``, containing all the headers, static libraries, symlinked shared object files and manuals (2, 3).
      * ``xxx-doc``, containing the offline documentation.

    Dependencies are as follow:

      * ``xxx`` has no pre-defined dependency.
      * ``xxx-dev`` depends on the exact version of ``xxx``.
      * ``xxx-doc`` has no pre-defined dependency.
    """

    build = stdlib.build.current_build()
    target = os.environ['TARGET']

    main = stdlib.package.Package(
        stdlib.package.PackageID(
            build.manifest.metadata.name,
        ),
    )

    devel = stdlib.package.Package(
        stdlib.package.PackageID(
            f'{build.manifest.metadata.name}-dev',
        ),
        description=f"Headers and manuals to compile or write a software using the {main.id.short_name()} package.",
    )

    documentation = stdlib.package.Package(
        stdlib.package.PackageID(
            f'{build.manifest.metadata.name}-doc',
        ),
        description=f"Offline documentation of {main.id.short_name()}."
    )

    # Main package (application or library)

    main.drain(
        '{,usr/{,local/}}{,s}bin/',
        '{,usr/{,local/}}lib{,32,64}/*.so.*',
        '{,usr/{,local/}}lib{,32,64}/pkgconfig/',
        '{,usr/{,local/}}lib{,32,64}/*.pc/',
        f'usr/{target}/{{,s}}bin/',
        f'usr/{target}/lib{{,32,64}}/*.so.*',
        f'usr/{target}/lib{{,32,64}}/pkgconfig/',
        f'usr/{target}/lib{{,32,64}}/*.pc',
        'usr/share/bash-completion/',
        'usr/share/man/man{1,4,5,6,7,8,9}/',
        'usr/share/locale/',
        'usr/libexec/',
        'etc/',
    )

    main.move('{,usr/local/}{,s}bin/*', 'usr/bin/')
    main.move('usr/sbin/*', 'usr/bin/')
    main.move(f'usr/{target}/sbin/*', f'usr/{target}/bin/')

    main.move('{lib,usr/local/lib}{,64}/*', 'usr/lib64/')
    main.move('{lib,usr/local/lib}32/*', 'usr/lib32/')
    main.move(f'usr/{target}/lib/*', f'usr/{target}/lib64/')

    # Devel

    devel.drain(
        'usr/include/',
        '{,usr/{,local/}}lib{,32,64}/*.{a,so}',
        f'usr/lib{{,32,64}}/{target}/*.so.*',
        'usr/share/man/man{2,3}/',
    )

    devel.move('{lib,usr/local/lib}{,64}/*', 'usr/lib64/')
    devel.move('{lib,usr/local/lib}32/*', 'usr/lib32/')
    devel.move(f'usr/{target}/lib/*', f'usr/{target}/lib64/')

    # Documentation

    documentation.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    devel.depends_on(main)

    return {
        main.id.short_name(): main,
        devel.id.short_name(): devel,
        documentation.id.short_name(): documentation,
    }
