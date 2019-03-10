#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provide a function to execute shell commands."""

import os
import core
import stdlib
import subprocess


def cmd(
    cmd: str,
    fail_ok: bool = False,
):
    """Execute a shell command.

    If the command fails and unless ``fail_ok`` is ``True``, the execution of the build manifest is aborted.

    :note: :py:func:`.cmd` doesn't return until the shell command finishes.

    :param cmd: The shell command to execute.
    :param fail_ok: Indicate whether or not to abort if the command returns a value different than 0.
    """

    if core.args.get_args().verbose >= 1:
        stdlib.log.dlog(cmd)

    if core.args.get_args().verbose < 2:
        code = subprocess.run(
            ['bash', '-e', '-c', cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
    else:
        code = subprocess.run(['bash', '-e', '-c', cmd]).returncode

    if code != 0 and not fail_ok:
        stdlib.log.flog(f"Command failed with error code {code}:")
        stdlib.log.dlog(f"Command: \"{cmd}\"")
        stdlib.log.dlog(f"Working directory: {os.getcwd()}")
        stdlib.log.dlog(f"Environment:")
        with stdlib.log.pushlog():
            for (key, value) in os.environ.items():
                stdlib.log.dlog(f'{key}={value}')

        exit(1)
