# Google Sans Repository Maintainer Documentation

## Project Dependency Management

The Google Sans typeface build workflow requires the following:

- Python 3.6+ interpreter
- [`fontmake`](https://github.com/googlefonts/fontmake) Python package
- `make`

Optional dependencies for project maintainers include:

- [`pip-tools` Python package](https://github.com/jazzband/pip-tools) - used to maintain the dependencies defined in the `requirements.txt` file

Install the `pip-tools` package with:

```
$ pip3 install --upgrade pip-tools
```

### How to Update Project Dependency Versions

The Python dependencies are defined in the `requirements.txt` file at the root of the repository.  This file is generated from the `requirements.in` file with the `pip-compile` executable, a tool that is part of the free [`pip-tools` Python package](https://github.com/jazzband/pip-tools).

Execute the following command in the root of the project repository to update the depenency version numbers to current release versions:

```
$ pip-compile --upgrade
```

This command is included in a `make` target as a convenience:

```
$ make update-deps
```

The updated `requirements.txt` file should be committed to the git version control history.  Project builders must be aware that this file was updated so that existing venv's can be synchronized with the new version definitions.  The changes will be reflected immediately in any new venv's that are generated as of the `requirements.txt` file change commit.

### How to List Project Dependency Versions Installed in `.venv`

```
$ make list-deps
```

### How to Synchronize Project Dependencies in an Existing `.venv` with Updated `requirements.txt` Definitions

```
$ make sync-deps
```