"""The logo on every brand background: square (2400), 4K wallpaper (3840x2160), phone wallpaper (1290x2796)."""
import os

from brand import C, KIT, mark_group
from render import Renderer
from social import BASE_CSS, HTML_DIR, badge_inline, bg_url, wordmark_svg

OUT = os.path.join(KIT, '03_Logo-Textures', 'On-Backgrounds')
os.makedirs(OUT, exist_ok=True)

# (background, badge disc, badge mark, wordmark ANTI, wordmark hero, ink for tagline, bg position)
# v2: bright, inspiring scenes first; one dark (concrete) kept for contrast.
SCENES = [
    ('rise-above', C['carbon'], '#fff', C['void'], C['ignition'], C['void'], 'center 45%'),
    ('first-light', C['carbon'], '#fff', C['void'], C['ignition'], C['void'], 'center 40%'),
    ('launch', C['carbon'], '#fff', C['void'], C['ignition'], C['void'], 'center 40%'),
    ('break-formation', C['carbon'], '#fff', C['void'], C['ignition'], C['void'], 'center 40%'),
    ('daybreak', C['carbon'], '#fff', C['void'], C['ignition'], C['void'], 'center'),
    ('concrete', C['carbon'], '#fff', '#fff', C['ignition'], '#fff', 'center'),
]


def html(W, H, bg, pos, inner, kind='desktop-3840x2160'):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:{W}px;height:{H}px}}
.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.t{{font-family:'Barlow Condensed';font-weight:700;letter-spacing:.32em;margin-right:-.32em}}</style></head><body>
<div class="bg" style="background-image:url('{bg_url(bg, kind)}');background-position:{pos}"></div><div class="c">{inner}</div></body></html>"""


if __name__ == '__main__':
    # retire the v1 dark renders (kept in an archive folder, not deleted)
    import shutil
    arch = os.path.join(OUT, '_previous-dark-set')
    for fn in os.listdir(OUT):
        if fn.endswith('.jpg') and any(f'-on-{old}_' in fn for old in ('first-light', 'smoke', 'grid', 'ignition-grain', 'paper-bone')):
            os.makedirs(arch, exist_ok=True)
            shutil.move(os.path.join(OUT, fn), os.path.join(arch, fn.replace('-on-first-light_', '-on-first-light-red_')))
    jobs = []
    for bg, disc, mk, wa, wh, ink, pos in SCENES:
        # square: badge + tagline
        inner = f'{badge_inline(1150, disc, mk)}<div class="t" style="font-size:44px;color:{ink};margin-top:90px">BE YOUR OWN HERO</div>'
        jobs.append((bg, 'square_2400x2400', 2400, 2400, html(2400, 2400, bg, pos, inner)))
        # desktop wallpaper: badge + wordmark lockup
        inner = (f'<div style="display:flex;align-items:center;gap:110px">{badge_inline(560, disc, mk)}<div style="display:flex;flex-direction:column;gap:46px">'
                 f'{wordmark_svg(wa, wh, 250)}<div class="t" style="font-size:42px;color:{ink}">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</div></div></div>')
        jobs.append((bg, 'wallpaper_3840x2160', 3840, 2160, html(3840, 2160, bg, pos, inner)))
        # phone wallpaper: badge high, clear of the clock and dock
        inner = f'<div style="margin-top:-120px">{badge_inline(760, disc, mk)}</div><div class="t" style="font-size:40px;color:{ink};margin-top:70px">BE YOUR OWN HERO</div>'
        phone_kind = 'phone-1290x2796' if bg in ('rise-above', 'launch', 'first-light', 'daybreak', 'concrete') else 'desktop-3840x2160'
        jobs.append((bg, 'phone_1290x2796', 1290, 2796, html(1290, 2796, bg, pos, inner, kind=phone_kind)))
    with Renderer() as r:
        for bg, tag, W, H, h in jobs:
            hp = os.path.join(HTML_DIR, f'logo-on-{bg}_{tag}.html')
            with open(hp, 'w', encoding='utf-8') as f:
                f.write(h)
            png = os.path.join(OUT, f'antihero-logo-on-{bg}_{tag}.png')
            r.png(hp, png, W, H)
    # PNGs of photographic backgrounds are heavy - convert to high-quality JPG
    from PIL import Image
    for fn in os.listdir(OUT):
        if fn.endswith('.png'):
            p = os.path.join(OUT, fn)
            Image.open(p).convert('RGB').save(p[:-4] + '.jpg', quality=92, subsampling=0, optimize=True)
            os.remove(p)
    print('rendered', len(jobs))
