#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A collection of splitters destined to applications.
"""

import stdlib.build
import stdlib.package
from typing import Dict


def standard() -> Dict[str, stdlib.package.Package]:
    """
    A standard splitter for applications that will try to build the following packages given a build named ``xxx``:

      * ``xxx``, containing the different binaries, configuration, manuals and shared files.
      * ``xxx-doc``, containing the offline documentation.

    All the generated packages don't have any pre-defined dependency.
    """
    build = stdlib.build.current_build()

    software = stdlib.package.Package(
        stdlib.package.PackageID(build.manifest.metadata.name),
    )

    documentation = stdlib.package.Package(
        stdlib.package.PackageID(f'{build.manifest.metadata.name}-doc'),
        description=f"Offline documentation of {software.id.short_name()}."
    )

    # Software

    software.drain(
        '{,usr/{,local/}}{,s}bin/*',
        'usr/libexec/',
        'usr/share/{locale,man,icons,applications}/',
        'usr/share/bash-completion/completions/',
        f'usr/share/{build.manifest.metadata.name}/',
        'etc/',
    )

    software.move('{,usr/local/}{,s}bin/*', 'usr/bin/')
    software.move('usr/sbin/*', 'usr/bin/')

    # Documentation

    documentation.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    return {
        software.id.short_name(): software,
        documentation.id.short_name(): documentation,
    }
