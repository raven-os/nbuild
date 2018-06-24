import os


def fmt_args(cmd, *args, **kwargs):
    cmd += args

    for key, value in kwargs.items():
        li = []
        if len(key) > 1:
            var = ""
            if not key.isupper():
                var = "--"
            var += "{}".format(key)
            if value is not None:
                var += "={}".format(value)
        else:
            var = "-{}".format(key)
            if value is not None:
                var += "={}".format(value)
        li.append(var)
        cmd += li
    return cmd


def fmt_env(new_env):
    env = os.environ
    for key, value in new_env.items():
        env[key] = value
    return env

