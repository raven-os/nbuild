#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from nbuild.cmd import cmd


def do_make(
    binary="make",
    folder=".",
    target="",
    extra_args=[],
    **kwargs,
):
    cmd(
        f'''{binary} -C {folder} {target} {' '.join(extra_args)}''',
        **kwargs
    )
