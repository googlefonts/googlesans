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

bounds_before = {'GoogleSans-Regular.ttf': (959, -253), 'GoogleSans-Italic.ttf': (959, -253), 'GoogleSans-Medium.ttf': (962, -263), 'GoogleSansDisplay-MediumItalic.ttf': (962, -265), 'GoogleSans-MediumItalic.ttf': (962, -265), 'GoogleSansDisplay-Bold.ttf': (964, -285), 'GoogleSansDisplay-BoldItalic.ttf': (964, -286), 'GoogleSans-BoldItalic.ttf': (964, -286), 'GoogleSansDisplay-Italic.ttf': (959, -253), 'GoogleSansDisplay-Medium.ttf': (962, -263), 'GoogleSans-Bold.ttf': (964, -285), 'GoogleSansDisplay-Regular.ttf': (959, -253)}


parser = argparse.ArgumentParser()
parser.add_argument("fonts", nargs='+')
args = parser.parse_args()

fonts = {'-'.join(os.path.basename(p).split('-')[:2]) + '.ttf': TTFont(p) for p in args.fonts}

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
