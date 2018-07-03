#!/usr/bin/env python3

from nbuild.manifest import BuildManifest
from templates.gnu import GnuTemplate


CATEGORY = "sys-bin"
NAME = "sed"
VERSION = "4.4.0"
RUN_DEPENDENCIES = {
    "stable::sys-lib/libc": ">=2.27.0"
}


class SedManifest(GnuTemplate, BuildManifest):
    def __init__(self):
        BuildManifest.__init__(self, CATEGORY, NAME, VERSION, RUN_DEPENDENCIES)
        GnuTemplate.__init__(
            self,
            fetch={
                "url": "http://ftp.gnu.org/gnu/sed/sed-4.4.tar.xz",
                "md5sum": "e0c583d4c380059abd818cd540fe6938",
            },
        )

SedManifest().build()
