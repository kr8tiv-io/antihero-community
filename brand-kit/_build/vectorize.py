"""
AntiHero logo reconstruction.

The circle-A is rebuilt from measured geometry (exact arcs and lines).
The hand-lettered "hero" is traced from the source bitmap: sub-pixel iso-contours,
light arc-length smoothing, then least-squares cubic Bezier fitting (Schneider).

Output: master/antihero-mark-paths.json  (path data in a 1000x1000 space, disc r=500)
"""
import json
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import measure

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work')
OUT = os.path.join(HERE, 'master')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Measured geometry (normalised to disc radius = 1, v axis points down)
# ---------------------------------------------------------------------------
STROKE = 0.1581                 # ring / diagonal / crossbar share one weight
RO = 0.7467                     # ring outer radius
RI = RO - STROKE                # ring inner radius
CUT = -0.0142                   # vertical cut line (right edge of the A group)
DIAG_ANGLE = math.radians(24.71)  # from vertical, leaning right as it rises
DIAG_AXIS_AT_CUT = -0.600       # diagonal centre line crosses the cut line here
BAR_TOP = -0.0144
BAR_BOT = BAR_TOP + STROKE

K = 500.0                       # 1000-unit artboard, centre (500, 500)


def to_px(u, v):
    return (500.0 + u * K, 500.0 + v * K)


def fmt(x):
    s = f'{x:.2f}'.rstrip('0').rstrip('.')
    return s if s != '-0' else '0'


def P(u, v):
    x, y = to_px(u, v)
    return f'{fmt(x)} {fmt(y)}'


# diagonal: direction pointing down-left
d = np.array([-math.sin(DIAG_ANGLE), math.cos(DIAG_ANGLE)])
n = np.array([d[1], -d[0]])            # normal pointing right/up
axis_pt = np.array([CUT, DIAG_AXIS_AT_CUT])
left_pt = axis_pt - n * STROKE / 2     # left (outer) edge of the leg
right_pt = axis_pt + n * STROKE / 2    # right (counter-side) edge of the leg


def line_at_u(p, u):
    t = (u - p[0]) / d[0]
    return p + t * d


def line_at_v(p, v):
    t = (v - p[1]) / d[1]
    return p + t * d


def line_circle(p, r, which):
    # intersections of p + t d with circle radius r, sorted by t
    b = np.dot(p, d)
    c = np.dot(p, p) - r * r
    disc = b * b - c
    t1, t2 = -b - math.sqrt(disc), -b + math.sqrt(disc)
    return p + (t1 if which == 0 else t2) * d


CA = line_at_u(right_pt, CUT)                  # apex of the counter
X1 = line_at_v(right_pt, BAR_TOP)              # counter meets bar top
X2 = line_at_v(right_pt, BAR_BOT)              # bar bottom meets leg
X3 = line_circle(right_pt, RI, 1)              # leg's right edge meets inner ring (lower-left)
L_TOP = line_circle(left_pt, RI, 0)            # lens tip, top
L_BOT = line_circle(left_pt, RI, 1)            # lens tip, bottom
T_OUT = (CUT, -math.sqrt(RO**2 - CUT**2))
B_IN = (CUT, math.sqrt(RI**2 - CUT**2))
B_OUT = (CUT, math.sqrt(RO**2 - CUT**2))

ro, ri = RO * K, RI * K
# Outer contour, clockwise on screen: top of cut -> down the cut -> counter -> bar -> leg -> inner arc -> cut -> big outer arc
a_outer = (
    f'M{P(*T_OUT)}'
    f'L{P(*CA)}'
    f'L{P(*X1)}'
    f'L{P(CUT, BAR_TOP)}'
    f'L{P(CUT, BAR_BOT)}'
    f'L{P(*X2)}'
    f'L{P(*X3)}'
    # inner circle from X3 (lower-left) to B_IN (bottom) : moving right along the bottom = counter-clockwise on screen
    f'A{fmt(ri)} {fmt(ri)} 0 0 0 {P(*B_IN)}'
    f'L{P(*B_OUT)}'
    # outer circle from bottom, round the left side, back to top: clockwise on screen.
    # The cut sits left of centre, so this arc spans just under 180 deg -> small-arc flag.
    f'A{fmt(ro)} {fmt(ro)} 0 0 1 {P(*T_OUT)}Z'
)
# Lens hole (left of the leg): inner arc from L_TOP round the left to L_BOT, then straight back up
a_lens = (
    f'M{P(*L_TOP)}'
    f'A{fmt(ri)} {fmt(ri)} 0 0 0 {P(*L_BOT)}'
    f'L{P(*L_TOP)}Z'
)
A_PATH = a_outer + a_lens

# ---------------------------------------------------------------------------
# 2. Trace the lettering
# ---------------------------------------------------------------------------
cx, cy, R, S = np.load(os.path.join(WORK, 'geom.npy'))
src = Image.open(os.path.join(WORK, 'source_logo.png')).convert('L')
big = src.resize((src.width * int(S), src.height * int(S)), Image.BICUBIC)
g = ndi.gaussian_filter(np.asarray(big).astype(float), 3.0)
LEVEL = 139.0


def resample_closed(pts, step):
    Pp = np.vstack([pts, pts[:1]])
    seg = np.hypot(*np.diff(Pp, axis=0).T)
    L = np.r_[0, np.cumsum(seg)]
    nn = max(12, int(round(L[-1] / step)))
    s = np.linspace(0, L[-1], nn, endpoint=False)
    return np.c_[np.interp(s, L, Pp[:, 0]), np.interp(s, L, Pp[:, 1])]


def signed_area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


# --- Schneider cubic fitting -------------------------------------------------
def bez_q(b, t):
    mt = 1 - t
    return (mt**3)[:, None] * b[0] + (3 * mt**2 * t)[:, None] * b[1] + (3 * mt * t**2)[:, None] * b[2] + (t**3)[:, None] * b[3]


def bez_qprime(b, t):
    mt = 1 - t
    return (3 * mt**2)[:, None] * (b[1] - b[0]) + (6 * mt * t)[:, None] * (b[2] - b[1]) + (3 * t**2)[:, None] * (b[3] - b[2])


def bez_qprimeprime(b, t):
    mt = 1 - t
    return (6 * mt)[:, None] * (b[2] - 2 * b[1] + b[0]) + (6 * t)[:, None] * (b[3] - 2 * b[2] + b[1])


def chord_params(pts):
    dd = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    return dd / dd[-1]


def gen_bezier(pts, u, t1, t2):
    p0, p3 = pts[0], pts[-1]
    A1 = (3 * (1 - u)**2 * u)[:, None] * t1
    A2 = (3 * (1 - u) * u**2)[:, None] * t2
    C = np.array([[np.sum(A1 * A1), np.sum(A1 * A2)], [np.sum(A1 * A2), np.sum(A2 * A2)]])
    base = bez_q(np.array([p0, p0, p3, p3]), u)
    tmp = pts - base
    X = np.array([np.sum(A1 * tmp), np.sum(A2 * tmp)])
    det = C[0, 0] * C[1, 1] - C[0, 1] * C[1, 0]
    seg = np.linalg.norm(p3 - p0)
    if abs(det) > 1e-12:
        a1 = (X[0] * C[1, 1] - X[1] * C[0, 1]) / det
        a2 = (C[0, 0] * X[1] - C[1, 0] * X[0]) / det
    else:
        a1 = a2 = seg / 3
    eps = 1e-6 * seg
    if a1 < eps or a2 < eps:
        a1 = a2 = seg / 3
    return np.array([p0, p0 + t1 * a1, p3 + t2 * a2, p3])


def max_err(pts, b, u):
    dd = np.linalg.norm(bez_q(b, u) - pts, axis=1)
    i = int(np.argmax(dd))
    return dd[i], i


def reparam(b, pts, u):
    q = bez_q(b, u) - pts
    q1 = bez_qprime(b, u)
    q2 = bez_qprimeprime(b, u)
    num = np.sum(q * q1, axis=1)
    den = np.sum(q1 * q1, axis=1) + np.sum(q * q2, axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        nu = np.where(np.abs(den) > 1e-12, u - num / den, u)
    return np.clip(nu, 0, 1)


def fit_cubic(pts, t1, t2, err):
    if len(pts) == 2:
        dist = np.linalg.norm(pts[1] - pts[0]) / 3
        return [np.array([pts[0], pts[0] + t1 * dist, pts[1] + t2 * dist, pts[1]])]
    u = chord_params(pts)
    b = gen_bezier(pts, u, t1, t2)
    e, split = max_err(pts, b, u)
    if e < err:
        return [b]
    if e < err * 4:
        for _ in range(24):
            u = reparam(b, pts, u)
            b = gen_bezier(pts, u, t1, t2)
            e, split = max_err(pts, b, u)
            if e < err:
                return [b]
    split = min(max(split, 1), len(pts) - 2)
    tc = pts[split - 1] - pts[split + 1]
    tc = tc / (np.linalg.norm(tc) + 1e-12)
    return fit_cubic(pts[:split + 1], t1, tc, err) + fit_cubic(pts[split:], -tc, t2, err)


def unit(v):
    return v / (np.linalg.norm(v) + 1e-12)


CORNER_K = int(os.environ.get('AH_CK', 9))
CORNER_T = float(os.environ.get('AH_CT', 62))
SMOOTH = float(os.environ.get('AH_SM', 6.0))
FIT_ERR = float(os.environ.get('AH_ERR', 0.9))


def corners(p, k=None, thresh_deg=None):
    k = k or CORNER_K
    thresh_deg = thresh_deg or CORNER_T
    n_ = len(p)
    # measure turning on a lightly pre-smoothed copy so pixel noise never reads as a corner
    p = np.c_[ndi.gaussian_filter1d(p[:, 0], 2.0, mode='wrap'), ndi.gaussian_filter1d(p[:, 1], 2.0, mode='wrap')]
    a = p - np.roll(p, k, axis=0)
    b = np.roll(p, -k, axis=0) - p
    ang = np.degrees(np.arccos(np.clip(np.sum(a * b, 1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + 1e-12), -1, 1)))
    cand = [i for i in range(n_) if ang[i] > thresh_deg and ang[i] >= ang[(i - 1) % n_] and ang[i] >= ang[(i + 1) % n_]]
    # non-max suppression within k
    out = []
    for i in sorted(cand, key=lambda i: -ang[i]):
        if all(min(abs(i - j), n_ - abs(i - j)) > k for j in out):
            out.append(i)
    return sorted(out), ang


def fit_closed(p, err, smooth_sigma):
    # smooth (wrap) but keep strong corners crisp
    cidx, _ = corners(p)
    if not cidx:
        ps = np.c_[ndi.gaussian_filter1d(p[:, 0], smooth_sigma, mode='wrap'),
                   ndi.gaussian_filter1d(p[:, 1], smooth_sigma, mode='wrap')]
        # start at the point of highest curvature to hide the seam
        start = 0
        ps = np.roll(ps, -start, axis=0)
        closed = np.vstack([ps, ps[:1]])
        t1 = unit(ps[1] - ps[-1])
        segs = fit_cubic(closed, t1, -t1, err)
        return segs, []
    segs_all = []
    n_ = len(p)
    corner_pts = []
    for ci in range(len(cidx)):
        i0, i1 = cidx[ci], cidx[(ci + 1) % len(cidx)]
        idx = np.arange(i0, i1 + (n_ if i1 <= i0 else 0) + 1) % n_
        seg = p[idx]
        if len(seg) > 6:
            sm = np.c_[ndi.gaussian_filter1d(seg[:, 0], smooth_sigma, mode='nearest'),
                       ndi.gaussian_filter1d(seg[:, 1], smooth_sigma, mode='nearest')]
            sm[0], sm[-1] = seg[0], seg[-1]
            # blend ends back toward the raw corner so the corner stays sharp
            seg = sm
        m = min(4, len(seg) - 1)
        t1 = unit(seg[m] - seg[0])
        t2 = unit(seg[-1 - m] - seg[-1])
        segs_all += fit_cubic(seg, t1, t2, err)
        corner_pts.append(p[i0])
    return segs_all, corner_pts


def to_d(segs):
    b0 = segs[0]
    x, y = b0[0]
    out = [f'M{fmt(x)} {fmt(y)}']
    for b in segs:
        out.append('C' + ' '.join(f'{fmt(q[0])} {fmt(q[1])}' for q in b[1:]))
    out.append('Z')
    return ''.join(out)


contours = measure.find_contours(g, LEVEL)
hero_d = []
stats = []
corner_log = []
for c in contours:
    u = (c[:, 1] - cx) / R
    v = (c[:, 0] - cy) / R
    if u.min() < 0.02:          # A group / page edge -> skip (A is rebuilt analytically)
        continue
    if (u**2 + v**2).max() > 0.985**2:   # disc boundary contour
        continue
    pts = np.c_[500 + u * K, 500 + v * K]
    if len(pts) < 20:
        continue
    pts = resample_closed(pts, 0.8)
    segs, cps = fit_closed(pts, err=FIT_ERR, smooth_sigma=SMOOTH)
    hero_d.append(to_d(segs))
    corner_log.extend([list(map(float, c_)) for c_ in cps])
    stats.append((len(pts), len(segs), len(cps), round(abs(signed_area(pts)))))

HERO_PATH = ''.join(hero_d)
bbox_pts = []
for c in contours:
    u = (c[:, 1] - cx) / R
    v = (c[:, 0] - cy) / R
    if u.min() >= 0.02 and (u**2 + v**2).max() <= 0.985**2:
        bbox_pts.append(np.c_[500 + u * K, 500 + v * K])
bb = np.vstack(bbox_pts)
info = {
    'viewBox': '0 0 1000 1000',
    'disc': {'cx': 500, 'cy': 500, 'r': 500},
    'stroke': STROKE * K, 'ring_outer': ro, 'ring_inner': ri, 'cut_x': 500 + CUT * K,
    'diag_angle_deg': math.degrees(DIAG_ANGLE),
    'hero_bbox': [float(bb[:, 0].min()), float(bb[:, 1].min()), float(bb[:, 0].max()), float(bb[:, 1].max())],
    'a_path': A_PATH, 'hero_path': HERO_PATH,
    'hero_contours': stats,
    'hero_corners': corner_log,
}
with open(os.path.join(OUT, 'antihero-mark-paths.json'), 'w') as f:
    json.dump(info, f, indent=1)
print('A path length', len(A_PATH), '| hero contours', stats, '| hero bbox', [round(x, 1) for x in info['hero_bbox']])
