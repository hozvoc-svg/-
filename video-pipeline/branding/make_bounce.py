"""Branding for the physics-simulation channel "Bounce Lab": profile picture and banner."""
import math, os, sys
import cairo
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sims"))
import escape as E

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bounce")


def bg(c, w, h):
    g = cairo.RadialGradient(w / 2, h / 2, 10, w / 2, h / 2, max(w, h) * 0.7)
    g.add_color_stop_rgb(0, 0.08, 0.06, 0.16)
    g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g)
    c.paint()


def rings(c, cx, cy, radii, rot, gap=0.75, lw=12):
    n = len(radii)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, R in enumerate(radii):
        col = E.hue(i, n)
        a = rot * (1 if i % 2 == 0 else -1) + i * 0.9
        for w, al in ((lw * 2.6, 0.10), (lw * 1.7, 0.18), (lw, 1.0)):
            c.set_source_rgba(*col, al)
            c.set_line_width(w)
            c.new_path()
            c.arc(cx, cy, R, a + gap / 2, a - gap / 2 + 2 * math.pi)
            c.stroke()


def ball(c, x, y, r, trail=None):
    if trail:
        for k, (tx, ty) in enumerate(trail):
            f = (k + 1) / (len(trail) + 1)
            c.set_source_rgba(1, 1, 1, 0.3 * f)
            c.arc(tx, ty, r * (0.5 + 0.5 * f), 0, 2 * math.pi)
            c.fill()
    g = cairo.RadialGradient(x, y, 2, x, y, r * 4)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.6)
    g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(g)
    c.arc(x, y, r * 4, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(1, 1, 1)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def profile():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    c = cairo.Context(s)
    bg(c, 800, 800)
    rings(c, 400, 400, [150, 215, 280], 0.3, gap=0.8, lw=22)
    ball(c, 400 + 60, 400 - 30, 34, trail=[(330, 470), (360, 440), (395, 405), (428, 375)])
    s.write_to_png(os.path.join(OUT, "profile.png"))


def banner():
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    bg(c, W, H)
    rings(c, 300, H / 2, [80, 135, 190, 245, 300, 355], 0.4, lw=14)   # decorative, outside the safe area
    rings(c, W - 300, H / 2, [80, 135, 190, 245, 300, 355], 1.7, lw=14)
    ball(c, W - 300 + 40, H / 2 - 70, 20, trail=[(W - 370, H / 2), (W - 345, H / 2 - 30), (W - 315, H / 2 - 55)])
    # safe area (1546x423) holds the name and tagline
    E.text(c, "BOUNCE LAB", W / 2, H / 2 + 20, 170, (1, 1, 1), glow=(0.3, 0.93, 1.0))
    E.text(c, "SATISFYING PHYSICS SIMULATIONS  ·  NEW EVERY DAY", W / 2, H / 2 + 115, 46, (0.3, 0.93, 1.0), outline=0.1)
    s.write_to_png(os.path.join(OUT, "banner.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    profile()
    banner()
