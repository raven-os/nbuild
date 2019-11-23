#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``meson`` subcommands."""

import stdlib


def meson(
    *args: str,
    binary: str = 'meson',
    backend: str = 'ninja',
    build_type: str = 'release',
    fail_ok: bool = False,
):
    """Run ``meson setup``.

    :note: Most ``--*dir`` flags are automatically added, but can be overriden with the extra ``args`` argument.
    :param args: Any extra arguments to give to ``meson setup``.
    :param binary: The command or path to use. The default value is ``meson``.
    :param backend: Backend to use. Default: ``ninja``.
    :param build_type: Build type to use. Default: ``release``.
    :param fail_ok: If ``False``, the execution is aborted if ``cargo`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''\
        {binary} setup \
            --prefix="/usr" \
            --bindir="/usr/bin" \
            --sbindir="/usr/bin" \
            --libdir="/usr/lib64" \
            --libexecdir="/usr/lib64" \
            --includedir="/usr/include" \
            --datadir="/usr/share" \
            --mandir="/usr/share/man" \
            --sysconfdir="/etc" \
            --localstatedir="/var" \
            --backend="{backend}" \
            --buildtype="{build_type}" \
            {' '.join(args)} \
        ''',
        fail_ok=fail_ok,
    )
