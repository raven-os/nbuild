import requests
import hashlib
import tarfile
import os

import templates.autotools


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


class Common:
    def __init__(self, name, version, *args, **kwargs):
        self.name = name
        self.version = version
        self.kwargs = kwargs

    def fetch(self):
        if "fetch" in self.kwargs:
            self.filename = fetch(**self.kwargs["fetch"])

    def unpack(self):
        unpack(self.filename)
        os.chdir("{}-{}".format(self.name.lower(), self.version))

    def configure(self):
        if "configure" in self.kwargs:
            templates.autotools.configure(**self.kwargs["configure"])

    def compile(self):
        templates.make.compile(**self.kwargs["compile"]
                               if "compile" in self.kwargs
                               else {})

    def check(self):
        templates.make.check(**self.kwargs["compile"]
                             if "compile" in self.kwargs
                             else {})
