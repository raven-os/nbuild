#!/usr/bin/env python3

from nbuild.cmd import exec


class MakeTemplate:
    def compile(self):
        exec(["make", "all"])
