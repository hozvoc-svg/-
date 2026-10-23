# hill_house told over Google Flow illustrations (images/hill_house/NN.png) instead of drawn scenes.
from episodes.hill_house import LONG as _STORY, PRON, SPEAKER, LENGTH_SCALE, GAP, TAIL
from episodes.hill_house_images import SEGMENT_IMAGES

SCENES_MODULE = "photo_scenes"
AMBIENT = "cozy"
CAPTIONS = False
FADE = 1.2

_RAIN = {"rain_window", "rain_room"}
_DUST = {"kitchen", "rain_room", "evening_room"}
_NIGHT = {"night_sky", "bedroom"}

LONG = []
for i, seg in enumerate(_STORY):
    n = SEGMENT_IMAGES[i]
    a = seg.get("args", {})
    fx = []
    if seg["scene"] in _RAIN or a.get("rain"):
        fx += ["rain"] + (["glass"] if seg["scene"] == "rain_window" else [])
    if seg["scene"] in _DUST:
        fx.append("dust")
    if a.get("fireflies"):
        fx.append("fireflies")
    if a.get("dark"):
        fx.append("night")
    args = dict(img=f"hill_house/{n:02d}.png", move=i, fx=tuple(fx), rain=bool(a.get("rain") or seg["scene"] in _RAIN))
    if i == 0:
        args["title"] = ("A Rainy Summer at Grandma's", "a cozy bedtime story")
    LONG.append(dict(seg, scene="photo", args=args))
SHORT = []
