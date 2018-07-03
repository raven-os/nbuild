#!/usr/bin/env python3

import os
import toml
from nbuild.log import *
from nbuild.args import get_args


class BuildManifest:
    def __init__(self, category, name, version, build_deps={}, run_deps={}):
        self.category = category
        self.name = name
        self.version = version
        self.run_dependencies = run_deps
        self.build_dependencies = build_deps

        directory = "{}/{}/{}".format(category, name, version)
        self.build_dir = os.path.join(
            os.getcwd(),
            get_args().build_dir,
            directory
        )
        self.pkg_dir = os.path.join(
            os.getcwd(),
            get_args().pkg_dir,
            directory
        )

    def build(self):
        ilog(
            "Building {}/{}#{}"
            .format(self.category, self.name, self.version),
            indent=False
        )

        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

        os.chdir(self.build_dir)

        ilog("Step 1/7: Fetch", indent=False)
        self.fetch()

        ilog("Step 2/7: Unpack", indent=False)
        self.unpack()

        ilog("Step 3/7: Patch", indent=False)
        self.patch()

        ilog("Step 4/7: Configure", indent=False)
        self.configure()

        ilog("Step 5/7: Compile", indent=False)
        self.compile()

        ilog("Step 6/7: Check", indent=False)
        self.check()

        ilog("Step 7/7: Wrap", indent=False)

        if not os.path.exists(self.pkg_dir):
            os.makedirs(self.pkg_dir)
        self.wrap()

        os.chdir(self.pkg_dir)
        with open("manifest.toml", "w") as f:
            manifest = {
                "metadata": {
                    "name": self.name,
                    "category": self.category,
                    "version": self.version
                },
                "dependencies": self.build_dependencies,
            }
            toml.dump(manifest, f)

        clog(
            "Done! Manifest and datas saved in \"{}\""
            .format(self.pkg_dir),
            indent=False
        )

    def fetch(self):
        pass

    def unpack(self):
        pass

    def patch(self):
        pass

    def configure(self):
        pass

    def compile(self):
        pass

    def check(self):
        pass

    def wrap(self):
        pass
