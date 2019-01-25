# Script to build brace layers
## Slices a glyphs file into single glyph files and moves brace layers to master layers
## Using a bash script the generated glyf and gvar data can then be inserted into the final font file

import sys
import os
import re
import copy
import time
from glyphsLib import GSFont
from glyphsLib import GSGlyph
from glyphsLib import GSLayer
from glyphsLib import GSFontMaster
from glyphsLib import GSInstance

start = time.time()

filename = sys.argv[-1]

font = GSFont(filename)

nonExportGlyphs = []
baseIndex = 0
for glyph in font.glyphs:
    if glyph.export == False:
        nonExportGlyphs.append(baseIndex)
        baseIndex -= 1
    baseIndex += 1

for baseIndex in nonExportGlyphs:
    del font._glyphs[baseIndex]

font.save(filename)
print "Removed all nonexporting glyphs, build file saved"

braceSources = []

def keepOneGlyph(font, glyphName):
    delGlyphs = []
    index = 0
    for glyph in font.glyphs:
        if glyph.name != glyphName:
            delGlyphs.append(index)
            index -= 1
        index += 1

    for glyphIndex in delGlyphs:
        del font._glyphs[glyphIndex]

for glyphIndex, glyph in enumerate(font.glyphs):
    hasBrace = False
    for layer in glyph.layers:
        if re.match('.*\d\}$', layer.name):
            hasBrace = True
            break
    if hasBrace == True:
        braceFont = GSFont(filename)
        braceFilename = glyph.name + "-source" + str(glyphIndex) + ".glyphs"
        print "Created file:" + glyph.name + "-source" + str(glyphIndex) + ".glyphs"
        braceFont.familyName = glyph.name + "-source" + str(glyphIndex)

        braceFont.features = []
        braceFont.classes = ()
        braceFont.kerning = {}

        glyphName = glyph.name
        keepOneGlyph(braceFont, glyphName)

        addMasters = []
        for layer in braceFont.glyphs[0].layers:
            if re.match('.*\d\}$', layer.name):
                values = map(int, re.sub('.*{|}', '', layer.name).split(','))
                newMaster = copy.copy(braceFont.masters[0])
                for axisIndex, value in enumerate(values):
                    if axisIndex == 0:
                        newMaster.weightValue = value
                    elif axisIndex == 1:
                        newMaster.widthValue = value
                    elif axisIndex == 2:
                        newMaster.customValue = value
                    elif axisIndex == 3:
                        newMaster.customValue1 = value
                    elif axisIndex == 4:
                        newMaster.customValue2 = value
                    elif axisIndex == 5:
                        newMaster.customValue3 = value
                newMaster.id = None
                newMaster.name = re.sub('.*{|}', '', layer.name)
                addMasters.append([newMaster, layer.layerId])

        for master in addMasters:
            braceFont.masters.append(master[0])
            masterId = braceFont.masters[-1].id
            braceFont.glyphs[0].layers[masterId].paths = braceFont.glyphs[0].layers[master[1]].paths
            braceFont.glyphs[0].layers[masterId].components = braceFont.glyphs[0].layers[master[1]].components
            braceFont.glyphs[0].layers[masterId].anchors = braceFont.glyphs[0].layers[master[1]].anchors
            braceFont.glyphs[0].layers[masterId].width = braceFont.glyphs[0].layers[master[1]].width
            
            del braceFont.glyphs[0].layers[master[1]]

        braceFont.save("brace-sources/" + braceFilename)
        print "Saved file:" + braceFilename

end = time.time()
print end - start


