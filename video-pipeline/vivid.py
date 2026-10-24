"""Vivid deep-space look: saturated multi-layer nebulae with filaments and dust lanes, spiked bright stars,
galaxies, planets on vivid backdrops. Plates are rendered once in numpy, then slowly flown through."""
import math, random
import numpy as np
import cairo
import space_art as A
from scenes import W, H, clamp, ease

BG1 = (0, 0, 0)
PLATE_W, PLATE_H = 2880, 1620
_plates = {}

PALETTES = {
    "crimson": [(1.0, 0.15, 0.10), (0.95, 0.35, 0.15), (0.35, 0.05, 0.25)],
    "teal": [(0.10, 0.75, 0.95), (0.20, 0.35, 0.95), (0.55, 0.95, 0.85)],
    "violet": [(0.75, 0.30, 0.95), (0.35, 0.25, 0.95), (1.0, 0.55, 0.85)],
    "aurora": [(0.10, 0.85, 0.55), (0.15, 0.45, 0.95), (0.95, 0.85, 0.30)],
    "fire": [(1.0, 0.55, 0.10), (0.95, 0.20, 0.30), (0.25, 0.55, 0.95)],
    "ocean": [(0.05, 0.45, 0.95), (0.10, 0.85, 0.95), (0.45, 0.20, 0.85)],
    "rose": [(1.0, 0.40, 0.65), (0.55, 0.20, 0.85), (0.20, 0.60, 0.95)],
    "gold": [(1.0, 0.70, 0.15), (1.0, 0.35, 0.10), (0.20, 0.55, 1.0)],
}


def _noise(h, w, seed, octaves=8, pers=0.55):
    return A.fractal_noise(h, w, seed, octaves, pers)


def _ridged(h, w, seed, octaves=8):
    n = _noise(h, w, seed, octaves, 0.6)
    return 1 - np.abs(2 * n - 1)


def nebula_plate(seed, palette="violet", density=1.0):
    """ARGB32 surface PLATE_W x PLATE_H: black space, glowing multi-colour gas with filaments and dark dust."""
    key = (seed, palette, density)
    if key in _plates:
        return _plates[key]
    h, w = PLATE_H // 2, PLATE_W // 2
    cols = PALETTES[palette]
    base = _noise(h, w, seed, 7, 0.5)
    shape = np.clip((base - 0.47) * 3.2 * density, 0, 1) ** 1.4          # less coverage, more black space
    fil = _ridged(h, w, seed + 1, 8) ** 6                               # thin bright filaments
    fil2 = _ridged(h, w, seed + 2, 8) ** 10
    mixa = _noise(h, w, seed + 3, 4)
    mixa = np.clip((mixa - 0.5) * 2.5 + 0.5, 0, 1)
    c0, c1, c2 = (np.array(x, np.float32) for x in cols)
    hue = c0 * mixa[..., None] + c1 * (1 - mixa[..., None])
    img = shape[..., None] * hue * 0.75
    img += (shape ** 0.7 * fil)[..., None] * (hue * 0.6 + c2 * 0.9)
    img += (shape ** 0.5 * fil2)[..., None] * (c2 * 0.5 + 0.6)
    core = np.clip((_noise(h, w, seed + 5, 6) - 0.66) * 5, 0, 1) * shape
    img += core[..., None] * (hue * 0.8 + 0.35)
    dust = np.clip((_ridged(h, w, seed + 6, 7) - 0.80) * 6, 0, 1) * np.clip((_noise(h, w, seed + 7, 4) - 0.35) * 3, 0, 1)
    img *= (1 - 0.92 * dust)[..., None]
    # saturation boost around luminance, then filmic tonemap
    lum = img.mean(-1, keepdims=True)
    img = np.clip(lum + (img - lum) * 1.6, 0, None)
    # bloom: a heavily blurred copy added back gives the soft photographic glow around bright gas
    small = img[::8, ::8]
    for _ in range(3):
        small = (small + np.roll(small, 1, 0) + np.roll(small, -1, 0) + np.roll(small, 1, 1) + np.roll(small, -1, 1)) / 5
    sh, sw = small.shape[:2]
    yi, xi = np.linspace(0, sh - 1, h), np.linspace(0, sw - 1, w)
    y0, x0 = yi.astype(int), xi.astype(int)
    y1, x1 = np.minimum(y0 + 1, sh - 1), np.minimum(x0 + 1, sw - 1)
    fy, fx = (yi - y0)[:, None, None], (xi - x0)[None, :, None]
    bloom = (small[y0][:, x0] * (1 - fx) + small[y0][:, x1] * fx) * (1 - fy) + \
            (small[y1][:, x0] * (1 - fx) + small[y1][:, x1] * fx) * fy  # bilinear: smooth, no blocks
    img = img * 0.8 + bloom * 0.45
    img = 1 - np.exp(-img * 1.7)
    buf = np.zeros((h, w, 4), np.uint8)
    buf[..., 2] = np.clip(img[..., 0] * 255, 0, 255)
    buf[..., 1] = np.clip(img[..., 1] * 255, 0, 255)
    buf[..., 0] = np.clip(img[..., 2] * 255, 0, 255)
    buf[..., 3] = 255
    small = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h)
    plate = cairo.ImageSurface(cairo.FORMAT_RGB24, PLATE_W, PLATE_H)
    c = cairo.Context(plate)
    c.scale(2, 2)
    c.set_source_surface(small, 0, 0)
    c.get_source().set_filter(cairo.FILTER_BEST)
    c.paint()
    c.identity_matrix()
    star_field(c, PLATE_W, PLATE_H, seed, n=3500)
    plate.flush()
    _plates[key] = plate
    return plate


def spiky_star(c, x, y, r, col=(1, 1, 1), a=1.0, spikes=True):
    A.glow(c, x, y, r * 9, col, 0.30 * a)
    A.glow(c, x, y, r * 3, col, 0.65 * a)
    c.set_source_rgba(1, 1, 1, a)
    c.arc(x, y, r * 0.9, 0, 2 * math.pi)
    c.fill()
    if spikes:
        for ang, L in ((0, r * 16), (math.pi / 2, r * 16)):
            for sgn in (1, -1):
                g = cairo.LinearGradient(x, y, x + math.cos(ang) * L * sgn, y + math.sin(ang) * L * sgn)
                g.add_color_stop_rgba(0, *col, 0.8 * a)
                g.add_color_stop_rgba(1, *col, 0)
                c.set_source(g)
                c.set_line_width(max(1.0, r * 0.35))
                c.move_to(x, y)
                c.line_to(x + math.cos(ang) * L * sgn, y + math.sin(ang) * L * sgn)
                c.stroke()


def star_field(c, w, h, seed, n=3000):
    r = random.Random(seed * 7 + 1)
    for i in range(n):
        x, y = r.random() * w, r.random() * h
        m = r.random() ** 9
        size = 0.5 + m * 3.5
        col = r.choice([(1, 1, 1), (0.8, 0.88, 1.0), (1.0, 0.9, 0.75), (0.75, 0.85, 1.0)])
        if size > 3.7:
            spiky_star(c, x, y, size * 0.7, col, 0.85)
        else:
            c.set_source_rgba(*col, 0.35 + 0.65 * r.random())
            c.arc(x, y, size * 0.6, 0, 2 * math.pi)
            c.fill()


def fly(c, plate, t, d, zoom0=1.0, zoom1=1.25, pan=(0.0, 0.0)):
    """Slow push-in through a plate, with a gentle drift."""
    f = t / d
    z = zoom0 + (zoom1 - zoom0) * f
    s = max(W / PLATE_W, H / PLATE_H) * z * 1.05
    cx = PLATE_W / 2 + pan[0] * PLATE_W * (f - 0.5)
    cy = PLATE_H / 2 + pan[1] * PLATE_H * (f - 0.5)
    c.save()
    c.translate(W / 2, H / 2)
    c.scale(s, s)
    c.translate(-cx, -cy)
    c.set_source_surface(plate, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    c.restore()


def twinkle_stars(c, T, seed, n=5):
    r = random.Random(seed + 99)
    for i in range(n):
        x, y = r.random() * W, r.random() * H
        tw = 0.6 + 0.4 * math.sin(T * (0.4 + r.random() * 0.5) + i)
        spiky_star(c, x, y, 1.6 + r.random() * 2.2, r.choice([(1, 1, 1), (0.8, 0.9, 1.0), (1, 0.9, 0.8)]), tw)


# ---------- scenes (build.py interface) ----------
import space_scenes as SP
from scenes import prog
from collections import OrderedDict

_lru = OrderedDict()


def plate(seed, palette, density=1.0):
    """LRU-limited plate cache so long renders don't hold hundreds of 18 MB plates."""
    key = (seed, palette, density)
    if key in _lru:
        _lru.move_to_end(key)
        return _lru[key]
    p = nebula_plate(seed, palette, density)
    _plates.pop(key, None)
    _lru[key] = p
    while len(_lru) > 4:
        _lru.popitem(last=False)
    return p


def _bg(c, t, d, T, a, z0=1.0, z1=1.2):
    fly(c, plate(a["seed"], a["pal"], a.get("density", 1.0)), t, d, z0, z1, a.get("pan", (0.0, 0.0)))
    twinkle_stars(c, T, a["seed"])


def sc_nebula(c, t, d, T, a):
    z0, z1 = (1.0, 1.28) if a.get("push", True) else (1.28, 1.0)
    _bg(c, t, d, T, a, z0, z1)


def sc_planet(c, t, d, T, a):
    _bg(c, t, d, T, a, 1.0, 1.08)
    body = a["body"]
    R = int(a.get("size", 380) * (1 + 0.06 * t / d))
    cx, cy = W * a.get("x", 0.62), H * a.get("y", 0.55)
    if a.get("rings"):
        A.rings(c, cx, cy, R, tilt=0.26, angle=-0.3, front=False)
    A.glow(c, cx, cy, R * 1.3, a.get("atm", (0.6, 0.75, 1.0)), 0.30)
    SP.paint_sphere(c, body, cx, cy, R, T * 0.006, light=(-0.65, -0.35, 0.68), tilt=0.15,
                    clouds_phase=T * 0.007 if body == "earth" else None)
    if a.get("rings"):
        A.rings(c, cx, cy, R, tilt=0.26, angle=-0.3, front=True)


def sc_horizon(c, t, d, T, a):
    """Sunrise over a planet's limb: dark curved horizon, glowing atmosphere, a star rising with a flare."""
    _bg(c, t, d, T, a, 1.0, 1.05)
    R = 2600
    cx, cy = W / 2, H + R - 330 + 40 * (1 - ease(t / d))
    rise = ease(t / d)
    sx, sy = W / 2 + 60, cy - R - 30 - 90 * rise
    A.glow(c, sx, sy, 900, (0.45, 0.75, 1.0), 0.35 * (0.4 + 0.6 * rise))
    A.glow(c, sx, sy, 260, (0.85, 0.95, 1.0), 0.8 * (0.3 + 0.7 * rise))
    spiky_star(c, sx, sy, 9 + 6 * rise, (0.9, 0.97, 1.0), 0.6 + 0.4 * rise)
    g = cairo.RadialGradient(cx, cy, R - 6, cx, cy, R + 60)
    g.add_color_stop_rgba(0, 0.35, 0.75, 1.0, 0.9)
    g.add_color_stop_rgba(0.3, 0.25, 0.55, 1.0, 0.6)
    g.add_color_stop_rgba(1, 0.1, 0.3, 0.9, 0)
    c.set_source(g)
    c.arc(cx, cy, R + 60, 0, 2 * math.pi)
    c.fill()
    lg = cairo.LinearGradient(0, cy - R, 0, cy - R + 400)
    lg.add_color_stop_rgb(0, 0.04, 0.07, 0.14)
    lg.add_color_stop_rgb(1, 0.0, 0.0, 0.02)
    c.set_source(lg)
    c.arc(cx, cy, R, 0, 2 * math.pi)
    c.fill()


def sc_galaxy(c, t, d, T, a):
    _bg(c, t, d, T, dict(a, density=a.get("density", 0.3)), 1.0, 1.06)
    SP.sc_galaxy(c, t, d, T, dict(seed=a.get("gseed", 3), scale=a.get("scale", 560), tilt=a.get("tilt", 0.38),
                                  neb=0, arms=a.get("arms", 2), no_bg=True))


def sc_ring(c, t, d, T, a):
    _bg(c, t, d, T, dict(a, density=0.5), 1.0, 1.08)
    cx, cy = W / 2, H / 2
    grow = 1 + 0.1 * t / d
    cols = PALETTES[a["pal"]]
    # soft overlapping shells whose colours blend, like a planetary nebula photo
    shells = [(420, cols[0], 0.22, 0.45), (360, cols[1], 0.20, 0.35), (300, cols[0], 0.18, 0.40),
              (240, cols[2], 0.20, 0.45), (170, (0.6, 0.85, 1.0), 0.16, 0.55)]
    for rad, col, al, width in shells:
        g = cairo.RadialGradient(cx, cy, rad * grow * (1 - width), cx, cy, rad * grow)
        g.add_color_stop_rgba(0, *col, 0)
        g.add_color_stop_rgba(0.6, *col, al)
        g.add_color_stop_rgba(1, *col, 0)
        c.save(); c.translate(cx, cy); c.rotate(0.3); c.scale(1.15, 0.9); c.translate(-cx, -cy)
        c.set_source(g); c.arc(cx, cy, rad * grow, 0, 2 * math.pi); c.fill(); c.restore()
    A.glow(c, cx, cy, 40, (0.85, 0.95, 1.0), 0.9)
    spiky_star(c, cx, cy, 4, (0.9, 0.95, 1.0), 1.0)


def vignette(c):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.55, W / 2, H / 2, H * 1.15)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.35)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


def snowfall(c, T, amount=1.0, wind=1.0):
    pass


INK = (1, 1, 1)


def text(c, s, x, y, size=48, col=INK, a=1.0, align="center", bold=True, italic=False):
    A.text(c, s, x, y, size, col, a, bold=bold, italic=italic)


SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_")}


# ---------- real telescope photographs (ESA/Hubble, ESA/Webb; CC BY 4.0) ----------
import os
TELESCOPE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "telescope")
_photos = OrderedDict()


def photo(name, max_w=4096):
    """Load a telescope JPEG (PIL), downscaled to at most max_w wide, as a cairo surface; LRU of 3."""
    if name in _photos:
        _photos.move_to_end(name)
        return _photos[name]
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(os.path.join(TELESCOPE_DIR, name + ".jpg")).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    arr = np.asarray(im)
    buf = np.zeros((im.height, im.width, 4), np.uint8)
    buf[..., 0], buf[..., 1], buf[..., 2], buf[..., 3] = arr[..., 2], arr[..., 1], arr[..., 0], 255
    src = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, im.width, im.height)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, im.width, im.height)
    cc = cairo.Context(surf)
    cc.set_source_surface(src, 0, 0)
    cc.paint()
    surf.flush()
    _photos[name] = surf
    while len(_photos) > 3:
        _photos.popitem(last=False)
    return surf


def sc_photo(c, t, d, T, a):
    """Slow Ken Burns move across a telescope image: zoom z0->z1 while the centre drifts c0->c1."""
    img = photo(a["img"])
    iw, ih = img.get_width(), img.get_height()
    f = ease(t / d) * 0.85 + 0.15 * t / d
    (z0, x0, y0), (z1, x1, y1) = a["cam"]
    z = z0 + (z1 - z0) * f
    cx, cy = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
    s = max(W / iw, H / ih) * z
    vw, vh = W / s, H / s
    ox = clamp(cx * iw - vw / 2, 0, iw - vw)
    oy = clamp(cy * ih - vh / 2, 0, ih - vh)
    c.save()
    c.scale(s, s)
    c.translate(-ox, -oy)
    c.set_source_surface(img, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    c.restore()


SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_")}
