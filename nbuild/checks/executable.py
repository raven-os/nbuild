import os
from nbuild.log import wlog, elog, ilog, clog
import nbuild.checks.check as check


def is_file_x(filename, pkg, x_expected=True):
    path_wo_prefix = filename[len(pkg.install_dir):]
    ret = os.access(filename, os.X_OK)
    if x_expected and not ret:
        elog(f"'{path_wo_prefix}' is not executable, but should be")
    elif not x_expected and ret:
        wlog(f"'{path_wo_prefix}' is executable, but should not be")
    return ret


def are_files_x(files, pkg):
    return all(map(lambda x: is_file_x(x, pkg), files))


def is_all_folder_x(dirpath, pkg):
    path_wo_prefix = dirpath[len(pkg.install_dir):]
    if os.path.exists(dirpath):
        ilog(f"Checking if all files in folder '{path_wo_prefix}' are executable")
        files = os.listdir(dirpath)
        files_path = map(lambda x: os.path.join(dirpath, x), files)
        return are_files_x(files_path, pkg)
    return True


def are_folders_x(pkg, dirpaths):
    return all(map(lambda x: is_all_folder_x(x, pkg), dirpaths))


def check_bins_x(pkg):
    bindirs = check.find_dirs_ending_in('bin', pkg.install_dir)
    return are_folders_x(pkg, bindirs)


def are_shared_libs_x(dirpath, pkg):
    path_wo_prefix = dirpath[len(pkg.install_dir):]
    if os.path.exists(dirpath):
        ilog(f"Checking if all shared libraries in folder '{path_wo_prefix}' are executable")
        files = [x for x in os.listdir(dirpath) if '.so' in x]
        files_path = map(lambda x: os.path.join(dirpath, x), files)
        return all(map(lambda x: is_file_x(x, pkg), files_path))
    return True


def check_libs_x(pkg):
    bindirs = check.find_dirs_ending_in('lib', pkg.install_dir)
    return all(map(lambda x: are_shared_libs_x(x, pkg), bindirs))


def check_exec(pkg):
    ret = all([
        check_bins_x(pkg),
        check_libs_x(pkg),
    ])
    if ret:
        clog("\tExecutable checks OK")
    else:
        elog("\tSome executable checks failed")
    return ret
