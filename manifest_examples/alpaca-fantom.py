import templates.git
import templates.common
import templates.make
import templates.autotools


class BuildManifest:
    def __init__(self):
        self.name = "alpaca-fantom"
        self.version = "0.1.0"

    def fetch(self):
        self.filename = templates.git.fetch("https://github.com/melis-m/alpaca-fantom",
                                            branch="dev")
