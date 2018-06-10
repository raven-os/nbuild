import subprocess

from . import helpers


def fetch(url, **kwargs):
    # subprocess.run(["rm", "-rf", url.split("/")[-1]])
    cmd = ["git", "clone", url]
    cmd += helpers.fmt_args(**kwargs)
    subprocess.run(cmd)
