## vf2s

A variable font to static instance generator for the Google Sans typeface

### Dependencies

- Python 3 interpreter
- fontTools Python library
    - install with `pip3 install --upgrade fontTools`

### Usage

`vf2s.py` is a Python script that takes a path to a single variable font and creates a single static instance using design axis values that are passed on the command line.  The application then writes a unique name to the static font name table records (and outfile path) so that two or more static instances derived from the variable font can be installed side-by-side to support A/B testing.

Help can be displayed by entering the following command using the directory that contains the script as the working directory:

```
$ python3 vf2s.py --help
```

and available arguments are:

```
usage: vf2s.py [-h] [--weight WEIGHT] [--xheight XHEIGHT] [--spacing SPACING]
               [--charwidth CHARWIDTH] [--ascender ASCENDER]
               [--counter COUNTER] [--version]
               path

A variable font to static instance generator for Google Sans.

positional arguments:
  path                  Variable font path

optional arguments:
  -h, --help            show this help message and exit
  --weight WEIGHT       Weight axis value (300-400)
  --xheight XHEIGHT     X-height axis value (170-200)
  --spacing SPACING     Spacing axis value (100-200)
  --charwidth CHARWIDTH
                        Character width axis value (0-100-200)
  --ascender ASCENDER   Ascender height axis value (0-100)
  --counter COUNTER     Counter axis value (0-100)
  --version             show program's version number and exit
```

Enter the desired value in the design axis range as an argument to the respective command line option.  For instance to define weight, xheight, and spacing values for a variable font on the path `path/to/GS-VF-Regular.ttf` use a command like this:

```
$ python3 vf2s.py --weight 350 --xheight 180 --spacing 120 path/to/GS-VF-Regular.ttf
```

`vf2s.py` creates a unique name for the font using a concatenated string of:

- one or two letter lowercase symbols that represent the design axis (using the field's first one or two letters to create unique values)
- axis integer value used in the static font build

The OpenType name table records nameID 1, nameID 4, and nameID 6 are then modified with appropriately formatted auto-generated values.

In the example above, the auto-generated nameID 4 record value is `GS w350x180s120 Regular` and the auto-generated font path write is `GS-w350x180s120-Regular.ttf` using the same directory where the variable font is located.

