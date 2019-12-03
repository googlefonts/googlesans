# Google Sans Build Documentation

## Dependencies

The Google Sans typeface compilation workflow requires the following:

- Python 3 interpreter
- [`fontmake`](https://github.com/googlefonts/fontmake) Python package
- `make`

## Virtual Environment Management
### Virtual Environment Set Up

The build workflow uses pinned build dependency versions and, therefore, requires a Python 3 virtual environment (venv).

Set up a venv with the following command:

```
$ python3 -m venv path/to/google-sans
```

where `path/to` can be any path on your system.  For instance, to set up your venv on the path `~/venv/google-sans`, use the following command:

```
$ python3 -m venv ~/venv/google-sans
```

For the remainder of the documentation, we will assume the path `~/venv/google-sans`.  Update the file paths below if you modify this default.

### Virtual Environment Activation

Activate the venv with the following command from any directory path:

```
$ source ~/venv/google-sans/bin/activate
```

The command line prompt will display the name of your venv on the left-hand side if your venv is active.  

### Install Build Dependencies

Install build dependencies in the venv with the following command:

```
$ pip install -r requirements.txt
```

Execute this command every time the dependency versions are updated in the `requirements.txt` file in order to sync your venv dependency versions if you maintain a venv for local Google Sans builds.

### Virtual Environment Deactivation

Use the following command to deactivate your Python 3 venv:

```
$ deactivate
```

Your Python package installs default back to system versions.

## Google Sans Build

Google Sans builds are supported through a `make` target workflow.  See the root level  `Makefile` and the `source/Makefile` for the full set of make targets.

To build all variable and static font files, execute the default make command in the root of the repository:

```
$ make
```

The build paths are `build/GoogleSans/static` and `build/GoogleSans/variable` for static font instances and variable fonts, respectively.

We support individual format and style compiles with explicit make targets.  For instance, to build the Google Sans medium static font instance, use the following make command:

```
$ make gs-medium
```

Please refer to the `source/Makefile` for the full set of make targets that are available for font compiles.









