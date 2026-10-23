# Illustrated version of hill_house: one image per story segment (index = LONG segment).
# Images are generated in Google Flow from PROMPTS and saved as images/hill_house/NN.png.

STYLE = ("Soft hand-drawn watercolor and ink illustration, cozy nostalgic hand-painted animated film look, "
         "warm natural light, gentle pastel colors, detailed painterly background, wide 16:9 frame, no text")
MIRA = ("Mira, a 10-year-old girl with a black chin-length bob, a small red flower hair clip, rosy cheeks, "
        "a blue-and-white striped long-sleeve shirt, denim overalls and yellow rubber boots")
GRAN = "Grandma, a kind elderly woman with silver hair in a low bun, a pink knitted cardigan and a cream apron"
CAT = "Biscuit, a chubby orange tabby cat with a white chest and white paws"

# image number -> prompt (without STYLE)
PROMPTS = {
    1: "A small white cottage with a red roof and green shutters under an enormous old tree, on top of a green hill above a summer valley, fluffy clouds, wildflowers",
    2: f"{MIRA} sitting by the window of an old countryside train, chin on her hand, looking out at rolling green fields and a sparkling river",
    3: f"{MIRA} dozing on a train seat with a small yellow suitcase on her knees, soft afternoon light through the window",
    4: "An old blue country bus driving along a narrow lane between hedges full of pink wild roses, rolling hills behind",
    5: f"{MIRA} pulling a small yellow suitcase up a winding dirt path between daisies and buttercups, a white cottage with a red roof at the top of the hill",
    6: f"{GRAN} standing in the doorway of the white cottage, smiling widely and waving at {MIRA} who has just arrived with her suitcase",
    7: "A warm rustic country kitchen: shelves of glowing jam jars in red, orange and purple, an old iron stove with a kettle, a golden loaf of bread cooling on a wooden table, sunlight through the window",
    8: f"{CAT} asleep on a wooden chair beside a warm stove, tail curled around its paws, {MIRA} leaning in to look at it curiously",
    9: f"{MIRA} and {GRAN} at a wooden kitchen table eating bread with apricot jam, steaming tea cups with tiny blue flowers",
    10: "Early morning view from a cottage attic window: soft white mist lying over a green valley, birds in a big tree, pale golden sunrise",
    11: f"{GRAN} scattering grain for five round brown chickens in the yard, {MIRA} holding four brown eggs carefully in her hands",
    12: f"Breakfast table with a stack of thin golden pancakes and a honey jar shaped like a beehive, {CAT} sitting politely under the table looking up",
    13: "Rain beginning to fall on an old wooden cottage window, first drops on the glass, silver-grey sky and a big tree outside",
    14: f"{MIRA} sitting on a wide windowsill wrapped in a knitted blanket, watching raindrops run down the glass, cozy indoor light",
    15: f"Cozy living room on a rainy afternoon: {GRAN} knitting in an old armchair, {MIRA} on the windowsill with {CAT} curled against her leg",
    16: f"Two mugs of hot cocoa and a plate of oat cookies on a small table, a warm lamp glowing, rain on the window behind, {CAT} purring nearby",
    17: "Close-up of raindrops running down a window pane, a softly blurred green tree and garden behind the glass",
    18: f"{MIRA} asleep with her head against the cool window glass, blanket around her shoulders, rain softly falling outside",
    19: f"A cottage vegetable garden just after rain in golden evening light, everything sparkling with drops, {GRAN} in rubber boots on the path",
    20: f"{MIRA} jumping into a big puddle that reflects the blue sky and white clouds, splash, {GRAN} laughing nearby",
    21: "Close-up of a small snail crawling across a wet green leaf, ripe red tomatoes with water drops in the background",
    22: f"{MIRA} and {GRAN} picking strawberries and tomatoes into a wicker basket, {CAT} stepping carefully around puddles behind them",
    23: f"{MIRA} and {GRAN} walking down a path through tall summer grass toward a clear river at the bottom of the hill",
    24: f"{MIRA} and {GRAN} sitting on the edge of a small wooden bridge with their feet dangling over a clear shallow river, a blue dragonfly on the railing",
    25: f"{GRAN} showing {MIRA} how to fold a paper boat from an old newspaper, sitting on the wooden bridge",
    26: "Two little paper boats drifting on a clear river under a small wooden bridge, warm late afternoon light, long shadows",
    27: "An enormous old tree behind a cottage with a wooden rope swing hanging from its lowest branch, dappled sunlight on the grass",
    28: f"{MIRA} on a rope swing under a huge old tree, swinging forward, a wide green valley with a river and tiny road below",
    29: f"{MIRA} touching the rough bark of the huge old tree at dusk, {GRAN} standing beside her, pink and orange sky",
    30: f"{GRAN} lighting an old oil lamp in a rustic kitchen at dusk, soft yellow light filling the room",
    31: f"{MIRA} chopping vegetables and {GRAN} stirring a steaming soup pot on an old stove, warm lamplight",
    32: f"{MIRA}, {GRAN} and {CAT} at a wooden dinner table with soup and a small candle, laughing together, night outside the window",
    33: f"{GRAN} and {MIRA} stepping out onto the wooden porch of the cottage at night, a sky full of thousands of stars",
    34: "Hundreds of glowing fireflies floating over a dark summer meadow below a starry sky, a cottage with warm lit windows in the distance",
    35: f"{MIRA} and {GRAN} seen from behind, sitting on the porch steps wrapped in one big blanket, watching fireflies and stars",
    36: f"A cozy attic bedroom under a slanted roof, a bed with a handmade patchwork quilt, a small round window showing a silver full moon, {CAT} curled on the bed",
    37: f"{MIRA} lying in bed under a patchwork quilt listening to the rain, {CAT} curled at her feet, rain on the round attic window, soft moonlight",
    38: f"{MIRA} sleeping peacefully on her side with {CAT} curled up next to her under a patchwork quilt, gentle smiles",
    39: "The white cottage with a red roof on the hill at night in soft rain, one warm lit window, the big tree swaying gently",
}

# story segment index -> image number (consecutive segments may share an image)
SEGMENT_IMAGES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                  23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 37, 38, 38, 39, 38, 39]
