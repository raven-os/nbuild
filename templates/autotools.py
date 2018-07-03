#!/usr/bin/env python3

import os
import tarfile
from nbuild.cmd import exec
from templates.autoconf import AutoconfTemplate
from templates.make import MakeTemplate


class AutotoolsTemplate(AutoconfTemplate, MakeTemplate):
    def check(self):
        exec(["make", "check"])

    def wrap(self):
        install_dir = './pkg-install/'
        data_path = os.path.join(self.pkg_dir, 'data.tar.gz')

        old_path = os.getcwd()
        if not os.path.exists(install_dir):
            os.mkdir(install_dir)

        exec(
            ["make", "install"],
            env={
                'DESTDIR': install_dir,
            }
        )

        os.chdir(install_dir)
        with tarfile.open(data_path, mode='w:gz') as archive:
            archive.add('./')

        os.chdir(old_path)
