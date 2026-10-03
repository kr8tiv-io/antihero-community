"""AntiHero brand constants + SVG building blocks shared by every generator."""
import json
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, 'fonts')
MASTER = json.load(open(os.path.join(HERE, 'master', 'antihero-mark-paths.json')))
A_PATH = MASTER['a_path']
HERO_PATH = MASTER['hero_path']

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
C = {
    'void':     '#0A0A0B',   # Anti Black - primary ground
    'carbon':   '#1D2124',   # the original badge disc (heritage)
    'graphite': '#2B3035',   # raised surfaces
    'ash':      '#8A9096',   # secondary text, hairlines
    'bone':     '#ECE8E1',   # warm paper white
    'white':    '#FFFFFF',   # Hero White - the mark, label boxes
    'ignition': '#E0261E',   # Ignition Red - the one accent (white text on it passes WCAG AA, 4.7:1)
    'ember':    '#A3160F',   # accent pressed/dark
    'dusk':     '#5B4F48',   # heritage sepia (photo duotone mid)
}

FONT_FILES = {
    'bebas': os.path.join(FONTS, 'bebasneue__BebasNeue-Regular.ttf'),
    'barlow': os.path.join(FONTS, 'barlow__Barlow-Regular.ttf'),
    'barlow-medium': os.path.join(FONTS, 'barlow__Barlow-Medium.ttf'),
    'barlow-semibold': os.path.join(FONTS, 'barlow__Barlow-SemiBold.ttf'),
    'barlow-bold': os.path.join(FONTS, 'barlow__Barlow-Bold.ttf'),
    'barlow-black': os.path.join(FONTS, 'barlow__Barlow-Black.ttf'),
    'barlowc-semibold': os.path.join(FONTS, 'barlowcondensed__BarlowCondensed-SemiBold.ttf'),
    'barlowc-bold': os.path.join(FONTS, 'barlowcondensed__BarlowCondensed-Bold.ttf'),
    'barlowc-extrabold': os.path.join(FONTS, 'barlowcondensed__BarlowCondensed-ExtraBold.ttf'),
    'mono': os.path.join(FONTS, 'JetBrainsMono-Regular.ttf'),
    'mono-bold': os.path.join(FONTS, 'JetBrainsMono-Bold.ttf'),
}

# ---------------------------------------------------------------------------
# Mark geometry (1000-unit artboard, disc r=500 centred at 500,500)
# ---------------------------------------------------------------------------
MARK_BBOX = (126.6, 125.9, 886.4, 873.4)     # A ring left edge .. hero ascender, ring top .. ring bottom
# upright "hero" lettering (rotate -90): baseline / x-height / ascender measured in badge units
HERO_UP = {'x0': 125.9, 'x1': 862.9, 'baseline_badge_x': 530.0, 'xheight': 215.0, 'ascender': 356.4, 'descent': 5.3}


def mark_group(fill_a='#FFFFFF', fill_hero=None):
    fill_hero = fill_hero or fill_a
    return (f'<path fill="{fill_a}" fill-rule="evenodd" d="{A_PATH}"/>'
            f'<path fill="{fill_hero}" fill-rule="evenodd" d="{HERO_PATH}"/>')


def badge_svg(disc='#1D2124', mark='#FFFFFF', size=None, ring=None, ring_w=10, knockout=False, pad=0, title='AntiHero'):
    """Round badge. knockout=True cuts the mark out of the disc (transparent letters)."""
    s = f' width="{size}" height="{size}"' if size else ''
    vb = f'{-pad} {-pad} {1000 + 2 * pad} {1000 + 2 * pad}'
    body = []
    if knockout:
        body.append(f'<defs><mask id="ko"><rect x="-10" y="-10" width="1020" height="1020" fill="#fff"/>'
                    f'{mark_group("#000")}</mask></defs>'
                    f'<circle cx="500" cy="500" r="500" fill="{disc}" mask="url(#ko)"/>')
    else:
        if disc:
            body.append(f'<circle cx="500" cy="500" r="500" fill="{disc}"/>')
        if ring:
            body.append(f'<circle cx="500" cy="500" r="{500 - ring_w / 2}" fill="none" stroke="{ring}" stroke-width="{ring_w}"/>')
        body.append(mark_group(mark))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{s} role="img" aria-label="{title}">'
            f'<title>{title}</title>' + ''.join(body) + '</svg>')


def mark_svg(color='#FFFFFF', size=None, pad=20, title='AntiHero mark'):
    """The mark alone (no disc), cropped to its own bounds."""
    x0, y0, x1, y1 = MARK_BBOX
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    s = f' width="{size}" height="{round(size * h / w)}"' if size else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - pad:.1f} {y0 - pad:.1f} {w:.1f} {h:.1f}"{s} role="img" aria-label="{title}">'
            f'<title>{title}</title>{mark_group(color)}</svg>')


def hero_upright_group(color, x, baseline, scale=1.0):
    """The lettering rotated upright. (x, baseline) = where the upright word's left edge / baseline land."""
    # rotate(-90): (bx, by) -> (by, -bx).  Upright left edge = HERO_UP.x0, baseline = -baseline_badge_x
    tx = x - HERO_UP['x0'] * scale
    ty = baseline + HERO_UP['baseline_badge_x'] * scale
    return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({scale:.5f}) rotate(-90)">'
            f'<path fill="{color}" fill-rule="evenodd" d="{HERO_PATH}"/></g>')


HERO_UP_W = HERO_UP['x1'] - HERO_UP['x0']


# ---------------------------------------------------------------------------
# Text -> outlines (so SVG logos never depend on installed fonts)
# ---------------------------------------------------------------------------
class FontOutline:
    _cache = {}

    def __new__(cls, key):
        if key not in cls._cache:
            o = super().__new__(cls)
            o._init(FONT_FILES[key])
            cls._cache[key] = o
        return cls._cache[key]

    def _init(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f['head'].unitsPerEm
        self.hmtx = self.f['hmtx']
        os2 = self.f['OS/2']
        self.cap = getattr(os2, 'sCapHeight', 0) or int(self.upm * 0.7)
        self.xh = getattr(os2, 'sxHeight', 0) or int(self.upm * 0.5)
        self._kern = self._build_kern()

    def _build_kern(self):
        subs = []
        if 'GPOS' in self.f:
            for lk in self.f['GPOS'].table.LookupList.Lookup:
                for st in lk.SubTable:
                    t = lk.LookupType
                    if t == 9:
                        t = st.ExtensionLookupType
                        st = st.ExtSubTable
                    if t == 2:
                        subs.append(st)
        return subs

    def kern(self, g1, g2):
        for st in self._kern:
            cov = st.Coverage.glyphs
            if g1 not in cov:
                continue
            if st.Format == 1:
                ps = st.PairSet[cov.index(g1)]
                for rec in ps.PairValueRecord:
                    if rec.SecondGlyph == g2:
                        return getattr(rec.Value1, 'XAdvance', 0) or 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(g1, 0)
                c2 = st.ClassDef2.classDefs.get(g2, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                v = getattr(rec.Value1, 'XAdvance', 0) or 0
                if v:
                    return v
        return 0

    def path(self, text, size, x=0.0, baseline=0.0, tracking=0.0):
        """Return (svg path d, advance width). tracking in em."""
        sc = size / self.upm
        cur = x
        out = []
        prev = None
        for ch in text:
            g = self.cmap.get(ord(ch), '.notdef')
            if prev is not None:
                cur += self.kern(prev, g) * sc
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cur, baseline)))
            out.append(pen.getCommands())
            cur += self.hmtx[g][0] * sc + tracking * size
            prev = g
        width = cur - x - (tracking * size if text else 0)
        return ' '.join(out), width

    def width(self, text, size, tracking=0.0):
        return self.path(text, size, tracking=tracking)[1]

    def cap_height(self, size):
        return self.cap * size / self.upm


def text_path(font, text, size, x, baseline, fill, tracking=0.0, anchor='start'):
    fo = FontOutline(font)
    w = fo.width(text, size, tracking)
    if anchor == 'middle':
        x -= w / 2
    elif anchor == 'end':
        x -= w
    d, _ = fo.path(text, size, x, baseline, tracking)
    return f'<path fill="{fill}" d="{d}"/>', w


def font_face_css(rel_prefix):
    """@font-face block for HTML templates; rel_prefix = path from the HTML file to _build/fonts."""
    faces = [
        ('Bebas Neue', 'bebasneue__BebasNeue-Regular.ttf', 400, 'normal'),
        ('Barlow', 'barlow__Barlow-Regular.ttf', 400, 'normal'),
        ('Barlow', 'barlow__Barlow-Italic.ttf', 400, 'italic'),
        ('Barlow', 'barlow__Barlow-Medium.ttf', 500, 'normal'),
        ('Barlow', 'barlow__Barlow-SemiBold.ttf', 600, 'normal'),
        ('Barlow', 'barlow__Barlow-Bold.ttf', 700, 'normal'),
        ('Barlow', 'barlow__Barlow-ExtraBold.ttf', 800, 'normal'),
        ('Barlow', 'barlow__Barlow-Black.ttf', 900, 'normal'),
        ('Barlow Condensed', 'barlowcondensed__BarlowCondensed-Medium.ttf', 500, 'normal'),
        ('Barlow Condensed', 'barlowcondensed__BarlowCondensed-SemiBold.ttf', 600, 'normal'),
        ('Barlow Condensed', 'barlowcondensed__BarlowCondensed-Bold.ttf', 700, 'normal'),
        ('Barlow Condensed', 'barlowcondensed__BarlowCondensed-ExtraBold.ttf', 800, 'normal'),
        ('Barlow Condensed', 'barlowcondensed__BarlowCondensed-Black.ttf', 900, 'normal'),
        ('JetBrains Mono', 'JetBrainsMono-Regular.ttf', 400, 'normal'),
        ('JetBrains Mono', 'JetBrainsMono-Bold.ttf', 700, 'normal'),
    ]
    return '\n'.join(
        f"@font-face{{font-family:'{fam}';src:url('{rel_prefix}/{fn}') format('truetype');font-weight:{w};font-style:{st};font-display:block}}"
        for fam, fn, w, st in faces)
