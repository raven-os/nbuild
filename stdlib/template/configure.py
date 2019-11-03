#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``configure`` command."""

import os
import stdlib
from typing import List


def get_dir_flags() -> List[str]:
    """Build a list of directory flags used by the :py:func:`.configure` template.

    The return value is a list of directory flags that indicates where the build software should be located
    in the filesystem.

    For example, it will provide flags like::

        --prefix='/usr'
        --bindir='/usr/bin'

    etc.

    :returns: A list of flags that can be given to a configure script.
    """
    return [
        '--prefix="/usr"',
        '--exec-prefix="/usr"',
        '--bindir="/usr/bin"',
        '--sbindir="/usr/bin"',
        '--libdir="/usr/lib64"',
        '--libexecdir="/usr/lib64"',
        '--includedir="/usr/include"',
        '--datarootdir="/usr/share"',
        '--datadir="/usr/share"',
        '--mandir="/usr/share/man"',
        '--sysconfdir="/etc"',
        '--localstatedir="/var"',
    ]


def get_feature_flags() -> List[str]:
    """Build a list of feature flags used by the :py:func:`.configure` template.

    The return value is a list of feature flags that enable parts of the target software based
    on the available dependencies.

    For example, it will provide flags like::

        --with-curses
        --with-pthread

    etc.

    :returns: A list of flags that can be given to a configure script.
    """
    return [
        '--with-ncursesw',
        '--with-pthreads',
        '--with-threads',
        '--with-readline',
        '--with-history',
    ]


def configure(
    *flags: str,
    make_configure=None,
    directory_flags: bool = True,
    feature_flags: bool = True,
    binary: str = './configure',
):
    """Run ``./configure`` with a specific set of arguments.


    Some configure scripts abort on unknown flags. If ``feature_flags`` or ``directory_flags`` is ``False``, the
    default system flags usually provided by this template won't be infused in the final call, making it more flexible
    for such configure scripts.

    In such cases, it is recommended to filter-out the bad flags from the return value of :py:func:`.get_dir_flags` and
    :py:func:`.get_feature_flags` instead of rebuilding them by hand and taking the risk of missing some of them.

    Even if both ``directory_flags`` and ``feature_flags`` are ``False``, some core flags will remain infused.
    If such flags are the cause of any error from the configure script, it is recommended to run ``./configure``
    manually, using :py:func:`~stdlib.cmd.cmd`.

    :note: The prefix used is ``/usr`` (as returned by :py:func:`.get_dir_flags`). Therefore, the environment variable
        ``DESTDIR`` **must** be set (pointing to the install cache of the current build) when installing the built software.
        Otherwise, the installation can damage and overwrite parts of the host system.

    :note: Because ``flags`` is appended at the end of the argument list, it overrides any system-wide flags. This is useful
        to easily disable a feature or package  with its ``--without-PACKAGE``/``--disable-FEATURE`` equivalent.

    :param flags: A list of flags to give to the configure script.
    :param make_configure: A function that can be executed before the configure script is run.
        Useful if the configure script isn't provided and must be generated beforehand.
        The default value is ``None``.
    :param directory_flags: If ``True``, the return value of :py:func:`.get_dir_flags` is prepended to ``flags``.
    :param feature_flags: If ``True``, the return value of :py:func:`.get_feature_flags` is prepended to ``flags``.
    :param binary: A path pointing to the configure script. The default value is ``./configure``, therefore assuming
        the configure script is in the current directory.
    """

    if make_configure is not None:
        make_configure()

    # Inflate system flags
    if directory_flags:
        flags = get_dir_flags() + list(flags)

    if feature_flags:
        flags = get_feature_flags() + list(flags)

    # Call the configure script
    stdlib.cmd(f''' \
        {binary} \
            --host="{os.environ['TARGET']}" \
            --build="{os.environ['TARGET']}" \
            --target="{os.environ['TARGET']}" \
            \
            --enable-stack-protector=all \
            --enable-stackguard-randomization \
            \
            --enable-shared \
            --enable-static \
            --with-shared \
            --with-static \
            \
            --disable-werror \
            --disable-option-checking \
            \
            --with-packager='Raven-OS' \
            --with-bugurl='https://bugs.raven-os.org' \
            \
            {' '.join(flags)}
        ''')
