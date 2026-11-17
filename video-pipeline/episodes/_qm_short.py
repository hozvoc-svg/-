# Shared settings for The Quiet Money Shorts (vertical scenes v_* in finance_scenes.py).
SCENES_MODULE = "finance_scenes"
AMBIENT = "finance"
MUSIC_VOL = 0.34
XFADE = 0.25
FADE = 0.001
GAP, TAIL = 0.16, 0.3
CAPTION_STYLE = "punch"
VERTICAL_FILL = True
CAPTION_Y = 0.75
CAPTION_PX = 84
EL_VOICE = "cjVigY5qzO86Huf0OWal"
EL_SETTINGS = dict(stability=0.42, similarity_boost=0.8, style=0.2, speed=1.06)
PRON = {"IRS": "I R S"}
LONG = []
GOLD, WHITE, RED, GREEN = (1.0, 0.78, 0.25), (0.96, 0.97, 1.0), (1.0, 0.36, 0.40), (0.35, 1.0, 0.60)


def shots(spec):
    return [dict(scene=s, args=dict(vx=0.5, **(args or {})), text=txt) for s, args, txt in spec]
