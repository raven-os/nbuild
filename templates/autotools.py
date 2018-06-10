import subprocess

from . import helpers


def configure(*args, **kwargs):
    cmd = ["./configure"]
    cmd += helpers.fmt_args(**kwargs)
    subprocess.run(cmd)
