.. NBuild documentation master file, created by
   sphinx-quickstart on Sun Feb 10 00:55:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NBuild's documentation!
==================================

This documentation covers all types and functions that can be found in a build manifest or in nbuild itself.

It is made of two major modules: the :py:mod:`core` module and the :py:mod:`stdlib` module.
The first one contains functions only used by :py:mod:`nbuild` or by :py:mod:`stdlib` and should not be used by a build manifest.
On the other hand, :py:mod:`stdlib` is made to be used by build manifests.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Content
=======

.. toctree::
   :maxdepth: 1

   core
   nbuild
   stdlib

Examples
========

Examples of build manifests can be found in the `nbuild-manifests <https://github.com/raven-os/nbuild-manifests>`_ repository.
