#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides an exhaustive  template that wraps the ``meson``+``ninja`` commonly used combination."""

import stdlib
import stdlib.template.meson
import stdlib.template.ninja
from stdlib.template import basic


def build(
    build_folder='build',
    fetch=stdlib.fetch.fetch,
    extract=stdlib.extract.flat_extract_all,
    patch=stdlib.patch.patch_all,
    configure=stdlib.template.meson.meson,
    compile=stdlib.template.ninja.ninja,
    check=stdlib.template.ninja.ninja_test,
    install=stdlib.template.ninja.ninja_install,
    split=stdlib.split.system.system,
    deplinker=stdlib.deplinker.elf.elf_deplinker,
):
    """Download, build and wrap a software based on ``meson`` and ``ninja``.

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

        This step is used to patch the downloaded source code. The default value is :py:func:`.patch_all`, with no argument.

    From now on, the current working directory is changed in favor of ``build_folder`` (which defaults to ``./build``).
    If the directory pointed by ``build_folder`` doesn't exist, it is created.

    **Configure**

        This step is used to configure the source code. The default value is :py:func:`.meson`, with no argument.

    **Build**

        This step compiles the source code. The default value is :py:func:`.ninja`, with no argument.

    **Check**

        This step runs the unit and integration tests. The default value is :py:func:`.ninja_test`, with no argument.

    **Install**

        This step installs the software in the install cache. The default value is :py:func:`.ninja_install`, with no argument.

    **Split**

        This step automatically splits the output of the build into multiple packages. The default value is :py:func:`~stdlib.split.system.system`.
        Alternative splitters can be found in the :py:mod:`~stdlib.split` module.

    **Dependency Linking**

        This step automatically finds requirements for the generated packages. The default value is :py:func:`~stdlib.deplinker.elf.elf_deplinker`.
        Alternative dependency linkers can be found in the :py:mod:`~stdlib.deplinker` module.

    """
    return basic.build(
        build_folder=build_folder,
        fetch=fetch,
        extract=extract,
        patch=patch,
        configure=configure,
        compile=compile,
        check=check,
        install=install,
        split=split,
        deplinker=deplinker,
    )
