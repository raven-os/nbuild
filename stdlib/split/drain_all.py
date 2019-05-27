#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
A very basic and primitive splitter that drains all the output files of a build into a single package, named after the
:py:class:`.BuildManifest`.
"""

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

    return {package.id.short_name(): package}
