"""Procedural texture toolkit (numpy/OpenCV). Everything returns float32 arrays in 0..1."""
import io

import cv2
import numpy as np
from PIL import Image


def hex2rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], np.float32)


def value_noise(h, w, scale, rng):
    gh, gw = int(np.ceil(h / scale)) + 3, int(np.ceil(w / scale)) + 3
    grid = rng.random((gh, gw)).astype(np.float32)
    up = cv2.resize(grid, (int(gw * scale), int(gh * scale)), interpolation=cv2.INTER_CUBIC)
    oy, ox = int(scale), int(scale)
    return up[oy:oy + h, ox:ox + w]


def fbm(h, w, scale, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
    rng = np.random.default_rng(seed)
    total = np.zeros((h, w), np.float32)
    amp, s, norm = 1.0, float(scale), 0.0
    for _ in range(octaves):
        if s < 1.0:
            break
        total += amp * value_noise(h, w, s, rng)
        norm += amp
        amp *= persistence
        s /= lacunarity
    return total / norm


def norm01(a):
    lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.5)
    return np.clip((a - lo) / (hi - lo + 1e-8), 0, 1).astype(np.float32)


def blur(a, sigma):
    if sigma <= 0:
        return a
    k = int(sigma * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), sigma)


def motion_blur(a, length, angle_deg=0):
    k = np.zeros((length, length), np.float32)
    k[length // 2, :] = 1.0
    M = cv2.getRotationMatrix2D((length / 2 - 0.5, length / 2 - 0.5), angle_deg, 1.0)
    k = cv2.warpAffine(k, M, (length, length))
    k /= k.sum()
    return cv2.filter2D(a, -1, k)


def warp(a, dx, dy):
    h, w = a.shape[:2]
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(a, xs + dx, ys + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def grain(h, w, amount=0.04, seed=7, size=1.0):
    rng = np.random.default_rng(seed)
    g = rng.standard_normal((h, w)).astype(np.float32)
    if size > 1.0:
        g = blur(g, size * 0.5)
        g /= g.std() + 1e-8
    return g * amount


def normals(height, strength=1.0):
    gy, gx = np.gradient(height * strength)
    nx, ny, nz = -gx, -gy, np.ones_like(height)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    return nx / n, ny / n, nz / n


def shade(height, light=(-0.55, -0.65, 0.52), strength=1.0, shininess=40, spec=0.0):
    nx, ny, nz = normals(height, strength)
    L = np.array(light, np.float32)
    L /= np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    out = {'diff': diff}
    if spec:
        H = L + np.array([0, 0, 1], np.float32)
        H /= np.linalg.norm(H)
        s = np.clip(nx * H[0] + ny * H[1] + nz * H[2], 0, 1) ** shininess
        out['spec'] = s * spec
    out['n'] = (nx, ny, nz)
    return out


def bevel(mask, width):
    """Rounded bevel height (0..1) inside a 0..1 mask using a distance transform."""
    m8 = (mask > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(m8, cv2.DIST_L2, 5).astype(np.float32)
    t = np.clip(d / width, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2)          # quarter-round profile
    # soften the rim so anti-aliased edges shade smoothly
    return blur(h * m8 + 0 * mask, 1.0)


def thin(mask_bool):
    """Zhang-Suen thinning (skimage.morphology is blocked on this machine). Works on the mask's bbox."""
    ys_, xs_ = np.nonzero(mask_bool)
    if len(ys_) == 0:
        return mask_bool.astype(np.uint8)
    y0, y1, x0, x1 = max(ys_.min() - 2, 0), ys_.max() + 3, max(xs_.min() - 2, 0), xs_.max() + 3
    I = mask_bool[y0:y1, x0:x1].astype(np.uint8).copy()
    while True:
        changed = False
        for step in (0, 1):
            P = np.pad(I, 1)
            p2, p3, p4 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:]
            p5, p6, p7 = P[2:, 2:], P[2:, 1:-1], P[2:, :-2]
            p8, p9 = P[1:-1, :-2], P[:-2, :-2]
            B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            A = np.zeros_like(I)
            for i in range(8):
                A += ((seq[i] == 0) & (seq[i + 1] == 1)).astype(np.uint8)
            if step == 0:
                c1, c2 = p2 * p4 * p6, p4 * p6 * p8
            else:
                c1, c2 = p2 * p4 * p8, p2 * p6 * p8
            m = (I == 1) & (B >= 2) & (B <= 6) & (A == 1) & (c1 == 0) & (c2 == 0)
            if m.any():
                I[m] = 0
                changed = True
        if not changed:
            break
    out = np.zeros(mask_bool.shape, np.uint8)
    out[y0:y1, x0:x1] = I
    return out


def drop_small(binary_u8, min_px):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(binary_u8, connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_px
    return keep[lab].astype(np.uint8)


def gradient_map(v, stops):
    """v in 0..1 -> RGB via [(pos, '#hex'), ...]."""
    pos = np.array([p for p, _ in stops], np.float32)
    cols = np.array([hex2rgb(c) for _, c in stops], np.float32)
    out = np.zeros(v.shape + (3,), np.float32)
    for ch in range(3):
        out[..., ch] = np.interp(v, pos, cols[:, ch])
    return out


def vignette(h, w, strength=0.55, power=2.2, cx=0.5, cy=0.5):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (xs / w - cx) / 0.75, (ys / h - cy) / 0.75
    r = np.sqrt(dx * dx + dy * dy)
    return np.clip(1 - strength * r ** power, 0, 1)


def radial(h, w, cx, cy, radius, power=1.6):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / radius
    return np.clip(1 - r, 0, 1) ** power


def comp(dst, color, alpha):
    """Alpha-composite a flat color or RGB array over dst."""
    a = alpha[..., None] if alpha.ndim == 2 else alpha
    c = color if isinstance(color, np.ndarray) and color.ndim == 3 else np.asarray(color, np.float32)[None, None, :]
    return dst * (1 - a) + c * a


def screen(a, b):
    return 1 - (1 - a) * (1 - b)


def to_img(rgb):
    return Image.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8))


def alpha_from_png_bytes(b):
    im = Image.open(io.BytesIO(b)).convert('RGBA')
    return np.asarray(im).astype(np.float32)[..., 3] / 255.0


def save(rgb, path, quality=92):
    im = to_img(rgb)
    if path.lower().endswith('.jpg'):
        im.save(path, quality=quality, subsampling=0, optimize=True)
    else:
        im.save(path, optimize=True)
    return path
