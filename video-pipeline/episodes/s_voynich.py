from episodes._short_common import *
PRON = {"Voynich": "Voy-nitch"}
SHORT_HOOK = [("NOBODY CAN", INK, 80), ("READ THIS BOOK", RED, 80)]
SHORT = shots([
    ("voy_book", None, ["This is the Voynich manuscript. About two hundred and forty handwritten pages, full of strange plants, stars and diagrams."]),
    ("voy_date", None, ["Tests show it was made in the early fourteen hundreds. Six hundred years ago."]),
    ("voy_script", None, ["But it is written in a script that matches no known language."]),
    ("voy_codebreakers", None, ["Even the codebreakers who cracked secret codes in World War Two failed."]),
    ("voy_plant", None, ["Many of its plants do not match any plant on Earth."]),
    ("voy_yale", None, ["Today it sits in a library at Yale University, and nobody can read a single word. Follow for more."]),
])
