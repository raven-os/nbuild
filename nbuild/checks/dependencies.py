import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from nbuild.log import ilog, elog
import nbuild.stdenv.package
import nbuild.checks.check as check


def find_dirs_ending_in(end, path):
    dirs = []
    for (dirname, dirnames, filenames) in os.walk(path):
        dirs += [os.path.join(dirname, subdirname) for subdirname in dirnames
                 if subdirname.endswith(end)]
    return dirs


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
            elog(f"Possible missing dependency to '{dep}' in {file_wo_prefix}")
    return True


def check_files(files, pkg):
    return all(map(lambda x: check_file(x, pkg), files))


def check_bins(pkg):
    dirs = find_dirs_ending_in('bin', pkg.install_dir)
    for dirpath in map(lambda x: os.path.join(pkg.install_dir, x), dirs):
        binpaths = map(lambda x: os.path.join(dirpath, x), os.listdir(dirpath))
        check_files(binpaths, pkg)


def check_libs(pkg):
    dirs = find_dirs_ending_in('lib', pkg.install_dir)
    for dirpath in map(lambda x: os.path.join(pkg.install_dir, x), dirs):
        libpaths = map(lambda x: os.path.join(dirpath, x),
                       (f for f in os.listdir(dirpath) if '.so' in f))
        check_files(libpaths, pkg)


def check_deps(pkg):
    ilog("Checking dependencies")
    check_bins(pkg)
    check_libs(pkg)
