# Wordless ASMR cut of rainy_autumn: same 49 illustrations, natural sounds only (rain, fire, thunder),
# with moving rain in the windows, drops on the glass, sparks and falling leaves.
from episodes.rainy_autumn import SHOTS, STORY

SCENES_MODULE = "photo_scenes"
AMBIENT = "nature"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}

# window boxes in normalized image coords: (x0, y0, x1, y1, "glass" | "out")
WINDOWS = {
    1: [(0.13, 0.17, 0.45, 0.78, "glass"), (0.52, 0.17, 0.77, 0.68, "glass")],
    2: [(0.39, 0.0, 0.97, 0.42, "glass")],
    3: [(0.35, 0.05, 0.55, 0.73, "glass"), (0.60, 0.0, 1.0, 0.85, "out")],
    4: [(0.68, 0.25, 0.98, 0.55, "glass")],
    5: [(0.15, 0.12, 0.42, 0.52, "glass")],
    7: [(0.39, 0.0, 0.97, 0.42, "glass")],
    8: [(0.39, 0.0, 0.97, 0.42, "glass")],
    9: [(0.39, 0.0, 0.97, 0.42, "glass")],
    10: [(0.39, 0.0, 0.97, 0.42, "glass")],
    11: [(0.11, 0.08, 0.66, 0.72, "glass")],
    12: [(0.58, 0.0, 1.0, 0.75, "glass")],
    13: [(0.62, 0.0, 1.0, 0.72, "glass")],
    14: [(0.62, 0.0, 1.0, 0.72, "glass")],
    16: [(0.0, 0.05, 0.28, 0.65, "glass")],
    17: [(0.0, 0.0, 0.45, 0.9, "glass")],
    18: [(0.53, 0.0, 0.92, 0.68, "glass")],
    22: [(0.10, 0.12, 0.32, 0.68, "out")],
    23: [(0.0, 0.0, 0.65, 0.9, "glass")],
    24: [(0.30, 0.0, 0.80, 0.9, "out")],
    27: [(0.22, 0.0, 0.88, 0.82, "glass")],
    28: [(0.0, 0.0, 0.42, 0.9, "glass")],
    29: [(0.30, 0.12, 0.78, 0.58, "glass")],
    30: [(0.0, 0.0, 1.0, 0.85, "glass")],
    31: [(0.0, 0.08, 0.10, 0.62, "glass")],
    32: [(0.74, 0.0, 1.0, 0.75, "glass")],
    33: [(0.74, 0.0, 1.0, 0.75, "glass")],
    34: [(0.74, 0.0, 1.0, 0.75, "glass")],
    35: [(0.74, 0.0, 1.0, 0.75, "glass")],
    36: [(0.10, 0.0, 0.82, 0.75, "glass")],
    38: [(0.68, 0.0, 1.0, 0.75, "glass")],
    39: [(0.62, 0.05, 1.0, 0.68, "glass")],
    40: [(0.30, 0.0, 0.92, 0.78, "glass")],
    41: [(0.74, 0.0, 1.0, 0.75, "glass")],
    42: [(0.62, 0.17, 0.88, 0.60, "glass")],
    43: [(0.74, 0.0, 1.0, 0.75, "glass")],
    44: [(0.62, 0.17, 0.88, 0.60, "glass")],
    45: [(0.62, 0.17, 0.88, 0.60, "glass")],
    46: [(0.62, 0.17, 0.88, 0.60, "glass")],
    47: [(0.18, 0.05, 0.86, 0.70, "glass")],
    48: [(0.16, 0.05, 0.70, 0.85, "glass")],
    49: [(0.20, 0.18, 0.53, 0.60, "glass")],
}
LEAVES = {1, 3, 23, 24}
SLOW_END = {2, 47, 49, 48}


def _order():
    seen, out = set(), []
    for img, _ in STORY:
        if img not in seen:
            seen.add(img)
            out.append(img)
    return out


def _build():
    segs, prev = [], None
    order = _order()
    for i, img in enumerate(order):
        lamps, path = SHOTS[img]
        fx = ["dust"] if lamps else []
        if img in LEAVES:
            fx.append("leaves")
        args = dict(img=f"rainy_autumn/{img:02d}.png", cam=(path[0], path[1]), lamps=tuple(lamps),
                    windows=tuple(WINDOWS.get(img, ())), fx=tuple(fx))
        if prev is None:
            args["fade_in"] = 5.0
        else:
            args["prev"] = {k: prev[k] for k in ("img", "cam")}
            args["xfade"] = 3.0
        if i == len(order) - 1:
            args["fade_out"] = 10.0
        segs.append(dict(scene="photo", args=args, duration=45 if img in SLOW_END else 30))
        prev = args
    return segs


LONG = _build()
SHORT = []


def thumb(S, c):
    """Same girl-by-the-window shot as the story cut, labelled for the ambience version."""
    import cairo
    import cozy_scenes as C
    S.draw_image(c, dict(img="rainy_autumn/08.png", cam=((1.08, .42, .5), (1.08, .42, .5))), 0)
    g = cairo.LinearGradient(1100, 0, 1920, 0)
    g.add_color_stop_rgba(0, 0.08, 0.05, 0.03, 0)
    g.add_color_stop_rgba(1, 0.08, 0.05, 0.03, 0.75)
    c.set_source(g)
    c.rectangle(0, 0, 1920, 1080)
    c.fill()
    C.serif(c, "Rainy", 1560, 330, 150, C.INK)
    C.serif(c, "Autumn", 1560, 480, 130, C.INK)
    C.serif(c, "at Grandma's", 1560, 590, 70, (1, 0.90, 0.70))
    C.rgba(c, (0.15, 0.10, 0.08), 0.8)
    C.rrect(c, 1270, 680, 580, 100, 50)
    c.fill()
    C.serif(c, "Rain & Fireplace", 1560, 750, 52, C.INK, bold=False, italic=True)
