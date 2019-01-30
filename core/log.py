#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Functions to write and manipulate logs.
"""

import enum
import termcolor
from contextlib import contextmanager

log_tab_level = 0


@contextmanager
def pushlog():
    """
    Increases the log indentation level by one, making all new lines indented by one more tabulation.
    """
    global log_tab_level
    log_tab_level += 1

    try:
        yield
    finally:
        log_tab_level -= 1


def dlog(*args, indent=True):
    """
    Prints a debug log, prefixed by a magenta `[d]`.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[d]', 'magenta', attrs=['bold'])} {indent}", *args)
    # print(f"{termcolor.colored("[d]", "magenta", end=' ')}{"\t" * tab_log_level}", *args)


def ilog(*args, indent=True):
    """
    Prints an informative log, prefixed by a blue `[*]`.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[*]', 'blue', attrs=['bold'])} {indent}", *args)


def slog(*args, indent=True):
    """
    Prints a success log, prefixed by a green `[+]`.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[+]', 'green', attrs=['bold'])} {indent}", *args)


def wlog(*args, indent=True):
    """
    Prints a warning log, prefixed by a yellow `[!]`.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[!]', 'yellow', attrs=['bold'])} {indent}", *args)


def elog(*args, indent=True):
    """
    Prints a non-fatal error log, prefixed by a red `[-]`.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[-]', 'red', attrs=['bold'])} {indent}", *args)


def flog(args):
    """
    Prints a fatal error log, all in red, prefixed by `[-]`.
    This function does NOT abort the current process's execution.
    """
    termcolor.cprint(f"[-] {args}", 'red', attrs=['bold'])
