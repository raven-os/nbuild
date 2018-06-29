import requests
import hashlib
import tarfile
import os
import subprocess

import templates.autotools
import templates.BaseManifest


def _download_file(url, local_filename):
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def _md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def fetch(url, md5sum=None):
    local_filename = url.split('/')[-1]
    if md5sum is not None \
            and os.path.exists(local_filename) \
            and _md5(local_filename) == md5sum:
                print("Using already present file '{}'".format(local_filename))
                return local_filename
    _download_file(url, local_filename)
    if md5sum is not None and _md5(local_filename) != md5sum:
        raise ValueError
    return local_filename


def unpack(filename):
    with tarfile.open(filename) as tar:
        tar.extractall()


def patch(url, md5sum=None):
    local_filename = url.split('/')[-1]
    if md5sum is not None \
            and os.path.exists(local_filename) \
            and _md5(local_filename) == md5sum:
                print("Using already present file '{}'".format(local_filename))
                return local_filename
    _download_file(url, local_filename)
    if md5sum is not None and _md5(local_filename) != md5sum:
        raise ValueError
    return subprocess.run(["patch", "-Np1", "-i", local_filename]).returncode


def wrap(install_dir):
    if not os.path.exists(install_dir):
        os.mkdir(install_dir)
    subprocess.run(["make", "install"])
    # files = [os.path.join(dirpath, f)
    #          for dirpath, _, filenames in os.walk(install_dir)
    #          for f in filenames]
    os.system("ls")
    print(os.getcwd())
    os.chdir(install_dir)
    with tarfile.open("data.tar.gz", mode="w:gz") as archive:
        archive.add("./")
    os.chdir("..")


class Common(templates.BaseManifest.BaseManifest):
    def __init__(self, name, version, *args, **kwargs):
        templates.BaseManifest.BaseManifest.__init__(self)
        self.name = name
        self.version = version
        self.kwargs = kwargs
        self.install_dir = "./tmp"

    def fetch(self):
        if "fetch" in self.kwargs:
            self.to_save["filename"] = fetch(**self.kwargs["fetch"])
            return 0

    def unpack(self):
        unpack(self.to_save["filename"])
        os.chdir("{}-{}".format(self.name, self.version))
        return 0

    def patch(self):
        if "patch" in self.kwargs:
            return patch(**self.kwargs["patch"])

    def configure(self):
        if "configure" in self.kwargs:
            return templates.autotools.configure(**self.kwargs["configure"])

    def compile(self):
        return templates.make.compile(**self.kwargs["compile"]
                                      if "compile" in self.kwargs
                                      else {})

    def check(self):
        return templates.make.check(**self.kwargs["compile"]
                                    if "compile" in self.kwargs
                                    else {})

    def wrap(self):
        wrap(self.install_dir)
