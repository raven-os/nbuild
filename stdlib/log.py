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
    """Increase the log indentation level by one, making every new line indented by one extra tabulation."""
    global log_tab_level
    log_tab_level += 1

    try:
        yield
    finally:
        log_tab_level -= 1


def dlog(*logs: str):
    """Print a debug log, prefixed by a magenta ``[d]``.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[d]', 'magenta', attrs=['bold'])} {indent}", *logs, flush=True)


def ilog(*logs: str):
    """Print an informative log, prefixed by a blue ``[*]``.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[*]', 'blue', attrs=['bold'])} {indent}", *logs, flush=True)


def slog(*logs: str):
    """Print a success log, prefixed by a green ``[+]``.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[+]', 'green', attrs=['bold'])} {indent}", *logs, flush=True)


def wlog(*logs: str):
    """Print a warning log, prefixed by a yellow ``[!]``.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[!]', 'yellow', attrs=['bold'])} {indent}", *logs, flush=True)


def elog(*logs: str):
    """Print a non-fatal error log, prefixed by a red ``[-]``.

    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[-]', 'red', attrs=['bold'])} {indent}", *logs, flush=True)


def flog(*logs: str):
    """Print a fatal error log, all in red, prefixed by ``[-]``.

    :info: This function does NOT abort the current process's execution.
    :param logs: The content of the log.
    """
    termcolor.cprint(f"[-]  {' '.join(logs)}", 'red', attrs=['bold'])
