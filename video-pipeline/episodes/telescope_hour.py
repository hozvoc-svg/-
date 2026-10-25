# Sleepy Cosmos ambience: "1 Hour of Real Space Images" — Hubble & Webb photographs, slow camera moves, ambient music.
import os, random
from PIL import Image

SCENES_MODULE = "vivid"
AMBIENT = "music"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
XFADE = 5.0
OVERLAY_FX = ()
MUSIC_SEED = 3
SHOT = 68  # seconds per image

_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "telescope")
# two-panel comparison images: keep the camera inside one panel so the split line never shows
_CAM_OVERRIDE = {"weic2320a": ((2.05, 0.25, 0.5), (2.3, 0.25, 0.47))}
_SKIP = {"weic2207a", "weic2220a", "weic2315a", "weic2402a", "weic2403a"}  # collages / labelled insets


def _shots():
    Image.MAX_IMAGE_PIXELS = None
    names = sorted(f[:-4] for f in os.listdir(_DIR) if f.endswith(".jpg") and f[:-4] not in _SKIP)
    hub = [n for n in names if n.startswith("heic")]
    webb = [n for n in names if n.startswith("weic")]
    order = []
    while hub or webb:  # interleave the two telescopes for variety
        if hub:
            order.append(hub.pop(0))
        if webb:
            order.append(webb.pop(0))
    r = random.Random(7)
    shots = []
    for i, n in enumerate(order):
        w, h = Image.open(os.path.join(_DIR, n + ".jpg")).size
        ratio = w / h
        if ratio < 1.3:      # tall image: glide vertically through it
            y0, y1 = (0.3, 0.7) if i % 2 else (0.7, 0.3)
            cam = ((1.0, 0.5, y0), (1.12, 0.5, y1))
        elif ratio > 2.4:    # very wide: glide horizontally
            x0, x1 = (0.25, 0.75) if i % 2 else (0.75, 0.25)
            cam = ((1.0, x0, 0.5), (1.1, x1, 0.5))
        elif i % 2:          # push in towards a point of interest
            cam = ((1.0, 0.5, 0.5), (1.45, 0.5 + r.uniform(-0.12, 0.12), 0.5 + r.uniform(-0.1, 0.1)))
        else:                # pull back to reveal the whole image
            cam = ((1.45, 0.5 + r.uniform(-0.12, 0.12), 0.5 + r.uniform(-0.1, 0.1)), (1.0, 0.5, 0.5))
        cam = _CAM_OVERRIDE.get(n, cam)
        shots.append(dict(scene="photo", args=dict(img=n, cam=cam), duration=SHOT))
    return shots


LONG = _shots()
SHORT = []


def thumb(S, c):
    """Webb's Cosmic Cliffs with a calm title on the starry sky above the cliffs."""
    import cairo
    import styles as ST
    S.sc_photo(c, 0.0, 1.0, 0.0, dict(img="weic2205a", cam=((1.0, 0.5, 0.55), (1.0, 0.5, 0.55))))
    g = cairo.LinearGradient(0, 0, 0, 1080)
    g.add_color_stop_rgba(0, 0, 0, 0.05, 0.55)
    g.add_color_stop_rgba(0.45, 0, 0, 0.05, 0.0)
    c.set_source(g)
    c.paint()
    ST._font(c, "Cinzel", 120, bold=True)
    t = "REAL SPACE"
    ST._glyphs(c, t, 960 - ST._width(c, t, 8) / 2, 230, (1, 0.95, 0.85), 1.0, 8, shadow=0.8)
    ST._font(c, "Cormorant Garamond Light", 70, bold=True)
    t = "Hubble & Webb  ·  Sleep Music"
    ST._glyphs(c, t, 960 - ST._width(c, t) / 2, 330, (0.85, 0.92, 1.0), 1.0, shadow=0.8)
    c.set_source_rgba(0.05, 0.05, 0.12, 0.8)
    c.new_path()
    c.arc(820, 420, 42, 1.5708, 4.7124)
    c.arc(1100, 420, 42, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    ST._font(c, "Montserrat Thin", 44, bold=True)
    t = "1 HOUR"
    ST._glyphs(c, t, 960 - ST._width(c, t, 6) / 2, 436, (1, 1, 1), 1.0, 6, shadow=0)
