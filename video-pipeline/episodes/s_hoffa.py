from episodes._short_common import *
XFADE = 0.0
PRON = {"Hoffa": "Hoff-uh"}
SHORT_HOOK = [("HE WALKED TO HIS CAR", INK, 62), ("AND VANISHED", RED, 82)]
SFX = [(1, "heartbeat", 0.2), (3, "hit", 0.2), (5, "hit", 0.3)]
SHORT = shots([
    ("hof_lot", None, ["July 30th, 1975. Jimmy Hoffa, one of the most powerful union bosses in America, waits in a restaurant parking lot near Detroit."]),
    ("hof_wait", dict(fx="zoom"), ["He's there to meet two men with ties to the mob. They never show up. At least, that's the story."]),
    ("hof_phone", dict(fx="glitch"), ["He calls his wife from a payphone to complain he's been stood up."]),
    ("hof_empty", dict(fx="shake"), ["Then he's gone. His car is found in the parking lot, unlocked."]),
    ("hof_dig", dict(fx="zoom"), ["Over the years, the FBI has dug up fields and farms looking for him. Nothing."]),
    ("hof_file", dict(fx="flash"), ["He was declared legally dead in 1982. Where is Jimmy Hoffa? Follow for more."]),
])
