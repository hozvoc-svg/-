from episodes._qm_short import *
SHORT_HOOK = [("YOU PAY MORE TAX", WHITE, 70), ("THAN BILLIONAIRES", GOLD, 70)]
SFX = [(0, "pop", 0.4), (0, "hit", 2.2), (1, "ching", 3.5), (2, "pop", 0.5)]
SHORT = shots([
    ("v_rates", None, ["Okay, so leaked IRS data showed the twenty-five richest Americans paid a true tax rate of just three point four percent. The typical household? About fourteen."]),
    ("v_salary", None, ["Why? Because the system taxes income, not wealth. Jeff Bezos's salary was about eighty-one thousand dollars. His stock was worth over a hundred billion, and growth isn't taxed until you sell."]),
    ("v_borrow", None, ["So they just... don't sell. They borrow against their shares, and loans aren't income."]),
    ("v_logo", None, ["It's called Buy, Borrow, Die. Full breakdown on our channel."]),
])
