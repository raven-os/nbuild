# nbuild - Nest's Package Builder

`nbuild` is Nest's package builder. It takes a `Build Manifest` (a python file) that describes the steps to be taken to build one or more packages, from retrieving the source files to achieving a fully built program.

Examples can be found in [nbuild-manifests](https://github.com/raven-os/nbuild-manifests).

`nbuild` places it's content in 4 seperate folders:
    * `/usr/nbuild/downloads/`: All downloads are placed there so they can be re-used when rebuilding the same package
    * `/usr/nbuild/sources/`: Packages are extracted and build there.
    * `/usr/nbuild/installs/`: Packages are installed in this folder before being compressed
    * `/usr/nbuild/packages`: The resulting package (`data.tar.gz` and `manifest.toml`) is placed there when the operation is successfully completed

## Prerequisites

* python3.6+

To install nbuild's dependencies, run

```bash
pip install -r requirements.txt
```

**Warning: Nest-build does NOT provide any kind of isolation**.

If the manifest is ill-formed, your main system may be damaged. That's why we recommend the use of our docker image: `ravenos/nbuild`.

Example:

```
docker run -v $PWD/build:/build -v $PWD/packages:/packages -v $PWD/examples:/manifests ravenos/nbuild /manifests/sed.py
```

### Examples

Here is an example manifest for a basic C project based on GNU's autotools.

```python
#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Example of a build manifest.
"""

from nbuild.stdenv.package import package
from nbuild.stdenv.fetch import fetch_url
from nbuild.stdenv.autotools import build_autotools_package


@package(
    id="stable::sys-lib/helloworld#1.0.0",
)
def build_helloworld():
    build_autotools_package(
        fetch=lambda: fetch_url(
            url=f"https://example.com/helloworld.tar.gz",
            sha256="729e344a01e52c822bdfdec61e28d6eda02658d2e7d2b80a9b9029f41e212dde",
        ),
    )
```
