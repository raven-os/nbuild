#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provides functions to apply patches to a code base."""

import os
import stdlib
import glob


def patch(
    path: str,
):
    """Apply the patch pointed to by ``path`` on the code base.

    :note: The patch must be a compatible input for the GNU ``patch`` utility.
    :note: Patch that appeared to already be applied are ignored

    :param path: The path pointing to the patch file. It must be relative to the current directory.
    """
    stdlib.cmd(f'patch -Np1 -i {path}')
    stdlib.log.slog(f"Applied patch {os.path.basename(path)}")


def patch_all():
    """Apply all patches of the current directory on the code base.

    :note: All patches must be a compatible input for the GNU ``patch`` utility.
    :note: The patches must be ``.patch`` files to be automatically picked up by this function.
    """

    for patch_path in glob.glob('*.patch'):
        patch(patch_path)
