#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Provide different dependency linkers that can be used interchangeably as part of a template.

All dependency linkers are python functions that try to assign requirements to the generated packages automatically.
They analyse the content of the package and do their best to figure out how those new packages are related to the other existing ones.

Even though they might not always find all requirements, they provide a solid base to avoid mistakes and obvious, redundant requirements.

A typical example is the :py:func:`~stdlib.deplinker.elf.elf_deplinker`, which looks for all ELF files in a package and for each of them retrieves its
ELF dependencies, then fetches a list of nest repositories to find out which package contains those dependencies.

They all share the same properties which are required to ensure they can be used interchangeably:
  * They take a list of :py:class:`.Package` s as their only mandatory parameter
  * They do not have any return value
  * They do not have any guarantee of sucess, only a guarantee of best-effort
  * They do not erase any existing ``run_requirements``, so they can be chained one after another safely
"""

pass
