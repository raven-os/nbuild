import json
import os


class BaseManifest:
    def __init__(self):
        self.to_save = {}

    def on_abort(self):
        with open(os.path.join(self.to_save["base_path"], ".data"), "w+") as f:
            self.to_save["cwd"] = os.getcwd()
            json.dump(self.to_save, f)
            print("saved {}".format(self.to_save))

    def on_resume(self):
        with open(os.path.join(self.to_save["base_path"], ".data"), "r") as f:
            self.to_save = json.load(f)
            os.chdir(self.to_save["cwd"])
            print("retrieveD {}".format(self.to_save))
