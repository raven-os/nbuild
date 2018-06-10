import templates.common
import templates.make
import templates.autotools
import os


class BuildManifest:
    def __init__(self):
        self.name = "Bison"
        self.version = "3.0.4"

    def fetch(self):
        self.filename = templates.common.fetch("http://ftp.gnu.org/gnu/bison/bison-3.0.4.tar.xz",
                                               md5sum="c342201de104cc9ce0a21e0ad10d4021")

    def unpack(self):
        templates.common.unpack(self.filename)
        os.chdir("bison-3.0.4")

    def configure(self):
        templates.autotools.configure(prefix="/tools")

    def compile(self):
        templates.make.compile(jobs=4)

    def check(self):
        templates.make.check(jobs=4)
