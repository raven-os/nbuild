import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from nbuild.log import ilog, elog, clog
import nbuild.stdenv.package
import nbuild.checks.check as check


def get_deps(filename):
    with open(filename, 'rb') as f:
        ret = elf_get_deps(f)
        if ret is None:
            return None
            # f.seek(0, 0)
            # ret = get_interpreter(f)
        return ret


def elf_get_deps(filehandle):
    try:
        elf = ELFFile(filehandle)
        section = next(x for x in elf.iter_sections()
                       if x.name.startswith('.dynamic'))
    except (StopIteration, ELFError):
        return None
    needed_tags = [tag.needed for tag in section.iter_tags()
                   if tag.entry['d_tag'] == 'DT_NEEDED']
    return needed_tags


def get_interpreter(filehandle):
    shebang = filehandle.readline()
    # if shebang.startswith('#!'):
    return shebang


def check_file(file, pkg):
    file_wo_prefix = file[len(pkg.install_dir):]
    found_deps = filter(lambda x: pkg.name not in x, get_deps(file))
    for dep in found_deps:
        found = False
        for key in pkg.run_dependencies.keys():
            _, _, name = nbuild.stdenv.package.Package.split_id(key)
            if name in dep:
                found = True
                break
        if not found:
            elog(f"Possible missing dependency to '{dep}' in '{file_wo_prefix}'")
    return True


def check_files(files, pkg):
    return all(map(lambda x: check_file(x, pkg), files))


def check_bins(pkg):
    dirs = check.find_dirs_ending_in('bin', pkg.install_dir)
    for dirpath in dirs:
        path_wo_prefix = dirpath[len(pkg.install_dir):]
        ilog(f"Checking dependencies for files in '{path_wo_prefix}'")
        binpaths = map(lambda x: os.path.join(dirpath, x), os.listdir(dirpath))
        if not check_files(binpaths, pkg):
            return False
    return True


def check_libs(pkg):
    dirs = check.find_dirs_ending_in('lib', pkg.install_dir)
    for dirpath in dirs:
        path_wo_prefix = dirpath[len(pkg.install_dir):]
        ilog(f"Checking dependencies for shared libraries in '{path_wo_prefix}'")
        libpaths = map(lambda x: os.path.join(dirpath, x),
                       (f for f in os.listdir(dirpath) if '.so' in f))
        if not check_files(libpaths, pkg):
            return False
    return True


def check_deps(pkg):
    ilog("Checking dependencies")
    ret = all([
        check_bins(pkg),
        check_libs(pkg),
    ])
    if ret:
        clog("\tDependency checks OK")
    else:
        elog("\tSome dependency checks failed")
    return ret
