#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``cmake`` build generator."""

import stdlib
from typing import Dict, List


def get_dir_flags() -> List[str]:
    """
    Build a list of directory flags used by the :py:func:`.cmake` template.

    The return value is a list of directory flags that indicates where the built software should be located in the filesystem.

    For example, it will provide flags like:

        -DCMAKE_INSTALL_PREFIX="/usr"
        -DCMAKE_INSTALL_BINDIR="/usr/bin"

    etc.

    :returns: A list of flags that can be given to cmake executable.
    """

    return [
        '-DCMAKE_INSTALL_PREFIX="/usr"',
        '-DCMAKE_INSTALL_BINDIR="/usr/bin"',
        '-DCMAKE_INSTALL_SBINDIR="/usr/bin"',
        '-DCMAKE_INSTALL_LIBDIR="/usr/lib64"',
        '-DCMAKE_INSTALL_LIBEXECDIR="/usr/lib64"',
        '-DCMAKE_INSTALL_INCLUDEDIR="/usr/include"',
        '-DCMAKE_INSTALL_DATAROOTDIR="/usr/share"',
        '-DCMAKE_INSTALL_DATADIR="/usr/share"',
        '-DCMAKE_INSTALL_MANDIR="/usr/share/man"',
        '-DCMAKE_INSTALL_SYSCONFDIR="/etc"',
        '-DCMAKE_INSTALL_LOCALSTATEDIR="/var"'
    ]


def cmake(
        *flags: str,
        folder: str = '.',
        generator: str = 'Unix Makefiles',
        build_type: str = 'Release',
        directory_flags: str = True,
        binary: str = 'cmake',
        fail_ok: bool = False
):
    """Run ``cmake`` to generate build files.

    :param flags: A list of flags to give to the cmake binary.
    :param folder: The target folder. The default value is ``.``.
    :param generator: The build generator to generate build files for. The default value is 'Unix Makefiles'.
    :param build_type: The build type to select to build
    :param directory_flags: If ``True``, the return value of :py:func:`.get_dir_flags` is prepended to ``flags``.
    :param binary: The command or path to the command to use. The default value is ``cmake``.
    :param fail_ok: If ``False``, the execution is aborted if ``cmake`` fails.
    """

    if directory_flags:
        flags = get_dir_flags() + list(flags)

    stdlib.cmd(
        f'''{binary} -G '{generator}' -DCMAKE_BUILD_TYPE={build_type} {' '.join(flags)} {folder}''', fail_ok=fail_ok
    )
