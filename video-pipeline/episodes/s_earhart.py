from episodes._short_common import *
XFADE = 0.0
PRON = {"Earhart": "Air-hart", "Noonan": "Noo-nan"}
SHORT_HOOK = [("SHE VANISHED", INK, 80), ("OVER THE OCEAN", RED, 76)]
SFX = [(2, "riser", 0.0), (3, "hit", 0.1), (5, "hit", 0.2)]
SHORT = shots([
    ("ae_pilot", None, ["1937. Amelia Earhart, the most famous pilot in the world, is trying to fly around the entire planet."]),
    ("ae_ocean", dict(fx="zoom"), ["With her navigator, Fred Noonan, she heads for a tiny island in the middle of the Pacific."]),
    ("ae_radio", dict(fx="glitch"), ["Hours later, her voice crackles over the radio. We must be on you, but cannot see you. Gas is running low."]),
    ("ae_silence", dict(fx="flash"), ["Then, silence. A huge search finds nothing."]),
    ("ae_island", dict(fx="zoom"), ["Some believe they crashed into the sea. Others think they landed on a remote island and lived as castaways."]),
    ("ae_mystery", dict(fx="flash"), ["Her plane has never been found. Follow for more."]),
])
