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


def draw_image(c, a, f, alpha=1.0):
    """Draw image a["img"] at camera progress f (0..1) along a["cam"] = ((z, x, y), (z, x, y))."""
    img = load(os.path.join(IMG_DIR, a["img"]))
    iw, ih = img.get_width(), img.get_height()
    (z0, x0, y0), (z1, x1, y1) = a.get("cam") or MOVES[a.get("move", 0) % len(MOVES)]
    z = z0 + (z1 - z0) * f
    cx = x0 + (x1 - x0) * f
    cy = y0 + (y1 - y0) * f
    s = max(W / iw, H / ih) * z
    vw, vh = W / s, H / s
    ox = clamp(cx * iw - vw / 2, 0, iw - vw)
    oy = clamp(cy * ih - vh / 2, 0, ih - vh)
    c.save()
    c.scale(s, s)
    c.translate(-ox, -oy)
    c.set_source_surface(img, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint_with_alpha(alpha)
    c.restore()
    return lambda nx, ny: ((nx * iw - ox) * s, (ny * ih - oy) * s, s)


def flicker(c, T, pos, size, col, a):
    x, y, s = pos
    k = 0.75 + 0.15 * math.sin(T * 7.1) + 0.10 * math.sin(T * 13.7 + 1.3)
    g = cairo.RadialGradient(x, y, 2, x, y, size * s)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.28 * k * a)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g)
    c.arc(x, y, size * s, 0, 2 * math.pi)
    c.fill()


LEAVES = [(i * 0.137 % 1, i * 0.291 % 1, i * 0.53 % 1) for i in range(40)]


def overlays(c, t, T, a, to_screen):
    """Moving rain inside window boxes, drops on glass, falling leaves and rising sparks."""
    for box in a.get("windows", ()):
        x0, y0, x1, y1, kind = box
        sx0, sy0, _ = to_screen(x0, y0)
        sx1, sy1, _ = to_screen(x1, y1)
        w, h = sx1 - sx0, sy1 - sy0
        if w < 20 or h < 20:
            continue
        area = w * h / (W * H)
        C.rain_lines(c, T, sx0, sy0, w, h, min(1.0, 0.35 + area), 0.30 if kind == "glass" else 0.40)
        if kind == "glass":
            C.glass_drops(c, T * 0.8, sx0, sy0, w, h, min(1.0, 0.25 + area))
        if "leaves" in a.get("fx", ()):
            c.save(); c.rectangle(sx0, sy0, w, h); c.clip()
            for i, (rx, ry, ph) in enumerate(LEAVES[:14]):
                fy = (ry + T * (0.025 + 0.02 * rx)) % 1.0
                lx = sx0 + (rx + 0.08 * math.sin(T * 0.9 + ph * 6)) % 1.0 * w
                ly = sy0 + fy * h
                c.save(); c.translate(lx, ly); c.rotate(T * (1 + rx) + ph * 6); c.scale(1, 0.55)
                rgba(c, (0.85, 0.42 + 0.2 * rx, 0.15), 0.85)
                c.arc(0, 0, 7 + 5 * ry, 0, 2 * math.pi); c.fill(); c.restore()
            c.restore()
    for lx, ly, kind in a.get("lamps", ()):
        if kind != "fire":
            continue
        x, y, s = to_screen(lx, ly)
        for i in range(14):
            ph = i * 1.37
            f = (T * (0.35 + 0.05 * (i % 4)) + i / 14) % 1.0
            px = x + (40 * math.sin(ph * 3) + 25 * math.sin(T * 2 + ph)) * f * s
            py = y - 260 * f * s
            rgba(c, (1.0, 0.65 + 0.25 * (i % 2), 0.25), 0.9 * (1 - f) * (0.6 + 0.4 * math.sin(T * 9 + ph)))
            c.arc(px, py, (2.2 - 1.2 * f) * max(1, s), 0, 2 * math.pi)
            c.fill()


def sc_photo(c, t, d, T, a):
    f = t / d
    to_screen = draw_image(c, a, f)
    xf = a.get("xfade", 0.0)
    if a.get("prev") and t < xf:  # dissolve from the previous shot's last frame
        draw_image(c, a["prev"], 1.0, 1 - ease(t / xf))
    alpha_in = ease(t / xf) if (a.get("prev") and t < xf) else 1.0
    c.push_group()
    overlays(c, t, T, a, to_screen)
    c.pop_group_to_source()
    c.paint_with_alpha(alpha_in)
    for lx, ly, kind in a.get("lamps", ()):
        col = (1.0, 0.55, 0.20) if kind == "fire" else (1.0, 0.78, 0.40)
        alpha = 1.0 if not (a.get("prev") and t < xf) else ease(t / xf)
        flicker(c, T, to_screen(lx, ly), 260 if kind == "fire" else 200, col, alpha)
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
    if a.get("fade_in"):
        rgba(c, (0, 0, 0), 1 - ease(t / a["fade_in"]))
        c.rectangle(0, 0, W, H)
        c.fill()
    if a.get("fade_out"):
        rgba(c, (0, 0, 0), ease((t - (d - a["fade_out"])) / a["fade_out"]))
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
