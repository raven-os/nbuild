#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides an exhaustive template that downloads, builds and wraps a software based on ``python``'s ``distutils``.
"""

import os
import stdlib
import stdlib.fetch
import stdlib.extract
import stdlib.patch
import stdlib.split.drain_all
import stdlib.deplinker.elf


def distutils_build(
    *args: str,
    python_binary: str = 'python3',
    script_path: str = './setup.py',
    fail_ok: bool = False,
):
    """Run ``python3 ./setup.py build``.

    :param args: Any extra arguments to give to ``setup.py``
    :param python_binary: The command or path to use. The default value is ``python3``.
    :param script_path: The path to the distutils script. The default value is ``./setup.py``.
    :param fail_ok: If ``False``, the execution is aborted if ``setup.py`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{python_binary} {script_path} build {' '.join(args)} ''', fail_ok=fail_ok)


def distutils_check(
    *args: str,
    python_binary: str = 'python3',
    script_path: str = './setup.py',
    fail_ok: bool = False,
):
    """Run ``python3 ./setup.py check``.

    :param args: Any extra arguments to give to ``setup.py``
    :param python_binary: The command or path to use. The default value is ``python3``.
    :param script_path: The path to the distutils script. The default value is ``./setup.py``.
    :param fail_ok: If ``False``, the execution is aborted if ``setup.py`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{python_binary} {script_path} check {' '.join(args)} ''', fail_ok=fail_ok)


def distutils_install(
    *args: str,
    python_binary: str = 'python3',
    script_path: str = './setup.py',
    fail_ok: bool = False,
):
    """Run ``python3 ./setup.py install``.

    :param args: Any extra arguments to give to ``setup.py``
    :param python_binary: The command or path to use. The default value is ``python3``.
    :param script_path: The path to the distutils script. The default value is ``./setup.py``.
    :param fail_ok: If ``False``, the execution is aborted if ``setup.py`` fails.
        The default value is ``False``.
    """
    build = stdlib.build.current_build()

    stdlib.cmd(f'''{python_binary} {script_path} install --prefix=/usr --root={build.install_cache} {' '.join(args)} ''', fail_ok=fail_ok)


def build(
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    build=distutils_build,
    check=distutils_check,
    install=distutils_install,
    split=stdlib.split.drain_all.drain_all_with_doc,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap a software based on ``python``'s ``distutils``.

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

        This step compiles the source code. The default value is :py:func:`.distutils_build`, with no argument.

    **Check**

        This step runs the unit and integration tests. The default value is :py:func:`.distutils_check`, with no argument.

    **Install**

        This step installs the software in the install cache. The default value is :py:func:`.distutils_install`, with no argument.

    **Split**

        This step automatically splits the output of the build into multiple packages. The default value is :py:func:`~stdlib.split.drain_all.drain_all_with_doc`.
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
