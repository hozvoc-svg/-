from episodes._short_common import *
PRON = {"D.B.": "D. B."}
SHORT_HOOK = [("HE JUMPED WITH", INK, 64), ("$200,000", (0.35, 1.0, 0.5), 96)]
SHORT = shots([
    ("db_board", None, ["November 1971. A man in a dark suit boards a flight from Portland to Seattle. He calls himself Dan Cooper."]),
    ("db_note", None, ["He hands the flight attendant a note. He has a bomb."]),
    ("db_money", None, ["He demands two hundred thousand dollars and four parachutes. In Seattle, he gets them, and lets the passengers go."]),
    ("db_jump", None, ["Then, somewhere over the forests of Washington, at night, in the rain, he opens the rear stairs... and jumps."]),
    ("db_found", None, ["He was never seen again. In 1980, a boy found part of the money, buried by the Columbia River."]),
    ("db_file", None, ["It is still the only unsolved plane hijacking in American history. Follow for more."]),
])
