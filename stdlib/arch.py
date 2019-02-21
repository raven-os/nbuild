#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""An enumeration of CPU architectures."""

from enum import Enum


class Arch(Enum):
    """An enumeration of CPU architectures.

    :info: This enumeration is of course incomplete, and will be completed when necessary.
    """
    X86_64 = 'x86_64'
    X86 = 'x86'
    ARM = 'arm'
    ARM64 = 'arm64'
