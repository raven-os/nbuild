#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides an exhaustive template that downloads, builds and wraps a software without assuming any of the build system used.
"""

import os
import stdlib
import stdlib.fetch
import stdlib.extract
import stdlib.patch
import stdlib.split.system
import stdlib.deplinker.elf


def build(
    build_folder='.',
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    configure=None,
    compile=None,
    check=None,
    install=None,
    split=stdlib.split.system.system,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap a software based on any build system.
    Use this template when there is no more appropriate exhaustive template for your use-case.

    This exhaustive template is made of 9 steps:
        * ``fetch``
        * ``extract``
        * ``patch``
        * ``configure``
        * ``compile``
        * ``check``
        * ``install``
        * ``split``
        * ``dependency linking``

    For each one of these steps, a function is called. This template simply calls each of them in the above order.
    All of these functions can be given as arguments, but each one of them has a default value that is explained below.
    If any of those functions is ``None``, the step is skipped.

    **Fetch**

        This step is used to download the source code. The default value is :py:func:`.fetch` with no argument.

    **Extract**

        This step is used to extract the downloaded source code. The default value is :py:func:`.flat_extract_all` with no argument.

    **Patch**

        This step is used to patch the downloaded source code. The default value is :py:func:`.patch_all` with no argument.

    From now on, the current working directory is changed in favor of ``build_folder`` (which defaults to ``.``).
    If the directory pointed by ``build_folder`` doesn't exist, it is created.

    This is useful for the few ``configure`` scripts that don't work if they aren't executed in a standalone directory.

    **Configure**

        This step is used to configure the source code. The default value is ``None``.

    **Compile**

        This step is used to build the source code. The default value is ``None``.

    **Check**

        This step is used to test the built binaries. The default value is ``None``.

    **Install**

        This step is used to install the software in the install cache. The default value is ``None``.

    **Split**

        This step automatically splits the output of the build into multiple packages. The default value is :py:func:`~stdlib.split.system.system`.
        Alternative splitters can be found in the :py:mod:`~stdlib.split` module.

    **Dependency Linking**

        This step automatically finds requirements for the generated packages. The default value is :py:func:`~stdlib.deplinker.elf.elf_deplinker`.
        Alternative dependency linkers can be found in the :py:mod:`~stdlib.deplinker` module.

    """
    build = stdlib.build.current_build()

    stdlib.log.ilog("Step 1/9: Fetch")
    if fetch is not None:
        with stdlib.log.pushlog():
            fetch()

    stdlib.log.ilog("Step 2/9: Extract")
    if extract is not None:
        with stdlib.log.pushlog():
            extract()

    stdlib.log.ilog("Step 3/9: Patch")
    if patch is not None:
        with stdlib.log.pushlog():
            patch()

    os.makedirs(build_folder, exist_ok=True)
    with stdlib.pushd(build_folder):
        stdlib.log.ilog("Step 4/9: Configure")
        if configure is not None:
            with stdlib.log.pushlog():
                configure()

        stdlib.log.ilog("Step 5/9: Compile")
        if compile is not None:
            with stdlib.log.pushlog():
                compile()

        stdlib.log.ilog("Step 6/9: Check")
        if check is not None:
            with stdlib.log.pushlog():
                check()

        stdlib.log.ilog("Step 7/9: Install")
        if install is not None:
            with stdlib.log.pushlog(), stdlib.pushenv():
                os.environ['DESTDIR'] = build.install_cache
                install()

        stdlib.log.ilog("Step 8/9: Split")
        if split is not None:
            with stdlib.log.pushlog():
                packages = split()

                if len(packages) > 0:
                    stdlib.log.ilog("The following packages were generated:")

                    with stdlib.log.pushlog():
                        for package in packages.values():
                            stdlib.log.ilog(str(package))

        stdlib.log.ilog("Step 9/9: Dependency Linking")
        if deplinker is not None:
            with stdlib.log.pushlog():
                deplinker(packages)

    return packages
