"""Avatar + banner for the 'Stix & Bolt' wordless cartoon channel (characters from toon.py)."""
import math, os, sys
import cairo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import toon as T

OUT = os.path.join(os.path.dirname(__file__), "stixbolt")
os.makedirs(OUT, exist_ok=True)
YEL = (1.0, 0.82, 0.2)


def avatar():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    c = cairo.Context(s)
    g = cairo.RadialGradient(400, 360, 60, 400, 400, 560)
    g.add_color_stop_rgb(0, 1.0, 0.86, 0.45)
    g.add_color_stop_rgb(1, 0.98, 0.58, 0.28)
    c.set_source(g); c.paint()
    # Stix (big head, happy) with Bolt peeking in
    T.bolt(c, x=800, y=1230, s=6.0, facing=-1, sit=1.0, eye="happy", tail=1.0, head=0.0, T=0.3)
    c.save(); c.translate(320, 400); c.scale(6.4, 6.4); c.rotate(-0.08)
    T.face(c, dict(T.STIX, eyes="happy", mouth="grin"))
    c.restore()
    s.write_to_png(os.path.join(OUT, "avatar_800.png"))


def banner():
    Wb, Hb = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wb, Hb)
    c = cairo.Context(s)
    c.save()
    c.scale(Wb / 1080 * 0.9, Wb / 1080 * 0.9)
    c.translate(-40, -880)
    T.kitchen(c, 3.0)
    c.restore()
    c.set_source_rgba(1, 0.95, 0.85, 0.35); c.paint()
    # safe area 1546x423 centred
    T.heavy_text(c, "STIX & BOLT", Wb / 2, 690, 170, (1, 1, 1), outline=0.14)
    T.heavy_text(c, "WORDLESS CARTOONS  ·  NEW EVERY DAY", Wb / 2, 800, 62, YEL)
    T.stix(c, x=520, y=1130, s=3.5, facing=1, eyes="happy", mouth="grin", aF=(1.9, 0.7), aB=(-1.9, -0.7))
    T.bolt(c, x=2110, y=1130, s=3.2, facing=-1, eye="happy", tail=1.0, head=0.2, T=0.4)
    s.write_to_png(os.path.join(OUT, "banner_2560x1440.png"))


if __name__ == "__main__":
    avatar(); banner()
