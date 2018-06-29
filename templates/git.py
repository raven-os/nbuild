import subprocess

from . import helpers


def fetch(url, **kwargs):
    env = None
    if "env" in kwargs:
        env = helpers.fmt_env(kwargs["env"])
        kwargs.pop("env")
    cmd = helpers.fmt_args(["git", "clone", url], **kwargs)
    return subprocess.run(cmd, env=env).returncode
