#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Functions to parse and retrieve the TOML configuration."""

import toml
import core.args
import stdlib.log
from typing import Dict

nbuild_config = None


def load_config():
    """Load the TOML configuration file pointed to by the argument ``--config``."""
    global nbuild_config

    nbuild_config = toml.load(core.args.get_args().config)


def get_config() -> Dict[str, object]:
    """Return the parsed configuration as a dictionary.

    :note: There is no guarantee whatsoever regarding the content of this dictionary.
        Therefore, it is the responsability of the caller to ensure any field is actually present in
        the returned dictionary.
    """
    return nbuild_config
