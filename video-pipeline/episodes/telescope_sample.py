# 4-minute sample: real Hubble/Webb images with slow camera moves, crossfades and ambient music.
SCENES_MODULE = "vivid"
AMBIENT = "music"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
XFADE = 4.0
OVERLAY_FX = ()
MUSIC_SEED = 2

_SHOTS = [
    ("heic1501a", ((1.0, .50, .50), (1.35, .55, .30))),   # Pillars of Creation (Hubble)
    ("weic2205a", ((1.25, .30, .45), (1.0, .55, .50))),   # Cosmic Cliffs (Webb)
    ("heic0601a", ((1.0, .50, .50), (1.4, .45, .45))),    # Orion Nebula
    ("weic2211a", ((1.3, .62, .50), (1.0, .50, .50))),    # Cartwheel galaxy
    ("heic0910h", ((1.0, .50, .50), (1.3, .50, .48))),    # Butterfly nebula
    ("heic0506a", ((1.0, .50, .50), (1.35, .47, .45))),   # Whirlpool galaxy
    ("weic2216b", ((1.25, .55, .40), (1.0, .50, .50))),   # Pillars (Webb)
    ("heic1206a", ((1.0, .40, .50), (1.3, .60, .50))),    # Tarantula region
]
LONG = [dict(scene="photo", args=dict(img=img, cam=cam), duration=30) for img, cam in _SHOTS]
SHORT = []
