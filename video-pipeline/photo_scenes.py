"""Illustration-based scenes: slow pan/zoom over a still image plus light ambient overlays."""
import math, os
import cairo
from scenes import W, H, clamp, ease, prog, rgba, text, text_w, rrect
import cozy_scenes as C

INK = C.INK
BG1 = (0.05, 0.05, 0.06)
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
_cache = {}


def load(path):
    if path not in _cache:
        if path.lower().endswith(".png"):
            _cache[path] = cairo.ImageSurface.create_from_png(path)
        else:  # jpg/webp: convert once to png next to the original
            png = path.rsplit(".", 1)[0] + "_conv.png"
            if not os.path.exists(png):
                import subprocess
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, png], check=True)
            _cache[path] = cairo.ImageSurface.create_from_png(png)
    return _cache[path]


# pan/zoom moves, chosen per image number so neighbouring shots move differently
MOVES = [((1.00, 0.50, 0.50), (1.10, 0.50, 0.45)),   # slow push in
         ((1.10, 0.40, 0.50), (1.10, 0.60, 0.50)),   # pan right
         ((1.12, 0.50, 0.45), (1.02, 0.50, 0.50)),   # pull out
         ((1.10, 0.60, 0.50), (1.10, 0.40, 0.52))]   # pan left


def dust(c, T, a=0.5):
    for i, (rx, ry, ph) in enumerate(C.FLIES[:45]):
        x = (rx * W + 25 * math.sin(T * 0.15 + ph)) % W
        y = (ry * H - T * 6 * (0.5 + rx)) % H
        rgba(c, (1, 0.97, 0.85), a * (0.3 + 0.4 * (0.5 + 0.5 * math.sin(T * 0.7 + ph))))
        c.arc(x, y, 1.5 + 2 * ry, 0, 2 * math.pi)
        c.fill()


def sc_photo(c, t, d, T, a):
    img = load(os.path.join(IMG_DIR, a["img"]))
    iw, ih = img.get_width(), img.get_height()
    (z0, x0, y0), (z1, x1, y1) = MOVES[a.get("move", 0) % len(MOVES)]
    f = ease(t / d) * 0.9 + 0.1 * (t / d)
    z = z0 + (z1 - z0) * f
    cx = x0 + (x1 - x0) * f
    cy = y0 + (y1 - y0) * f
    base = max(W / iw, H / ih)
    s = base * z
    vw, vh = W / s, H / s  # visible window in image pixels
    ox = clamp(cx * iw - vw / 2, 0, iw - vw)
    oy = clamp(cy * ih - vh / 2, 0, ih - vh)
    c.save()
    c.scale(s, s)
    c.translate(-ox, -oy)
    c.set_source_surface(img, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    c.restore()
    fx = a.get("fx", ())
    if "rain" in fx:
        C.rain_lines(c, T, 0, 0, W, H, 0.7, 0.28)
    if "glass" in fx:
        C.glass_drops(c, T, 0, 0, W, H, 0.6)
    if "dust" in fx:
        dust(c, T, 0.45)
    if "fireflies" in fx:
        C.fireflies(c, T, 0, H * 0.45, W, H * 0.5, 45, 0.9)
    if "night" in fx:
        rgba(c, (0.02, 0.03, 0.08), 0.25 + 0.25 * prog(t, 0, d))
        c.rectangle(0, 0, W, H)
        c.fill()
    if a.get("title"):
        ap = prog(t, 0.8, 2.5) * (1 - prog(t, d - 2.5, d - 0.5))
        rgba(c, (0.1, 0.08, 0.06), 0.35 * ap)
        rrect(c, W / 2 - 700, 70, 1400, 250, 40)
        c.fill()
        C.serif(c, a["title"][0], W / 2, 180, 72, INK, ap)
        C.serif(c, a["title"][1], W / 2, 270, 44, (1, 0.93, 0.75), ap, bold=False, italic=True)


def vignette(c):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 1.1)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.05, 0.02, 0.0, 0.35)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


def snowfall(c, T, amount=1.0, wind=1.0):
    pass


SCENES = {"photo": sc_photo}
