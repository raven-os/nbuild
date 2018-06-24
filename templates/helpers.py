def fmt_args(cmd, *args, **kwargs):
    cmd += args

    for key, value in kwargs.items():
        li = []
        if len(key) > 1:
            var = "--{}".format(key)
            if value is not None:
                var += "={}".format(value)
        else:
            var = "-{}".format(key)
            if value is not None:
                var += "={}".format(value)
        li.append(var)
        cmd += li
    return cmd
