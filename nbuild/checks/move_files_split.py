import os
import shutil
import re
import glob
from nbuild.stdenv.package import Package
from nbuild.log import elog, clog, ilog


def move_files_split(package: Package, suffix: str):
    if suffix != 'whole':
        pkg_name = f"{package.name.split('-')[0]}"
        move_folder_content(package, 'usr/bin', f'{pkg_name}-whole')
        if suffix != 'dev':
            move_folder_content(package, 'usr/include/', f'{pkg_name}-dev')
        if suffix != 'doc':
            move_folder_content(package, 'usr/share/doc/', f'{pkg_name}-doc')
        if suffix != 'lib':
            folder_regex = r'usr/lib*'
            path = f'{package.install_dir}/{folder_regex}'
            results = glob.glob(path)
            if len(results) > 0:
                for path in results:
                    folder = path.split('/')[-1]
                    move_folder_content(package, f'usr/{folder}', f'{pkg_name}-lib', path)

def move_folder_content(package: Package, folder: str, new_split: str, path = ''):
    if len(path) == 0:
        path = f'{package.install_dir}/{folder}'
    if os.path.isdir(path):
        new_path = re.sub(package.name, new_split, package.install_dir)
        if os.path.exists(new_path):
            files = os.listdir(path)
            new_path += f'/{folder}'
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
            for file in files:
                shutil.move(f'{path}/{file}', new_path)
            os.rmdir(path)
            ilog(f"Moved the content of the folder {folder} from its old split '{package.name}' "
            f"to '{new_split}'")
        else:
            elog(f"Unable to move {path} to its expected split {new_split}, as it's not installed.")
