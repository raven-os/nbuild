#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides an exhaustive template that downloads, builds and wraps a software based on ``autoconf`` and ``make``.
"""

import os
import stdlib
import stdlib.fetch
import stdlib.extract
import stdlib.patch
import stdlib.split.system
import stdlib.deplinker.elf

from stdlib.template.configure import configure
from stdlib.template.make import make


def build(
    build_folder='.',
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    configure=configure,
    compile=make,
    check=lambda: make('check', fail_ok=True),
    install=lambda: make('install', f'DESTDIR={stdlib.build.current_build().install_cache}'),
    split=stdlib.split.system.system,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap a software based on ``autoconf`` and ``make``.

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

        This step uses the ``configure`` script to configure the source code. The default value is :py:func:`.configure` with no argument.

        When ``build_folder`` isn't ``.``, it is usually necessary to override this step with an other call to :py:func:`.configure` with
        the argument ``binary='../configure'``.

    **Compile**

        This step compiles the source code. The default value is :py:func:`.make` with no argument.

    **Check**

        This step runs the unit and integration tests. The default value is :py:func:`.make` with the arguments ``'check'`` and ``fail_ok=True``.

    **Install**

        This step installs the software in the install cache. The default value is :py:func:`.make` with the arguments ``'install'`` and
        ``f'DESTDIR={stdlib.build.current_build().install_cache}'``

        If this step is overriden, the ``DESTDIR`` variable is crucial and should be reused. Otherwise, and unless the ``configure`` script has been
        configured to work without it, the installation can damage and overwrite parts of the host system.

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

    packages = dict()

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


def build_all(
    build_folder='.',
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    compilations=[],
    split=stdlib.split.system.system,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap multiple configurations of the same software based on ``autoconf`` and ``make``.

    This exhaustive template is made of 9 steps, where some of them are repeatable:
        * ``fetch``
        * ``extract``
        * ``patch``
        * ``compilation``, which is an array containing multiple iterations of the following steps:
            * ``clean_before``
            * ``configure``
            * ``compile``
            * ``check``
            * ``install``
            * ``clean_after``
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

    From now on, the following four steps are repeated for each item in ``compilation``. Each item must be an object containing
    a ``clean_before``, ``configure``, ``compile``, ``check``, ``install`` and ``clean_after`` key where the value must be a function.
    If the key is not present, the default value is taken instead.

    There is persistence in a all caches of the build. Therefore, the build folder is dirty of any previous iteration, as is the install cache
    and any other cache. This means that it is usually wise to run ``make clean`` before compiling the package again, hence the
    ``clean_before`` and ``clean_after`` steps.

    For each iteration, the current working directory is changed in favor of ``build_folder`` (which defaults to ``.``).
    If the directory pointed by ``build_folder`` doesn't exist, it is created.

    This is useful for the few ``configure`` scripts that don't work if they aren't executed in a standalone directory.

    **Clean Before**

        This step is used to clean any cache from impurities left by the previous iteration, before configuring and compiling the source code.

    **Configure**

        This step uses the ``configure`` script to configure the source code. The default value is :py:func:`.configure` with no argument.

        When ``build_folder`` isn't ``.``, it is usually necessary to override this step with an other call to :py:func:`.configure` with
        the argument ``binary='../configure'``.

    **Compile**

        This step compiles the source code. The default value is :py:func:`.make` with no argument.

    **Check**

        This step runs the unit and integration tests. The default value is :py:func:`.make` with the arguments ``'check'`` and ``fail_ok=True``.

    **Install**

        This step installs the software in the install cache. The default value is :py:func:`.make` with the arguments ``'install'`` and
        ``f'DESTDIR={stdlib.build.current_build().install_cache}'``

        If this step is overriden, the ``DESTDIR`` variable is crucial and should be reused. Otherwise, and unless the ``configure`` script has been
        configured to work without it, the installation can damage and overwrite parts of the host system.

    **Clean After**

        This step is used to clean any cache from impurities left by the current iteration, after configuring and compiling the source code.

    **Split**

        This step automatically splits the output of the build into multiple packages. The default value is :py:func:`~stdlib.split.system.system`.
        Alternative splitters can be found in the :py:mod:`~stdlib.split` module.

    **Dependency Linking**

        This step automatically finds requirements for the generated packages. The default value is :py:func:`~stdlib.deplinker.elf.elf_deplinker`.
        Alternative dependency linkers can be found in the :py:mod:`~stdlib.deplinker` module.

    """
    build = stdlib.build.current_build()

    nb_steps = 5 + len(compilations) * 6

    stdlib.log.ilog(f"Step 1/{nb_steps}: Fetch")
    if fetch is not None:
        with stdlib.log.pushlog():
            fetch()

    stdlib.log.ilog(f"Step 2/{nb_steps}: Extract")
    if extract is not None:
        with stdlib.log.pushlog():
            extract()

    stdlib.log.ilog(f"Step 3/{nb_steps}: Patch")
    if patch is not None:
        with stdlib.log.pushlog():
            patch()

    packages = dict()

    os.makedirs(build_folder, exist_ok=True)
    with stdlib.pushd(build_folder):
        for idx, compilation in enumerate(compilations):

            relative_step = 3 + idx * 6

            stdlib.log.ilog(f"Step {relative_step + 1}/{nb_steps}: Clean before")
            if compilation.get('clean_before') is not None:
                with stdlib.log.pushlog():
                    compilation['clean_before']()

            stdlib.log.ilog(f"Step {relative_step + 2}/{nb_steps}: Configure")
            if compilation.get('configure') is None:
                compilation['configure'] = configure
            with stdlib.log.pushlog():
                compilation['configure']()

            stdlib.log.ilog(f"Step {relative_step + 3}/{nb_steps}: Compilation")
            if compilation.get('compile') is None:
                compilation['compile'] = make
            with stdlib.log.pushlog():
                compilation['compile']()

            stdlib.log.ilog(f"Step {relative_step + 4}/{nb_steps}: Check")
            if compilation.get('check') is None:
                compilation['check'] = lambda: make('check', fail_ok=True)
            with stdlib.log.pushlog():
                compilation['check']()

            stdlib.log.ilog(f"Step {relative_step + 5}/{nb_steps}: Install")
            if compilation.get('install') is None:
                compilation['install'] = lambda: make('install', f'DESTDIR={stdlib.build.current_build().install_cache}')
            with stdlib.log.pushlog(), stdlib.pushenv():
                os.environ['DESTDIR'] = build.install_cache
                compilation['install']()

            stdlib.log.ilog(f"Step {relative_step + 6}/{nb_steps}: Clean after")
            if compilation.get('clean_after') is not None:
                with stdlib.log.pushlog():
                    compilation['clean_after']()

        stdlib.log.ilog(f"Step {nb_steps-1}/{nb_steps}: Split")
        if split is not None:
            with stdlib.log.pushlog():
                packages = split()

                if len(packages) > 0:
                    stdlib.log.ilog("The following packages were generated:")

                    with stdlib.log.pushlog():
                        for package in packages.values():
                            stdlib.log.ilog(str(package))

        stdlib.log.ilog(f"Step {nb_steps}/{nb_steps}: Dependency Linking")
        if deplinker is not None:
            with stdlib.log.pushlog():
                deplinker(packages)

    return packages
