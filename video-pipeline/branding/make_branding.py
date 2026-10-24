"""Render Sleepy Cosmos channel art: banner (2560x1440, safe area 1546x423) and profile picture (800x800)."""
import os, sys
import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import space_art as A

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
GOLD = (1.0, 0.90, 0.70)


def banner():
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    A.background(c, W, H, (0.02, 0.02, 0.07), (0.04, 0.03, 0.12))
    neb = A.nebula_surface(W, H, seed=4, strength=0.9)
    c.set_source_surface(neb, 0, 0)
    c.paint_with_alpha(0.85)
    A.stars(c, W, H, n=1400, seed=5, scale=1.2)
    # ringed planet on the right, crescent moon on the left; both sit beside the mobile-safe centre strip
    A.rings(c, 2310, 700, 150, front=False)
    A.planet(c, 2310, 700, 150, base=(0.88, 0.72, 0.52), dark=(0.20, 0.12, 0.10), bands=9, seed=2,
             atmosphere=(1.0, 0.85, 0.6), atm=0.25)
    A.rings(c, 2310, 700, 150, front=True)
    A.crescent(c, 330, 650, 110)
    A.planet(c, 200, 840, 40, base=(0.35, 0.55, 0.90), dark=(0.04, 0.06, 0.18), bands=3, seed=4)
    # safe area: x 507..2053, y 508..931
    A.text(c, "Sleepy Cosmos", W / 2, 735, 150, (1, 1, 1))
    A.text(c, "FALL ASLEEP TO THE WONDERS OF THE UNIVERSE", W / 2, 830, 40, GOLD, family="Inter",
           bold=False, spacing=6)
    A.text(c, "New calm space journeys every week", W / 2, 895, 30, (0.75, 0.80, 0.95), family="Inter",
           bold=False, spacing=2)
    s.write_to_png(os.path.join(OUT, "banner_2560x1440.png"))


def avatar():
    S = 800
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    c = cairo.Context(s)
    A.background(c, S, S, (0.04, 0.03, 0.12), (0.10, 0.06, 0.25))
    neb = A.nebula_surface(S, S, seed=9, strength=1.0)
    c.set_source_surface(neb, 0, 0)
    c.paint_with_alpha(0.9)
    A.stars(c, S, S, n=160, seed=8, scale=1.4)
    # big crescent moon "sleeping" over a small ringed planet: readable even at 48 px
    A.crescent(c, 360, 360, 230, phase=0.45)
    A.rings(c, 560, 575, 95, front=False, tilt=0.32)
    A.planet(c, 560, 575, 95, base=(0.95, 0.65, 0.45), dark=(0.30, 0.10, 0.12), bands=6, seed=3,
             atmosphere=(1.0, 0.8, 0.6), atm=0.3)
    A.rings(c, 560, 575, 95, front=True, tilt=0.32)
    s.write_to_png(os.path.join(OUT, "profile_800x800.png"))


def watermark():
    """Small subscribe watermark (150x150) with the same moon motif."""
    S = 150
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    c = cairo.Context(s)
    c.arc(S / 2, S / 2, S / 2, 0, 6.2832)
    c.set_source_rgba(0.05, 0.04, 0.15, 0.9)
    c.fill()
    A.crescent(c, 68, 68, 42, phase=0.45)
    A.planet(c, 105, 105, 18, base=(0.95, 0.65, 0.45), dark=(0.30, 0.10, 0.12), bands=3, atm=0.2)
    s.write_to_png(os.path.join(OUT, "watermark_150x150.png"))


if __name__ == "__main__":
    banner()
    avatar()
    watermark()
