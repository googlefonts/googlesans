import os
from fontTools.ttLib import TTFont
from glob import glob



def main():
    this_dir = os.path.dirname(__file__)
    fonts_paths = glob(os.path.join(this_dir, 'src', '*.ttf'))

    for font_path in fonts_paths:
        ttfont = TTFont(font_path)

        if len(ttfont['cmap'].tables) != 1:
            raise Exception('Warning these fonts are not for Android. '
                            'They contain more than 1 cmap subtable')

        # Update cmap
        ttfont['cmap'].tables[0].platformID = 3
        ttfont['cmap'].tables[0].platEncID = 1

        # Update version
        ttfont['head'].fontRevision = 1.028

        # Name table font revision
        for name in ttfont['name'].names:
            name_text = name.toUnicode()

            if '1.027' in name_text:
                name_text = name_text.replace('1.027', '1.028')
                ttfont['name'].setName(
                    unicode(name_text),
                    name.nameID,
                    name.platformID,
                    name.platEncID,
                    name.langID
                )

        out_path = os.path.join(this_dir, 'fixed', os.path.basename(font_path))
        ttfont.save(out_path)





if __name__ == '__main__':
    main()
