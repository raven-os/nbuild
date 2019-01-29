from nbuild.checks.executable import check_exec
from nbuild.log import ilog


def check_package(pkg):
    suffix = pkg.name.split('-')[-1] if '-' in pkg.name else None
    ilog(f"Checking package installed at {pkg.install_dir}", indent=False)
    if suffix is None or suffix == 'bin':
        check_exec(pkg)
    ilog("All checks done")
