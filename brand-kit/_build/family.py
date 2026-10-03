"""The AntiHero family: AntiHero (learn it) + KR8TIV (design it) + KR8TIV AI (automate it). Lockups + endorsements."""
import os
import re

from brand import C, KIT, FontOutline, mark_group, text_path
from render import Renderer, file_url

OUT = os.path.join(KIT, '02_Logos', '07_Family')
os.makedirs(OUT, exist_ok=True)
KR_SRC = os.path.expandvars(r'%USERPROFILE%\Desktop\kr8tiv-io-v2-website\public\kr8tiv-assets\kr8tiv-logo-clean.svg')
svg_src = open(KR_SRC, encoding='utf-8').read()
KR_D = re.search(r' d="([^"]+)"', svg_src).group(1)
KR_VB = (104.5, 85.0, 1640.5, 402.0)          # x, y, w, h of the clean KR8TIV wordmark


def kr8tiv(x, y, height, fill):
    """KR8TIV wordmark placed with its top-left at (x, y), scaled to `height`."""
    s = height / KR_VB[3]
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f}) translate({-KR_VB[0]},{-KR_VB[1]})">'
            f'<path fill="{fill}" fill-rule="evenodd" d="{KR_D}"/></g>'), KR_VB[2] * s


def badge(x, y, size, disc=C['carbon'], mk='#fff'):
    s = size / 1000.0
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})"><circle cx="500" cy="500" r="500" fill="{disc}"/>'
            f'{mark_group(mk)}</g>')


def family_lockup(ink, disc, mk, rule):
    """Three columns, each: logo row (same cap height feel) + caption; hairline dividers."""
    parts = []
    H = 150                                    # logo row height
    cap_y = 250                                # caption baseline
    cap_font, cap_track = 'barlowc-bold', 0.30
    # col 1: badge + ANTIHERO
    parts.append(badge(0, 0, H, disc, mk))
    fo = FontOutline('bebas')
    size = 116 / (fo.cap / fo.upm)
    t, tw = text_path('bebas', 'ANTIHERO', size, H + 34, 75 + 58, ink, tracking=0.03)
    parts.append(t)
    c1w = H + 34 + tw
    cap, cw = text_path(cap_font, 'LEARN IT', 34, 0, cap_y, ink, tracking=cap_track)
    parts.append(cap)
    gap = 120
    x2 = c1w + gap
    parts.append(f'<rect x="{c1w + gap / 2 - 1.5:.1f}" y="-10" width="3" height="{cap_y + 20}" fill="{rule}"/>')
    # col 2: KR8TIV
    k, kw = kr8tiv(x2, 18, 114, ink)
    parts.append(k)
    cap, _ = text_path(cap_font, 'DESIGN IT', 34, x2, cap_y, ink, tracking=cap_track)
    parts.append(cap)
    x3 = x2 + kw + gap
    parts.append(f'<rect x="{x2 + kw + gap / 2 - 1.5:.1f}" y="-10" width="3" height="{cap_y + 20}" fill="{rule}"/>')
    # col 3: KR8TIV AI (wordmark + mono AI tag)
    k, kw3 = kr8tiv(x3, 18, 114, ink)
    parts.append(k)
    ai, aw = text_path('mono-bold', 'AI', 64, x3 + kw3 + 22, 18 + 60, ink)
    parts.append(ai)
    cap, _ = text_path(cap_font, 'AUTOMATE IT', 34, x3, cap_y, ink, tracking=cap_track)
    parts.append(cap)
    width = x3 + kw3 + 22 + aw
    return ''.join(parts), width, cap_y + 12


def endorsement(ink, text='AN ANTIHERO COMPANY', disc=C['carbon'], mk='#fff'):
    parts = [badge(0, 0, 90, disc, mk)]
    t, tw = text_path('barlowc-bold', text, 40, 118, 60, ink, tracking=0.26)
    parts.append(t)
    return ''.join(parts), 118 + tw, 90


def doc(vb, body, title):
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>'


if __name__ == '__main__':
    jobs = []
    for name, ink, disc, mk, rule, bg in [('on-dark', '#FFFFFF', C['carbon'], '#FFFFFF', 'rgba(255,255,255,0.28)', C['void']),
                                           ('on-light', C['void'], C['carbon'], '#FFFFFF', 'rgba(10,10,11,0.25)', C['bone'])]:
        body, w, h = family_lockup(ink, disc, mk, rule)
        pad = 30
        vb = f'{-pad} {-pad - 12} {w + 2 * pad:.1f} {h + 2 * pad + 12:.1f}'
        p = os.path.join(OUT, f'antihero-family-lockup-{name}.svg')
        open(p, 'w', encoding='utf-8').write(doc(vb, body, 'AntiHero, KR8TIV, KR8TIV AI'))
        jobs.append((p, os.path.join(OUT, f'antihero-family-lockup-{name}_3000px.png'), 3000, int(3000 * (h + 2 * pad + 12) / (w + 2 * pad)), None))
        for label, txt in [('an-antihero-company', 'AN ANTIHERO COMPANY'), ('antihero-family', 'PART OF THE ANTIHERO FAMILY')]:
            body, w, h = endorsement(ink, txt)
            vb = f'-12 -12 {w + 24:.1f} {h + 24}'
            p = os.path.join(OUT, f'kr8tiv-endorsement-{label}-{name}.svg')
            open(p, 'w', encoding='utf-8').write(doc(vb, body, txt.title()))
            jobs.append((p, os.path.join(OUT, f'kr8tiv-endorsement-{label}-{name}_1200px.png'), 1200, int(1200 * (h + 24) / (w + 24)), None))
    wrap = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', '_family_wrap.html')
    with Renderer() as r:
        for svg, png, w, h, bg in jobs:
            open(wrap, 'w').write(f'<html><body style="margin:0;background:{bg or "transparent"}"><img src="{file_url(svg)}" '
                                  f'style="display:block;width:{w}px;height:{h}px"></body></html>')
            r.png(wrap, png, w, h, transparent=bg is None)
    print('family assets:', len(jobs))

