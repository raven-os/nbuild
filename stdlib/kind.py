#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""An enumeration of all possible kinds for a package."""

from enum import Enum


class Kind(Enum):
    """An enumeration of all kinds for a package."""

    EFFECTIVE = 'effective'
    VIRTUAL = 'virtual'
