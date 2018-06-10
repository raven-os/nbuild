import templates.common
import templates.make
import templates.autotools


class BuildManifest(templates.common.Common):
    def __init__(self):
        templates.common.Common.__init__(self, "Binutils", "2.30",
                                         fetch={"url": "http://ftp.gnu.org/gnu/binutils/binutils-2.30.tar.xz",
                                                "md5sum": "ffc476dd46c96f932875d1b2e27e929f"},
                                         configure={"prefix": "/tools"},
                                         compile={"jobs": 4},
                                         check={"jobs": 4})
        self.name = "Binutils"
        self.version = "2.30"
