from episodes._short_common import *
XFADE = 0.0
PRON = {"Babushka": "Ba-boosh-ka", "Dealey": "Dee-lee"}
SHORT_HOOK = [("SHE FILMED IT ALL", INK, 70), ("AND DISAPPEARED", RED, 72)]
SFX = [(0, "hit", 0.6), (1, "riser", 0.0), (3, "hit", 0.3)]
SHORT = shots([
    ("bab_plaza", None, ["November 22nd, 1963. Dallas. President Kennedy's car passes through Dealey Plaza, when shots are fired."]),
    ("bab_woman", dict(fx="zoom"), ["In photos of that moment, there's a woman in a brown coat and a headscarf. She seems to be filming everything."]),
    ("bab_close", dict(fx="flash"), ["She was closer to the president than almost anyone. Her footage could show what really happened."]),
    ("bab_film", dict(fx="glitch"), ["Investigators wanted her film. It has never been seen."]),
    ("bab_unknown", dict(fx="zoom"), ["Years later, a woman claimed to be her, but her story had problems. Who was the Babushka Lady? Follow for more."]),
])
