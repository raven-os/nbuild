import templates.common
import templates.make
import templates.autotools


class BuildManifest(templates.common.Common):
    def __init__(self):
        templates.common.Common.__init__(self, "sed", "4.4",
                                         fetch={"url": "http://ftp.gnu.org/gnu/sed/sed-4.4.tar.xz",
                                                "md5sum": "e0c583d4c380059abd818cd540fe6938"},
                                         compile={"jobs": 4},
                                         check={"jobs": 4})
