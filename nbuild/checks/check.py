from nbuild.checks.dependencies import check_deps
from nbuild.log import ilog


def check_package(pkg):
    suffix = pkg.name.split('-')[-1] if '-' in pkg.name else None
    ilog(f"Checking package installed at {pkg.install_dir}", indent=False)
    if suffix is None or suffix == 'bin':
        check_deps(pkg)
    ilog("All checks done")
