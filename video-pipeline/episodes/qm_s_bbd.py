from episodes._qm_short import *
SHORT_HOOK = [("BILLIONAIRES PAY $0 TAX", WHITE, 64), ("...LEGALLY", GOLD, 76)]
SFX = [(0, "hit", 0.1), (1, "pop", 0.4), (2, "ching", 2.0), (4, "riser", 1.5), (5, "hit", 0.2)]
SHORT = shots([
    ("v_zero", None, ["In 2018, one of the richest men alive paid zero dollars in federal income tax. Legally. Here's the three-step trick."]),
    ("v_buy", None, ["Step one: buy assets that grow, like stock in your own company. And never sell, because selling is what gets taxed."]),
    ("v_borrow", None, ["Step two: borrow against those shares. A loan isn't income, so there's no tax. You live on borrowed money while the stock keeps growing."]),
    ("v_die", None, ["Step three: die."]),
    ("v_stepup", None, ["Your heirs inherit the shares, and the law resets their cost to today's value. Decades of gains, never taxed."]),
    ("v_cycle", None, ["Buy, borrow, die. Completely legal. Follow for the part you can actually use."]),
])
