import subprocess

from . import helpers


def compile(**kwargs):
    cmd = ["make"]
    cmd += helpers.fmt_args(**kwargs)
    subprocess.run(cmd)


def check(**kwargs):
    cmd = ["make", "check"]
    cmd += helpers.fmt_args(**kwargs)
    subprocess.run(cmd)
