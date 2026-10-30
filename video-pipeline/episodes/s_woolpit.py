from episodes._short_common import *
PRON = {"Woolpit": "Wool-pit"}
SHORT_HOOK = [("TWO GREEN", (0.45, 0.85, 0.35), 86), ("CHILDREN", INK, 86)]
SHORT = shots([
    ("wp_found", None, ["England, in the 1100s. Villagers in Woolpit find two children near a pit. Their skin is green."]),
    ("wp_language", None, ["They speak a language nobody understands."]),
    ("wp_beans", None, ["At first, they refuse all food, except raw beans."]),
    ("wp_fade", None, ["The boy soon dies. The girl survives, learns English, and slowly loses her green colour."]),
    ("wp_land", None, ["She said they came from a land of twilight, where the sun never fully shone. Where was it? Follow for more."]),
])
