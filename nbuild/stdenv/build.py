#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import shutil
import random
from nbuild.args import get_args
from nbuild.log import clog, ilog
from nbuild.checks import check_package

_current_build = None


class Build():
    def __init__(self):
        self.name = _gen_random_name()
        self.current_package = None
        self.packages = []

        cwd = os.getcwd()
        cache_dir = get_args().cache_dir
        self.build_dir = os.path.join(cwd, cache_dir, 'builds/', self.name)

    def __str__(self):
        return self.name

    def queue_package(self, package):
        self.packages += [package]

    def build(self):
        clog(f"New manifest loaded. Name: {self.name}", indent=False)
        nb_packages = len(self.packages)
        ilog(f"{nb_packages} package(s) to build", indent=False)

        for (i, package) in enumerate(self.packages):
            ilog(f"    {i + 1}/{nb_packages}: {package}", indent=False)

        # Delete build directory if it already exists, and recreate it
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir, exist_ok=True)

        for (i, package) in enumerate(self.packages):
            clog(f"Building ({1}/{nb_packages}) - {package}", indent=False)
            self.current_package = package
            package.build()
            if not get_args().no_sanity_checks:
                check_package(package)
            self.current_package = None

        clog(f"Finished building packages of {self.name}.", indent=False)


def current_build():
    global _current_build
    return _current_build


def set_current_build(build):
    global _current_build
    _current_build = build


def _gen_random_name():
    with open('wordlists/adjectives.txt') as file:
        adj = next(file)
        for num, line in enumerate(file, 2):
            if random.randrange(num):
                continue
            adj = line

    with open('wordlists/nouns.txt') as file:
        noun = next(file)
        for num, line in enumerate(file, 2):
            if random.randrange(num):
                continue
            noun = line
    return f'{adj.rstrip()}-{noun.rstrip()}'
