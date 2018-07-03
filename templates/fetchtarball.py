#!/usr/bin/env python3

import os
import requests
import hashlib
import tarfile
from nbuild.log import *
from nbuild.cmd import exec


class FetchTarballTemplate:
    def __init__(self, url, md5sum=None):
        self.url = url
        self.md5sum = md5sum
        self.tarball_path = self.url.split('/')[-1]
        if md5sum is None:
            wlog("No md5sum specified for FetchTarball template")

    def fetch(self):
        if self._check_md5():
            clog("Using cache \"{}\"".format(self.tarball_path))
        else:
            ilog("Downloading \"{}\"".format(self.url))

            req = requests.get(self.url, stream=True)
            with open(self.tarball_path, 'wb') as f:
                for chunk in req.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)

            clog(
                "Download complete. "
                "File saved at \"{}\""
                .format(self.tarball_path)
            )

            if not self._check_md5():
                flog(
                    "The downloaded file's md5 does "
                    "not match the template's one ({})"
                    .format(md5sum)
                )
                exit(1)

    def unpack(self):
        dir_path = os.path.basename(self.tarball_path).split('.tar')[0]
        if not os.path.exists(dir_path):
            with tarfile.open(self.tarball_path) as tar:
                tar.extractall()
            clog(
                "Unpacked \"{}\" in \"{}\""
                .format(self.tarball_path, dir_path)
            )
        else:
            clog("Tarball already unpacked in \"{}\"".format(dir_path))
        os.chdir(dir_path)

    def _check_md5(self):
        if self.md5sum is None or not os.path.exists(self.tarball_path):
            return False

        hash_md5 = hashlib.md5()
        with open(self.tarball_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest() == self.md5sum
