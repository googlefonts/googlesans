gSource=${!#}

cp "$gSource.glyphs" Build.glyphs

mkdir brace-sources
mkdir brace-ttfs

# Remove nonexporting glyphs + slice file
python2 $(dirname ${BASH_SOURCE[0]})/fixBraces.py Build.glyphs

for path in brace-sources/*.glyphs; do
	filename=${path##*/}
	ttfname="${filename%.*}-VF.ttf"
	
	fontmake -o variable -g $path --no-production-names

	mv variable_ttf/$ttfname brace-ttfs/$ttfname
	rm -rf master_ufo
	rm -rf variable_ttf
done

rm -rf brace-sources

fontmake -o variable -g Build.glyphs

mv variable_ttf/*.ttf Build-VF.ttf
rm -rf master_ufo
rm -rf instance_ufo
rm -rf variable_ttf
rm -rf Build.glyphs

for path in brace-ttfs/*.ttf; do
	ttx $path
	rm -rf $path
done

ttx Build-VF.ttf

rm -rf Build-VF.ttf

# cp Build-VF.ttx BuildBase-VF.ttx

for path in brace-ttfs/*.ttx; do
	filename=${path##*/}
    glyphName="$(echo $filename | sed -e 's,-source.*,,')"
    gvar="$(cat $path | tr '\n' '\r' | sed -n "s,.*\(<glyphVariations glyph=\"$glyphName\".*<\/glyphVariations>\).*,\1,p")"
    glyf="$(cat $path | tr '\n' '\r' | sed -n "s,.*\(<TTGlyph name=\"$glyphName\".*<\/TTGlyph>\).*,\1,p")"

    echo $filename
    echo $glyphName

    echo "Adding $glyphName glyf data..."
	cat Build-VF.ttx | tr '\n' '\r' | sed -e "s,<TTGlyph name=\"$glyphName\"[^T]*TTGlyph>,$glyf," | tr '\r' '\n' > BuildGlyf-VF.ttx
	echo "Adding $glyphName gvar data..."
	cat BuildGlyf-VF.ttx | tr '\n' '\r' | sed -e "s,<glyphVariations glyph=\"$glyphName\"[^V]*Variations>,$gvar," | tr '\r' '\n' > Build-VF.ttx

	rm -rf BuildGlyf-VF.ttx
done

rm -rf brace-ttfs

ttx Build-VF.ttx

rm -rf Build-VF.ttx

mv Build-VF.ttf "$gSource-VF.ttf"