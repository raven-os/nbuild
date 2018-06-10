import templates.common
import templates.make
import templates.autotools
import os


class BuildManifest:
    def __init__(self):
        self.name = "libpipeline"
        self.version = "1.5.0"

    def fetch(self):
        self.filename = templates.common.fetch("http://download.savannah.gnu.org/releases/libpipeline/libpipeline-1.5.0.tar.gz",
                                               md5sum="b7437a5020190cfa84f09c412db38902")

    def unpack(self):
        templates.common.unpack(self.filename)
        os.chdir("libpipeline-1.5.0")

    def configure(self):
        templates.autotools.configure()

    def compile(self):
        templates.make.compile(jobs=4)

    def check(self):
        templates.make.check(jobs=4)
