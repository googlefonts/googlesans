#!/bin/bash
# This script will replace glyph uni000A for uniE007. It solves an issue
# reported by a Google team who were using the font on CJK text. It also
# bumps the version number from v2.001 to v2.002.
# Note: This script overwrites the existing file.

# Usage:
# To convert a single font:
# sh glyph_replace.sh font.ttf
# To convert all fonts in a folder:
# for i in /path/to/fonts_dir/*.ttf;do sh glyph_replace.sh $i;done

set -e

echo "$1: Swapping uni000A for uniE007"

ttx_file="$(basename -s ".ttf" $1).ttx"
if [ -f $ttx_file ]; then
    rm $ttx_file
fi

ttx $1
sed -i '' 's/"uni000A"/"uniE007"/g' $ttx_file
sed -i '' 's/"0xa"/"0xe007"/g' $ttx_file

# Bump version number
sed -i '' 's/2.001/2.002/g' $ttx_file

rm $1
ttx -b $ttx_file
rm $ttx_file