#!/usr/bin/env python3

from nbuild.log import *
from nbuild.cmd import exec


class GitTemplate:
    def __init__(self, url):
        self.url = url

    def fetch(self):
        exec(["git", "clone", self.url])
