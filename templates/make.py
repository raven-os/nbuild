import subprocess

from . import helpers


def compile(*args, **kwargs):
    env = None
    if "env" in kwargs:
        kwargs.pop("env")
    cmd = helpers.fmt_args(["make"], *args, **kwargs)
    return subprocess.run(cmd, env=env).returncode


def check(*args, **kwargs):
    env = None
    if "env" in kwargs:
        kwargs.pop("env")
    cmd = helpers.fmt_args(["make", "check"], *args, **kwargs)
    return subprocess.run(cmd, env=env).returncode
