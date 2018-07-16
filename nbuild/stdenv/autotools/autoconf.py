#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from nbuild.cmd import cmd


def do_configure(
    binary='../configure',
    prefix='/usr',
    sysconfdir='/etc',
    localstatedir='/var',
    extra_configure_flags=[],
):
    cmd(f'''
        {binary} \
            --build={os.environ['TARGET']} \
            --host={os.environ['HOST']} \
            --prefix={prefix} \
            --sysconfdir={sysconfdir} \
            --localstatedir={localstatedir} \
            --disable-werror \
            --enable-stack-protector=all \
            --enable-stackguard-randomization \
            --with-pkgversion='Raven-OS' \
            --with-bugurl='https://bugs.raven-os.org' \
            {' '.join(extra_configure_flags)}
        ''')
