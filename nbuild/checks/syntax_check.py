#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re


def id_syntax_check(id):
    pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
    if pattern.match(id) == None:
        print(f"The ID {id} doesn't respect the required syntax.")
        return 1
    return 0