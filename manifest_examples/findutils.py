import templates.common
import templates.make
import templates.autotools
import os


class BuildManifest:
    def __init__(self):
        self.name = "Findutils"
        self.version = "4.6.0"

    def fetch(self):
        self.filename = templates.common.fetch("http://ftp.gnu.org/gnu/findutils/findutils-4.6.0.tar.gz",
                                               md5sum="9936aa8009438ce185bea2694a997fc1")

    def unpack(self):
        templates.common.unpack(self.filename)
        os.chdir("findutils-4.6.0")

    def configure(self):
        templates.autotools.configure(prefix="/tools")

    def compile(self):
        templates.make.compile(jobs=4)

    def check(self):
        templates.make.check(jobs=4)
