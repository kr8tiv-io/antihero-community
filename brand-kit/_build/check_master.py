"""Render the rebuilt mark and compare it against the source bitmap."""
import json
import os

import numpy as np
from PIL import Image, ImageChops

from render import Renderer

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work')
M = json.load(open(os.path.join(HERE, 'master', 'antihero-mark-paths.json')))
cx, cy, R, S = np.load(os.path.join(WORK, 'geom.npy'))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
<circle cx="500" cy="500" r="500" fill="#1D2124"/>
<path fill="#fff" fill-rule="evenodd" d="{M['a_path']}"/>
<path fill="#fff" fill-rule="evenodd" d="{M['hero_path']}"/>
</svg>'''
p = os.path.join(WORK, 'master_check.svg')
open(p, 'w').write(svg)
html = os.path.join(WORK, 'master_check.html')
open(html, 'w').write(f'<html><body style="margin:0;background:#fff">{svg.replace("<svg ", "<svg width=1000 height=1000 ")}</body></html>')

with Renderer() as r:
    r.png(html, os.path.join(WORK, 'master_1000.png'), 1000, 1000)

new = Image.open(os.path.join(WORK, 'master_1000.png')).convert('L')
# map source into the same 1000 frame: disc centre (cx,cy)/S in source px, radius R/S
src = Image.open(os.path.join(WORK, 'source_logo.png')).convert('L')
scale = 500.0 / (R / S)
sw, sh = int(src.width * scale), int(src.height * scale)
srcb = src.resize((sw, sh), Image.BICUBIC)
ox, oy = int(round(cx / S * scale - 500)), int(round(cy / S * scale - 500))
srcc = srcb.crop((ox, oy, ox + 1000, oy + 1000))
srcc.save(os.path.join(WORK, 'source_in_frame.png'))

a = np.asarray(srcc).astype(float) > 139
b = np.asarray(new).astype(float) > 139
yy, xx = np.mgrid[0:1000, 0:1000]
inside = (xx - 500)**2 + (yy - 500)**2 < 480**2
diff = (a ^ b) & inside
print('pixels differing inside disc: %.3f%%' % (100 * diff.sum() / inside.sum()))
print('white area source %.0f  new %.0f' % ((a & inside).sum(), (b & inside).sum()))
# overlay: source=red channel, new=green channel
ov = np.zeros((1000, 1000, 3), np.uint8)
ov[..., 0] = np.asarray(srcc)
ov[..., 1] = np.asarray(new)
ov[..., 2] = np.asarray(new) // 2
Image.fromarray(ov).save(os.path.join(WORK, 'overlay.png'))
side = Image.new('RGB', (2000, 1000), 'white')
side.paste(srcc.convert('RGB'), (0, 0))
side.paste(new.convert('RGB'), (1000, 0))
side.resize((1400, 700), Image.LANCZOS).save(os.path.join(WORK, 'side_by_side.png'))
