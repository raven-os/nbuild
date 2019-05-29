#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""A primary dependency linker that assign requirements based on ELF dependencies."""

import requests
import ntpath
import glob
import braceexpand
import urllib.parse
import core.config
import stdlib
import stdlib.log
from typing import Optional
from elftools.elf.elffile import ELFFile


def elf_deplinker(
    packages,
    search_patterns=[
        '{,usr/}bin/*',
        '{,usr/}lib{,32,64}/*',
    ],
    local_resolving: bool = True,
    remote_resolving: bool = True,
):
    """A primordial dependency linker that assign requirements based on ELF dependencies.

    This dependency linker will expand all ``search_patterns`` and try to analyse all files as ELF.

    For each ELF, this dependency linker will retrieve all the ELF dependencies. It will then see if any of those dependencies
    are either provided by another package of the same build; or try to fetch the list of repositories
    written in the :py:mod:`~core.config` file (in the order indicated) to find the unique package that contains
    any of those files; and add it as a requirement.

    :param packages: The packages which should have their dependencies assigned
    :paramtype packages: ``List`` [ :py:class:`.Package` ]

    :param search_patterns: A list of patterns which should match any ELF file present in the package's content.
        Any element of this list supports the globbing and braces syntax of common shells.

        The default value is: ::

            [
                '{,usr/}}bin/*',
                '{,usr/}}lib{,32,64}/*',
            ]

        Which expands to: ::

            [
                'bin/*'
                'usr/bin/*'
                'lib/*'
                'usr/lib/*'
                'lib32/*'
                'usr/lib32/*'
                'lib64/*'
                'usr/lib64/*'
            ]

    :paramtype search_patterns: ``List`` [ :py:class:`.Package` ]
    :param local_resolving: Indicate whether or not other packages for ``packages`` should be used to solve dependencies. Default value is ``True``.
    :param remote_resolving: Indicate whether or not remote repositories should be used to solve dependencies. Default value is ``True``.
    """
    binaries = dict()  # Key = a binary filename, Value = a package ID
    dependencies = dict()  # Key = a package ID, Value = a list of ELF filenames

    for package in packages.values():
        stdlib.log.ilog(f"ELF Dependency Linker: Looking for binaries and their dependencies in {package.id.full_name()}...")

        pkg_id = package.id

        # Find all elfs in this package
        elfs = _find_elfs(package, search_patterns)

        # Fill the `binaries` dict, to keep track of who owns a binary in the local context
        #
        # This generates unspecified behaviour if two packages have two binaries with the same filename, so
        # we're actively checking against it.
        for elf in map(ntpath.basename, elfs):

            if elf in binaries:
                stdlib.log.flog(f"Two packages have the same file \"{elf}\": {binaries[elf]} and {pkg_id} -- Aborting")
                exit(1)

            binaries[elf] = pkg_id

        # Find the dependencies of every binaries
        dependencies[pkg_id] = list()
        for elf in elfs:
            elf_dependencies = _fetch_elf_dependencies(package, elf)
            dependencies[pkg_id] += elf_dependencies

            # Log results
            with stdlib.log.pushlog():
                stdlib.log.ilog(f"/{elf}: {' '.join(elf_dependencies)}")

        # Remove duplicate
        dependencies[pkg_id] = list(dict.fromkeys(dependencies[pkg_id]))

    # So from now on, we have all the dependencies in `dependencies`, and all
    # the binaries in `binaries`.
    #
    # We want to try and match the dependencies with the existing binaries,
    # and if it's not possible, with the remote repositories.

    for (package_id, dependencies) in dependencies.items():

        stdlib.log.ilog(f"ELF Dependency Linker: Solving dependencies of {package_id.full_name()}...")
        requirements = {}

        with stdlib.log.pushlog():

            for dependency in dependencies:
                stdlib.log.ilog(f"Looking for a package containing \"{dependency}\"...")

                if local_resolving and dependency in binaries.keys():
                    dependency_id = binaries[dependency]

                    requirements.update({dependency_id.full_name(): f'={dependency_id.version}'})
                    stdlib.log.slog(f"Found locally: {dependency_id.full_name()}#={dependency_id.version}")
                    continue
                elif remote_resolving:
                    with stdlib.log.pushlog():
                        solver_fullname = _solve_remotely(dependency)

                    if solver_fullname is not None:
                        requirements.update({solver_fullname: '*'})
                        stdlib.log.slog(f"Found remotely: {solver_fullname}#*")
                        continue

                stdlib.log.elog(f"Requirement couldn't be solved -- Manual dependency linking required!")

        packages[package_id.short_name()].run_dependencies.update(requirements)


def _solve_remotely(dependency) -> Optional[str]:
    config = core.config.get_config()

    if config.get('repositories') is None:
        return None

    # Try all repositories from top to bottom
    for repository in config['repositories']:
        try:
            url = core.config.get_config()['repositories'][repository]['url']
            r = requests.get(
                url=f'{url}/api/search?q={urllib.parse.quote(dependency)}&search_by=content&exact_match=true',
            )

            if r.status_code == 200:
                results = r.json()

                if len(results) == 1:
                    result = results[0]
                    if not result['all_versions']:
                        stdlib.log.elog(f"\"{repository}\" contains a single package with file \"{dependency}\" but not for all versions")
                    else:
                        stdlib.log.slog(f"\"{repository}\" contains a single package with file \"{dependency}\"!")
                        return result['name']
                elif len(results) > 1:
                    stdlib.log.elog(f"\"{repository}\" contains more than one package with file \"{dependency}\"")
                else:
                    stdlib.log.elog(f"\"{repository}\" doesn't contain any package with file \"{dependency}\"")
            elif r.status_code == 404:
                stdlib.log.elog(f"\"{repository}\" doesn't contain a package with file \"{dependency}\"")
            else:
                raise RuntimeError("Repository returned an unknown status code")
        except:
            stdlib.log.elog(f"An unknown error occurred when fetching \"{repository}\" (is the link dead?), skipping...")

    return None


def _fetch_elf_dependencies(package, elf_path) -> [str]:
    deps = []

    with stdlib.pushd(package.wrap_cache):
        try:
            with open(elf_path, 'rb') as file:
                elf = ELFFile(file)
                dyn = elf.get_section_by_name(".dynamic")
                if dyn is not None:
                    for tag in dyn.iter_tags():
                        if tag.entry.d_tag == 'DT_NEEDED':
                            deps += [tag.needed]
        except:
            pass  # Ignore invalid ELFs (dangling/text files in bin/ or lib/)

    return deps


def _find_elfs(package, search_patterns) -> [str]:
    files = []

    with stdlib.pushd(package.wrap_cache):
        for search_pattern in search_patterns:
            for rglob in braceexpand.braceexpand(search_pattern):  # Expand braces
                for rpath in glob.glob(rglob):  # Expand globbing

                    # We want to retain ELFs only
                    #
                    # Unfortunately, I couldn't find a better way but to try to open the file
                    # and catch any exception.
                    #
                    # "Better ask for forgiveness than permission", they say... :°

                    try:
                        with open(rpath, 'rb') as file:
                            ELFFile(file)  # This throws if the file isn't a valid ELF
                            files += [rpath]
                    except:
                        pass  # Ignore invalid ELFs (dangling/text files in bin/ or lib/)
    return files
