# Google Sans Build Documentation

## Dependencies

The Google Sans typeface build workflow requires the following:

- Python 3.6+ interpreter
- [`fontmake`](https://github.com/googlefonts/fontmake) Python package
- `make`

Optional dependencies for project maintainers include:

- `pip-tools` Python package - used to maintain the dependencies defined in the `requirements.txt` file

## Quickstart

Source files are located on the directory path: `source/GoogleSans`.

Run the following commands in the root of the repository to install the required build dependencies in a Python virtual environment and compile all variable and static instance fonts:

```
$ make setup
# Activate .venv now
$ make
```

Static fonts are located in the directories `build/GoogleSans/static/expert` and `build/GoogleSans/static/default`.

Variable fonts are located in the directories `build/GoogleSans/variable/expert` and `build/GoogleSans/variable/default`.

Remove the virtual environment and intermediate UFO source files that are generated during the build with the following command:

```
$ make clean
```

Please refer to the documentation below for additional details.

## Google Sans Build

The Google Sans build workflow uses `make` targets to build a Python 3 virtual environment, install all required compiler dependencies at appropriate versions, and compile the fonts from Glyphs source files. See the root level `Makefile` and source subdirectory `source/Makefile` for the full set of annotated make targets.

### Create a Python 3 virtual environment

The build process requires a Python 3 virtual environment. The virtual environment is created with the command `make setup`. See the Install Build Dependencies section below for additional details.

### Install build dependencies

The build process uses the root level `requirements.txt` file definitions of project build dependencies. The packages are installed in a virtual environment on the path `.venv` in the root of the repository. The directory is included in the `.gitignore` file, and the contents of the virtual environment should be excluded from the git version control history.

Install build dependencies by running the following command in the root of the repository:

```
$ make setup
```

### Build fonts

Build all defined static instance and variable fonts by running the following command in the root of the repository:

```
$ make
```

The build paths are `build/GoogleSans/static` and `build/GoogleSans/variable` for static instance and variable fonts, respectively.

Individual styles are with explicit make targets. For instance, to build the Google Sans Medium static font instance, use the following make command:

```
$ make gs-medium
```

Please refer to the `source/Makefile` for the full set of make build targets.

#### Build incoming Glyphs.app sources

Build incoming Glyphs.app sources dropped in by vendors into variable fonts by running the following command in the root of the repository:

```
$ make gs-vf-vendor
```

#### Build outgoing Glyphs.app sources

Build outgoing Glyphs.app sources for vendors from the Designspaces by running the following command in the root of the repository:

```
$ make gs-ufo2glyphs
```

### Remove temporary UFO source files

The fontmake compiler builds UFO source file intermediates during the compilation of Google Sans fonts from Glyphs source files. These are found in directories on the paths `build/GoogleSans/instance_ufo` and `build/GoogleSans/master_ufo`.

Remove these files by running the following command in the root of the repository:

```
$ make clean
```

Note: this command also removes the `.venv` virtual environment directory

### Remove Python 3 virtual environment

Remove the virtual environment by running the following command in the root of the repository:

```
$ make clean
```

Note: this command also removes the temporary intermediate UFO source files located in the build directory.
