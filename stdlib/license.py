#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""An enumeration of possible software licenses."""

from enum import Enum


class License(Enum):
    """An enumeration of software licenses.

    :info: This enumeration is of course incomplete, and will be completed when necessary.
    """

    GPL_V1 = 'GPL v1'
    GPL_V2 = 'GPL v2'
    GPL_V3 = 'GPL v3'
    AGPL_V3 = 'AGPL v3'
    LGPL_V3 = 'LGPL v3'
    BSD = 'BSD'
    MOZILLA = 'MPL'
    MIT = 'MIT'
    APACHE = 'Apache'
    PUBLIC_DOMAIN = 'Public Domain'

    CUSTOM = 'Custom'
    NONE = 'None'
