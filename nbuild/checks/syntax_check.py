#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re
from nbuild.log import elog, ilog, wlog


def id_syntax_check(package):
    ilog("Checking id")
    pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
    if pattern.match(package.id) is None:
        elog(f"The ID {package.id} doesn't respect the required syntax.")
        return False
    return True


def desc_syntax_check(package):
    ilog("Checking description")
    pattern = re.compile(r'^[A-Z].*\.$')
    if pattern.match(package.description) is None:
        elog(
            f"The description of the package {package.id} "
            "doesn't respect the required syntax."
            )
        return False
    return True


def check_syntax(pkg):
    ret = all([
        id_syntax_check(pkg),
        desc_syntax_check(pkg),
    ])
    if ret:
        ilog("\tAll syntax checks OK")
    else:
        wlog("\tSome syntax checks failed")
    return ret
