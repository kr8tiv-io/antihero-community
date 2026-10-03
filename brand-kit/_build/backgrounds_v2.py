"""Promote the Blender renders into the kit's backgrounds and archive the old dark set."""
import glob
import os
import shutil

import numpy as np
from PIL import Image, ImageFilter

from brand import KIT

HERE = os.path.dirname(os.path.abspath(__file__))
FINAL = os.path.join(HERE, 'scenes', 'out', 'final')
BG = os.path.join(KIT, '04_Backgrounds')
ARCH = os.path.join(BG, '_previous-dark-set')
SCENES = ['rise-above', 'launch', 'break-formation', 'first-light', 'see-further']
RETIRED = ['first-light', 'smoke', 'grid', 'ignition-grain']      # the dark, red-heavy originals


def finish(src, size, out, grain=0.011, seed=0):
    im = Image.open(src).convert('RGB').resize(size, Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.3, percent=35, threshold=2))
    a = np.asarray(im).astype(np.float32) / 255.0
    rng = np.random.default_rng(seed)
    n = rng.standard_normal(a.shape[:2]).astype(np.float32)[..., None] * grain
    a = np.clip(a + n * (0.35 + 0.65 * (1 - np.abs(a - 0.5) * 2)), 0, 1)       # grain strongest in the midtones
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out, quality=93, subsampling=0, optimize=True)
    return out


if __name__ == '__main__':
    os.makedirs(ARCH, exist_ok=True)
    for name in RETIRED:
        for f in glob.glob(os.path.join(BG, f'antihero-bg-{name}_*.jpg')):
            dst = os.path.join(ARCH, os.path.basename(f).replace('first-light', 'first-light-red'))
            if not os.path.exists(dst):
                shutil.move(f, dst)
    done = []
    for i, name in enumerate(SCENES):
        src = os.path.join(FINAL, name + '.png')
        if os.path.exists(src):
            done.append(finish(src, (3840, 2160), os.path.join(BG, f'antihero-bg-{name}_desktop-3840x2160.jpg'), seed=i))
        ph = os.path.join(FINAL, name + '_phone.png')
        if os.path.exists(ph):
            done.append(finish(ph, (1290, 2796), os.path.join(BG, f'antihero-bg-{name}_phone-1290x2796.jpg'), seed=100 + i))
    print('\n'.join(os.path.basename(d) for d in done))
