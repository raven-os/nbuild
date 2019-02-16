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
    """Increases the log indentation level by one, making every new line indented by one extra tabulation."""
    global log_tab_level
    log_tab_level += 1

    try:
        yield
    finally:
        log_tab_level -= 1


def dlog(*logs):
    """Prints a debug log, prefixed by a magenta `[d]`.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[d]', 'magenta', attrs=['bold'])} {indent}", *logs)


def ilog(*logs):
    """Prints an informative log, prefixed by a blue `[*]`.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[*]', 'blue', attrs=['bold'])} {indent}", *logs)


def slog(*args):
    """Prints a success log, prefixed by a green `[+]`.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[+]', 'green', attrs=['bold'])} {indent}", *args)


def wlog(*logs):
    """Prints a warning log, prefixed by a yellow `[!]`.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[!]', 'yellow', attrs=['bold'])} {indent}", *logs)


def elog(*logs):
    """Prints a non-fatal error log, prefixed by a red `[-]`.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[-]', 'red', attrs=['bold'])} {indent}", *logs)


def flog(logs):
    """Prints a fatal error log, all in red, prefixed by `[-]`.

    :info: This function does NOT abort the current process's execution.
    :param logs: The content of the log.
    """
    termcolor.cprint(f"[-] {logs}", 'red', attrs=['bold'])
