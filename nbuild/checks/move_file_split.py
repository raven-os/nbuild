import os
import shutil
import re
from nbuild.stdenv.package import Package
from nbuild.log import elog, clog, ilog


def move_file_split(package: Package, suffix: str):
    if suffix != 'whole':
        if suffix != 'dev':
            find_file_by_extension(package, '.h', 'dev')
        if suffix != 'doc':
            find_file_by_extension(package, '.html', 'doc')
        if suffix != 'lib':
            find_file_by_extension(package, '.so', 'lib')
            find_file_by_extension(package, '.la', 'lib')
            find_file_by_extension(package, '.a', 'lib')


def find_file_by_extension(package: Package, ext: str, split:str):
    for subdir, dirs, files in os.walk(package.install_dir):
        for file_name in files:
            if file_name.endswith(ext):
                repl = f"{package.name.split('-')[0]}-{split}"
                new_path = re.sub(package.name, repl, package.install_dir)
                if not os.path.exists(new_path):
                    elog(f"The split '-{split} hasn't been found for the package "
                         f"{package.name}.")
                    elog(f"Can't move the file {file_name} to its correct split.")
                else:
                    move_file(package, file_name, new_path, subdir, split)


def move_file(package: Package, file_name: str, new_path: str, old_path: str, split):
    shutil.move(f'{old_path}/{file_name}', new_path)
    old_split = package.name.split('-')[1]
    ilog(f"Moved {file_name} from its old split '-{old_split}' "
         f"to '-{split}'")
