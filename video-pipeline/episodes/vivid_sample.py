# 4-minute sample of the vivid, music-only space style (reference: long colourful space ambience videos).
SCENES_MODULE = "vivid"
AMBIENT = "music"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
XFADE = 3.0
OVERLAY_FX = (("shooting_star", 0.8),)
MUSIC_SEED = 1
LONG = [dict(scene=sc, args=a, duration=30) for sc, a in [
    ("nebula", dict(seed=31, pal="violet")),
    ("planet", dict(seed=32, pal="teal", body="jupiter", size=420)),
    ("nebula", dict(seed=33, pal="crimson", push=False, pan=(0.15, 0.0))),
    ("horizon", dict(seed=34, pal="ocean", density=0.6)),
    ("galaxy", dict(seed=35, pal="rose", density=0.3)),
    ("planet", dict(seed=36, pal="violet", body="saturn", size=300, rings=True, atm=(1, 0.85, 0.6))),
    ("ring", dict(seed=37, pal="fire")),
    ("nebula", dict(seed=38, pal="aurora", pan=(-0.12, 0.05))),
]]
SHORT = []
