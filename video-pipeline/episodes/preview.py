# Short check reel for the upgraded look: crossfades, chapter titles, shooting stars, sharper textures.
from episodes.solar_journey import EL_VOICE, EL_SETTINGS
SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 0.0
PRON = {}
XFADE = 2.5
OVERLAY_FX = (("shooting_star", 0.7),)
CHAPTER_STYLE = "letters"
CHAPTER_PAIR = "classic"
LONG = [
    dict(scene="title", args=dict(subtitle="A Calm Journey Through the Solar System"), duration=8),
    dict(scene="sun", args=dict(zoom=1.3), chapter="The Sun", duration=12),
    dict(scene="planet", args=dict(body="jupiter", size=470, x=0.5), chapter="Jupiter", duration=12),
    dict(scene="planet", args=dict(body="saturn", size=330, x=0.5, rings=True, moons=1), chapter="Saturn", duration=12),
    dict(scene="earth", args=dict(zoom=1.3), chapter="Home", duration=12),
]
SHORT = []
