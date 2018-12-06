#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import subprocess
from copy import deepcopy
from textwrap import dedent
from nbuild.args import nbuild_args
from nbuild.log import ilog, dlog, flog


def cmd(
    cmd,
    env={},
    fail_ok=False,
):
    """
    Executes the given command, after removing any prior whitespaces with
    `textwrap.dedent()`.

    This is nothing more than a wrapper to reduce boilerplate.
    """
    global nbuild_args

    cmd = dedent(cmd)
    new_env = deepcopy(os.environ)
    new_env.update(env)

    if nbuild_args.verbose >= 1:
        ilog(cmd)
        dlog(f"Working directory: {os.getcwd()}")

        if nbuild_args.verbose >= 2:
            for (key, value) in new_env.items():
                dlog(f'    {key}={value}')

    if nbuild_args.verbose >= 3:
        code = subprocess.run(
            ['bash', '-e', '-c', cmd],
            env=new_env
        ).returncode
    else:
        code = subprocess.run(
            ['bash', '-e', '-c', cmd],
            env=new_env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode

    if code != 0 and not fail_ok:
        flog(f"Command failed with error code {code}:")
        print(cmd)
        print(f"Working directory: {os.getcwd()}")
        for (key, value) in new_env.items():
            print(f"    {key}={value}")
        exit(1)
