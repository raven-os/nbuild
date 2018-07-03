# nuild - Nest's Package Builder

`nbuild` is Nest's package builder. It takes a `Build Manifest` (a python file) that describes the steps to be taken to build the package, from retrieving the source files to achieving a fully built program.

There are in total 7 steps:
```
- Fetch      -> Fetching the needed sources
- Unpack     -> Extracting the sources
- Patch      -> Applying potentially patches
- Configure  -> Configuring the build
- Compile    -> Compiling the source code
- Check      -> Running the test suites
- Wrap       -> Creating all necessary files to install the package (data and install manifest)
```

The `Build Manifest` can inherits existing templates to reuse some of their steps. For example, `CoreutilsManifest` uses `GnuTemplate`, which in turns uses `FetchTarballTemplate` to retrieve the source code (step `Fetch` and `Unpack`) and `AutotoolsTemplate`. `AutotoolsTemplate` uses `AutoconfTemplate` and `MakeTemplate` to provide the steps `Configure`, `Compile`, `Check` and `Wrap`. The step `Patch` is left empty.

All steps are then done in order.

## Prerequisites

* python3

To install nbuild's dependencies, run

```bash
pip install -r requirements.txt
```

**Warning: Nest-build does NOT provide any kind of isolation**.

If the manifest is ill-formed, your main system may be damaged. That's why we recommend the use of our docker image: `ravenos/nbuild`.

### Examples

Here is `coreutil`'s `Build Manifest`. More can be found in the `example/` folder.

```python
#!/usr/bin/env python3

from nbuild.manifest import BuildManifest
from templates.gnu import GnuTemplate


CATEGORY = "sys-bin"
NAME = "coreutils"
VERSION = "8.29.0"
RUN_DEPENDENCIES = {
    "stable::sys-lib/libc": ">=2.27.0"
}


class CoreutilsManifest(GnuTemplate, BuildManifest):
    def __init__(self):
        BuildManifest.__init__(self, CATEGORY, NAME, VERSION, RUN_DEPENDENCIES)
        GnuTemplate.__init__(
            self,
            fetch={
                "url": "http://ftp.gnu.org/gnu/coreutils/coreutils-8.29.tar.xz",
                "md5sum": "960cfe75a42c9907c71439f8eb436303",
            },
        )

CoreutilsManifest().build()
```
