import os
from nbuild.checks.dependencies import check_deps
from nbuild.checks.executable import check_exec
from nbuild.log import ilog
from nbuild.checks.syntax_check import check_syntax
from nbuild.checks.suffix_check import suffix_checks


def find_dirs_ending_in(end, path):
    dirs = []
    for (dirname, dirnames, filenames) in os.walk(path):
        dirs += [os.path.join(dirname, subdirname) for subdirname in dirnames
                 if subdirname.endswith(end)]
    return dirs


def check_package(pkg):
    suffix = pkg.name.split('-')[-1] if '-' in pkg.name else None
    ilog(f"Checking package installed at {pkg.install_dir}", indent=False)

    check_syntax(pkg)
    if suffix is None or suffix == 'bin':
        check_deps(pkg)
        check_exec(pkg)
    suffix_checks(pkg)
    ilog("All checks done")
