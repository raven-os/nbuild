#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""An enumeration of possible software licenses."""

from enum import Enum


class License(Enum):
    """An enumeration of software licenses.

    :info: This enumeration is of course incomplete, and will be completed when necessary.
    """

    GPL_V1 = 'gpl_v1'
    GPL_V2 = 'gpl_v2'
    GPL_V3 = 'gpl_v3'
    AGPL_V3 = 'agpl_v3'
    LGPL_V3 = 'lgpl_v3'
    BSD = 'bsd'
    MOZILLA = 'mozilla'
    MIT = 'mit'
    APACHE = 'apache'
    PUBLIC_DOMAIN = 'public_domain'

    CUSTOM = 'custom'
    NONE = 'none'
