#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a small, partial template that wraps the ``cmake`` build generator."""

import stdlib
from typing import Dict


def cmake(
        generator: str = 'Unix Makefiles',
        binary: str = 'cmake',
        folder: str = '.',
        cache_entries: Dict[str, str] = None,
        fail_ok: bool = False
):
    """Run ``cmake`` to generate build files.

    :param generator: The build generator to generate build files for. The default value is 'Unix Makefiles'.
    :param binary: The command or path to the command to use. The default value is ``cmake``.
    :param folder: The target folder. The default value is ``.``.
    :param cache_entries: A dictionary whose entries are to be populated into the cmake cache.
    :param fail_ok: If ``False``, the execution is aborted if ``cmake`` fails.
    """
    cache_entries = cache_entries or {}
    cache_entries_options = ' '.join(f'-D{key}={value}' for key, value in cache_entries.items())
    stdlib.cmd(f'''{binary} -G '{generator}' {cache_entries_options} {folder}''', fail_ok=fail_ok)
