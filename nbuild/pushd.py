#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager


@contextmanager
def pushd(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)
