# Shared settings for vertical-first Stickman Unsolved Shorts (scenes in short_scenes.py).
SCENES_MODULE = "short_scenes"
XFADE = 0.25
FADE = 0.001
GAP, TAIL = 0.18, 0.3
OVERLAY_FX = (("film_grain", 0.5),)
CAPTION_STYLE = "punch"
VERTICAL_FILL = True
CAPTION_Y = 0.74
CAPTION_PX = 84
EL_SETTINGS = dict(stability=0.42, similarity_boost=0.75, style=0.2, speed=1.04)
LONG = []
RED, AMBER, INK = (0.92, 0.22, 0.24), (1.0, 0.66, 0.22), (0.95, 0.96, 0.98)


def shots(spec):
    return [dict(scene=s, args=dict(vx=0.5, **(args or {})), text=txt) for s, args, txt in spec]
