from episodes._short_common import *
XFADE = 0.0
PRON = {"Hessdalen": "Hess-dah-len"}
SHORT_HOOK = [("STRANGE LIGHTS", (1.0, 0.85, 0.3), 76), ("NOBODY CAN EXPLAIN", INK, 62)]
SFX = [(0, "riser", 0.5), (2, "hit", 0.2), (3, "glitch", 0.3)]
SHORT = shots([
    ("hes_valley", None, ["Hessdalen. A quiet valley in Norway. In the early 1980s, people start seeing strange lights in the sky."]),
    ("hes_colors", dict(fx="zoom"), ["Glowing balls, white, yellow, or red. Sometimes hovering for over an hour. Sometimes racing across the valley."]),
    ("hes_count", dict(fx="flash"), ["At their peak, they were reported up to twenty times a week."]),
    ("hes_station", dict(fx="glitch"), ["Scientists set up cameras and instruments. They have recorded the lights, but still can't fully explain them. And they still appear today. Follow for more."]),
])
