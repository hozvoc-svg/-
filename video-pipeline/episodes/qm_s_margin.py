from episodes._qm_short import *
SHORT_HOOK = [("BORROW, DON'T SELL?", WHITE, 70), ("HERE'S THE CATCH", RED, 72)]
SFX = [(0, "pop", 0.3), (1, "glitch", 1.5), (1, "hit", 3.0)]
SHORT = shots([
    ("v_borrow", None, ["Billionaires borrow against their stock instead of selling it, because loans aren't taxed. Sounds perfect."]),
    ("v_margin", None, ["But here's the catch. If the stock crashes, the bank demands more collateral. It's called a margin call, and it can force you to sell at the worst possible moment."]),
    ("v_logo", None, ["Debt is a tool, not free money. Follow The Quiet Money for more."]),
])
