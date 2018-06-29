import templates.git
import templates.common


class BuildManifest(templates.BaseManifest.BaseManifest):
    def __init__(self):
        templates.BaseManifest.BaseManifest.__init__(self)
        self.name = "alpaca-fantom"
        self.version = "0.1.0"

    def fetch(self):
        self.filename = templates.git.fetch("https://github.com/melis-m/alpaca-fantom",
                                            branch="dev")
