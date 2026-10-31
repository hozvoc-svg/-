from episodes._short_common import *
PRON = {"Hauser": "How-zer", "Ansbach": "Ahns-bahk", "Nuremberg": "Nyoor-em-berg"}
XFADE = 0.0  # hard cuts with entrance effects instead of dissolves
SHORT_HOOK = [("THE BOY", INK, 84), ("FROM NOWHERE", RED, 84)]
SFX = [(0, "heartbeat", 0.2), (3, "heartbeat", 0.4), (4, "hit", 0.25), (5, "riser", 0.0), (6, "hit", 0.1)]
SHORT = shots([
    ("kh_cell", None, ["Imagine you spent your whole childhood in a dark cell and never saw a face. In 1828, one boy said he did. But who was he?"]),
    ("kh_square", dict(fx="zoom"), ["May 1828. Nuremberg. A teenage boy stumbles into the town square, barely able to speak, holding a letter."]),
    ("kh_name", dict(fx="flash"), ["Asked his name, he writes two words. Kaspar Hauser."]),
    ("kh_captor", dict(fx="glitch"), ["He said he grew up alone in a dark cell, on bread and water, and never saw his captor's face."]),
    ("kh_park", dict(fx="shake"), ["Five years later, he staggers home with a stab wound. Near the scene: a note, written backwards. Days later, he is dead."]),
    ("kh_prince", dict(fx="zoom"), ["A lost prince? DNA says probably not. Did he stab himself? Some think so."]),
    ("kh_grave", dict(fx="flash"), ["Victim, or liar? Follow for more."]),
])
