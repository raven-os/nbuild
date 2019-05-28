#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provide different splitters that can be used interchangeably as part of a template.

All splitters are functions that try to split the output of a build into one or multiple packages.
They approach the problem differently, letting the maintainer choose the one that fits most the package
he is building.

They all share the same properties which are required to ensure they can be used interchangeably:
  * They don't take any mandatory parameter
  * They return a dictionary, with the generated packages' :py:func:`~stdlib.package.PackageID.short_name` as the key, and the
    associated :py:class:`.Package` as the value.
  * The :py:func:`~stdlib.package.PackageID.short_name` used as a key is guaranteed to match the one of the package matching that key.
  * The generated packages have their content already filled with files drained from the build's output.
  * The name and category of the generated packages may or may not be predictable, depending on the splitter and what it finds in the build's output.
  * A maintainer can override anything a splitter has decided (like a package name, category or content) by using the returned dictionary.
"""

pass
