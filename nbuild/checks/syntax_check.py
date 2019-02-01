#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re
from nbuild.log import elog
from nbuild.stdenv.package import Package


def id_syntax_check(package):
    pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
    if pattern.match(package.id) == None:
        elog(
            f"The ID {package.id} doesn't respect the required syntax."
            )
        return 1
    return 0


def desc_syntax_check(package):
    pattern = re.compile(r'^[A-Z].*\.$')
    if pattern.match(package.description) == None:
        elog(
            f"The description of the package {package.id} "
            "doesn't respect the required syntax."
            )
        return 1
    return 0