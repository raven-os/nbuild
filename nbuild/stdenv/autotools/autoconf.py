#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from nbuild.cmd import cmd
from nbuild.stdenv.build import current_build


def do_configure(
    binary='../configure',
    prefix=None,
    sysconfdir='/etc',
    localstatedir='/var',
    extra_configure_flags=[],
):
    package = current_build().current_package
    if prefix is None:
        prefix = package.install_dir + '/usr'
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
