#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``ninja`` subcommands."""

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
    :param backend: Backend to use. Default: ``ninja``.
    :param build_type: Build type to use. Default: ``release``.
    :param build_folder: The build folder when object files should be put. Default: ``.``.
    :param source_folder: The source folder to setup. Default: ``.``.
    :param fail_ok: If ``False``, the execution is aborted if ``ninja`` fails.
        The default value is ``False``.
    """
    stdlib.cmd(f'''{binary} -C "{folder}" {' '.join(args)} ''', fail_ok=fail_ok)
