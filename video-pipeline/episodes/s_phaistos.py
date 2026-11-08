from episodes._short_common import *
XFADE = 0.0
PRON = {"Phaistos": "Fy-stos"}
SHORT_HOOK = [("NOBODY CAN", INK, 80), ("READ THIS DISC", RED, 80)]
SFX = [(1, "riser", 0.0), (2, "hit", 0.3), (4, "hit", 0.2)]
SHORT = shots([
    ("ph_find", None, ["1908. On the Greek island of Crete, an archaeologist digging in an ancient palace finds a small clay disc."]),
    ("ph_spiral", dict(fx="zoom"), ["Both sides are covered with a spiral of strange symbols. Heads, fish, plants, ships."]),
    ("ph_stamp", dict(fx="flash"), ["The symbols weren't drawn. They were stamped, like early printing, thousands of years before the printing press."]),
    ("ph_count", dict(fx="glitch"), ["There are two hundred and forty one of them, using forty five different signs. They match no other writing ever found."]),
    ("ph_unread", dict(fx="zoom"), ["A prayer? A calendar? A hoax? More than a century later, nobody can read it. Follow for more."]),
])
