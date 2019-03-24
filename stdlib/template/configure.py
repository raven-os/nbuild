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
        '--bindir="/usr/bin"',
        '--sbindir="/usr/bin"',
        '--libdir="/usr/lib64"',
        '--libexecdir="/usr/libexec"',
        '--includedir="/usr/include"',
        '--datarootdir="/usr/share"',
        '--datadir="/usr/share"',
        '--infodir="/usr/share/info"',
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
        '--with-curses',
        '--with-cursesw',
        '--with-ncurses',
        '--with-ncursesw',
        '--with-pthreads',
        '--with-threads',
        '--with-readline',
        '--with-history',
    ]


def get_flags() -> List[str]:
    """Build a list of system-wide flags used by the :py:func:`.configure` template.

    :returns: The merged output of :py:func:`.get_dir_flags` and :py:func:`.get_feature_flags`.
    """
    return get_dir_flags() + get_feature_flags()


def configure(
    *flags: str,
    system_flags: bool = True,
    binary: str = './configure',
):
    """Run ``./configure`` with a specific set of arguments.

    The flags given to the configure script are both the return value of :py:func:`.get_flags()` and the given ``flags``.

    Some configure scripts abort on unknown flags. If ``system_flags`` is ``False``, the default system flags
    usually provided by this template won't be infused in the final call, making it more flexible for such
    configure scripts.

    In such cases, it is recommended to filter-out the bad flags from the return value of :py:func:`.get_flags` instead of
    rebuilding them by hand and taking the risk of missing some of them.

    Even if ``system_flags`` is ``False``, some core flags will remain infused.
    If such flags are the cause of any error from the configure script, it is recommended to run ``./configure``
    manually, using :py:func:`~stdlib.cmd.cmd`.

    :note: The prefix used is ``/usr`` (as returned by :py:func:`.get_dir_flags`). Therefore, the environment variable
        ``DESTDIR`` **must** be set (pointing to the install cache of the current build) when installing the built software.
        Otherwise, the installation can damage and overwrite parts of the host system.

    :note: Because ``flags`` is appended at the end of the argument list, it overrides any system-wide flags. This is useful
        to easily disable a feature or package  with its ``--without-PACKAGE``/``--disable-FEATURE`` equivalent.

    :param flags: A list of flags to give to the configure script.
    :param system_flags: Indicate whether or not the template should include the system flags returned by :py:func:`.get_flags`.
        The default value is ``True``.
    :param binary: A path pointing to the configure script. The default value is ``./configure``, therefore assuming
        the configure script is in the current directory.
    """

    # Inflate system flags
    if system_flags:
        flags = get_flags() + list(flags)

    # Call the configure script
    stdlib.cmd(f''' \
        {binary} \
            --build="{os.environ['TARGET']}" \
            --host="{os.environ['HOST']}" \
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
