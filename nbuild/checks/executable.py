import os
import sys
from nbuild.log import wlog, elog, ilog


def is_file_x(filename, x_expected=True):
    ret = os.access(filename, os.X_OK)
    if x_expected and not ret:
        elog(f"'{filename}' is not executable, but should be")
    elif not x_expected and ret:
        wlog(f"'{filename}' is executable, but should not be")
    return ret


def is_all_folder_x(dirpath):
    if os.path.exists(dirpath):
        ilog(f"Checking if all files in folder '{dirpath}' are executable")
        files = os.listdir(dirpath)
        files_path = map(lambda x: os.path.join(dirpath, x), files)
        return are_files_x(*list(files_path))
    return True


def are_folders_x(*dirpaths):
    return all(map(is_all_folder_x, dirpaths))


def check_bins_x():
    bin_path = os.path.join('/bin')
    sbin_path = os.path.join('/sbin')
    usrbin_path = os.path.join('/usr', 'bin')

    return are_folders_x(bin_path, sbin_path, usrbin_path)


def are_files_x(*files):
    return all(map(is_file_x, files))


def are_shared_libs_x(dirpath):
    if os.path.exists(dirpath):
        ilog(f"Checking if all shared libraries in folder '{dirpath}' are executable")
        files = [x for x in os.listdir(dirpath) if '.so' in x]
        files_path = map(lambda x: os.path.join(dirpath, x), files)
        return all(map(is_file_x, files_path))
    return True


def check_libs_x():
    lib_path = os.path.join('/lib')
    usrlib_path = os.path.join('/usr', 'lib')

    return all(map(are_shared_libs_x, [lib_path, usrlib_path]))


def check_exec(pkg):
    ret = all(
        [
            check_bins_x(),
            check_libs_x(),
        ]
    )
    if ret:
        ilog("Executable checks OK")
    return ret
