# Sleepy Cosmos: "Drifting Past the Giants" — 2 hours, no narration: slow dark flybys of Jupiter, Saturn,
# Uranus and Neptune with their moons, calm generative ambient music (format chosen from the niche research:
# long, dark, slow visuals perform best for sleep).
SCENES_MODULE = "space_scenes"
AMBIENT = "music"
MUSIC_SEED = 7
CAPTIONS = False
XFADE = 5.0
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
SEG_CRF = 21
OVERLAY_FX = ()

_SHOTS = [
    ("travel", dict(neb=2, slow=True, warp=0.1)),
    ("planet", dict(body="jupiter", size=360, x=0.5, moons=4)),
    ("moon", dict(body="io", parent="jupiter", size=270, parent_size=620, px=0.12, py=0.8)),
    ("planet", dict(body="jupiter", size=430, x=0.58, night=0.35, moons=2)),
    ("moon", dict(body="europa", parent="jupiter", size=280, parent_size=600, px=0.12, py=0.8, x=0.58)),
    ("moon", dict(body="ganymede", parent="jupiter", size=270, parent_size=640, px=0.1, py=0.78)),
    ("planet", dict(body="jupiter", size=300, x=0.45, night=0.55, moons=3)),
    ("travel", dict(neb=3, slow=True, warp=0.1)),
    ("planet", dict(body="saturn", size=330, x=0.5, rings=True, moons=1)),
    ("moon", dict(body="titan", parent="saturn", size=280, parent_size=560, px=0.12, py=0.78)),
    ("planet", dict(body="saturn", size=410, x=0.58, rings=True, night=0.35)),
    ("moon", dict(body="enceladus", parent="saturn", size=260, parent_size=560, px=0.12, py=0.78, x=0.6)),
    ("planet", dict(body="saturn", size=300, x=0.45, rings=True, night=0.55, moons=1)),
    ("travel", dict(neb=4, slow=True, warp=0.1)),
    ("planet", dict(body="uranus", size=220, x=0.52, rings=True, tilt=1.7)),
    ("planet", dict(body="uranus", size=250, x=0.58, rings=True, tilt=1.7, night=0.4)),
    ("travel", dict(neb=5, slow=True, warp=0.1)),
    ("planet", dict(body="neptune", size=340, x=0.5, moons=1)),
    ("planet", dict(body="neptune", size=420, x=0.45, night=0.45)),
    ("travel", dict(neb=1, slow=True, warp=0.08)),
    ("planet", dict(body="pluto", size=300, x=0.55, moons=1, night=0.3)),
    ("travel", dict(neb=0, slow=True, warp=0.06, fade_out=30.0)),
]
SHOT = 332  # seconds per shot -> 22 x 332 s = 2 h 1 min 44 s

LONG = [dict(scene=s, args=a, duration=SHOT) for s, a in _SHOTS]
SHORT = []


def thumb(S, c):
    import space_art as A
    S.draw_backdrop(c, 3, 50.0, 0)
    A.glow(c, 640, 600, 420, (0.9, 0.75, 0.55), 0.25)
    S.paint_sphere(c, "jupiter", 640, 600, 330, 0.4, light=(-0.6, -0.3, 0.72), tilt=0.05, night=0.15)
    A.rings(c, 1420, 470, 230, tilt=0.28, angle=-0.35, front=False)
    S.paint_sphere(c, "saturn", 1420, 470, 230, 0.3, light=(-0.6, -0.3, 0.72), tilt=0.12)
    A.rings(c, 1420, 470, 230, tilt=0.28, angle=-0.35, front=True)
    S.paint_sphere(c, "neptune", 1700, 860, 90, 0.2, light=(-0.6, -0.3, 0.72), tilt=0.1)
    S.paint_sphere(c, "uranus", 1180, 900, 70, 0.2, light=(-0.6, -0.3, 0.72), tilt=1.7)
    A.text(c, "Drifting Past", 960, 140, 74, (1, 1, 1))
    A.text(c, "THE GIANTS", 960, 250, 110, (1, 0.88, 0.62))
    A.text(c, "2 HOURS · DEEP SPACE AMBIENT", 960, 1030, 46, (0.85, 0.9, 1.0), family="Inter", spacing=4)
