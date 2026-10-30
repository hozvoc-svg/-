from episodes._short_common import *
PRON = {"Antikythera": "Anti-kee-theera"}
SHORT_HOOK = [("A 2,000-YEAR-OLD", INK, 70), ("COMPUTER", (0.3, 0.93, 1.0), 96)]
SHORT = shots([
    ("ant_divers", None, ["1901. Sponge divers in Greece find an ancient shipwreck near the island of Antikythera."]),
    ("ant_lump", None, ["Among the treasures is a lump of corroded bronze. Inside it, someone notices gears."]),
    ("ant_gears", None, ["X-rays later revealed at least thirty precise bronze gears, working together."]),
    ("ant_sky", None, ["It could predict eclipses, and the movements of the sun, the moon, and probably the planets."]),
    ("ant_age", None, ["And it is about two thousand years old."]),
    ("ant_mystery", None, ["Nothing this complex appears again for over a thousand years. Who built it? Follow for more."]),
])
