"""Construction + clear-space drawings, colour files (ASE/CSS/JSON/GPL/PNG), font package + specimen."""
import json
import math
import os
import shutil
import struct

from brand import C, KIT, MASTER, A_PATH, HERO_PATH, FONTS, font_face_css, mark_group
from render import Renderer, file_url

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, 'templates')
os.makedirs(TPL, exist_ok=True)

PALETTE = [
    # key, name, hex, role, pantone suggestion
    ('void', 'Anti Black', C['void'], 'Primary ground. Most layouts start here.', 'Black 6 C'),
    ('carbon', 'Carbon', C['carbon'], 'The badge disc (from the original logo). Cards, panels.', '419 C'),
    ('graphite', 'Graphite', C['graphite'], 'Raised surfaces, dividers on dark.', '432 C'),
    ('ash', 'Ash', C['ash'], 'Secondary text, hairlines, captions.', 'Cool Gray 8 C'),
    ('bone', 'Bone', C['bone'], 'Warm paper white for light layouts and print.', 'Warm Gray 1 C (tint)'),
    ('white', 'Hero White', C['white'], 'The mark, label boxes, headlines on dark.', '-'),
    ('ignition', 'Ignition Red', C['ignition'], 'The one accent. CTAs, the word HERO, one idea per layout.', '485 C'),
    ('ember', 'Ember', C['ember'], 'Pressed / hover state of Ignition. Never as a fill on its own.', '7621 C'),
    ('dusk', 'Dusk', C['dusk'], 'Photo duotone midtone (from the original sunset channel art).', '7531 C'),
]


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_cmyk(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k >= 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return tuple(round(v * 100) for v in (c, m, y, k))


def rel_lum(hexv):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(hexv)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def write_color_files(out):
    os.makedirs(out, exist_ok=True)
    # ASE (Adobe Swatch Exchange) - Illustrator / Photoshop / InDesign / Affinity
    blocks = []

    def ase_str(s):
        s = s + '\0'
        return struct.pack('>H', len(s)) + s.encode('utf-16-be')

    grp = ase_str('AntiHero')
    blocks.append(struct.pack('>HI', 0xC001, len(grp)) + grp)
    for key, name, hx, role, _ in PALETTE:
        r, g, b = hex_to_rgb(hx)
        body = ase_str(f'AntiHero {name}') + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 0)
        blocks.append(struct.pack('>HI', 0x0001, len(body)) + body)
    blocks.append(struct.pack('>HI', 0xC002, 0))
    with open(os.path.join(out, 'antihero-palette.ase'), 'wb') as f:
        f.write(b'ASEF' + struct.pack('>HHI', 1, 0, len(blocks)) + b''.join(blocks))
    # GIMP / Inkscape / Krita palette
    with open(os.path.join(out, 'antihero-palette.gpl'), 'w') as f:
        f.write('GIMP Palette\nName: AntiHero\nColumns: 3\n#\n')
        for key, name, hx, *_ in PALETTE:
            r, g, b = hex_to_rgb(hx)
            f.write(f'{r:3d} {g:3d} {b:3d}\t{name} {hx.upper()}\n')
    # CSS custom properties
    css = [':root {'] + [f'  --ah-{key}: {hx.upper()};  /* {name} - {role} */' for key, name, hx, role, _ in PALETTE]
    css += ['',
            "  --ah-font-display: 'Bebas Neue', 'Oswald', 'Arial Narrow', sans-serif;",
            "  --ah-font-body: 'Barlow', 'Helvetica Neue', Arial, sans-serif;",
            "  --ah-font-condensed: 'Barlow Condensed', 'Arial Narrow', sans-serif;",
            "  --ah-font-mono: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;",
            '}']
    with open(os.path.join(out, 'antihero-palette.css'), 'w') as f:
        f.write('/* AntiHero brand tokens */\n' + '\n'.join(css) + '\n')
    # JSON design tokens (W3C draft format)
    tokens = {'color': {key: {'$value': hx.upper(), '$type': 'color', '$description': f'{name}. {role}'} for key, name, hx, role, _ in PALETTE},
              'font': {'display': {'$value': 'Bebas Neue', '$type': 'fontFamily'}, 'body': {'$value': 'Barlow', '$type': 'fontFamily'},
                       'condensed': {'$value': 'Barlow Condensed', '$type': 'fontFamily'}, 'mono': {'$value': 'JetBrains Mono', '$type': 'fontFamily'}}}
    with open(os.path.join(out, 'antihero-tokens.json'), 'w') as f:
        json.dump(tokens, f, indent=2)
    # human-readable reference
    rows = []
    for key, name, hx, role, pms in PALETTE:
        r, g, b = hex_to_rgb(hx)
        cm = rgb_to_cmyk(r, g, b)
        rows.append({'name': name, 'hex': hx.upper(), 'rgb': f'{r} {g} {b}', 'cmyk': ' '.join(map(str, cm)),
                     'pantone': pms, 'on_white': round(contrast(hx, '#FFFFFF'), 2), 'on_black': round(contrast(hx, C['void']), 2), 'role': role})
    with open(os.path.join(out, 'antihero-palette.txt'), 'w', encoding='utf-8') as f:
        f.write('ANTIHERO PALETTE\n================\nCMYK values are straight conversions - let your printer convert from RGB with their profile.\n'
                'Pantone values are nearest-match suggestions: confirm against a physical swatch book before any print run.\n\n')
        for rw in rows:
            f.write(f"{rw['name']:<13} {rw['hex']}   RGB {rw['rgb']:<12} CMYK {rw['cmyk']:<14} PMS {rw['pantone']:<14} "
                    f"contrast vs white {rw['on_white']}:1 / vs Anti Black {rw['on_black']}:1\n    {rw['role']}\n")
    return rows


def swatch_card_html(rows):
    cards = []
    for rw, (key, name, hx, role, _) in zip(rows, PALETTE):
        ink = '#0A0A0B' if rel_lum(hx) > 0.35 else '#FFFFFF'
        cards.append(f"""<div class="sw" style="background:{hx};color:{ink}"><div class="n">{name.upper()}</div>
<div class="v">{hx.upper()}<br>RGB {rw['rgb']}<br>CMYK {rw['cmyk']}<br>PMS {rw['pantone']}</div></div>""")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_face_css(os.path.relpath(FONTS, TPL).replace(os.sep, '/'))}
*{{margin:0;box-sizing:border-box}}body{{width:2400px;height:1350px;background:#0A0A0B;padding:90px;font-family:'Barlow'}}
h1{{font-family:'Bebas Neue';font-weight:400;font-size:120px;color:#fff;line-height:1}}
.g{{display:grid;grid-template-columns:repeat(9,1fr);gap:0;margin-top:60px;height:960px}}
.sw{{padding:34px 26px;display:flex;flex-direction:column;justify-content:space-between;outline:1px solid rgba(255,255,255,.08)}}
.n{{font-family:'Bebas Neue';font-size:54px;line-height:.95}}.v{{font-family:'JetBrains Mono';font-size:21px;line-height:1.6;opacity:.92}}
.sw:nth-child(7){{grid-column:span 1}}</style></head><body><h1>ANTIHERO / COLOR</h1><div class="g">{''.join(cards)}</div></body></html>"""


def construction_svg():
    g = MASTER
    ro, ri, cut, ang = g['ring_outer'], g['ring_inner'], g['cut_x'], g['diag_angle_deg']
    t = g['stroke']
    a = math.radians(ang)
    # diagonal centre-line through (cut, 200) leaning 24.71deg
    x0, y0 = cut, 200.0
    dx, dy = -math.sin(a), math.cos(a)
    L1 = (x0 - dx * 260, y0 - dy * 260)
    L2 = (x0 + dx * 900, y0 + dy * 900)
    red = C['ignition']
    ash = '#8A9096'
    mono = "font-family:'JetBrains Mono',monospace"
    lines = f"""
<rect x="-300" y="-300" width="1600" height="1600" fill="{C['carbon']}"/>
<g stroke="{ash}" stroke-opacity=".28" stroke-width="1">{''.join(f'<line x1="{i}" y1="-300" x2="{i}" y2="1300"/><line x1="-300" y1="{i}" x2="1300" y2="{i}"/>' for i in range(-300, 1301, 50))}</g>
<circle cx="500" cy="500" r="500" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<g fill="#fff" fill-opacity=".10" stroke="#fff" stroke-width="2.2">{mark_group('#ffffff').replace('fill="#ffffff"', '')}</g>
<g fill="none" stroke="{red}" stroke-width="2" stroke-dasharray="10 8">
 <circle cx="500" cy="500" r="{ro:.1f}"/><circle cx="500" cy="500" r="{ri:.1f}"/>
 <line x1="{cut:.1f}" y1="-60" x2="{cut:.1f}" y2="1060"/>
 <line x1="{L1[0]:.1f}" y1="{L1[1]:.1f}" x2="{L2[0]:.1f}" y2="{L2[1]:.1f}"/>
 <line x1="60" y1="{500 - 7.2:.1f}" x2="560" y2="{500 - 7.2:.1f}"/><line x1="60" y1="{500 - 7.2 + t:.1f}" x2="560" y2="{500 - 7.2 + t:.1f}"/>
 <line x1="530" y1="60" x2="530" y2="940"/><line x1="745" y1="60" x2="745" y2="940"/>
</g>
<line x1="500" y1="500" x2="{500 + ro * math.cos(math.radians(150)):.1f}" y2="{500 - ro * math.sin(math.radians(150)):.1f}" stroke="#fff" stroke-width="2"/>
<circle cx="500" cy="500" r="5" fill="#fff"/>
<path d="M{x0:.1f} {y0 + 120:.1f} A120 120 0 0 1 {x0 + dx * 120:.1f} {y0 + dy * 120:.1f}" fill="none" stroke="#fff" stroke-width="2"/>
<g style="{mono}" font-size="19" fill="#fff">
 <text x="{x0 - 150:.1f}" y="{y0 + 175:.1f}">{ang:.1f}&#176;</text>
 <text x="215" y="318" transform="rotate(-30 215 318)">r = {ro / 500:.3f} R</text>
 <text x="{cut + 12:.1f}" y="-30">cut x = {(cut - 500) / 500:+.3f} R</text>
 <text x="70" y="{500 - 16:.1f}">bar top</text>
 <text x="70" y="{500 - 7.2 + t + 30:.1f}">bar bottom  (t)</text>
 <text x="536" y="990">baseline</text><text x="751" y="990">x-height</text>
 <text x="-250" y="-240" font-size="24">ANTIHERO MARK / CONSTRUCTION</text>
 <text x="-250" y="-205" fill="{ash}">R = disc radius &#183; every stroke t = {t / 500:.3f} R &#183; ring r = {ro / 500:.3f} R / {ri / 500:.3f} R</text>
 <text x="-250" y="1255" fill="{ash}">diagonal {ang:.2f}&#176; from vertical &#183; its axis meets the cut at the inner ring &#183; lettering is custom (traced + rebuilt)</text>
</g>"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 1600 1600">{lines}</svg>'


def clearspace_svg():
    ash = '#8A9096'
    red = C['ignition']
    x = 250  # clear space = 1/4 of the badge diameter
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="-400 -400 1800 1800">
<rect x="-400" y="-400" width="1800" height="1800" fill="{C['bone']}"/>
<rect x="-{x}" y="-{x}" width="{1000 + 2 * x}" height="{1000 + 2 * x}" fill="none" stroke="{red}" stroke-width="3" stroke-dasharray="14 10"/>
<rect x="0" y="0" width="1000" height="1000" fill="none" stroke="{ash}" stroke-width="2"/>
<circle cx="500" cy="500" r="500" fill="{C['carbon']}"/>{mark_group('#ffffff')}
<g fill="{red}" opacity=".18"><rect x="-{x}" y="-{x}" width="{1000 + 2 * x}" height="{x}"/><rect x="-{x}" y="1000" width="{1000 + 2 * x}" height="{x}"/>
<rect x="-{x}" y="0" width="{x}" height="1000"/><rect x="1000" y="0" width="{x}" height="1000"/></g>
<g font-family="'JetBrains Mono',monospace" font-size="30" fill="{C['void']}">
<text x="-{x - 20}" y="-{x + 30}">CLEAR SPACE = 1/4 OF THE BADGE DIAMETER (the "quarter")</text>
<text x="-{x - 20}" y="{1000 + x + 60}">MINIMUM SIZE: badge 24 px on screen / 0.4 in (10 mm) in print</text>
<text x="-{x - 20}" y="{1000 + x + 100}">Below 32 px use the favicon files (tuned for small sizes)</text></g></svg>"""


def type_specimen_html():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_face_css(os.path.relpath(FONTS, TPL).replace(os.sep, '/'))}
*{{margin:0;box-sizing:border-box}}body{{width:2400px;height:1180px;background:#0A0A0B;color:#fff;padding:70px 100px;font-family:'Barlow'}}
.row{{display:grid;grid-template-columns:420px 1fr;gap:60px;padding:46px 0;border-top:1px solid rgba(255,255,255,.14)}}
.k{{font-family:'JetBrains Mono';font-size:22px;color:#8A9096;line-height:1.7}}.k b{{color:#fff;font-weight:700;font-size:26px}}
.d{{font-family:'Bebas Neue';font-size:200px;line-height:.9}}.d span{{color:{C['ignition']}}}
.b{{font-size:44px;line-height:1.35;max-width:1500px}}.b strong{{font-weight:700}}
.c{{font-family:'Barlow Condensed';font-weight:700;font-size:64px;letter-spacing:.2em}}
.m{{font-family:'JetBrains Mono';font-size:40px;color:#e9e9e9}}.m b{{color:{C['ignition']}}}</style></head><body>
<div class="row"><div class="k"><b>BEBAS NEUE</b><br>Display &middot; headlines<br>always uppercase<br>tracking 0 to +2%</div><div class="d">BE YOUR OWN <span>HERO.</span></div></div>
<div class="row"><div class="k"><b>BARLOW</b><br>Body &middot; 400 / 500 / 700<br>line-height 1.35-1.5</div><div class="b">Nobody is coming to save your business. <strong>Good.</strong> AI gives one person the reach of a small team: you just have to learn the tools and show up every day.</div></div>
<div class="row"><div class="k"><b>BARLOW CONDENSED</b><br>Labels &middot; eyebrows<br>700, tracking +20-30%</div><div class="c">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</div></div>
<div class="row"><div class="k"><b>JETBRAINS MONO</b><br>Prompts &middot; tools &middot; data<br>400 / 700</div><div class="m"><b>&gt;</b> Write 5 Google Business Profile posts for my shop in Edmonton.</div></div>
</body></html>"""


if __name__ == '__main__':
    col = os.path.join(KIT, '07_Color')
    rows = write_color_files(col)
    cons_dir = os.path.join(KIT, '02_Logos', '06_Construction')
    os.makedirs(cons_dir, exist_ok=True)
    jobs = []
    for name, svg, w, h in [('antihero-construction', construction_svg(), 2400, 2400), ('antihero-clearspace', clearspace_svg(), 2400, 2400)]:
        with open(os.path.join(cons_dir, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)
        hp = os.path.join(TPL, name + '.html')
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(f"<!doctype html><html><head><style>{font_face_css(os.path.relpath(FONTS, TPL).replace(os.sep, '/'))}*{{margin:0}}svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg}</body></html>")
        jobs.append((hp, os.path.join(cons_dir, name + f'_{w}px.png'), w, h))
    hp = os.path.join(TPL, 'antihero-palette-card.html')
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(swatch_card_html(rows))
    jobs.append((hp, os.path.join(col, 'antihero-palette-card_2400x1350.png'), 2400, 1350))
    # fonts
    fdir = os.path.join(KIT, '06_Fonts')
    for sub, files in {
        'Bebas Neue (display)': ['bebasneue__BebasNeue-Regular.ttf', 'bebasneue__OFL.txt'],
        'Barlow (body)': [f for f in os.listdir(FONTS) if f.startswith('barlow__')],
        'Barlow Condensed (labels)': [f for f in os.listdir(FONTS) if f.startswith('barlowcondensed__')] + ['barlow__OFL.txt'],
        'JetBrains Mono (prompts + data)': ['JetBrainsMono-Regular.ttf', 'JetBrainsMono-Bold.ttf', 'jetbrainsmono__OFL.txt'],
    }.items():
        d = os.path.join(fdir, sub)
        os.makedirs(d, exist_ok=True)
        for fn in files:
            dst = fn.split('__', 1)[-1]
            if dst == 'OFL.txt':
                dst = 'OFL-license.txt'
            shutil.copy2(os.path.join(FONTS, fn), os.path.join(d, dst))
    hp = os.path.join(TPL, 'antihero-type-specimen.html')
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(type_specimen_html())
    jobs.append((hp, os.path.join(fdir, 'antihero-type-specimen_2400x1180.png'), 2400, 1180))
    with Renderer() as r:
        for hp, png, w, h in jobs:
            r.png(hp, png, w, h)
    for rw in rows:
        print(f"{rw['name']:<13} {rw['hex']} on white {rw['on_white']}  on black {rw['on_black']}")

