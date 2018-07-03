#!/usr/bin/env python3

import os
import subprocess
from nbuild.args import *
from nbuild.log import *


def exec(args, env=None):
    new_env = os.environ.copy()
    if env is not None:
        new_env.update(env)

    out = subprocess.DEVNULL
    err = subprocess.DEVNULL

    if get_args().verbose >= 1:
        dlog("Executing \"{}\"".format(' '.join(args)))

    if get_args().verbose >= 2:
        code = subprocess.run(args, env=new_env).returncode
    else:
        code = subprocess.run(
            args,
            env=new_env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode

    if code != 0:
        flog("Command \"{}\" failed with error code {}".format(args[0], code))
        print("Command:\n\t", ' '.join(args))
        print("Environment:")
        for (key, value) in new_env.items():
            print("\t{}={}".format(key, value))
        exit(1)
