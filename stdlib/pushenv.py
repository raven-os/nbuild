#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides a function to save the current environment for the duration of a new context."""

import os
from copy import deepcopy
from contextlib import contextmanager


@contextmanager
def pushenv():
    """Save the current environment for the duration of the new context."""

    old_env = deepcopy(os.environ)
    try:
        yield
    finally:
        os.environ = old_env
