from episodes._qm_short import *
SHORT_HOOK = [("THE DEATH LOOPHOLE", GOLD, 72), ("WORTH BILLIONS", WHITE, 70)]
SFX = [(0, "hit", 0.2), (1, "riser", 6.0), (1, "ching", 9.5)]
SHORT = shots([
    ("v_die", None, ["The biggest tax break in America only kicks in when you die."]),
    ("v_stepup", None, ["Buy a stock for one million dollars and it grows to one billion. Sell it, and you owe tax on nine hundred ninety-nine million. But hold it until death, and your heirs inherit it at the new value. The gain is erased."]),
    ("v_cycle", None, ["It's called the step-up in basis, and it's the final step of the billionaire playbook."]),
    ("v_logo", None, ["It works for a family home too. Follow for more."]),
])
