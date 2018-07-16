#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from contextlib import contextmanager


@contextmanager
def pushenv():
    old_env = deepcopy(os.environ)
    try:
        yield
    finally:
        os.environ = old_env
