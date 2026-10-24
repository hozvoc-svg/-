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
        shots.append(dict(scene="photo", args=dict(img=n, cam=cam), duration=SHOT))
    return shots


LONG = _shots()
SHORT = []
