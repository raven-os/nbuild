import templates.common
import templates.make
import templates.autotools
import os


class BuildManifest(templates.common.Common):
    def __init__(self):
        templates.common.Common.__init__(self, "Bison", "3.0.4",
                                         fetch={"url": "http://ftp.gnu.org/gnu/bison/bison-3.0.4.tar.xz",
                                                "md5sum": "c342201de104cc9ce0a21e0ad10d4021"},
                                         configure={"prefix": "/tools"},
                                         compile={"jobs": 4},
                                         check={"jobs": 4})
        self.name = "Bison"
        self.version = "3.0.4"
