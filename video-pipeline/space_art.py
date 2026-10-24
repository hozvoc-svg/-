"""Procedural space art (stars, nebulae, planets, rings, glows) shared by channel branding and space episodes."""
import math, random
import cairo
import numpy as np


def fractal_noise(h, w, seed=0, octaves=6, persistence=0.55):
    """Smooth fractal noise in [0, 1] built from upsampled random grids."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        gh, gw = 3 * 2 ** o + 1, int((3 * 2 ** o) * w / h) + 2
        grid = rng.random((gh, gw)).astype(np.float32)
        ys = np.linspace(0, gh - 1.001, h)
        xs = np.linspace(0, gw - 1.001, w)
        y0 = ys.astype(int); x0 = xs.astype(int)
        fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
        fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
        a = grid[y0][:, x0]; b = grid[y0][:, x0 + 1]
        c = grid[y0 + 1][:, x0]; d = grid[y0 + 1][:, x0 + 1]
        out += amp * ((a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy)
        total += amp
        amp *= persistence
    return out / total


def nebula_surface(w, h, seed=1, colors=((0.20, 0.10, 0.45), (0.10, 0.35, 0.60), (0.75, 0.25, 0.55)),
                   strength=1.0, scale=1.0):
    """ARGB surface with a soft multi-colour nebula (premultiplied alpha)."""
    sh, sw = max(8, int(h / 2 * scale)), max(8, int(w / 2 * scale))
    n1 = fractal_noise(sh, sw, seed)
    n2 = fractal_noise(sh, sw, seed + 7)
    n3 = fractal_noise(sh, sw, seed + 13)
    dens = np.clip((n1 - 0.42) * 2.6, 0, 1) ** 1.6 * strength
    rgb = np.zeros((sh, sw, 3), np.float32)
    mix = np.stack([n2, n3, 1 - n2], -1)
    mix /= mix.sum(-1, keepdims=True)
    for k, col in enumerate(colors):
        rgb += mix[..., k:k + 1] * np.array(col, np.float32)
    a = np.clip(dens, 0, 1)
    buf = np.zeros((sh, sw, 4), np.uint8)
    buf[..., 0] = np.clip(rgb[..., 2] * a * 255, 0, 255)
    buf[..., 1] = np.clip(rgb[..., 1] * a * 255, 0, 255)
    buf[..., 2] = np.clip(rgb[..., 0] * a * 255, 0, 255)
    buf[..., 3] = np.clip(a * 255, 0, 255)
    small = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, sw, sh)
    big = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(big)
    c.scale(w / sw, h / sh)
    c.set_source_surface(small, 0, 0)
    c.get_source().set_filter(cairo.FILTER_BEST)
    c.paint()
    big.flush()
    del c, small, buf  # pixels are copied into `big`, so the numpy-backed surface can go
    return big


def background(c, w, h, top=(0.02, 0.02, 0.07), bot=(0.05, 0.04, 0.14)):
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(0, 0, w, h)
    c.fill()


def stars(c, w, h, n=900, seed=3, t=0.0, scale=1.0):
    r = random.Random(seed)
    for i in range(n):
        x, y = r.random() * w, r.random() * h
        size = (r.random() ** 6 * 2.6 + 0.4) * scale
        tw = 0.65 + 0.35 * math.sin(t * (0.5 + r.random()) + i)
        warm = r.random()
        col = (1.0, 0.92, 0.80) if warm < 0.15 else (0.80, 0.88, 1.0) if warm > 0.8 else (1, 1, 1)
        c.set_source_rgba(*col, (0.35 + 0.65 * r.random()) * tw)
        c.arc(x, y, size, 0, 2 * math.pi)
        c.fill()
        if size > 2.2 * scale:
            glow(c, x, y, size * 7, col, 0.25 * tw)


def glow(c, x, y, r, col=(1, 1, 1), a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def planet(c, x, y, r, base=(0.85, 0.55, 0.35), dark=(0.25, 0.10, 0.08), light_dir=(-0.6, -0.5),
           bands=0, band_col=(0.95, 0.80, 0.60), seed=0, atmosphere=(0.6, 0.75, 1.0), atm=0.35):
    """Lit sphere with optional bands and a thin atmosphere rim."""
    glow(c, x, y, r * 1.35, atmosphere, atm * 0.6)
    c.save()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    lx, ly = x + light_dir[0] * r * 0.6, y + light_dir[1] * r * 0.6
    g = cairo.RadialGradient(lx, ly, r * 0.05, x, y, r * 1.05)
    g.add_color_stop_rgb(0, *[min(1, v * 1.25) for v in base])
    g.add_color_stop_rgb(0.55, *base)
    g.add_color_stop_rgb(1, *dark)
    c.set_source(g)
    c.paint()
    rr = random.Random(seed)
    for i in range(bands):
        yy = y - r + (i + 0.5) * 2 * r / bands + rr.uniform(-r * 0.05, r * 0.05)
        c.set_source_rgba(*band_col, 0.10 + 0.12 * rr.random())
        c.rectangle(x - r, yy, 2 * r, r * rr.uniform(0.04, 0.12))
        c.fill()
    # night side shadow
    sg = cairo.LinearGradient(x + light_dir[0] * r, y + light_dir[1] * r, x - light_dir[0] * r, y - light_dir[1] * r)
    sg.add_color_stop_rgba(0, 0, 0, 0, 0)
    sg.add_color_stop_rgba(0.55, 0, 0, 0, 0.05)
    sg.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    c.set_source(sg)
    c.paint()
    c.restore()
    c.set_line_width(max(1.5, r * 0.015))
    c.set_source_rgba(*atmosphere, atm)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.stroke()


def rings(c, x, y, r, tilt=0.28, angle=-0.35, col=(0.92, 0.85, 0.70), front=True):
    """Draw the front or back half of a planet's ring system (call back half before the planet)."""
    c.save()
    c.translate(x, y)
    c.rotate(angle)
    c.scale(1, tilt)
    for k, (r0, r1, a) in enumerate([(1.35, 1.55, 0.35), (1.6, 1.95, 0.55), (2.0, 2.15, 0.3)]):
        c.new_path()
        if front:
            c.arc(0, 0, r * r1, 0, math.pi)
            c.arc_negative(0, 0, r * r0, math.pi, 0)
        else:
            c.arc(0, 0, r * r1, math.pi, 2 * math.pi)
            c.arc_negative(0, 0, r * r0, 2 * math.pi, math.pi)
        c.close_path()
        c.set_source_rgba(*col, a)
        c.fill()
    c.restore()


def crescent(c, x, y, r, col=(1.0, 0.95, 0.82), phase=0.42):
    glow(c, x, y, r * 2.2, (1, 0.93, 0.75), 0.30)
    c.save()
    c.push_group()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgb(*col)
    c.fill()
    c.set_operator(cairo.OPERATOR_CLEAR)
    c.arc(x + r * phase * 1.25, y - r * phase * 0.6, r * 0.92, 0, 2 * math.pi)
    c.fill()
    c.pop_group_to_source()
    c.paint()
    c.restore()


def text(c, s, x, y, size, col=(1, 1, 1), a=1.0, family="DejaVu Serif", bold=True, italic=False, spacing=0.0,
         shadow=True):
    c.select_font_face(family, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    widths = [c.text_extents(ch).x_advance for ch in s]
    total = sum(widths) + spacing * (len(s) - 1)
    cx = x - total / 2
    for dx, alpha in ((size * 0.04, 0.5), (0, 1.0)) if shadow else ((0, 1.0),):
        px = cx
        for ch, wch in zip(s, widths):
            c.move_to(px + dx, y + dx)
            if dx:
                c.set_source_rgba(0, 0, 0.05, 0.6 * a)
            else:
                c.set_source_rgba(*col, a * alpha)
            c.show_text(ch)
            px += wch + spacing
    c.new_path()
    return total
