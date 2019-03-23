#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""Templates are functions that provide a default, configurable and extendable way to
build packages of a certain type.

There are different kinds of template:

  * **Partial templates**: templates that provide only **a chunk** of the overall build process, like a
    template that wraps a specific build system but doesn't download any source code or generate
    any package.

    They are usually used as a sub-part of an *exhaustive template*.

    Examples of partial templates:
        * :py:mod:`.configure`
        * :py:mod:`.make`

  * **Exhaustive templates** : templates that provide **all the steps** involved in the building process, like downloading
    the source code, building it, generating the packages, managing dependencies etc.

    Example of exhaustive templates:
        * :py:mod:`.autotools`
"""

pass
