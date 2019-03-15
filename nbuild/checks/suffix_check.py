#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import re
import glob
from nbuild.stdenv.package import Package
from nbuild.log import elog, clog, ilog


def man_checker(package: Package, man_section):
    path = f'{package.install_dir}/usr/share/man/man'
    ret = True
    if not os.path.isdir(f'{path}{str(man_section)}'):
        elog(f"The manuals {man_section} are missing for the package "
             f"{package.id}.")
        return False
    for i in range(0, 8):
        if i != man_section and os.path.isdir(f'{path}{i}'):
            elog(f"The manuals {str(i)} should not be installed for the package "
                 f"{package.id}")
            ret = False
    return ret


def man_installed(package: Package, man_section=-1):
    path = f'{package.install_dir}/usr/share/man'
    if man_section == -1 and os.path.isdir(path):
        elog(f"The manuals should not be installed for the package "
             f"{package.id}.")
        return False
    elif os.path.isdir(path):
        for i in range(0, 8):
            if i == man_section and os.path.isdir(f'{path}/man{i}'):
                elog(f"The manuals {str(i)} should not be installed for the package "
                     f"{package.id}.")
                return False
    return True


def lib_installed(package: Package):
    path = package.install_dir + r'/usr/lib*'
    results = glob.glob(path)
    if len(results) > 0:
        elog(f"The libraries should not be installed for the package "
             f"{package.id}.")
        return False
    return True


def lib_checker(package: Package, lib_extension=''):
    path = package.install_dir + r'/usr/lib*'
    results = glob.glob(path)
    if len(results) == 0:
        elog(f"No library found for the package {package.id}.")
        return False

    suffix = package.name.split('-')[-1]
    for root, dirs, files in os.walk(results[0]):
        for file in files:
            if suffix == '-lib' or suffix == package.name:
                if not file.endswith(lib_extension) and not re.search(r'.*\.la$', file):
                    elog(f"The libraries are not correctly installed for "
                         f"the package {package.id}.")
                    return False
            elif suffix == '-dev':
                if not re.search(r'.*\.[la|pc]$', file):
                    elog(f"The libraries are not correctly installed for "
                         f"the package {package.id}.")
                    return False
    return True


def header_installed(package: Package):
    path = f'{package.install_dir}/usr/include'
    if os.path.isdir(path):
        elog(f"The headers should not be installed for the package "
             f"{package.id}.")
        return False
    return True


def bin_installed(package: Package):
    path = f'{package.install_dir}/usr/bin'
    if os.path.isdir(path):
        elog(f"The binaries should not be installed for the package "
             f"{package.id}.")
        return False
    return True


def doc_installed(package: Package):
    path = f'{package.install_dir}/usr/share/doc'
    if os.path.isdir(path):
        elog(f"The documentation should not be installed for the package "
             f"{package.id}.")
        return False
    return True


def dev_check(package: Package):
    return all(
        [
            man_checker(package, 3),
            bin_installed(package),
            doc_installed(package),
            lib_installed(package),
        ]
    )


def doc_check(package: Package):
    return all(
        [
            man_installed(package),
            bin_installed(package),
            lib_installed(package),
            header_installed(package)
        ]
    )


def bin_check(package: Package):
    pass


def lib_check(package: Package):
    return all(
        [
            man_installed(package),
            bin_installed(package),
            lib_checker(package, '.a'),
            doc_installed(package),
            header_installed(package)
        ]
    )


def classic_check(package: Package):
    return all(
        [
            man_installed(package, 3),
            lib_checker(package, '.so'),
            doc_installed(package),
            header_installed(package)
        ]
    )


def suffix_checks(package: Package):
    ilog("Looking for files that should not be there")
    suffix = package.name.split('-')[-1]
    if suffix == 'dev':
        ret = dev_check(package)
    elif suffix == 'doc':
        ret = doc_check(package)
    elif suffix == 'bin':
        ret = bin_check(package)
    elif suffix == 'lib':
        ret = lib_check(package)
    else:
        ret = classic_check(package)
    if ret:
        clog("\tEverything seems OK")
    else:
        elog("\tSome files should not be there")
