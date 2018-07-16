#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from termcolor import cprint


def dlog(*args, indent=True):
    cprint("[d]", "magenta", attrs=['bold'], end=' ')
    if indent:
        print("\t", end='')
    print(*args)


def ilog(*args, indent=True):
    cprint("[*]", "blue", attrs=['bold'], end=' ')
    if indent:
        print("\t", end='')
    print(*args)


def clog(*args, indent=True):
    cprint("[+]", "green", attrs=['bold'], end=' ')
    if indent:
        print("\t", end='')
    print(*args)


def wlog(*args, indent=True):
    cprint("[!]", "yellow", attrs=['bold'], end=' ')
    if indent:
        print("\t", end='')
    print(*args)


def elog(*args, indent=True):
    cprint("[-]", "red", attrs=['bold'], end=' ')
    if indent:
        print("\t", end='')
    print(*args)


def flog(args):
    cprint(f"[-] {args}", "red", attrs=['bold'])
