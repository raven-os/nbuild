#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides an exhaustive template that downloads, builds and wraps a software based on ``cargo`` and ``rust``.
"""

import os
import stdlib
import stdlib.fetch
import stdlib.extract
import stdlib.patch
import stdlib.split.system
import stdlib.deplinker.elf
from multiprocessing import cpu_count


def cargo_build(
    *args: str,
    cargo_binary: str = 'cargo',
    fail_ok: bool = False,
):
    """Run ``cargo build``.

    :param args: Any extra arguments to give to cargo
    :param cargo_binary: The command or path to use. The default value is ``cargo``.
    :param fail_ok: If ``False``, the execution is aborted if ``cargo`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{cargo_binary} build --release {' '.join(args)} ''', fail_ok=fail_ok)


def cargo_check(
    *args: str,
    cargo_binary: str = 'cargo',
    fail_ok: bool = False,
):
    """Run ``cargo build``.

    :param args: Any extra arguments to give to cargo
    :param cargo_binary: The command or path to use. The default value is ``cargo``.
    :param fail_ok: If ``False``, the execution is aborted if ``cargo`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{cargo_binary} check --release {' '.join(args)} ''', fail_ok=fail_ok)


def cargo_install(
    *args: str,
    path='.',
    cargo_binary: str = 'cargo',
    fail_ok: bool = False,
):
    """Run ``cargo install``.

    :param args: Any extra arguments to give to cargo
    :param path: The path pointing to the directory or Cargo manifest to install.
    :param cargo_binary: The command or path to use. The default value is ``cargo``.
    :param fail_ok: If ``False``, the execution is aborted if ``cargo`` fails.
        The default value is ``False``.
    """
    build = stdlib.build.current_build()

    stdlib.cmd(f'''{cargo_binary} install --root={build.install_cache} --path={path} {' '.join(args)}''', fail_ok=fail_ok)


def build(
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    build=cargo_build,
    check=cargo_check,
    install=cargo_install,
    split=stdlib.split.system.system,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap a software based on ``cargo`` and ``rust``.

    This exhaustive template is made of 8 steps:
        * ``fetch``
        * ``extract``
        * ``patch``
        * ``build``
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

    **Build**

        This step compiles the source code. The default value is :py:func:`.cargo_build`, with no argument.

    **Check**

        This step runs the unit and integration tests. The default value is :py:func:`.cargo_check`, with no argument.

    **Install**

        This step installs the software in the install cache. The default value is :py:func:`.cargo_install`, with no argument.

    **Split**

        This step automatically splits the output of the build into multiple packages. The default value is :py:func:`~stdlib.split.system.system`.
        Alternative splitters can be found in the :py:mod:`~stdlib.split` module.

    **Dependency Linking**

        This step automatically finds requirements for the generated packages. The default value is :py:func:`~stdlib.deplinker.elf.elf_deplinker`.
        Alternative dependency linkers can be found in the :py:mod:`~stdlib.deplinker` module.

    """
    stdlib.log.ilog("Step 1/8: Fetch")
    if fetch is not None:
        with stdlib.log.pushlog():
            fetch()

    stdlib.log.ilog("Step 2/8: Extract")
    if extract is not None:
        with stdlib.log.pushlog():
            extract()

    stdlib.log.ilog("Step 3/8: Patch")
    if patch is not None:
        with stdlib.log.pushlog():
            patch()

    stdlib.log.ilog("Step 4/8: Build")
    if build is not None:
        with stdlib.log.pushlog():
            build()

    stdlib.log.ilog("Step 5/8: Check")
    if check is not None:
        with stdlib.log.pushlog():
            check()

    stdlib.log.ilog("Step 6/8: Install")
    if install is not None:
        with stdlib.log.pushlog(), stdlib.pushenv():
            install()

    stdlib.log.ilog("Step 7/8: Split")
    if split is not None:
        with stdlib.log.pushlog():
            packages = split()

            if len(packages) > 0:
                stdlib.log.ilog("The following packages were generated:")

                with stdlib.log.pushlog():
                    for package in packages.values():
                        stdlib.log.ilog(str(package))

    stdlib.log.ilog("Step 8/8: Dependency Linking")
    if deplinker is not None:
        with stdlib.log.pushlog():
            deplinker(packages)

    return packages
