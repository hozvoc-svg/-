from episodes._short_common import *
PRON = {"Tamam Shud": "Tah-mahm Shood"}
SHORT_HOOK = [("UNKNOWN MAN", RED, 80), ("+ a secret code", INK, 48)]
SHORT = shots([
    ("som_beach", None, ["December 1st, 1948. A man is found dead on a beach in Australia. Neatly dressed. No ID."]),
    ("som_labels", None, ["Every label on his clothes has been cut off."]),
    ("som_scrap", None, ["In a hidden pocket, police find a tiny scrap of paper. Two words: Tamam Shud. It means, it is finished."]),
    ("som_code", None, ["The words were torn from a rare book of poems. Inside it: a phone number, and a code nobody has ever cracked."]),
    ("som_dna", None, ["In 2022, DNA finally gave him a name. Carl Webb, an engineer from Melbourne."]),
    ("som_code", dict(end=True), ["But why he died, and what the code means, is still a mystery. Follow for more."]),
])
