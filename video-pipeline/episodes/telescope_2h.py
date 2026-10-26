# Sleepy Cosmos ambience: "Real Space 2" — 2 hours of new Hubble & Webb photographs with calm ambient music.
import os, random
from PIL import Image

SCENES_MODULE = "vivid"
SEG_CRF = 21  # 116 one-minute segments: keep the temp files small enough for the disk
AMBIENT = "music"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
XFADE = 5.0
OVERLAY_FX = ()
MUSIC_SEED = 4
SHOT = 63  # seconds per image

_HERE = os.path.dirname(os.path.abspath(__file__))
_DIR = os.path.join(os.path.dirname(_HERE), "images", "telescope")


def _shots():
    Image.MAX_IMAGE_PIXELS = None
    names = open(os.path.join(_HERE, "telescope_2h_list.txt")).read().split()
    r = random.Random(11)
    r.shuffle(names)  # mix nebulae, galaxies and planets
    shots = []
    for i, n in enumerate(names):
        w, h = Image.open(os.path.join(_DIR, n + ".jpg")).size
        ratio = w / h
        zmax = 1.12 if w < 3000 else 1.4  # wallpaper-size files stay sharp only with gentle zoom
        if ratio < 1.3:
            y0, y1 = (0.35, 0.65) if i % 2 else (0.65, 0.35)
            cam = ((1.0, 0.5, y0), (min(zmax, 1.1), 0.5, y1))
        elif i % 2:
            cam = ((1.0, 0.5, 0.5), (zmax, 0.5 + r.uniform(-0.08, 0.08), 0.5 + r.uniform(-0.06, 0.06)))
        else:
            cam = ((zmax, 0.5 + r.uniform(-0.08, 0.08), 0.5 + r.uniform(-0.06, 0.06)), (1.0, 0.5, 0.5))
        shots.append(dict(scene="photo", args=dict(img=n, cam=cam), duration=SHOT))
    return shots


LONG = _shots()
SHORT = []


def thumb(S, c):
    """Webb's Southern Ring / a different image from the 1-hour video, calm title, '2 HOURS' pill."""
    import cairo
    import styles as ST
    S.sc_photo(c, 0.0, 1.0, 0.0, dict(img=_THUMB_IMG, cam=((1.0, 0.5, 0.5), (1.0, 0.5, 0.5))))
    g = cairo.LinearGradient(0, 0, 0, 1080)
    g.add_color_stop_rgba(0, 0, 0, 0.05, 0.6)
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
    c.arc(800, 420, 42, 1.5708, 4.7124)
    c.arc(1120, 420, 42, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    ST._font(c, "Montserrat Thin", 44, bold=True)
    t = "2 HOURS"
    ST._glyphs(c, t, 960 - ST._width(c, t, 6) / 2, 436, (1, 1, 1), 1.0, 6, shadow=0)
_THUMB_IMG = "heic1520a"  # Veil Nebula: appears in the video, differs from the 1-hour thumbnail
