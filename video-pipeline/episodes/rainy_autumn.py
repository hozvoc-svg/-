# Episode: "A Rainy Autumn Day at Grandma's House" — bedtime story told over 16 illustrations
# (images/rainy_autumn/NN.png, made by the channel owner in Google Flow).

SCENES_MODULE = "photo_scenes"
AMBIENT = "cozy"
CAPTIONS = False
FADE = 0.001
SPEAKER = 76
LENGTH_SCALE = 1.18
GAP, TAIL = 0.95, 2.2
PRON = {"Yuna": "Yoo-na", "Mochi": "Mo-chee"}

# image -> (lamp/fire positions in normalized image coords, camera waypoints (zoom, center x, center y))
SHOTS = {
    1: ([(0.80, 0.51, "lamp")], [(1.00, .5, .5), (1.12, .62, .55), (1.18, .45, .45), (1.06, .5, .5)]),
    2: ([(0.09, 0.55, "lamp")], [(1.00, .5, .5), (1.10, .40, .55), (1.22, .35, .55), (1.30, .30, .55), (1.25, .55, .55), (1.12, .5, .5), (1.30, .5, .55)]),
    3: ([(0.37, 0.66, "lamp")], [(1.00, .5, .5), (1.15, .70, .45), (1.25, .75, .45), (1.08, .5, .5)]),
    4: ([(0.59, 0.49, "lamp")], [(1.02, .5, .5), (1.18, .45, .45), (1.25, .55, .50), (1.08, .6, .5)]),
    5: ([(0.42, 0.86, "fire")], [(1.00, .5, .5), (1.15, .45, .45), (1.22, .55, .40), (1.08, .5, .5)]),
    6: ([(0.81, 0.66, "lamp")], [(1.10, .45, .55), (1.22, .45, .60), (1.05, .6, .5), (1.15, .7, .5)]),
    7: ([(0.09, 0.56, "lamp")], [(1.02, .5, .5), (1.18, .35, .45), (1.22, .45, .40), (1.08, .5, .5)]),
    8: ([(0.09, 0.55, "lamp")], [(1.00, .5, .5), (1.20, .40, .40), (1.25, .65, .35), (1.10, .5, .5)]),
    9: ([(0.09, 0.55, "lamp")], [(1.05, .5, .5), (1.20, .65, .45), (1.10, .55, .5)]),
    10: ([(0.09, 0.55, "lamp")], [(1.05, .55, .5), (1.20, .70, .55), (1.10, .5, .5)]),
    11: ([(0.23, 0.66, "lamp")], [(1.00, .5, .5), (1.15, .35, .55), (1.20, .55, .55), (1.06, .5, .5)]),
    12: ([], [(1.00, .5, .5), (1.18, .65, .40), (1.25, .60, .35), (1.08, .5, .5)]),
    13: ([(0.85, 0.63, "lamp")], [(1.00, .5, .5), (1.18, .35, .40), (1.20, .62, .40), (1.06, .5, .5)]),
    14: ([(0.81, 0.63, "lamp")], [(1.02, .5, .5), (1.15, .70, .45), (1.20, .45, .50), (1.06, .5, .5)]),
    15: ([(0.65, 0.62, "lamp")], [(1.05, .45, .55), (1.20, .40, .60), (1.10, .55, .5)]),
    16: ([], [(1.00, .5, .5), (1.15, .45, .40), (1.22, .45, .45), (1.06, .5, .5)]),
}

# (image, sentences); consecutive segments on the same image continue its camera path
STORY = [
    (1, ["Hello, and welcome.",
         "Tonight's story is a quiet one, so let yourself get comfortable.",
         "Let your shoulders drop. Take a slow breath in... and let it out.",
         "This is the story of a rainy autumn day at Grandma's house."]),
    (1, ["Far away, in a valley between soft green mountains, there is an old house made of wood and stone.",
         "Its windows are old, and a little crooked, and they rattle gently when the wind blows.",
         "On this particular morning, the rain had been falling since before the sun came up.",
         "Not a storm. Just a steady, patient rain, the kind that seems as if it could go on forever."]),
    # waking up
    (7, ["Upstairs, in a small room with a wooden floor, a little girl named Yuna was waking up.",
         "She sat up in bed, stretched her arms high above her head, and gave the biggest yawn of the whole autumn.",
         "Her hair was sticking up on one side, and her red hair clip was hanging on by just one corner."]),
    (7, ["On the chair beside the bed, Mochi the cat opened one eye.",
         "Mochi was orange and white, round and soft, and she had slept on that chair every night since Yuna arrived.",
         "She looked at Yuna as if to say, it is far too early for all this stretching."]),
    (7, ["Yuna had come to stay with her grandparents for the autumn holidays.",
         "At home, in the city, mornings were always in a hurry. Alarms, and toast, and shoes, and running for the bus.",
         "But here, mornings came slowly. And this morning, the rain had made them even slower."]),
    (8, ["Yuna pulled the soft patchwork quilt over her knees and rested her chin in her hands.",
         "Outside, the rain was falling over the fields and the mountains.",
         "The trees on the hills had turned orange and red and gold, and the rain made all the colors shine."]),
    (8, ["Raindrops ran down the window glass in long, wobbly lines.",
         "Some of them raced each other. Some of them joined together and became one bigger drop.",
         "Yuna watched them, one after another, and did not think about anything at all."]),
    (8, ["The little oil lamp on the bedside table was still glowing from the night before.",
         "Its light was small and warm and golden, and it made the grey morning feel cozy instead of gloomy.",
         "Somewhere downstairs, a door creaked, and she heard footsteps on the old wooden floor."]),
    (9, ["Grandma had left a cup of warm tea on the windowsill, as she did every morning.",
         "A thin line of steam rose from it, curling slowly in the cool air.",
         "Mochi jumped down from the chair, walked across the quilt with very careful paws, and went to inspect the tea."]),
    (9, ["Mochi sniffed the steam. She sniffed it again.",
         "Then she decided that tea was not for cats, and turned around with great dignity, as if it had been her idea all along.",
         "Yuna laughed softly. Even Mochi's mistakes looked elegant."]),
    (10, ["Mochi climbed back onto her chair, turned around once, then twice, and looked at Yuna.",
          "Are you getting up, or not? her eyes seemed to ask.",
          "Yuna was not sure yet. The bed was warm, the quilt was soft, and the rain was singing on the roof."]),
    (10, ["But then, from downstairs, came a smell. Warm, and sweet, and toasty.",
          "Fresh bread.",
          "Yuna pushed back the quilt, put on her soft cream cardigan over her pajamas, and went to see."]),
    # grandpa in the garden
    (3, ["In the hallway, she stopped by the big window.",
         "Outside, in the garden, Grandpa was walking slowly along the stone path, holding his old red umbrella.",
         "He wore his straw hat even in the rain. He said it kept his thoughts dry."]),
    (3, ["Every morning, rain or shine, Grandpa walked around the garden.",
         "He checked on the old stone lantern, the persimmon tree, and the little vegetable beds.",
         "Today, the wind was blowing the last orange leaves from the branches, and they spun slowly down around him like tiny dancers."]),
    (3, ["Yuna pressed her nose against the cool glass and watched him go.",
         "His steps were slow and steady, and he did not seem to mind the rain at all.",
         "Grandpa always said that rain was simply the sky taking care of the garden, and that it would be rude to complain."]),
    # grandma in the kitchen
    (5, ["In the kitchen, Grandma was standing by the old stone stove.",
         "A fire crackled softly inside it, and its orange light flickered through the little iron door.",
         "Grandma lifted the heavy black kettle and set it right in the middle, where the heat was strongest."]),
    (5, ["Good morning, sleepy one, she said, without even turning around. Grandma always knew who was coming.",
         "The kitchen smelled of woodsmoke and dried herbs, which hung in little bundles from the wooden beams.",
         "Thyme, and mint, and lavender, and something Grandma called mountain tea, which she had picked herself in the summer."]),
    (5, ["Soon the kettle began to whisper, and then to hum, and then to sing.",
         "A cloud of white steam rose up and drifted toward the window, where the rain kept falling.",
         "It was the kind of sound that makes a kitchen feel alive."]),
    (6, ["On the wooden counter, a round loaf of bread was waiting, still warm from the oven.",
         "Grandma took her old bread knife and began to slice it, slowly and carefully.",
         "The crust crackled under the blade. Inside, the bread was soft and white and full of tiny holes."]),
    (6, ["Grandma's hands were old, and covered in little freckles and lines.",
         "They had baked this same bread for more than fifty years, and they knew exactly what to do, without hurrying.",
         "Yuna liked to watch them. They moved the way the rain fell. Calm, and steady, and sure."]),
    (6, ["Beside the bread, a little brass oil lamp glowed on the counter.",
         "Grandma lit lamps even in the daytime when it rained. She said the house liked it.",
         "And Yuna thought that maybe the house really did."]),
    (4, ["The rain grew heavier, and the kitchen became darker, so Grandma lit another lamp on the big table.",
         "She struck a match, and for a moment, its little flame danced in the air.",
         "Then she touched it to the wick, and a warm golden light bloomed and spread across the old wooden table."]),
    (4, ["Through the window, Yuna could see the misty hills and the roofs of the other houses in the valley.",
         "Thin grey smoke was rising from their chimneys too.",
         "Everyone in the valley was staying inside today, warm and dry, listening to the same rain."]),
    (4, ["There, said Grandma, putting the glass chimney back on the lamp. Now it is a proper rainy day.",
         "She wiped her hands on her apron and smiled.",
         "And the lamp made a soft, quiet sound, like a tiny breath."]),
    (11, ["On the kitchen windowsill, Grandma had set out breakfast in a row.",
          "A cup of tea. A round, golden loaf of bread. A jar of dark blueberry jam with a wooden spoon in it.",
          "And the little lamp, glowing beside them, its reflection shining in the wet glass."]),
    (11, ["Outside, in the garden, the stone lantern stood quietly in the rain, the way it had for a hundred years.",
          "The bare branches of the old tree swayed slowly, and the raindrops slid down the window, one by one.",
          "Everything was grey and silver outside, and everything was golden inside."]),
    (11, ["Yuna thought it looked like a painting.",
          "The kind of painting you could look at for a very long time, and still find something new.",
          "A drop of rain. A curl of steam. The tiny flicker of the flame."]),
    # drawing on the window
    (12, ["While the kettle boiled again, Yuna climbed onto the wooden stool by the window.",
          "The glass was misty from the warm kitchen air.",
          "She reached out with one finger, and began to draw."]),
    (12, ["First, she drew a sun. A round one, with little lines all around it.",
          "Then, a fluffy cloud.",
          "And then, at the bottom, a small house with a pointed roof, and a door, and one little window."]),
    (12, ["That is our house, she said. And the sun is for tomorrow.",
          "Grandma came to look, and nodded seriously, as if she were looking at a very important plan.",
          "A good plan, she said. But today, I think, belongs to the rain."]),
    # tea together
    (13, ["They sat together at the table by the window, and Grandma poured the tea.",
          "She held a soft cloth in her hands and dried the cups, one by one, the way she always did.",
          "Yuna sat beside her with her hands folded on the table, and watched the steam rise from her cup."]),
    (13, ["Grandma, said Yuna, what did you do on rainy days when you were little?",
          "Grandma smiled, and her eyes became small and crinkly, the way they did when she remembered something.",
          "Oh, the same as you, she said. I watched the rain. I drew on the windows. And I drank tea with my own grandmother, right here, at this very table."]),
    (13, ["Yuna looked at the old wooden table.",
          "It was scratched and worn and smooth from so many years of cups and plates and elbows.",
          "She tried to imagine Grandma as a little girl, sitting in this same spot, listening to this same rain. It made her feel warm inside."]),
    (14, ["Then Grandma brought the bread, and the jar of blueberry jam, and set them on the table.",
          "Yuna looked out of the window while she waited.",
          "In the garden, the persimmon tree was glowing orange through the rain, and the old stone lantern wore a little cap of wet leaves."]),
    (14, ["Is Grandpa coming back soon? she asked.",
          "Soon, said Grandma. When the garden has finished telling him its news.",
          "Yuna liked that idea. A garden full of news. The snails, the leaves, the puddles. Everyone with something to say."]),
    (14, ["The rain tapped on the window, gentle and steady.",
          "The lamp glowed.",
          "And for a long while, nobody said anything at all, and that was perfectly fine."]),
    (15, ["Yuna took a thick slice of the warm bread, and Grandma passed her the jar of jam.",
          "She dipped the wooden spoon in, and spread the dark blueberries slowly across the soft white bread, all the way to the edges.",
          "The jam was made from blueberries they had picked together on the hill, at the very end of summer."]),
    (15, ["She took a bite.",
          "It was sweet, and a little bit sour, and it tasted like sunshine that had been saved in a jar for a rainy day.",
          "Yuna closed her eyes. This, she decided, was the best breakfast in the whole world."]),
    (16, ["Grandma held her teacup in both hands, the way you hold something precious.",
          "She lifted it, breathed in the steam, and took a slow, quiet sip.",
          "Then she smiled, a small, contented smile, and looked out at the rain."]),
    (16, ["You know, she said softly, when I was young, I always wanted to be somewhere else. Somewhere exciting.",
          "But now I think the best moments are the quiet ones. A cup of tea. A warm kitchen. Someone you love, sitting beside you.",
          "Yuna did not say anything. She just leaned her head against Grandma's soft pink cardigan, and listened to the rain."]),
    (16, ["Later, the door opened, and Grandpa came in, shaking the rain from his umbrella.",
          "The garden says hello, he announced. The persimmons are ripe, and the snails are very happy.",
          "And Grandma poured him a cup of tea, and the three of them sat together in the lamplight for a long, long time."]),
    # evening
    (1, ["The day went by slowly, the way rainy days do.",
         "Yuna read a book. Mochi slept on every chair in the house, one after another. Grandpa fixed a squeaky drawer. Grandma knitted.",
         "And outside, the rain kept falling, softly, steadily, never in a hurry."]),
    (1, ["When evening came, the last orange leaves on the branch outside the window glowed in the fading light.",
         "A cup of tea sat on the windowsill, still warm, its steam curling slowly upward.",
         "And the little lamp was lit again, its reflection shining in the dark, wet glass."]),
    # sleep
    (2, ["At bedtime, Yuna climbed back into her little bed, under the soft patchwork quilt.",
         "The lamp on the bedside table glowed low and golden.",
         "Mochi jumped onto her chair, curled into a perfect round ball, and tucked her nose under her tail."]),
    (2, ["Yuna lay on her side and listened.",
         "The rain was still falling on the roof. Tap, tap, tap.",
         "The old house creaked softly, settling down for the night, like a big friendly animal getting comfortable."]),
    (2, ["She thought about the day.",
         "The warm bread. The blueberry jam. Grandpa's red umbrella. The little house she drew on the misty window.",
         "And Grandma, holding her cup with both hands, smiling at the rain."]),
    (2, ["Her eyes grew heavy. Her breathing grew slow.",
         "In... and out.",
         "The rain kept falling, gently, covering the valley like a soft grey blanket.",
         "There was nowhere to go. Nothing to do. Nothing to worry about."]),
    (2, ["And you can rest now too.",
         "Let your forehead soften. Let your jaw relax.",
         "Let your shoulders sink down, heavy and warm, as if they were melting slowly into the bed.",
         "Feel your arms grow heavy. Your hands. Your fingers. Your legs, all the way down to your toes."]),
    (2, ["Somewhere, in a quiet valley, there is an old house made of wood and stone.",
         "The rain is falling softly on it now.",
         "A little lamp is glowing. A cat is sleeping. A little girl is dreaming of tomorrow's sun.",
         "All is well. All is quiet.",
         "Good night."]),
    (1, ["Thank you for spending this quiet time with me.",
         "If this story helped you relax, you can subscribe for a new cozy story every week.",
         "Sleep well, and sweet dreams."]),
]


def _build():
    segs, used, prev = [], {}, None
    for i, (img, text) in enumerate(STORY):
        lamps, path = SHOTS[img]
        k = used.get(img, 0)
        cam = (path[k % (len(path) - 1)], path[k % (len(path) - 1) + 1])
        used[img] = k + 1
        args = dict(img=f"rainy_autumn/{img:02d}.png", cam=cam, lamps=tuple(lamps),
                    rain=True, fx=("dust",) if lamps else ())
        if prev is None:
            args["fade_in"] = 2.5
            args["title"] = ("A Rainy Autumn Day at Grandma's", "a cozy bedtime story")
        elif prev["img"] != args["img"]:
            args["prev"] = prev
            args["xfade"] = 2.0
        if i == len(STORY) - 1:
            args["fade_out"] = 6.0
        segs.append(dict(scene="photo", args=args, text=text))
        prev = args
    return segs


LONG = _build()
SHORT = []


def thumb(S, c):
    """Thumbnail: the girl watching the rain, with a short warm title on the right."""
    import cairo
    import cozy_scenes as C
    S.draw_image(c, dict(img="rainy_autumn/08.png", cam=((1.08, .42, .5), (1.08, .42, .5))), 0)
    g = cairo.LinearGradient(1100, 0, 1920, 0)
    g.add_color_stop_rgba(0, 0.08, 0.05, 0.03, 0)
    g.add_color_stop_rgba(1, 0.08, 0.05, 0.03, 0.75)
    c.set_source(g)
    c.rectangle(0, 0, 1920, 1080)
    c.fill()
    C.serif(c, "Rainy", 1560, 330, 150, C.INK)
    C.serif(c, "Autumn", 1560, 480, 130, C.INK)
    C.serif(c, "at Grandma's", 1560, 590, 70, (1, 0.90, 0.70))
    C.rgba(c, (0.15, 0.10, 0.08), 0.8)
    C.rrect(c, 1310, 680, 500, 100, 50)
    c.fill()
    C.serif(c, "Sleep Story", 1560, 750, 56, C.INK, bold=False, italic=True)
