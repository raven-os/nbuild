#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import ntpath
import stdlib
import shutil
import hashlib
import requests
import ftplib
from urllib.parse import urlparse


def fetch():
    """Fetch the input data contained in the versionized argument ``fetch``.

    The versionized argument ``fetch`` must be an array of dictionaries. Each entry in the array is a data to fetch.
    The dictionary indicates how to retrieve the data and some optional parameters.

    If the dictionary contains the key:

        * ``url``: the function :py:func:`.fetch_url` is called with the remaining values as arguments.
        * ``file``: the function :py:func:`.fetch_file` is called with the remaining values as arguments.

    If the dictionary contains both the key ``url`` and ``file``, a ``RuntimeError`` is raised.

    *Example:* ::

        'fetch': [{
                'url': 'https://example.com/hello.tar.gz',
                'sha256': '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
            }, {
                'url': 'https://example.com/world.tar.gz',
            }, {
                'file': './hello_world'
            },
        ]

    With the above example, ``fetch`` will perform these calls, respectively: ::

        fetch_url(
            url='https://example.com/hello.tar.gz',
            sha256='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
        )

        fetch_url(url='https://example.com/world.tar.gz')

        fetch_file(file='./hello_world')

    """
    build = stdlib.build.current_build()

    inputs = build.args.get('fetch', [])

    for input in inputs:
        if ('url' in input) ^ ('file' in input):
            if 'url' in input:
                fetch_url(**input)
            elif 'file' in input:
                fetch_file(**input)
        else:
            raise RuntimeError("A single entry of data given to fetch() contains either no `url` or `file` key, or both of them.")


def fetch_file(file: str):
    """Copy a file or directory to the current build cache.

    :note: The path must be relative to the build manifest. If an absolute path is given, a ``RuntimeError`` is raised.

    :param file: The file or directory to copy.
    """
    if os.path.isabs(file):
        raise RuntimeError("fetch_file() received an absolute path as parameter, while it expects a relative one")

    build = stdlib.build.current_build()

    srcpath = os.path.join(
        os.path.dirname(build.manifest.path),
        file,
    )

    if os.path.isdir(srcpath):
        dstpath = os.path.join(
            build.build_cache,
            os.path.basename(file),
        )

        shutil.copytree(
            srcpath,
            dstpath,
        )
    else:
        shutil.copy(
            srcpath,
            build.build_cache,
        )


def fetch_url(url: str, sha256: str = None):
    """Download a file from an URL and ensure its integrity

    The downloaded file is put in the build cache of the current build, but a copy
    is also stored in the download cache. If :py:func:`.fetch_url` is called again
    with the same ``url`` argument, the already-downloaded file will be copied
    instead, avoiding any extra download.

    :note: Only HTTP, HTTPS and FTP protocols are supported.

    :param url: The URL pointing to the file to download.
    :param sha256: The SHA256 used to ensure the integrity of the file.
    """
    build = stdlib.build.current_build()

    url_object = urlparse(url)
    filename = os.path.basename(url_object.path)
    build_path = os.path.join(
        build.build_cache,
        filename,
    )
    install_path = os.path.join(
        build.download_cache,
        filename,
    )

    if not sha256:
        stdlib.log.wlog(f"No sha256 to ensure the integrity of {url}")

    if os.path.exists(install_path) and _check_sha256(install_path, sha256):
        stdlib.log.slog(f"Cache hit for {url}")
        shutil.copy2(
            install_path,
            build_path
        )
    else:
        stdlib.log.ilog(f"Cache miss for {url}, fetching now...")
        if url_object.scheme == 'http' or url_object.scheme == 'https':
            _download_http(url, install_path)
        elif url_object.scheme == ('ftp'):
            _download_ftp(url_object, install_path)
        else:
            stdlib.log.flog(f"Unknown protocol to download file from url {url}")
            exit(1)

        stdlib.log.slog(f"Fetch done.")

        if not _check_sha256(install_path, sha256):
            stdlib.log.flog(
                "Downloaded file's signature is invalid. "
                "Please verify the signature(s) in the build manifest "
                "and the authenticity of the given link."
            )
            exit(1)

        shutil.copy2(
            install_path,
            build_path,
        )


def _download_http(url, path):
        req = requests.get(url, stream=True)
        with open(path, 'wb') as file:
            for chunk in req.iter_content(chunk_size=4096):
                file.write(chunk)


def _download_ftp(url_object, path):
    ftp = ftplib.FTP(url_object.netloc)
    ftp.login()
    with open(path, 'wb') as out_file:
        ftp.retrbinary(
                f'RETR {url_object.path}',
                lambda data: out_file.write(data),
        )


def _check_sha256(path, sha256):
    hash_sha256 = hashlib.sha256()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest() == sha256
