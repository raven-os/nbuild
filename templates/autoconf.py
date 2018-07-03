#!/usr/bin/env python3

from nbuild.cmd import exec


class AutoconfTemplate:
    def configure(self):
        exec(["./configure"])
