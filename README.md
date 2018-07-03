# nbuild
Nest Build System

## Prerequisites
python3


### Using it

`nbuild` takes a python file as its first parameter, this file is a `Build Manifest`, it is a file that describes the steps to be taken, from retrieving the source files to achieving a fully built program.

There are in total 7 steps:
```
- Fetch     -> Fetching the needed sources
- Unpack    -> Extracting if an archive was fetched
- Patch     -> Applying the potential needed patches
- Configure  -> Configuring the build
- Compile   -> Compiling the source code
- Check     -> Running the test suites
- Wrap      -> Creating a pair of a Package Manifest and an archive of the files to install
```
The build manifest file must contain a class named `BuildManifest`, itself optionally containing a function for each step, and with a constructor with no parameters.
The class must inherit from the class `templates.BaseManifest.Manifest`.
You can omit functions in the manifest, as some are not always needed.

### Examples
```python3
import templates.BaseManifest


class BuildManifest(templates.BaseManifest.BaseManifest):
    def __init__(self):
        self.name = "alpaca-fantom"
        self.version = "0.1.0"
  
    def fetch(self):
        pass
  
    def wrap(self):
        pass
```

To reduce boilerplate in manifests, some templates are provided:
`templates.common` and `templates.autotools` for  packages that use autotools
 
```python3
import os
import templates.common


class BuildManifest(templates.BaseManifest.BaseManifest):
    def __init__(self):
        templates.BaseManifest.BaseManifest.__init__(self)
        self.name = "sed"
        self.version = "4.4"

    def fetch(self):
        self.filename = templates.common.fetch("http://ftp.gnu.org/gnu/sed/sed-4.4.tar.xz",
                                               md5sum="e0c583d4c380059abd818cd540fe6938")

    def unpack(self):
        templates.common.unpack(self.filename)
        os.chdir("sed-4.4")

    def wrap(self):
        pass
```

`templates.common` defines a class `Common`, that inherits from `BaseManifest`, and implement multiples steps, and which constructor takes as parameters the arguments to the steps

```python3
import templates.common
import templates.make
import templates.autotools


class BuildManifest(templates.common.Common):
    def __init__(self):
        templates.common.Common.__init__(self, "sed", "4.4",
                                         fetch={"url": "http://ftp.gnu.org/gnu/sed/sed-4.4.tar.xz",
                                                "md5sum": "e0c583d4c380059abd818cd540fe6938"},
                                         configure={"prefix": "/tools"})
