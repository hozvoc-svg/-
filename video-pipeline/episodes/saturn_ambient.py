# Sleepy Cosmos ambience: "Drifting Past Saturn" — 1 hour, no narration, slow orbital views and space drones.
SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
XFADE = 2.5
OVERLAY_FX = (("shooting_star", 0.7),)
CHAPTER_STYLE = "letters"
CHAPTER_PAIR = "classic"
FINAL = "hevc1440"
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}

_SHOTS = [
    ("title", dict(subtitle="Drifting Past Saturn  ·  1 hour of calm space ambience")),
    ("planet", dict(body="saturn", size=300, x=0.5, rings=True)),
    ("moon", dict(body="titan", parent="saturn", size=280, parent_size=560, px=0.12, py=0.78)),
    ("planet", dict(body="saturn", size=360, x=0.42, rings=True, moons=1)),
    ("moon", dict(body="enceladus", parent="saturn", size=260, parent_size=560, px=0.12, py=0.78, x=0.6)),
    ("planet", dict(body="saturn", size=420, x=0.58, rings=True, night=0.3)),
    ("moon", dict(body="mimas", parent="saturn", size=240, parent_size=600, px=0.1, py=0.8)),
    ("planet", dict(body="saturn", size=300, x=0.62, rings=True, moons=1)),
    ("moon", dict(body="iapetus", parent="saturn", size=260, parent_size=520, px=0.12, py=0.8, x=0.58)),
    ("planet", dict(body="saturn", size=380, x=0.5, rings=True, night=0.45)),
    ("travel", dict(neb=3, slow=True, warp=0.12)),
    ("planet", dict(body="saturn", size=340, x=0.45, rings=True, night=0.6)),
]

LONG = []
for i, (scene, args) in enumerate(_SHOTS):
    dur = 25 if scene == "title" else 330
    if i == len(_SHOTS) - 1:
        scene, args = "travel", dict(neb=0, slow=True, warp=0.1, fade_out=25.0)
    LONG.append(dict(scene=scene, args=args, duration=dur))
SHORT = []


def thumb(S, c):
    import space_art as A
    S.draw_backdrop(c, 3, 50.0, 0)
    A.rings(c, 1220, 560, 360, front=False)
    S.paint_sphere(c, "saturn", 1220, 560, 360, 0.3, light=(-0.6, -0.3, 0.72), tilt=0.12)
    A.rings(c, 1220, 560, 360, front=True)
    A.glow(c, 1780, 250, 90, (1.0, 0.7, 0.35), 0.4)
    S.paint_sphere(c, "titan", 1780, 250, 70, 0.2, light=(-0.6, -0.3, 0.72))
    A.text(c, "Drifting Past", 960, 900, 90, (1, 1, 1))
    A.text(c, "SATURN", 960, 1010, 110, (1, 0.88, 0.62))
    A.text(c, "1 HOUR SPACE AMBIENCE", 960, 120, 48, (0.85, 0.9, 1.0), family="Inter", spacing=4)
