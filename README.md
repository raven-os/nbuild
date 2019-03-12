# Nest Build 

*An automated package builder for lazy maintainers.*

## Dependencies

Nest build requires python3.6+. To install its dependencies, run

```bash
$ pip install -r requirements.txt
```

## How it works

Nest build uses a python file (called a build manifest) to describe how the compilation should be performed. The build manifest downloads the source code of a software, compiles it and splits it into multiple packages.
All of this is done thanks to a powerful library included in nest build: the standard compilation library. This library automates all the hard tasks while still providing a great granularity of modifications regarding those automated tasks.

Examples of build manifests can be found in the [nbuild-manifests](https://github.com/raven-os/nbuild-manifests/) repository.

## Documentation

The documentation of the standard compilation library is hosted [here](https://docs.raven-os.org/nbuild/master/), but it can also be locally generated with the following commands:

```bash
$ pip install -r docs/requirements.txt
$ sphinx-apidoc -f --separate -o docs/source/ .
$ make -C docs html
```

The main page can be accessed at `docs/build/html/index.html`.
