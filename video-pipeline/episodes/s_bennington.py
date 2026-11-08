from episodes._short_common import *
XFADE = 0.0
PRON = {"Welden": "Well-den"}
SHORT_HOOK = [("PEOPLE VANISH", RED, 80), ("IN THIS FOREST", INK, 76)]
SFX = [(1, "heartbeat", 0.2), (2, "hit", 0.3), (4, "glitch", 0.3), (5, "hit", 0.4)]
SHORT = shots([
    ("ben_trail", None, ["December 1st, 1946. Vermont. Eighteen-year-old student Paula Welden goes for a walk on a mountain trail."]),
    ("ben_vanish", dict(fx="zoom"), ["Hikers see her on the trail, in a red coat. She is never seen again."]),
    ("ben_search", dict(fx="shake"), ["Hundreds of people search the forest. No trace."]),
    ("ben_more", dict(fx="flash"), ["And she wasn't the only one. In just a few years, several other people vanished in the same area."]),
    ("ben_bus", dict(fx="glitch"), ["One man reportedly disappeared from a moving bus. His bags were still on the rack."]),
    ("ben_triangle", dict(fx="zoom"), ["Locals call it the Bennington Triangle. Follow for more."]),
])
