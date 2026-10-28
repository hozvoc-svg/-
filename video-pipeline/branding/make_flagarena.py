"""TikTok branding for "Flag Arena": profile picture (flag balls inside a neon ring with a gap)."""
import math, os, sys
import cairo
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sims"))
import country_ring as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flagarena")


def profile():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    c = cairo.Context(s)
    g = cairo.RadialGradient(400, 400, 10, 400, 400, 560)
    g.add_color_stop_rgb(0, 0.10, 0.08, 0.20)
    g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g)
    c.paint()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, al in ((60, 0.10), (38, 0.2), (20, 1.0)):
        lg = cairo.LinearGradient(100, 100, 700, 700)
        lg.add_color_stop_rgba(0, 0.3, 0.93, 1.0, al)
        lg.add_color_stop_rgba(1, 1.0, 0.3, 0.8, al)
        c.set_source(lg)
        c.set_line_width(lw)
        c.new_path()
        c.arc(400, 400, 300, -0.9, -0.9 + 2 * math.pi - 0.75)
        c.stroke()
    for code, x, y, r in (("us", 300, 470, 92), ("br", 500, 470, 92), ("jp", 400, 300, 92)):
        C.draw_ball(c, x, y, r, code)
    s.write_to_png(os.path.join(OUT, "profile.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    profile()
