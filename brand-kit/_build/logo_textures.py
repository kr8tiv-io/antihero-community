"""AntiHero logo in materials - 15 procedural texture studies (2400x2400)."""
import os
import sys

import cv2
import numpy as np

from backgrounds import concrete_albedo_height
from brand import C, KIT, mark_group
from render import Renderer
from tex import (alpha_from_png_bytes, bevel, blur, comp, fbm, gradient_map, grain, hex2rgb, motion_blur,
                 norm01, radial, save, screen, shade, vignette, warp)

N = 2400
OUT = os.path.join(KIT, '03_Logo-Textures')
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work')
os.makedirs(OUT, exist_ok=True)
_R = None
_CACHE = {}


def _svg(body, scale, cx, cy):
    k = scale * N / 1000.0
    tx, ty = cx * N - 500 * k, cy * N - 500 * k
    return (f'<html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="{N}" height="{N}" '
            f'viewBox="0 0 {N} {N}"><g transform="translate({tx:.2f},{ty:.2f}) scale({k:.5f})">{body}</g></svg></body></html>')


def mask(kind, scale=0.62, cx=0.5, cy=0.5):
    key = (kind, scale, cx, cy)
    if key not in _CACHE:
        body = {
            'mark': mark_group('#fff'),
            'disc': '<circle cx="500" cy="500" r="500" fill="#fff"/>',
            'ring': '<circle cx="500" cy="500" r="486" fill="none" stroke="#fff" stroke-width="28"/>',
        }[kind]
        b = _R.png_bytes_from_html(_svg(body, scale, cx, cy), N, N, transparent=True, base_dir=WORK)
        _CACHE[key] = alpha_from_png_bytes(b)
    return _CACHE[key]


def rgb(h):
    return hex2rgb(h)[None, None, :]


def drop_shadow(alpha, dx, dy, sigma, strength):
    s = np.roll(np.roll(alpha, int(dy), 0), int(dx), 1)
    return blur(s, sigma) * strength


# ---------------------------------------------------------------------------
def concrete_stencil():
    alb, hgt = concrete_albedo_height(N, N, seed=12, scale=1.0)
    lit = shade(blur(hgt, 0.8), light=(-0.5, -0.7, 0.55), strength=3.2)['diff']
    wall = (0.40 * alb * (0.72 + 0.42 * lit))[..., None] * rgb('#dfe0dc') / 0.87
    ys = np.linspace(0, 1, N, dtype=np.float32)[:, None]
    wall *= (1.18 - 0.35 * ys)[..., None]
    m = mask('mark', 0.70)
    m_soft = blur(m, 1.4)
    dens = 0.86 + 0.14 * norm01(fbm(N, N, 60, 4, seed=4))
    pores = np.clip((hgt < np.percentile(hgt, 1.5)).astype(np.float32), 0, 1)
    paint_a = m_soft * dens * (1 - 0.8 * blur(pores, 0.8))
    over = blur(m, 16) * 0.16 + blur(m, 45) * 0.06
    rng = np.random.default_rng(3)
    spk = (rng.random((N, N)) > 0.9965).astype(np.float32) * np.clip(blur(m, 26) * 1.6 - m, 0, 1)
    spk = blur(spk, 0.7) * 2.5
    paint_col = rgb('#f4f3ef') * (0.86 + 0.18 * lit)[..., None]
    img = comp(wall, paint_col, np.clip(over * (1 - m) + spk, 0, 0.7))
    img = comp(img, paint_col, np.clip(paint_a, 0, 1))
    img *= vignette(N, N, 0.45, 2.2)[..., None]
    return img + grain(N, N, 0.012, seed=1)[..., None]


def spun_steel():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    cx = cy = N / 2
    R = 0.40 * N
    r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    th = np.arctan2(ys - cy, xs - cx)
    disc = np.clip(R - r + 0.5, 0, 1)
    # background: charcoal with a soft spotlight
    bgc = rgb('#0c0d0f') + radial(N, N, cx, cy * 0.9, N * 0.75, 1.8)[..., None] * rgb('#2a2e33')
    # spun brushing: fine concentric rings + slight angular jitter
    rng = np.random.default_rng(9)
    rings_1d = rng.standard_normal(int(R * 4) + 8).astype(np.float32)
    rings_1d = cv2.GaussianBlur(rings_1d.reshape(1, -1), (0, 0), 1.2).ravel()
    rr = np.clip(r * 4, 0, len(rings_1d) - 1).astype(np.int32)
    brushed = rings_1d[rr] * 0.5 + 0.5 * norm01(fbm(N, N, 30, 3, seed=2)) * 0.3
    # anisotropic bow-tie highlight typical of spun metal
    bow = np.cos(th - np.deg2rad(-35)) ** 2
    base = 0.42 + 0.28 * bow + 0.06 * (brushed - 0.5)
    # height: rim + raised mark
    rim = np.clip((r - (R - 34)) / 34, 0, 1) * disc
    k = 0.8 * N / 1000.0
    m = mask('mark', 0.80 * 0.84)            # mark sized inside the coin
    hm = bevel(m, 10) * 1.0
    height = 0.8 * np.sin(np.pi * rim) + hm * 1.6
    sh = shade(blur(height, 1.2), light=(-0.5, -0.65, 0.58), strength=6.0, shininess=60, spec=0.9)
    metal = base * (0.55 + 0.6 * sh['diff'])
    # polished mark: brighter, smoother, stronger spec
    polish = 0.62 + 0.30 * sh['diff'] + 0.10 * bow
    val = metal * (1 - m) + polish * m
    val = val + sh['spec'] * (0.35 + 0.65 * m)
    steel = val[..., None] * rgb('#d9dde2') / 0.87
    shadow = drop_shadow(disc, 26, 40, 30, 0.75)
    img = bgc * (1 - shadow[..., None])
    img = comp(img, steel, disc)
    img *= vignette(N, N, 0.35, 2.0)[..., None]
    return img + grain(N, N, 0.01, seed=3)[..., None]


def gold_foil():
    fib = motion_blur(fbm(N, N, 3, 2, seed=7), 11, 15)
    mott = norm01(fbm(N, N, N / 5, 5, seed=8))
    card = (0.035 + 0.012 * mott + (fib - 0.5) * 0.02)[..., None] * rgb('#e8e4dc') / 0.9
    card += radial(N, N, N * 0.38, N * 0.30, N * 0.9, 2.2)[..., None] * 0.035
    m = mask('mark', 0.64)
    wr = fbm(N, N, 14, 4, persistence=0.6, seed=21)
    hgt = blur(m, 2.5) * 1.0 + (wr - 0.5) * 0.35 * m
    sh = shade(hgt, light=(-0.4, -0.75, 0.52), strength=5.0, shininess=28, spec=1.0)
    v = np.clip(0.35 + 0.5 * sh['diff'] + 0.25 * norm01(fbm(N, N, 90, 3, seed=5)), 0, 1)
    gold = gradient_map(v, [(0, '#3d2708'), (0.35, '#8a5e17'), (0.6, '#c99a3c'), (0.8, '#efd18a'), (1, '#fff3cf')])
    gold = screen(gold, sh['spec'][..., None] * rgb('#fff5d8') * 0.9)
    rng = np.random.default_rng(4)
    sparkle = (rng.random((N, N)) > 0.9993).astype(np.float32) * m
    gold = screen(gold, blur(sparkle, 1.0)[..., None] * 3.0 * rgb('#fff6dc'))
    deboss = blur(m, 5) - blur(np.roll(np.roll(m, 3, 0), 3, 1), 5)
    card = card * (1 - 0.6 * np.clip(-deboss, 0, 1))[..., None] + np.clip(deboss, 0, 1)[..., None] * 0.05
    img = comp(card, gold, m)
    img *= vignette(N, N, 0.35, 2.0)[..., None]
    return img + grain(N, N, 0.008, seed=2)[..., None]


def chrome():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32) / N
    bg = gradient_map(ys, [(0, '#050506'), (0.6, '#0d0e10'), (1, '#050506')])
    glow = radial(N, N, N * 0.5, N * 0.52, N * 0.62, 1.8)
    bg = screen(bg, glow[..., None] * rgb(C['ignition']) * 0.55)
    m = mask('mark', 0.70)
    # pillow profile (no flat top) + generous smoothing -> liquid, crease-free chrome
    mb = (m > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(mb, cv2.DIST_L2, cv2.DIST_MASK_PRECISE).astype(np.float32)
    h = np.sqrt(np.clip(d / 70.0, 0, 1)) * mb
    h = blur(h, 4.0)
    nx, ny, nz = shade(h, strength=38.0)['n']
    ry = 2 * nz * ny                      # reflection of a viewer ray, y component
    t = np.clip(0.5 + 0.55 * ry + 0.32 * (ys - 0.5), 0, 1)
    env = gradient_map(t, [(0, '#1b1f25'), (0.30, '#8d98a3'), (0.44, '#eef3f7'), (0.49, '#ffffff'),
                           (0.505, '#1a1512'), (0.60, '#4e4038'), (0.80, '#9a8574'), (1, '#e6d9c9')])
    sh = shade(h, light=(-0.45, -0.7, 0.55), strength=38.0, shininess=90, spec=1.0)
    chrome_c = screen(env, sh['spec'][..., None] * 0.9)
    edge = np.clip(blur(m, 1.2) - blur(m, 6), 0, 1)
    chrome_c = screen(chrome_c, edge[..., None] * rgb(C['ignition']) * 0.35)   # red rim from the glow behind
    shadow = drop_shadow(m, 0, 36, 40, 0.8)
    img = bg * (1 - shadow[..., None])
    img = comp(img, chrome_c, m)
    return img + grain(N, N, 0.01, seed=5)[..., None]


def neon_brick():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    bw, bh, mo = 250, 84, 12
    row = (ys // (bh + mo)).astype(np.int32)
    off = (row % 2) * (bw + mo) / 2
    bx = ((xs + off) // (bw + mo)).astype(np.int32)
    lx = (xs + off) % (bw + mo)
    ly = ys % (bh + mo)
    mortar = ((lx > bw) | (ly > bh)).astype(np.float32)
    mortar = blur(mortar, 1.5)
    rng = np.random.default_rng(11)
    tone = rng.uniform(0.75, 1.15, (row.max() + 2, bx.max() + 2)).astype(np.float32)
    btone = tone[row, bx]
    surf = norm01(fbm(N, N, 18, 4, seed=12))
    alb = (0.5 * btone * (0.8 + 0.35 * surf)) * (1 - 0.55 * mortar)
    hgt = (1 - mortar) * 1.0 + surf * 0.25
    lit_amb = shade(blur(hgt, 1.5), light=(0.0, -0.6, 0.8), strength=2.0)['diff']
    wall_alb = alb[..., None] * rgb('#6f5a52')
    m = mask('mark', 0.62, cy=0.5)
    # outlined neon: a smooth tube riding 11px inside every edge of the vector mark
    mb = (m > 0.5).astype(np.uint8)
    d_in = cv2.distanceTransform(mb, cv2.DIST_L2, 5).astype(np.float32)
    d_out = cv2.distanceTransform(1 - mb, cv2.DIST_L2, 5).astype(np.float32)
    sd = blur(d_in - d_out, 1.5)
    tube = np.exp(-((sd - 11.0) / 6.0) ** 2)
    core = np.exp(-((sd - 11.0) / 2.2) ** 2)
    red = rgb(C['ignition'])
    hot = rgb('#ffd6cc')
    g1, g2, g3, g4 = blur(tube, 8), blur(tube, 28), blur(tube, 90), blur(tube, 260)
    light = (g1 * 0.8 + g2 * 1.2 + g3 * 2.4 + g4 * 6.0)
    wall = wall_alb * (0.06 + 0.07 * lit_amb[..., None]) + wall_alb * light[..., None] * red * 2.6
    img = wall
    img = screen(img, (g2 * 0.6 + g3 * 0.5)[..., None] * red)
    img = screen(img, tube[..., None] * (red * 0.9 + 0.1))
    img = screen(img, core[..., None] * hot)
    img *= vignette(N, N, 0.4, 2.0)[..., None]
    return img + grain(N, N, 0.012, seed=6)[..., None]


def letterpress():
    fib = motion_blur(fbm(N, N, 3, 2, seed=31), 13, 40)
    fib2 = motion_blur(fbm(N, N, 3, 2, seed=32), 13, -30)
    mott = norm01(fbm(N, N, N / 6, 5, seed=33))
    paper_h = (fib + fib2) * 0.5
    disc = mask('disc', 0.62)
    m = mask('mark', 0.62)
    ink = np.clip(disc - m, 0, 1)
    press = blur(ink, 2.2)
    height = paper_h * 0.4 - press * 1.0
    sh = shade(height, light=(-0.45, -0.7, 0.56), strength=5.5)
    paper = rgb(C['bone']) * (0.90 + 0.12 * sh['diff'] + 0.04 * (mott - 0.5))[..., None]
    salt = norm01(fbm(N, N, 5, 2, seed=34))
    density = np.clip(0.93 - 0.20 * np.clip(salt - 0.72, 0, 1) * 3 - 0.08 * (paper_h - 0.5), 0.6, 1)
    inkc = rgb(C['carbon']) * (0.85 + 0.25 * sh['diff'])[..., None]
    edge = np.clip(press - blur(ink, 6), 0, 1)
    a = np.clip(ink * density + edge * 0.15, 0, 1)
    img = comp(paper, inkc, a)
    img *= (0.93 + 0.07 * vignette(N, N, 0.6, 2.0))[..., None]
    return img + grain(N, N, 0.008, seed=8)[..., None]


def worley(h, w, npts, seed):
    rng = np.random.default_rng(seed)
    img = np.ones((h, w), np.uint8)
    ys_, xs_ = rng.integers(0, h, npts), rng.integers(0, w, npts)
    img[ys_, xs_] = 0
    d = cv2.distanceTransform(img, cv2.DIST_L2, 5).astype(np.float32)
    return d / (d.max() + 1e-6)


def leather():
    cells = worley(N, N, 90000, 5)
    peb = 1 - np.clip(cells * 6.5, 0, 1) ** 0.6
    fine = norm01(fbm(N, N, 4, 2, seed=6))
    mott = norm01(fbm(N, N, N / 5, 5, seed=7))
    m = mask('mark', 0.58)
    ring = mask('ring', 0.58)
    stamp = np.clip(m + ring, 0, 1)
    press = blur(stamp, 2.0)
    # stitch line around the badge
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    r = np.sqrt((xs - N / 2) ** 2 + (ys - N / 2) ** 2)
    th = np.arctan2(ys - N / 2, xs - N / 2)
    Rst = 0.58 * N / 2 + 70
    band = np.exp(-((r - Rst) / 7) ** 2)
    dash = (np.sin(th * 150) > 0.15).astype(np.float32)
    stitch = blur(band * dash, 1.0)
    height = peb * 0.55 * (1 - 0.8 * press) + fine * 0.15 - press * 2.2 + stitch * 0.9
    sh = shade(blur(height, 0.9), light=(-0.5, -0.75, 0.45), strength=7.0, shininess=18, spec=0.35)
    base = rgb('#4a3a30') * (0.80 + 0.35 * mott)[..., None]
    key = radial(N, N, N * 0.35, N * 0.25, N * 1.1, 1.3)[..., None]
    img = base * (0.35 + 0.95 * sh['diff'])[..., None] * (0.55 + 0.6 * key)
    img = img * (1 - 0.30 * press)[..., None]                    # burnished stamp darkens
    img = screen(img, (sh['spec'] * (0.5 + 1.4 * press))[..., None] * rgb('#e8d8c8') * 0.6)
    img = comp(img, rgb('#cdbfae') * (0.6 + 0.4 * sh['diff'])[..., None], stitch * 0.85)
    img *= vignette(N, N, 0.45, 2.0)[..., None]
    return img + grain(N, N, 0.008, seed=9)[..., None]


def screen_print_tee():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    knit = 0.5 + 0.5 * np.sin(xs * np.pi / 3.0) * (0.6 + 0.4 * np.sin(ys * np.pi / 4.0 + xs * 0.3))
    fib = norm01(motion_blur(fbm(N, N, 2, 2, seed=41), 7, 90))
    folds_n = fbm(N, N, N / 3, 4, seed=42)
    folds = blur(folds_n, 30)
    fold_sh = shade(folds, light=(-0.4, -0.8, 0.45), strength=900.0)['diff']
    shirt = (0.050 + 0.018 * knit + 0.02 * fib)[..., None] * rgb('#dcdfe3') / 0.87
    shirt *= (0.55 + 0.75 * fold_sh)[..., None]
    gy, gx = np.gradient(folds * 900)
    disc = mask('disc', 0.58, cy=0.47)
    m = mask('mark', 0.58, cy=0.47)
    ink = np.clip(disc - m, 0, 1)
    ink = warp(ink, gx * 6, gy * 6)
    crack = norm01(fbm(N, N, 26, 5, seed=43))
    crack2 = norm01(fbm(N, N, 7, 3, seed=44))
    distress = np.clip((crack - 0.70) * 5, 0, 1) * 0.9 + np.clip((crack2 - 0.80) * 6, 0, 1) * 0.6
    cov = np.clip(ink * (1 - distress) * (0.82 + 0.18 * knit), 0, 1)
    inkc = rgb('#efeeea') * (0.62 + 0.45 * fold_sh)[..., None]
    img = comp(shirt, inkc, cov)
    return img + grain(N, N, 0.01, seed=10)[..., None]


def chalkboard():
    base = rgb('#232a28') * (0.88 + 0.20 * norm01(fbm(N, N, N / 4, 5, seed=51)))[..., None]
    smudge = norm01(fbm(N, N, N / 3, 4, seed=52))
    base = comp(base, rgb('#e9ece6'), np.clip((smudge - 0.45) * 0.12, 0, 0.06))
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32) / N
    for i, (y0, amp, a) in enumerate([(0.22, 0.05, 0.05), (0.55, 0.04, 0.04), (0.83, 0.06, 0.045)]):
        arc = np.exp(-((ys - y0 - amp * np.sin(xs * 3.1 + i)) / 0.035) ** 2)      # eraser swipes
        base = comp(base, rgb('#e9ece6'), arc * a * norm01(motion_blur(fbm(N, N, 6, 2, seed=60 + i), 41, 0)))
    m = mask('mark', 0.66)
    edge_n = fbm(N, N, 6, 3, seed=53)
    mm = blur(m, 2.5)
    rough = np.clip((mm - 0.5 + (edge_n - 0.5) * 0.35) * 4 + 0.5, 0, 1)
    streak = norm01(motion_blur(fbm(N, N, 2.5, 2, seed=54), 15, -25))
    chalk = rough * np.clip((streak - 0.28) * 2.2, 0, 1) ** 0.8
    img = comp(base, rgb('#eef0ea'), chalk * 0.9)
    img = comp(img, rgb('#eef0ea'), blur(m, 22) * 0.05)
    img *= vignette(N, N, 0.45, 2.0)[..., None]
    return img + grain(N, N, 0.012, seed=11)[..., None]


def carbon_fiber():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    s = 34
    cx_, cy_ = (xs // s).astype(np.int32), (ys // s).astype(np.int32)
    u, v = (xs % s) / s, (ys % s) / s
    horiz = ((cx_ + cy_ // 2 * 1 + (cy_ % 2)) // 2 % 2 == 0)
    horiz = (((cx_ - cy_) // 2) % 2 == 0)
    prof = np.where(horiz, np.sin(np.pi * v), np.sin(np.pi * u)) ** 0.7
    fibers = np.where(horiz, motion_blur(fbm(N, N, 2, 1, seed=61), 9, 0), motion_blur(fbm(N, N, 2, 1, seed=62), 9, 90))
    weave = 0.05 + 0.10 * prof + 0.03 * (fibers - 0.5)
    gloss = radial(N, N, N * 0.32, N * 0.22, N * 0.9, 1.6) * 0.20
    cf = (weave + gloss * (0.4 + 0.6 * prof))[..., None] * rgb('#cfd6de') / 0.84
    m = mask('mark', 0.66)
    h = blur(bevel(m, 8), 1.0)
    brushed = norm01(motion_blur(fbm(N, N, 2, 2, seed=63), 61, 0))
    sh = shade(h, light=(-0.45, -0.7, 0.55), strength=10.0, shininess=50, spec=0.8)
    alu = (0.60 + 0.12 * (brushed - 0.5) + 0.30 * sh['diff'] + 0.25 * (1 - ys / N))
    alu = alu[..., None] * rgb('#dde1e6') / 0.88
    alu = screen(alu, sh['spec'][..., None] * 0.7)
    shadow = drop_shadow(m, 10, 16, 12, 0.85)
    img = cf * (1 - shadow[..., None])
    img = comp(img, alu, m)
    img *= vignette(N, N, 0.4, 2.0)[..., None]
    return img + grain(N, N, 0.008, seed=12)[..., None]


def halftone():
    from backgrounds import paper
    img = paper(N, N, seed=71)
    m = mask('mark', 0.64, cx=0.49, cy=0.49)
    msh = mask('mark', 0.64, cx=0.49 + 0.012, cy=0.49 + 0.012)
    img = comp(img, rgb(C['void']), msh)
    # 45-degree halftone screen, dot size ramps across the mark
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    p = 26.0
    a = np.deg2rad(45)
    u = (xs * np.cos(a) + ys * np.sin(a)) / p
    v = (-xs * np.sin(a) + ys * np.cos(a)) / p
    du, dv = u - np.round(u), v - np.round(v)
    d = np.sqrt(du * du + dv * dv)
    tone = np.clip(0.30 + 0.62 * (ys / N) * 0.6 + 0.62 * (1 - xs / N) * 0.4, 0, 1)
    rad = 0.5 * np.sqrt(tone) * 1.08
    dots = np.clip((rad - d) * p * 0.9 + 0.5, 0, 1)
    fill = np.clip(m * (0.35 + 0.65 * dots), 0, 1)
    img = comp(img, rgb('#ffffff'), m * 0.96)
    img = comp(img, rgb(C['ignition']), fill)
    return img + grain(N, N, 0.006, seed=13)[..., None]


def glitch():
    base = np.zeros((N, N, 3), np.float32) + rgb('#070708')
    base = screen(base, radial(N, N, N / 2, N / 2, N * 0.6, 2.0)[..., None] * rgb('#1a1c20'))
    m = mask('mark', 0.66)
    red_g = np.roll(m, -26, 1)
    ash_g = np.roll(m, 22, 1)
    img = comp(base, rgb(C['ignition']), red_g * 0.95)
    img = comp(img, rgb('#8a9096'), ash_g * 0.55)
    img = comp(img, rgb('#ffffff'), m)
    rng = np.random.default_rng(8)
    y = 0
    out = img.copy()
    while y < N:
        hgt = int(rng.integers(6, 70))
        if rng.random() < 0.28:
            shift = int(rng.integers(-110, 110))
            out[y:y + hgt] = np.roll(img[y:y + hgt], shift, 1)
            if rng.random() < 0.3:
                out[y:y + hgt] = comp(out[y:y + hgt], rgb(C['ignition']), np.full(out[y:y + hgt].shape[:2], 0.25, np.float32))
        y += hgt
    scan = (np.arange(N) % 4 < 2).astype(np.float32)[:, None, None]
    out *= (0.86 + 0.14 * scan)
    blocks = (norm01(fbm(N, N, 40, 1, seed=81)) > 0.93).astype(np.float32) * (norm01(fbm(N, N, 3, 1, seed=82)) > 0.5)
    out = screen(out, blocks[..., None] * 0.08)
    return out + grain(N, N, 0.02, seed=14)[..., None]


def holo_sticker():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    brushed = norm01(motion_blur(fbm(N, N, 2, 2, seed=91), 91, 0))
    lid = (0.16 + 0.03 * (brushed - 0.5) + 0.06 * (1 - ys / N))[..., None] * rgb('#c9ced4') / 0.85
    disc = mask('disc', 0.62)
    m = mask('mark', 0.62)
    border = np.clip(cv2.dilate((disc > 0.5).astype(np.float32), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71))), 0, 1)
    border = blur(border, 1.2)
    shadow = drop_shadow(border, 14, 26, 26, 0.7)
    img = lid * (1 - shadow[..., None])
    img = comp(img, rgb('#f7f7f5') * (0.92 + 0.08 * (1 - ys / N))[..., None], border)
    hue = (xs / N * 0.9 + ys / N * 0.6 + norm01(fbm(N, N, 260, 3, seed=92)) * 0.8) % 1.0
    hsv = np.stack([hue * 179, np.full_like(hue, 110), np.full_like(hue, 235)], -1).astype(np.uint8)
    holo = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB).astype(np.float32) / 255
    sparkle = (norm01(fbm(N, N, 3, 2, seed=93)) > 0.82).astype(np.float32) * 0.25
    holo = screen(holo, sparkle[..., None])
    band = np.exp(-((xs / N + ys / N - 1.0) / 0.18) ** 2)[..., None]
    holo = screen(holo, band * 0.35)
    img = comp(img, holo, disc)
    img = comp(img, rgb(C['void']), m)
    return img + grain(N, N, 0.008, seed=15)[..., None]


def wood_burn():
    ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
    # flat-sawn plank: grain runs horizontally, gently waving; warp varies slowly along the grain
    wn1 = fbm(N, N, N / 2.2, 4, seed=101)                                           # broad, smooth sweep
    wn2 = cv2.resize(fbm(N // 24, N // 160, 2, 3, seed=106), (N, N), interpolation=cv2.INTER_CUBIC)  # fine waviness, long along x
    t = ys / N + (wn1 - 0.5) * 0.16 + (wn2 - 0.5) * 0.018
    rings = 0.5 + 0.5 * np.sin(t * 44 * np.pi)
    late = np.clip((rings - 0.78) / 0.22, 0, 1) ** 1.5 * (0.7 + 0.3 * norm01(fbm(N, N, 40, 3, seed=107)))
    pores = norm01(motion_blur(fbm(N, N, 2.2, 2, seed=102), 81, 0))
    v = np.clip(0.62 - 0.30 * late + 0.10 * (pores - 0.5) + 0.06 * norm01(fbm(N, N, 90, 3, seed=105)), 0, 1)
    wood = gradient_map(v, [(0, '#6b4424'), (0.5, '#b07a45'), (0.75, '#cf9d62'), (1, '#e3bb82')])
    wood *= (0.92 + 0.08 * norm01(fbm(N, N, N / 3, 4, seed=103)))[..., None]
    m = mask('mark', 0.60)
    ring = mask('ring', 0.60)
    burn = np.clip(m + ring, 0, 1)
    soot = blur(burn, 9)
    hgt = -blur(burn, 1.6)
    sh = shade(hgt, light=(-0.45, -0.7, 0.55), strength=6.0)['diff']
    char = gradient_map(np.clip(0.3 + 0.7 * norm01(fbm(N, N, 8, 3, seed=104)), 0, 1),
                        [(0, '#140b06'), (0.6, '#2c1a0e'), (1, '#4a2c16')])
    img = wood * (1 - 0.35 * soot)[..., None]
    img = comp(img, char * (0.7 + 0.5 * sh)[..., None], burn)
    img *= vignette(N, N, 0.4, 2.0)[..., None]
    return img + grain(N, N, 0.008, seed=16)[..., None]


def paper_cut():
    from backgrounds import paper
    img = paper(N, N, seed=111)
    disc = mask('disc', 0.64)
    m = mask('mark', 0.64)
    # red sheet (whole disc) under a carbon sheet with the mark cut out
    sh1 = drop_shadow(disc, 16, 30, 26, 0.55)
    img = img * (1 - sh1[..., None])
    red = rgb(C['ignition']) * (0.93 + 0.07 * norm01(fbm(N, N, 6, 2, seed=112)))[..., None]
    img = comp(img, red, disc)
    top = np.clip(disc - m, 0, 1)
    inner = drop_shadow(top, 8, 14, 10, 0.55) * m          # shadow cast inside the cut-outs
    img = img * (1 - inner[..., None])
    carbon = rgb(C['carbon']) * (0.92 + 0.10 * norm01(fbm(N, N, 6, 2, seed=113)))[..., None]
    edge = np.clip(blur(top, 1.2) - blur(top, 4), 0, 1)
    carbon = screen(carbon, edge[..., None] * 0.18)
    img = comp(img, carbon, top)
    return img + grain(N, N, 0.006, seed=17)[..., None]


SCENES = {
    '01-concrete-stencil': concrete_stencil,
    '02-spun-steel-coin': spun_steel,
    '03-gold-foil-black-card': gold_foil,
    '04-liquid-chrome': chrome,
    '05-neon-brick': neon_brick,
    '06-letterpress-bone': letterpress,
    '07-leather-deboss': leather,
    '08-screen-print-tee': screen_print_tee,
    '09-chalkboard': chalkboard,
    '10-carbon-fiber-aluminum': carbon_fiber,
    '11-halftone-pop': halftone,
    '12-glitch-signal': glitch,
    '13-holo-sticker': holo_sticker,
    '14-laser-etched-wood': wood_burn,
    '15-paper-cut': paper_cut,
}

if __name__ == '__main__':
    only = sys.argv[1:] or list(SCENES)
    with Renderer() as r:
        _R = r
        globals()['_R'] = r
        for name in only:
            key = next(k for k in SCENES if k.startswith(name) or name in k)
            img = SCENES[key]()
            save(np.clip(img, 0, 1), os.path.join(OUT, f'antihero-texture-{key}_2400px.jpg'))
            print('done', key, flush=True)
