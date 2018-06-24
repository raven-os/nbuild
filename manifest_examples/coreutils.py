import templates.common
import templates.make
import templates.autotools


class BuildManifest(templates.common.Common):
    def __init__(self):
        templates.common.Common.__init__(self, "coreutils", "8.29",
                                         fetch={"url": "http://ftp.gnu.org/gnu/coreutils/coreutils-8.29.tar.xz",
                                                "md5sum": "960cfe75a42c9907c71439f8eb436303"},
                                         patch={"url": "http://www.linuxfromscratch.org/patches/lfs/8.2/coreutils-8.29-i18n-1.patch",
                                                "md5sum": "a9404fb575dfd5514f3c8f4120f9ca7d"},
                                         configure={"enable-no-install-program=kill,uptime": None,
                                                    "prefix": "/tools",
                                                    "env": {"FORCE_UNSAFE_CONFIGURE": 1}})
