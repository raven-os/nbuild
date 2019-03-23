#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``make`` command."""

import stdlib


def make(
    *targets: str,
    binary: str = 'make',
    folder: str = '.',
    fail_ok: bool = False,
):
    """Run ``make``.

    :note: Targets are each executed by one instance of ``make``, therefore they are run in parallel.

    :param targets: The targets to run.
    :param binary: The command or path to use. The default value is ``make``.
    :param folder: The target folder. The default value is ``.``.
    :param fail_ok: If ``True``, the execution is aborted if ``make`` fails.
    """
    stdlib.cmd(f'''{binary} -C {folder} {' '.join(targets)}''', fail_ok=fail_ok)
