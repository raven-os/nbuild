import subprocess

from . import helpers


def configure(*args, **kwargs):
    env = None
    if "env" in kwargs:
        env = helpers.fmt_env(kwargs["env"])
        kwargs.pop("env")
    cmd = helpers.fmt_args(["./configure"], *args, **kwargs)
    return subprocess.run(cmd, env=env).returncode
