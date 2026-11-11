# Test Short written with the video-studio skills (short-form-script + video-hooks):
# hook = sound from frame 0 (the hum itself) + moving rings + on-screen text different from the voice.
from episodes._short_common import *
XFADE = 0.0
PRON = {"Taos": "Tauss"}
SHORT_HOOK = [("ONLY SOME PEOPLE", INK, 70), ("HEAR THIS SOUND", RED, 76)]
SFX = [(0, "hum", 0.0), (1, "hum", 0.0), (2, "heartbeat", 0.3), (3, "hit", 0.4), (4, "hum", 0.0), (4, "riser", 2.0), (5, "hum", 0.0)]
SHORT = shots([
    ("th_town", None, ["Some people in this small town hear a sound... most people never will."]),
    ("th_wave", dict(fx="zoom"), ["Taos, New Mexico. In the early nineties, residents start reporting a low, constant hum. Like a diesel engine, idling far away."]),
    ("th_sleep", dict(fx="glitch"), ["It's there day and night. Some can't sleep. Others feel pressure in their ears."]),
    ("th_neighbors", dict(fx="shake"), ["But the people standing right next to them... hear nothing."]),
    ("th_science", dict(fx="zoom"), ["In 1993, scientists brought sensitive equipment. About two percent of residents said they could hear it. The instruments found no source."]),
    ("th_world", dict(fx="flash"), ["Similar hums have been reported all over the world. Can you hear it? Follow for more."]),
])
