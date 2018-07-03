#!/usr/bin/env python3

from nbuild.manifest import BuildManifest
from templates.gnu import GnuTemplate


CATEGORY = "sys-bin"
NAME = "coreutils"
VERSION = "8.29.0"
RUN_DEPENDENCIES = {
    "stable::sys-lib/libc": ">=2.27.0"
}


class CoreutilsManifest(GnuTemplate, BuildManifest):
    def __init__(self):
        BuildManifest.__init__(self, CATEGORY, NAME, VERSION, RUN_DEPENDENCIES)
        GnuTemplate.__init__(
            self,
            fetch={
                "url": "http://ftp.gnu.org/gnu/coreutils/coreutils-8.29.tar.xz",
                "md5sum": "960cfe75a42c9907c71439f8eb436303",
            },
        )

CoreutilsManifest().build()
