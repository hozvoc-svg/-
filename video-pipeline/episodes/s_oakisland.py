from episodes._short_common import *
XFADE = 0.0
PRON = {}
SHORT_HOOK = [("6 PEOPLE DIED", RED, 78), ("DIGGING THIS HOLE", INK, 66)]
SFX = [(1, "heartbeat", 0.2), (2, "riser", 0.0), (3, "hit", 0.2)]
SHORT = shots([
    ("oak_find", None, ["1795. Nova Scotia, Canada. A teenager on Oak Island finds a strange round dip in the ground, under an old oak tree."]),
    ("oak_logs", dict(fx="zoom"), ["He and his friends start digging. Every few meters, according to the legend, they hit a layer of logs."]),
    ("oak_flood", dict(fx="glitch"), ["Later treasure hunters went deeper. The shaft kept flooding with seawater, as if it had been booby-trapped."]),
    ("oak_deaths", dict(fx="shake"), ["Over two centuries, six people have died searching for whatever is down there."]),
    ("oak_question", dict(fx="zoom"), ["Pirate gold? Lost manuscripts? Or just a natural sinkhole? Nobody has found a treasure yet. Follow for more."]),
])
