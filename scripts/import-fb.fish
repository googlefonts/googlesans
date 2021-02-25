for ufo in source/GoogleSans/*.ufo
    rm -rf $ufo/glyphs
end

set B_UP "../GoogleSans-fb/sources/GS Cubic Sources/Regular/"
set B_IT "../GoogleSans-fb/sources/GS Cubic Sources/Italic/"

set SRC "$B_UP/Google Sans-opsz17-wght400-GRAD0.ufo/"
set DST "source/GoogleSans/GoogleSans-TextRegular.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_UP/Google Sans-opsz17-wght700-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-TextBold.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_UP/Google Sans-opsz18-wght400-GRAD-50.ufo"
set DST "source/GoogleSans/GoogleSans-Regular-GRAD-50.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_UP/Google Sans-opsz18-wght400-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-Regular.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_UP/Google Sans-opsz18-wght400-GRAD200.ufo"
set DST "source/GoogleSans/GoogleSans-Regular-GRAD200.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_UP/Google Sans-opsz18-wght700-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-Bold.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST


set SRC "$B_IT/Google Sans Italic-opsz17-wght400-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-TextItalic.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_IT/Google Sans Italic-opsz17-wght700-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-TextBoldItalic.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_IT/Google Sans Italic-opsz18-wght400-GRAD-50.ufo"
set DST "source/GoogleSans/GoogleSans-Italic-GRAD-50.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_IT/Google Sans Italic-opsz18-wght400-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-Italic.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_IT/Google Sans Italic-opsz18-wght400-GRAD200.ufo"
set DST "source/GoogleSans/GoogleSans-Italic-GRAD200.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST

set SRC "$B_IT/Google Sans Italic-opsz18-wght700-GRAD0.ufo"
set DST "source/GoogleSans/GoogleSans-BoldItalic.ufo"
cp -r $SRC/glyphs $DST
cp $SRC/groups.plist $DST
cp $SRC/kerning.plist $DST


python scripts/gs-normalize-designspace.py
