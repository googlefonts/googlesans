## vf2s

A variable font to static instance generator for the Google Sans typeface

### Dependencies

- Python 3 interpreter
- fontTools Python library
    - install with `pip3 install --upgrade fontTools`

For the GUI version only:
- Gooey Python library
    - install with `pip3 install --upgrade Gooey`

### Usage

`vf2s.py` is a Python script that takes a path to a single variable font and creates a single static instance using design axis values that are passed on the command line.  The application then writes a unique name to the static font name table records (and outfile path) so that two or more static instances derived from the variable font can be installed side-by-side to support A/B testing.

Help can be displayed by entering the following command using the directory that contains the script as the working directory:

```
$ python3 vf2s.py --help
```

and available arguments are:

```
usage: vf2s.py [-h] [--weight WEIGHT] [--width WIDTH] [-v] path

A variable font to static instance generator for Google Sans.

positional arguments:
  path             Variable font path

optional arguments:
  -h, --help       show this help message and exit
  --weight WEIGHT  Weight axis value (380-734)
  --width WIDTH    Width axis value (0-400)
  -v, --version    Display application version
```

Enter the desired value in the design axis range as an argument to the respective command line option.  For instance to define weight, xheight, and spacing values for a variable font on the path `path/to/GS-VF-Regular.ttf` use a command like this:

```
$ python3 vf2s.py --weight 350 --width 270 path/to/GS-VF-Regular.ttf
```

`vf2s.py` creates a unique name for the font using a concatenated string of:

- one or two letter lowercase abbreviations that represent the design axis
- axis integer value used in the static font build

The OpenType name table records nameID 1, nameID 4, and nameID 6 are then modified with appropriately formatted auto-generated values.

#### GUI

The graphical user interface version of the script requires installation of the Gooey Python library (see Dependencies section above).  Open your terminal, navigate to the `vf2s-gui.py` script and enter the following command to launch the GUI window:

```
$ python3 vf2s-gui.py
```

Open the file path selection dialog and select the path to the variable font file.  Then enter the desired design axis values and click the Start button.  To select new values and instantiate additional fonts, click the Edit button to return to the settings window.


### Changes

#### v0.6.0

- refactored vf2s.py source to support weight and width axis definitions only
- refactored vf2s-gui.py source to support weight and width axis definitions only
- fixed opsz axis value at 14 across all instance builds (defined using the slnt axis for technical reasons)
- compiled PyInstaller build of vf2s from the vf2s.py script using Python 3.7 interpreter
- these updates were designed to work with the Google Sans Text beta v2.006 design changes

#### v.0.5.0

- initial testing release version with support for six design axis values that were in use as of Google Sans Text v2.005 build