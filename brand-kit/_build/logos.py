"""Generate the AntiHero logo system: badges, marks, wordmarks, lockups, icons (SVG + PNG)."""
import os

from PIL import Image

from brand import (C, KIT, A_PATH, HERO_PATH, MARK_BBOX, HERO_UP, HERO_UP_W,
                   FontOutline, hero_upright_group, mark_group, text_path)
from render import Renderer, file_url

OUT = os.path.join(KIT, '02_Logos')
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'wrap')
os.makedirs(TMP, exist_ok=True)

CIRCLE_D = 'M0 500a500 500 0 1 0 1000 0a500 500 0 1 0-1000 0Z'
JOBS = []   # (svg_path, png_path, w, h, bg or None)


def save_svg(rel, svg, pngs=(), bg=None, aspect=None):
    path = os.path.join(OUT, rel + '.svg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg)
    for w in pngs:
        h = round(w / aspect) if aspect else w
        JOBS.append((path, os.path.join(OUT, rel + f'_{w}px.png'), w, h, bg))
    return path


def svg_doc(vb, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>')


# ---------------------------------------------------------------------------
# 01 Badge (primary logo)
# ---------------------------------------------------------------------------
BIG = (8192, 4096, 2048, 1024, 512, 256)
STD = (4096, 2048, 1024, 512)
badges = [
    ('carbon', C['carbon'], C['white'], BIG, 'Primary. The original badge, rebuilt.'),
    ('black', C['void'], C['white'], STD, ''),
    ('ignition', C['ignition'], C['white'], STD, ''),
    ('white', C['white'], C['void'], STD, ''),
    ('bone', C['bone'], C['carbon'], STD, ''),
]
for name, disc, mark, sizes, _ in badges:
    body = f'<circle cx="500" cy="500" r="500" fill="{disc}"/>' + mark_group(mark)
    save_svg(f'01_Badge/antihero-badge-{name}', svg_doc('0 0 1000 1000', body, 'AntiHero'), sizes)

# outline badge for photos: ring + mark, no fill
for name, col in [('white', C['white']), ('black', C['void'])]:
    body = f'<circle cx="500" cy="500" r="488" fill="none" stroke="{col}" stroke-width="24"/>' + mark_group(col)
    save_svg(f'01_Badge/antihero-badge-outline-{name}', svg_doc('0 0 1000 1000', body, 'AntiHero'), STD)

# knockout: one compound path (disc minus mark) - letters are truly transparent
for name, col in [('carbon', C['carbon']), ('white', C['white']), ('ignition', C['ignition']), ('black', C['void'])]:
    body = f'<path fill="{col}" fill-rule="evenodd" d="{CIRCLE_D}{A_PATH}{HERO_PATH}"/>'
    save_svg(f'01_Badge/antihero-badge-knockout-{name}', svg_doc('0 0 1000 1000', body, 'AntiHero'), STD)

# ---------------------------------------------------------------------------
# 02 Mark only (no disc)
# ---------------------------------------------------------------------------
x0, y0, x1, y1 = MARK_BBOX
pad = 12
mvb = f'{x0 - pad:.1f} {y0 - pad:.1f} {x1 - x0 + 2 * pad:.1f} {y1 - y0 + 2 * pad:.1f}'
mark_aspect = (x1 - x0 + 2 * pad) / (y1 - y0 + 2 * pad)
for name, col, sizes in [('white', C['white'], BIG), ('black', C['void'], BIG), ('carbon', C['carbon'], STD),
                         ('ignition', C['ignition'], STD), ('bone', C['bone'], STD)]:
    save_svg(f'02_Mark/antihero-mark-{name}', svg_doc(mvb, mark_group(col), 'AntiHero mark'), sizes, aspect=mark_aspect)
# two-tone: A in white, hero in ignition (and reverse) - accent use
save_svg('02_Mark/antihero-mark-duo-white-ignition', svg_doc(mvb, mark_group(C['white'], C['ignition']), 'AntiHero mark'), STD, aspect=mark_aspect)
save_svg('02_Mark/antihero-mark-duo-black-ignition', svg_doc(mvb, mark_group(C['void'], C['ignition']), 'AntiHero mark'), STD, aspect=mark_aspect)

# ---------------------------------------------------------------------------
# 03 Wordmarks
# ---------------------------------------------------------------------------
CAP_RATIO, GAP = 0.86, 40
asc = HERO_UP['ascender']
cap = asc * CAP_RATIO
fo = FontOutline('bebas')
bsize = cap / (fo.cap / fo.upm)


def script_wordmark(col_anti, col_hero, x=0.0, base=0.0):
    anti, w = text_path('bebas', 'ANTI', bsize, x, base, col_anti, tracking=0.01)
    hero = hero_upright_group(col_hero, x + w + GAP, base)
    return anti + hero, w + GAP + HERO_UP_W


# bounds: top = base - asc (h ascender), bottom = base + 12 (h terminal dips a hair), left 0
wm_body, wm_w = script_wordmark('#000', '#000')
WM_TOP, WM_BOT = -asc - 4, HERO_UP['descent'] + 10
wpad = 30
wm_vb = f'{-wpad} {WM_TOP - wpad:.1f} {wm_w + 2 * wpad:.1f} {WM_BOT - WM_TOP + 2 * wpad:.1f}'
wm_aspect = (wm_w + 2 * wpad) / (WM_BOT - WM_TOP + 2 * wpad)
for name, ca, ch in [('white', C['white'], C['white']), ('black', C['void'], C['void']),
                     ('white-ignition', C['white'], C['ignition']), ('black-ignition', C['void'], C['ignition']),
                     ('carbon', C['carbon'], C['carbon'])]:
    body, _ = script_wordmark(ca, ch)
    save_svg(f'03_Wordmark/antihero-wordmark-{name}', svg_doc(wm_vb, body, 'AntiHero'), (4096, 2048, 1024), aspect=wm_aspect)

# all-caps typographic wordmark
for name, col in [('white', C['white']), ('black', C['void'])]:
    t, w = text_path('bebas', 'ANTIHERO', 400, 0, 0, col, tracking=0.04)
    capH = fo.cap_height(400)
    vb = f'-20 {-capH - 20:.1f} {w + 40:.1f} {capH + 40:.1f}'
    save_svg(f'03_Wordmark/antihero-wordmark-caps-{name}', svg_doc(vb, t, 'AntiHero'), (4096, 2048, 1024), aspect=(w + 40) / (capH + 40))

# heritage label box (as on the original channel art): text on a solid box
for name, box, ink in [('white', C['white'], C['void']), ('black', C['void'], C['white']), ('ignition', C['ignition'], C['white'])]:
    size = 400
    capH = fo.cap_height(size)
    t, w = text_path('bebas', 'ANTIHERO', size, 0, 0, ink, tracking=0.035)
    px, py = 0.16 * capH, 0.20 * capH
    rect = f'<rect x="{-px:.1f}" y="{-capH - py:.1f}" width="{w + 2 * px:.1f}" height="{capH + 2 * py:.1f}" fill="{box}"/>'
    vb = f'{-px:.1f} {-capH - py:.1f} {w + 2 * px:.1f} {capH + 2 * py:.1f}'
    save_svg(f'03_Wordmark/antihero-wordmark-label-{name}', svg_doc(vb, rect + t, 'AntiHero'), (4096, 2048, 1024), aspect=(w + 2 * px) / (capH + 2 * py))

# ---------------------------------------------------------------------------
# 04 Lockups
# ---------------------------------------------------------------------------
DESC = 'AI & ENTREPRENEURSHIP'
TAG = 'BE YOUR OWN HERO'


def sized_to(font, text, target_w, tracking):
    """Font size at which `text` (with tracking) spans exactly target_w."""
    w100 = FontOutline(font).width(text, 100, tracking)
    return 100 * target_w / w100


def horizontal(ink, disc, mark_col, hero_col=None):
    scale = 0.96                        # wordmark ascender ~ 1/3 of the badge height
    parts = [f'<circle cx="500" cy="500" r="500" fill="{disc}"/>', mark_group(mark_col)]
    wx = 1000 + 120
    wm, w = script_wordmark(ink, hero_col or ink, 0, 0)
    wmw = w * scale
    dfont, dtrack = 'barlowc-bold', 0.22
    dsize = sized_to(dfont, DESC, wmw * 0.985, dtrack)
    dcap = FontOutline(dfont).cap_height(dsize)
    gap2 = 0.20 * asc * scale
    block = asc * scale + gap2 + dcap          # ascender top -> descriptor baseline
    base = 500 - block / 2 + asc * scale
    parts.append(f'<g transform="translate({wx},{base:.1f}) scale({scale})">{wm}</g>')
    dp, dw = text_path(dfont, DESC, dsize, wx + 4, base + gap2 + dcap, ink, tracking=dtrack)
    parts.append(dp)
    width = wx + max(wmw, dw) + 10
    return ''.join(parts), width


def stacked(ink, disc, mark_col, hero_col=None, rule=None):
    rule = rule or ink
    parts = [f'<circle cx="500" cy="500" r="500" fill="{disc}"/>', mark_group(mark_col)]
    scale = 0.74
    wm, w = script_wordmark(ink, hero_col or ink, 0, 0)
    wmw = w * scale
    wx = 500 - wmw / 2
    base = 1000 + 110 + asc * scale
    parts.append(f'<g transform="translate({wx:.1f},{base:.1f}) scale({scale})">{wm}</g>')
    tfont, ttrack = 'barlowc-bold', 0.30
    tsize = sized_to(tfont, TAG, wmw * 0.60, ttrack)
    tcap = FontOutline(tfont).cap_height(tsize)
    ty = base + 70 + tcap
    # optical centring: tracking leaves one trailing track - shift left by half of it
    tp, tw = text_path(tfont, TAG, tsize, 500, ty, ink, tracking=ttrack, anchor='middle')
    parts.append(tp)
    rl, g = wmw * 0.13, wmw * 0.045
    yl = ty - tcap / 2
    rh = max(4.0, tcap * 0.09)
    parts.append(f'<rect x="{500 - tw / 2 - g - rl:.1f}" y="{yl - rh / 2:.1f}" width="{rl:.1f}" height="{rh:.1f}" fill="{rule}"/>')
    parts.append(f'<rect x="{500 + tw / 2 + g:.1f}" y="{yl - rh / 2:.1f}" width="{rl:.1f}" height="{rh:.1f}" fill="{rule}"/>')
    left = min(0, wx, 500 - tw / 2 - g - rl)
    right = max(1000, wx + wmw, 500 + tw / 2 + g + rl)
    return ''.join(parts), left, right, ty + 12


for name, ink, disc, mk, hc in [('on-dark', C['white'], C['carbon'], C['white'], None),
                                 ('on-light', C['void'], C['carbon'], C['white'], None),
                                 ('on-dark-ignition', C['white'], C['carbon'], C['white'], C['ignition']),
                                 ('on-light-ignition', C['void'], C['void'], C['white'], C['ignition'])]:
    body, width = horizontal(ink, disc, mk, hc)
    vb = f'-20 -20 {width + 40:.1f} 1040'
    save_svg(f'04_Lockups/antihero-lockup-horizontal-{name}', svg_doc(vb, body, 'AntiHero'), (4096, 2048, 1024), aspect=(width + 40) / 1040)
    body, l, r, b = stacked(ink, disc, mk, hc)
    vb = f'{l - 20:.1f} -20 {r - l + 40:.1f} {b + 40:.1f}'
    save_svg(f'04_Lockups/antihero-lockup-stacked-{name}', svg_doc(vb, body, 'AntiHero'), (3000, 1500), aspect=(r - l + 40) / (b + 40))

# tagline lockup (flanking rules - lifted from the original channel art)
for name, ink in [('white', C['white']), ('black', C['void']), ('ignition', C['ignition'])]:
    tsize = 120
    tp, tw = text_path('bebas', TAG, tsize, 0, 0, ink, tracking=0.12)
    rl, g = 260, 60
    capH = fo.cap_height(tsize)
    yl = -capH / 2
    body = (f'<rect x="{-g - rl}" y="{yl - 4:.1f}" width="{rl}" height="8" fill="{ink}"/>' + tp +
            f'<rect x="{tw + g:.1f}" y="{yl - 4:.1f}" width="{rl}" height="8" fill="{ink}"/>')
    vb = f'{-g - rl - 10} {-capH - 20:.1f} {tw + 2 * (g + rl) + 20:.1f} {capH + 40:.1f}'
    save_svg(f'04_Lockups/antihero-tagline-{name}', svg_doc(vb, body, 'Be your own hero'), (3000, 1500),
             aspect=(tw + 2 * (g + rl) + 20) / (capH + 40))

# ---------------------------------------------------------------------------
# 05 Icons (favicon, app icons, avatars)
# ---------------------------------------------------------------------------
# square app icon: carbon field, mark centred at ~74% width
cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2


def square_icon(bg, col, frac=0.74, rounded=0):
    s = frac * 1000 / (x1 - x0)
    tx, ty = 500 - cxm * s, 500 - cym * s
    rect = f'<rect width="1000" height="1000" rx="{rounded}" fill="{bg}"/>'
    return rect + f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">{mark_group(col)}</g>'


save_svg('05_Icons/antihero-app-icon', svg_doc('0 0 1000 1000', square_icon(C['carbon'], C['white']), 'AntiHero'), (1024, 512, 180))
save_svg('05_Icons/antihero-app-icon-rounded', svg_doc('0 0 1000 1000', square_icon(C['carbon'], C['white'], rounded=225), 'AntiHero'), (1024, 512))
save_svg('05_Icons/antihero-app-icon-ignition', svg_doc('0 0 1000 1000', square_icon(C['ignition'], C['white']), 'AntiHero'), (1024, 512))
save_svg('05_Icons/antihero-maskable-icon', svg_doc('0 0 1000 1000', square_icon(C['carbon'], C['white'], frac=0.60), 'AntiHero'), (512, 192))

if __name__ == '__main__':
    with Renderer() as r:
        for svg_path, png, w, h, bg in JOBS:
            wrap = os.path.join(TMP, os.path.basename(png) + '.html')
            bgcss = bg or 'transparent'
            with open(wrap, 'w', encoding='utf-8') as f:
                f.write(f'<html><body style="margin:0;background:{bgcss}"><img src="{file_url(svg_path)}" '
                        f'style="display:block;width:{w}px;height:{h}px"></body></html>')
            r.png(wrap, png, w, h, transparent=bg is None)
    # favicons from the badge (small sizes rendered directly, then packed into .ico)
    with Renderer() as r:
        src = os.path.join(OUT, '01_Badge', 'antihero-badge-carbon.svg')
        for s in (16, 32, 48, 64, 180, 192, 512):
            wrap = os.path.join(TMP, f'fav{s}.html')
            with open(wrap, 'w') as f:
                f.write(f'<html><body style="margin:0;background:transparent"><img src="{file_url(src)}" style="display:block;width:{s}px;height:{s}px"></body></html>')
            r.png(wrap, os.path.join(OUT, '05_Icons', f'favicon-{s}.png'), s, s, transparent=True)
    ims = [Image.open(os.path.join(OUT, '05_Icons', f'favicon-{s}.png')).convert('RGBA') for s in (64, 48, 32, 16)]
    ims[0].save(os.path.join(OUT, '05_Icons', 'favicon.ico'), format='ICO',
                sizes=[(64, 64), (48, 48), (32, 32), (16, 16)], append_images=ims[1:])
    print('rendered', len(JOBS), 'PNGs')
