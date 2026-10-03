"""Brand backgrounds: First Light (horizon), Concrete, Smoke, Paper, Red Grain, Grid."""
import os
import sys

import cv2
import numpy as np

from brand import C, KIT
from tex import (blur, fbm, gradient_map, grain, hex2rgb, motion_blur, norm01, radial,
                 save, screen, vignette, warp)

OUT = os.path.join(KIT, '04_Backgrounds')
os.makedirs(OUT, exist_ok=True)


def first_light(w, h, horizon=0.60, seed=3):
    """Dark sea horizon at first light - the brand's evolution of the original sunset channel art."""
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32)
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :] * np.ones((h, 1), np.float32)
    hy = horizon * h
    # sky: void at the top -> carbon -> warm dusk at the horizon
    t = np.clip(ys / horizon, 0, 1)
    sky = gradient_map(t ** 1.6, [(0, '#050506'), (0.55, '#15181b'), (0.85, '#2c2320'), (1.0, '#4a2a22')])
    # clouds: stretched fbm bands, warmer & brighter near the horizon
    cl = fbm(h, w, w / 3.2, octaves=7, seed=seed)
    cl = motion_blur(cl, max(3, w // 60) | 1, 0)
    cl = norm01(cl)
    bands = np.clip((cl - 0.45) * 2.2, 0, 1) * np.clip(1 - np.abs(ys - horizon * 0.72) / (horizon * 0.7), 0, 1)
    warm = hex2rgb('#6a3526')
    sky = sky + bands[..., None] * (0.10 + 0.35 * t[..., None] ** 3) * warm[None, None, :]
    # the glow: a wide, flattened bloom of Ignition sitting on the horizon
    gx = (xs - 0.5) / 0.55
    gy = (ys - horizon) / 0.16
    bloom = np.exp(-(gx ** 2 + gy ** 2) * 1.2)
    core = np.exp(-(((xs - 0.5) / 0.20) ** 2 + ((ys - horizon) / 0.018) ** 2))
    red = hex2rgb(C['ignition'])
    hot = hex2rgb('#ffb08a')
    img = sky.copy()
    img = screen(img, bloom[..., None] * red[None, None, :] * 0.55)
    img = screen(img, core[..., None] * hot[None, None, :] * 0.85)
    # sea: below the horizon - dark, with streaked reflections of the glow.
    # Streaks live in a perspective space: rows compress toward the horizon.
    below = ys > horizon
    depth = np.clip((ys - horizon) / (1 - horizon), 0, 1)
    sea = gradient_map(depth, [(0, '#1b1514'), (0.25, '#0e0d0e'), (1, '#060607')])
    SH = 900                                        # rows in perspective space
    streak_src = fbm(SH, max(64, w // 48), 3, octaves=4, seed=seed + 11)
    streak_src = cv2.resize(streak_src, (w, SH), interpolation=cv2.INTER_CUBIC)   # stretch horizontally
    streak_src = norm01(streak_src)
    z = 1.0 / (depth + 0.035)                      # perspective depth per screen row
    zr = (z - z.min()) / (z.max() - z.min())
    map_y = ((1 - zr) * (SH - 1)).astype(np.float32)
    map_x = (xs * (w - 1)).astype(np.float32)
    streak = cv2.remap(streak_src, map_x, map_y, cv2.INTER_LINEAR)
    streak = np.clip((streak - 0.45) * 2.4, 0, 1) ** 1.3
    refl_x = np.exp(-((xs - 0.5) / (0.07 + 0.30 * depth)) ** 2)
    refl = streak * refl_x * np.exp(-depth * 2.6)
    sea = screen(sea, refl[..., None] * (red * 0.7 + hot * 0.3)[None, None, :] * 0.9)
    img = np.where(below[..., None], sea, img)
    # soften the horizon seam
    seam = np.exp(-((ys - horizon) / 0.004) ** 2)[..., None]
    img = img * (1 - seam * 0.3) + seam * 0.3 * (hot * 0.6)[None, None, :]
    img *= vignette(h, w, 0.55, 2.4, cy=horizon)[..., None]
    img += grain(h, w, 0.022, seed=seed + 5)[..., None]
    return np.clip(img, 0, 1)


def concrete_albedo_height(w, h, seed=5, scale=1.0):
    """Shared concrete model: returns (albedo variation ~1.0, height map)."""
    big = norm01(fbm(h, w, w / 3, octaves=5, seed=seed))
    mid = norm01(fbm(h, w, 38 * scale, octaves=4, seed=seed + 1))
    fine = norm01(fbm(h, w, 3.5 * scale, octaves=2, seed=seed + 2))
    trowel = norm01(motion_blur(fbm(h, w, 20 * scale, octaves=3, seed=seed + 3), int(61 * scale) | 1, 28))
    rng = np.random.default_rng(seed + 4)
    pores = np.zeros((h, w), np.float32)
    n = int(w * h * 0.0009)
    ys_, xs_ = rng.integers(0, h, n), rng.integers(0, w, n)
    pores[ys_, xs_] = rng.uniform(0.4, 1.0, n)
    pores = blur(pores, 1.1 * scale)
    pores = np.clip(pores / (pores.max() * 0.25 + 1e-6), 0, 1)
    albedo = (0.80 + 0.32 * big) * (0.90 + 0.14 * mid) * (0.93 + 0.12 * fine) * (0.96 + 0.07 * trowel) * (1 - 0.45 * pores)
    height = 0.55 * mid + 0.35 * fine + 0.25 * trowel - 1.2 * pores
    return albedo.astype(np.float32), height.astype(np.float32)


def concrete(w, h, tone=0.13, seed=5, light=True, tint='#1d2124'):
    from tex import shade
    albedo, height = concrete_albedo_height(w, h, seed)
    lit = shade(blur(height, 0.8), light=(-0.45, -0.75, 0.55), strength=3.0)['diff']
    v = tone * albedo * (0.70 + 0.45 * lit)
    if light:
        ys = np.linspace(0, 1, h, dtype=np.float32)[:, None]
        v = v * (1.30 - 0.60 * ys)          # soft top light
    col = hex2rgb(tint) / max(1e-3, hex2rgb(tint).mean())
    img = v[..., None] * col[None, None, :]
    img = img * vignette(h, w, 0.5, 2.0)[..., None] + grain(h, w, 0.014, seed=seed + 9)[..., None]
    return np.clip(img, 0, 1)


def smoke(w, h, seed=9, rim='#E0261E'):
    n1 = fbm(h, w, w / 2.2, octaves=5, seed=seed)
    n2 = fbm(h, w, w / 2.2, octaves=5, seed=seed + 1)
    dx = (n1 - 0.5) * w * 0.45
    dy = (n2 - 0.5) * h * 0.45
    # ridged noise -> thin, turbulent wisps
    r = fbm(h, w, w / 5, octaves=8, persistence=0.55, seed=seed + 2)
    r = 1 - np.abs(2 * norm01(r) - 1)
    r = warp(r, dx, dy)
    haze = norm01(warp(fbm(h, w, w / 3, octaves=4, seed=seed + 3), dx * 0.5, dy * 0.5))
    wisps = (np.clip((r - 0.55) / 0.45, 0, 1) ** 2.2) * (0.35 + 0.65 * haze) + 0.18 * haze ** 2
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    base = gradient_map(np.clip(ys * np.ones_like(xs), 0, 1), [(0, '#0b0c0d'), (1, '#070708')])
    grey = hex2rgb('#8a9096')
    red = hex2rgb(rim)
    side = np.clip(1.15 - xs * 1.6, 0, 1) ** 2      # red rim light from the left
    img = base + wisps[..., None] * (grey * 0.16 + red * 0.34 * side[..., None])
    img *= vignette(h, w, 0.5, 2.0)[..., None]
    img += grain(h, w, 0.02, seed=seed + 4)[..., None]
    return np.clip(img, 0, 1)


def paper(w, h, seed=21, col='#ECE8E1'):
    fib = fbm(h, w, 3, octaves=2, seed=seed)
    fib = motion_blur(fib, 9, 20)
    mott = norm01(fbm(h, w, w / 5, octaves=5, seed=seed + 1))
    v = 1.0 + (fib - 0.5) * 0.06 + (mott - 0.5) * 0.035
    img = hex2rgb(col)[None, None, :] * v[..., None]
    img *= (0.94 + 0.06 * vignette(h, w, 0.6, 2.0))[..., None]
    return np.clip(img + grain(h, w, 0.01, seed=seed + 2)[..., None], 0, 1)


def red_grain(w, h, seed=31):
    mott = norm01(fbm(h, w, w / 4, octaves=5, seed=seed))
    base = hex2rgb(C['ignition'])
    img = base[None, None, :] * (0.92 + 0.10 * mott)[..., None]
    img *= (0.78 + 0.22 * vignette(h, w, 0.9, 2.0))[..., None]
    return np.clip(img + grain(h, w, 0.03, seed=seed + 1)[..., None], 0, 1)


def grid(w, h, step=None, seed=41):
    step = step or max(24, w // 48)
    img = np.zeros((h, w, 3), np.float32) + hex2rgb('#0a0a0b')[None, None, :]
    lines = np.zeros((h, w), np.float32)
    lines[:, ::step] = 1
    lines[::step, :] = 1
    major = np.zeros((h, w), np.float32)
    major[:, ::step * 4] = 1
    major[::step * 4, :] = 1
    fade = radial(h, w, w * 0.5, h * 0.45, max(w, h) * 0.75, 1.2)
    lines = blur(lines, 0.6) * 1.6
    major = blur(major, 0.7) * 1.6
    img += (lines * 0.10 + major * 0.16)[..., None] * fade[..., None] * hex2rgb('#8a9096')[None, None, :]
    glow = radial(h, w, w * 0.5, h * 0.55, max(w, h) * 0.5, 2.0)
    img = screen(img, glow[..., None] * hex2rgb(C['ignition'])[None, None, :] * 0.10)
    return np.clip(img + grain(h, w, 0.015, seed=seed)[..., None], 0, 1)


def daybreak(w, h, seed=51, sun=(0.24, 0.72)):
    """Bright morning sky: clear blue up top, warm cream at the horizon, soft sun bloom, faint cirrus. For text-heavy layouts."""
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32)
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :] * np.ones((h, 1), np.float32)
    sky = gradient_map(ys, [(0.0, '#6f98c9'), (0.45, '#a9c4e0'), (0.78, '#e6e4dc'), (1.0, '#f6ead6')])
    ar = w / h
    d = np.sqrt(((xs - sun[0]) * ar) ** 2 + (ys - sun[1]) ** 2)
    sky = screen(sky, (np.exp(-d * 2.4) * 0.55)[..., None] * hex2rgb('#fff1d6')[None, None, :])
    sky = screen(sky, (np.exp(-d * 14) * 0.9)[..., None] * hex2rgb('#fffaf0')[None, None, :])
    ci = norm01(motion_blur(fbm(h, w, w / 5, 6, seed=seed), max(5, w // 18) | 1, -8))
    cir = np.clip((ci - 0.55) * 2.2, 0, 1) ** 1.5 * np.clip(1.2 - ys * 1.4, 0, 1)
    sky = screen(sky, cir[..., None] * 0.22)
    sky += grain(h, w, 0.008, seed=seed + 1)[..., None]
    return np.clip(sky, 0, 1)


SETS = {
    'daybreak': daybreak,
    'first-light': first_light,
    'concrete': concrete,
    'smoke': smoke,
    'paper-bone': paper,
    'ignition-grain': red_grain,
    'grid': grid,
}

if __name__ == '__main__':
    only = sys.argv[1:] or list(SETS)
    for name in only:
        fn = SETS[name]
        for tag, (w, h) in {'desktop-3840x2160': (3840, 2160), 'phone-1290x2796': (1290, 2796)}.items():
            img = fn(w, h)
            save(img, os.path.join(OUT, f'antihero-bg-{name}_{tag}.jpg'))
        print('done', name)
