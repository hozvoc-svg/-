# Episode: "A Rainy Summer at Grandma's Hill House" — cozy bedtime story (~20 min).
# Original story and characters; cozy hand-drawn look, no third-party characters.

SCENES_MODULE = "cozy_scenes"
SPEAKER = 76
LENGTH_SCALE = 1.18
GAP, TAIL = 0.95, 2.4
AMBIENT = "cozy"
CAPTION_SIZE = 40
FADE = 0.9

PRON = {}

LONG = [
    dict(scene="title", text=[
        "Hello, and welcome.",
        "Tonight's story is a quiet one.",
        "So get comfortable, let your shoulders drop, and take a slow breath in... and out.",
        "This is the story of a rainy summer at Grandma's hill house.",
    ]),
    # ---- the journey
    dict(scene="train", chapter="The journey", text=[
        "The train moved slowly through the green countryside, as if it had all the time in the world.",
        "Mira sat by the window with her small yellow suitcase on her knees.",
        "Outside, the fields went by in soft waves. Wheat, then clover, then a little river that sparkled for a moment and was gone.",
    ]),
    dict(scene="train", args=dict(evening=0.2), text=[
        "She was ten years old, and this was the first summer she would spend away from the city.",
        "Her mother had kissed her on the platform and said, Grandma's house is very quiet. You will like it, I think.",
        "Mira was not so sure. She liked noise. She liked busy streets and bright shop windows.",
        "But the gentle rocking of the train made her eyes heavy, and for a while, she simply watched the clouds.",
    ]),
    dict(scene="busstop", text=[
        "The train stopped at a tiny station with a single bench and a clock that was five minutes slow.",
        "From there, an old blue bus carried her along a narrow road between hedges full of wild roses.",
        "The bus driver hummed a tune under his breath. He did not seem to be in any hurry either.",
        "At the very last stop, where the road simply ended in a field of tall grass, Mira got off.",
    ]),
    dict(scene="path", text=[
        "A small path wound up the hill, between daisies and buttercups.",
        "The air smelled of warm grass and something sweet, like honey.",
        "Mira pulled her suitcase behind her. Its little wheels bumped over the stones, click, click, click.",
        "And then, at the top of the hill, she saw it.",
    ]),
    dict(scene="hill_house", chapter="Grandma's house", text=[
        "A white house with a red roof, sitting under an enormous old tree.",
        "The tree was so big that its branches reached over the whole roof, like an arm around a friend's shoulders.",
        "The windows had green shutters, and in one of them, a curtain moved.",
        "The front door opened, and there was Grandma, wiping her hands on her apron and smiling the widest smile.",
    ]),
    dict(scene="kitchen", text=[
        "Grandma's kitchen was the warmest room Mira had ever been in.",
        "There were jars of jam on every shelf, red and orange and dark purple, glowing in the light from the window.",
        "A kettle sat on the old stove, and a loaf of bread was cooling on the table, its crust golden and crackly.",
        "You must be hungry, Grandma said. And Mira realized that she was.",
    ]),
    dict(scene="kitchen", args=dict(cat=True), text=[
        "That was when she noticed the cat.",
        "He was round and orange, sleeping on a chair by the stove, his tail curled neatly around his paws.",
        "That is Biscuit, said Grandma. He has lived here longer than the kettle.",
        "Biscuit opened one eye, looked at Mira for a long moment, and then closed it again, as if to say, you may stay.",
    ]),
    dict(scene="kitchen", args=dict(steam=True), text=[
        "They ate warm bread with butter and apricot jam, and drank tea from cups with tiny blue flowers painted on them.",
        "Grandma asked about the train, about school, about the city.",
        "But she never hurried. She listened to every answer as if it were the most interesting thing in the world.",
        "And slowly, without noticing, Mira began to relax.",
    ]),
    # ---- the morning
    dict(scene="hill_house", chapter="The first morning", args=dict(morning=True), text=[
        "The next morning, Mira woke up to a sound she did not recognize.",
        "It took her a moment to understand. It was birds. Dozens of them, singing in the old tree outside her window.",
        "In the city, she woke up to cars and buses. Here, she woke up to a whole choir.",
        "She went to the window. A soft white mist lay over the valley, like a blanket that the hills had not yet thrown off.",
    ]),
    dict(scene="hill_house", args=dict(morning=True, chickens=True), text=[
        "Grandma was already outside, scattering grain for the chickens.",
        "There were five of them, round and brown and very busy, and each one had a name.",
        "Pepper, Clover, Dot, Marigold, and Mrs. Plum, who was the oldest and the bossiest.",
        "Mira helped to look for eggs in the straw. She found four, still warm, and carried them inside like treasure.",
    ]),
    dict(scene="kitchen", args=dict(steam=True), text=[
        "For breakfast, Grandma made pancakes, thin and golden, with honey from a jar shaped like a little beehive.",
        "Biscuit sat under the table, hoping very politely that something might fall.",
        "Something did. Grandma pretended not to notice.",
        "Outside, the mist slowly lifted, and the whole valley appeared, green and fresh and sparkling with dew.",
    ]),
    # ---- the rain
    dict(scene="rain_window", chapter="The rain", args=dict(start=True), text=[
        "On the third day, the rain came.",
        "It started softly, in the early afternoon. A few drops on the window. Then a few more.",
        "Then the whole sky turned a gentle silver grey, and the rain began to fall properly, steady and calm.",
    ]),
    dict(scene="rain_window", text=[
        "Mira sat on the wide windowsill with a blanket around her shoulders.",
        "The raindrops ran down the glass in little rivers, joining and splitting and joining again.",
        "She tried to guess which drop would reach the bottom first. She was almost always wrong.",
        "Outside, the big tree swayed slowly, and its leaves shone like they had been polished.",
    ]),
    dict(scene="rain_room", text=[
        "Biscuit jumped up beside her, turned around three times, and settled against her leg.",
        "He was warm and heavy, and he began to purr. A low, soft sound, like a tiny engine far away.",
        "Grandma brought two cups of hot cocoa and a plate of oat cookies, and sat down in her old armchair with her knitting.",
        "For a long time, nobody said anything at all.",
    ]),
    dict(scene="rain_room", args=dict(lamp=True), text=[
        "There was only the sound of the rain on the roof.",
        "The click of the knitting needles.",
        "The purring of the cat.",
        "And Mira noticed something strange. She did not miss the noise of the city at all.",
    ]),
    dict(scene="rain_window", args=dict(slow=True), text=[
        "Why does rain sound so nice, Grandma? she asked.",
        "Grandma thought about it for a while.",
        "Maybe, she said, because when it rains, the whole world gives us permission to slow down.",
        "Nobody expects you to do anything on a rainy afternoon. You can simply be.",
    ]),
    dict(scene="rain_window", args=dict(slow=True), text=[
        "Mira liked that idea very much.",
        "She leaned her head against the cool glass and watched the rain.",
        "Drop after drop. Slow and steady.",
        "And somewhere between one drop and the next, she fell asleep.",
    ]),
    # ---- the garden
    dict(scene="garden", chapter="The garden after rain", text=[
        "When she woke up, the rain had stopped.",
        "The light outside had changed. It was golden now, and everything sparkled.",
        "Come, said Grandma, putting on her rubber boots. The garden is always most beautiful after the rain.",
    ]),
    dict(scene="garden", args=dict(puddles=True), text=[
        "The air was cool and fresh, and smelled of wet earth and green leaves.",
        "There were puddles on the path, and each one held a little piece of the sky, blue with soft white clouds.",
        "Mira jumped into the biggest one. Splash.",
        "Grandma laughed and jumped into the one next to it.",
    ]),
    dict(scene="garden", args=dict(butterflies=True), text=[
        "In the vegetable beds, the tomatoes hung heavy and red, with drops of water still shining on their skins.",
        "The beans had climbed all the way up their poles, and the sunflowers were turning their faces back toward the sun.",
        "A small snail was making its way across a leaf, very slowly, very carefully.",
        "Where is he going? Mira asked. Nowhere in particular, said Grandma. And he is taking his time getting there.",
    ]),
    dict(scene="garden", args=dict(basket=True), text=[
        "They picked tomatoes and green beans and a handful of strawberries, and put them in a wicker basket.",
        "Mira ate one strawberry straight from the plant. It was warm from the sun and tasted like summer itself.",
        "Biscuit followed them along the path, carefully stepping around every puddle, as cats do.",
        "And the evening sun painted everything in shades of gold and honey.",
    ]),
    # ---- the river
    dict(scene="river", chapter="The river", text=[
        "The next day was warm and still, and Grandma said, let's walk down to the river.",
        "They took a path through the meadow, where the grass was so tall it brushed Mira's shoulders.",
        "Grasshoppers jumped out of the way with tiny clicks, and somewhere a bee was humming its long, lazy song.",
        "At the bottom of the hill, the river ran clear and shallow over smooth round stones.",
    ]),
    dict(scene="river", args=dict(bridge=True), text=[
        "There was a little wooden bridge, with a railing worn silver by the weather.",
        "They sat on the edge of it and let their feet hang down, just above the water.",
        "Mira could see small fish, quick and silver, hiding in the shadows of the stones.",
        "A blue dragonfly landed on the railing right beside her hand, stayed for a moment, and flew away again.",
    ]),
    dict(scene="river", args=dict(bridge=True, boat=True), text=[
        "Grandma took a page from an old newspaper and folded it, corner by corner, into a little paper boat.",
        "She showed Mira how to do it. Fold, and press. Fold, and press.",
        "Then they set their boats on the water, and watched them drift away under the bridge.",
        "The boats turned slowly in the current, bumped gently against a stone, and floated on, toward somewhere far away.",
    ]),
    dict(scene="river", args=dict(bridge=True, boat=True), text=[
        "Where will they go? Mira asked.",
        "Maybe to the sea, said Grandma. Maybe just to the next bend in the river. Either way, it will be a fine journey.",
        "They sat on the bridge until the shadows grew long, listening to the water.",
        "It talked to itself softly, the way rivers do, and never seemed to run out of things to say.",
    ]),
    # ---- the tree
    dict(scene="tree", chapter="The old tree", text=[
        "Behind the house, under the big old tree, there was a swing.",
        "It hung from the lowest branch on two thick ropes, and its wooden seat was worn smooth by many years.",
        "Your mother used to sit here for hours, said Grandma. And I did too, when I was your age.",
    ]),
    dict(scene="tree", args=dict(swing=True), text=[
        "Mira sat on the swing and pushed off gently with her feet.",
        "Forward, and back. Forward, and back.",
        "Above her, the leaves moved in the breeze, and little spots of light danced across the grass.",
        "From up high, she could see the whole valley. The fields, the river, the tiny road where the blue bus had brought her.",
    ]),
    dict(scene="tree", args=dict(swing=True, dusk=True), text=[
        "How old is the tree? Mira asked.",
        "Older than the house, said Grandma. Older than anyone remembers. It has seen a great many summers.",
        "Mira put her hand on the rough, warm bark.",
        "She imagined all those summers. All the children who had sat on this swing, looking at this same valley, feeling this same breeze.",
        "It made her feel small, but in a good way. Like being part of something very big and very gentle.",
    ]),
    # ---- evening
    dict(scene="evening_room", chapter="Evening", text=[
        "When the sun went down, Grandma lit the old lamp in the kitchen.",
        "Its light was soft and yellow, and it made the whole room look like a painting.",
        "They made soup together, with the tomatoes and beans from the garden.",
        "Mira chopped the vegetables, very carefully, and Grandma stirred the pot and added a pinch of this and a pinch of that.",
    ]),
    dict(scene="evening_room", args=dict(steam=True), text=[
        "The soup bubbled quietly on the stove, and the smell filled the house.",
        "Outside the window, the sky turned from orange to pink, and then to a deep, soft blue.",
        "They ate at the wooden table, with fresh bread and a little candle between them.",
        "Biscuit sat on the third chair, as if he were part of the dinner too. Which, of course, he was.",
    ]),
    dict(scene="evening_room", args=dict(steam=True), text=[
        "After dinner, Grandma told stories.",
        "About the winter when the snow reached the windows, and they had to dig a tunnel to the gate.",
        "About the summer when a family of hedgehogs lived under the porch.",
        "About Mira's mother, when she was small, and how she once tried to teach Biscuit's great-grandmother to fetch a ball.",
        "Did it work? Mira asked. Not even once, said Grandma, and they both laughed.",
    ]),
    # ---- night
    dict(scene="night_sky", chapter="The night", text=[
        "Before bed, Grandma said, come outside. I want to show you something.",
        "They stepped out onto the porch, into the cool night air.",
        "And Mira gasped.",
        "The sky was full of stars. More stars than she had ever seen. In the city, there were only a few. Here, there were thousands.",
    ]),
    dict(scene="night_sky", args=dict(fireflies=True), text=[
        "And then, down in the grass, little lights began to appear.",
        "One. Then three. Then dozens.",
        "Fireflies, said Grandma softly. They come out on warm nights after the rain.",
        "The tiny lights floated slowly over the meadow, blinking on and off, like stars that had come down to visit.",
    ]),
    dict(scene="night_sky", args=dict(fireflies=True), text=[
        "They sat on the porch steps for a long time, wrapped in one big blanket, watching.",
        "Somewhere far away, an owl called. Hoo. Hoo.",
        "The breeze moved through the old tree with a sound like a long, slow breath.",
        "Grandma, Mira whispered. I think I like quiet after all.",
        "Grandma smiled and put her arm around her. I thought you might, she said.",
    ]),
    dict(scene="bedroom", chapter="Sleep", text=[
        "Mira's bedroom was in the attic, under the slanted roof.",
        "The bed was soft, with a heavy quilt made of many colorful squares, each one sewn by hand.",
        "Through the little round window, she could see the moon, round and silver, resting just above the hill.",
        "Biscuit climbed up the stairs, jumped onto the bed, and curled up by her feet.",
    ]),
    dict(scene="bedroom", args=dict(rain=True), text=[
        "And then, very softly, the rain began again.",
        "Tap. Tap. Tap, on the roof, just above her head.",
        "Mira pulled the quilt up to her chin.",
        "She listened to the rain, and the purring of the cat, and the creak of the old house settling for the night.",
    ]),
    dict(scene="bedroom", args=dict(rain=True), text=[
        "She thought about the train, and the fields, and the blue bus.",
        "About the puddles full of sky, and the warm strawberry, and the snail who was in no hurry at all.",
        "About the swing, and the old tree, and all its summers.",
        "And the fireflies, floating over the dark meadow like little lanterns.",
    ]),
    dict(scene="bedroom", args=dict(rain=True, dark=True), text=[
        "Her breathing became slow and deep.",
        "In... and out.",
        "The rain kept falling, gently, steadily, covering the hill house like a soft grey blanket.",
        "There was nowhere to go. Nothing to do. Nothing to worry about.",
        "Only the rain. Only the quiet. Only rest.",
    ]),
    dict(scene="bedroom", args=dict(rain=True, dark=True), text=[
        "Let your forehead soften. Let your jaw relax.",
        "Let your shoulders sink down into the bed, as if they were melting, slowly, like butter on warm bread.",
        "Feel your arms grow heavy. Your hands. Your fingers.",
        "Feel your legs grow heavy too, all the way down to your toes.",
        "And with every breath out, sink a little deeper into rest.",
    ]),
    dict(scene="bedroom", args=dict(rain=True, dark=True), text=[
        "Somewhere, on a quiet hill, there is a white house with a red roof.",
        "The rain is falling softly on it now.",
        "A cat is sleeping by a warm stove. A tree is swaying gently in the dark.",
        "And the river is still talking softly to itself, carrying little paper boats toward the sea.",
        "All is well. All is quiet.",
    ]),
    dict(scene="bedroom", args=dict(rain=True, dark=True), text=[
        "And you can rest now too.",
        "Let the rain carry your thoughts away, one drop at a time.",
        "Your body is heavy and warm. Your breath is slow.",
        "Everything is quiet. Everything is safe.",
        "Good night.",
    ]),
    dict(scene="outro", text=[
        "Thank you for spending this quiet time with me.",
        "If you enjoyed this story, you can subscribe for a new cozy story every week.",
        "Sleep well, and sweet dreams.",
    ]),
]

SHORT = []


def thumb(S, c):
    """1280x720 thumbnail drawn on the 1920x1080 canvas: rainy window, cottage, sleeping cat."""
    import math
    T = 4.0
    S.interior(c, wall=(0.55, 0.45, 0.45), dim=0.4)
    wx, wy, ww, wh = 120, 80, 1100, 840
    c.save(); c.rectangle(wx, wy, ww, wh); c.clip()
    S.sky(c, (0.30, 0.34, 0.52), (0.85, 0.62, 0.55))
    S.hill(c, 640, 40, (0.30, 0.40, 0.42), 1.0)
    c.move_to(-100, 1200); c.line_to(-100, 820); c.curve_to(400, 700, 900, 700, 1400, 820)
    c.line_to(1400, 1200); c.close_path(); S.rgba(c, (0.25, 0.38, 0.32)); c.fill()
    S.big_tree(c, 760, 760, 1.2, T, night=0.3)
    S.house(c, 680, 790, 1.1, lit=1.0, night=0.3, T=T)
    S.rain_lines(c, T, wx, wy, ww, wh, 1.0, 0.55)
    c.restore()
    S.glass_drops(c, T, wx, wy, ww, wh, 1.0)
    S.window_frame(c, wx, wy, ww, wh)
    S.rgba(c, (0.92, 0.90, 0.85)); c.rectangle(80, 920, 1180, 50); c.fill()
    S.cat(c, 900, 922, 1.4, T)
    S.rgba(c, (0.95, 0.95, 1.0)); c.rectangle(400, 850, 80, 70); c.fill()
    S.steam(c, 440, 840, T, 0.7, 1.2)
    S.glow(c, 1600, 500, 700, S.WARM, 0.35)
    S.serif(c, "Rainy", 1590, 330, 150, S.INK)
    S.serif(c, "Summer", 1590, 480, 130, S.INK)
    S.serif(c, "at Grandma's", 1590, 590, 70, (1, 0.90, 0.70))
    S.rgba(c, (0.15, 0.12, 0.22), 0.8); S.rrect(c, 1330, 680, 520, 100, 50); c.fill()
    S.serif(c, "Sleep Story", 1590, 750, 56, S.INK, bold=False, italic=True)
    S.grain(c, 0.06)
