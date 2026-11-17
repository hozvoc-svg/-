"""Branding for the finance channel "The Quiet Money": profile picture and banner (same look as the videos)."""
import math, os, sys
import cairo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import finance_scenes as F

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quietmoney")


def avatar(size=800):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    c = cairo.Context(s)
    g = cairo.RadialGradient(size / 2, size / 2, 10, size / 2, size / 2, size * 0.7)
    g.add_color_stop_rgb(0, 0.07, 0.10, 0.20); g.add_color_stop_rgb(1, 0.01, 0.02, 0.05)
    c.set_source(g); c.paint()
    F.logo(c, size / 2, size / 2, size * 0.34, halo=0.18)
    s.write_to_png(os.path.join(OUT, "avatar_800.png"))


def banner(w=2560, h=1440):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(s)
    c.save(); c.scale(w / F.W, h / F.H); F.bg(c, 2.0); c.restore()
    cy = h / 2
    # rising chart line across the visible desktop strip
    c.set_line_width(6); c.set_source_rgba(*F.GREEN, 0.35)
    c.move_to(0, cy + 180)
    for k in range(1, 41):
        x = w * k / 40
        c.line_to(x, cy + 180 - (k / 40) ** 2 * 300 + 18 * math.sin(k * 1.3))
    c.stroke()
    F.logo(c, w / 2 - 640, cy - 10, 110)
    F.big(c, "THE QUIET MONEY", w / 2 + 90, cy + 30, 130, F.WHITE)
    F.small(c, "How money really works, from the inside", w / 2 + 90, cy + 110, 44, F.GOLD, bold=True)
    F.small(c, "New breakdown every week", w / 2 + 90, cy + 165, 32, F.DIM)
    F.coin_pile(c, 2330, cy + 200, 300, 5)
    F.rich(c, 2330, cy - 40, 0.9, arms=(0.6, -2.4))
    F.joe(c, 230, cy + 200, 1.1, arms=(0.4, -2.0))
    F.cash_stack(c, 420, cy + 190, 4, 150)
    s.write_to_png(os.path.join(OUT, "banner_2560x1440.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    avatar(); banner()
