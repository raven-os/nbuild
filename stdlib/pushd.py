#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a function to save the current working directory and switch to the given one for the duration of a new context."""

import os
from contextlib import contextmanager


@contextmanager
def pushd(path: str = '.'):
    """Save the current working directory and switch to the given one for the duration of the new context.

    :info: A default value of `path` is provided, pointing to the current working directory (`.`).
    :param path: The new current working directory.
    """
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)
