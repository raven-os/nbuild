def fmt_args(*args, **kwargs):
    return list(args) \
            + ["--{}{}".format(key,
                               "={}".format(value)
                               if value is not None
                               else "")
               if len(key) > 1
               else "-{}{}".format(key,
                                   " {}".format(value)
                                   if value is not None
                                   else "")
               for key, value in kwargs.items()]
