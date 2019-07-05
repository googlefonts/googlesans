from glob import glob
from fontTools.ttLib import TTFont
import os
import shutil
import argparse

cwd = os.path.dirname(__file__)

fix_dir = os.path.join(cwd, 'fixed')

if os.path.isdir(fix_dir):
    shutil.rmtree(fix_dir)
os.mkdir(fix_dir)

bounds_before = {'GoogleSans-Regular.ttf': (1056, -271), 'GoogleSans-Italic.ttf': (1056, -271), 'GoogleSans-Medium.ttf': (1056, -271), 'GoogleSansDisplay-MediumItalic.ttf': (1056, -271), 'GoogleSans-MediumItalic.ttf': (1056, -271), 'GoogleSansDisplay-Bold.ttf': (1056, -271), 'GoogleSansDisplay-BoldItalic.ttf': (1056, -271), 'GoogleSans-BoldItalic.ttf': (1056, -271), 'GoogleSansDisplay-Italic.ttf': (1056, -271), 'GoogleSansDisplay-Medium.ttf': (1056, -271), 'GoogleSans-Bold.ttf': (1056, -271), 'GoogleSansDisplay-Regular.ttf': (1056, -271)}


parser = argparse.ArgumentParser()
parser.add_argument("fonts", nargs='+')
args = parser.parse_args()

fonts = {'-'.join(os.path.basename(p).split('-')[:2]) : TTFont(p) for p in args.fonts}

print("Transferring yMax, yMin")
for name, font in fonts.items():
    new_ymax, new_ymin = bounds_before[name]
    font['head'].yMax = new_ymax
    font['head'].yMin = new_ymin

    assert font['head'].yMax == new_ymax
    assert font['head'].yMin == new_ymin
    fixed_font = os.path.join(fix_dir, name)
    print('saving font: {}'.format(fixed_font))
    font.save(fixed_font)
