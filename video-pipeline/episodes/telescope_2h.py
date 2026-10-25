# Sleepy Cosmos ambience: "Real Space 2" — 2 hours of new Hubble & Webb photographs with calm ambient music.
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
