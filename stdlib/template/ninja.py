#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``ninja`` subcommands."""

import os
import stdlib


def ninja(
    *args: str,
    binary: str = 'ninja',
    folder: str = '.',
    fail_ok: bool = False,
):
    """Run ``ninja``.

    :param args: Any extra arguments to give to ``ninja``.
    :param binary: The command or path to use. The default value is ``ninja``.
    :param folder: The target folder. The default value is ``.``.
    :param fail_ok: If ``False``, the execution is aborted if ``ninja`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{binary} -C "{folder}" {' '.join(args)} ''', fail_ok=fail_ok)


def ninja_test(
    *args: str,
    binary: str = 'ninja',
    folder: str = '.',
    fail_ok: bool = False,
):
    """Run ``ninja test``.

    :param args: Any extra arguments to give to ``ninja``.
    :param binary: The command or path to use. The default value is ``ninja``.
    :param folder: The target folder. The default value is ``.``.
    :param fail_ok: If ``False``, the execution is aborted if ``ninja`` fails.
        The default value is ``False``.
    """
    ninja('test', *args, binary=binary, folder=folder, fail_ok=fail_ok)


def ninja_install(
    *args: str,
    target: str = '',
    binary: str = 'ninja',
    folder: str = '.',
    fail_ok: bool = False,
):
    """Run ``ninja install``.

    :param args: Any extra arguments to give to ``ninja``.
    :param binary: The command or path to use. The default value is ``ninja``.
    :param folder: The target folder. The default value is ``.``.
    :param fail_ok: If ``False``, the execution is aborted if ``ninja`` fails.
        The default value is ``False``.
    """
    with stdlib.pushenv():
        if not os.environ['DESTDIR']:
            os.environ['DESTDIR'] = stdlib.build.current_build().install_cache
    ninja('install', *args, binary=binary, folder=folder, fail_ok=fail_ok)
