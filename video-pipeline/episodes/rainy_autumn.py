# Episode: "A Rainy Autumn Day at Grandma's House" — bedtime story told over 48 illustrations
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
    3: ([(0.37, 0.66, "lamp")], [(1.00, .5, .5), (1.15, .70, .45), (1.08, .5, .5)]),
    4: ([(0.59, 0.49, "lamp")], [(1.02, .5, .5), (1.18, .45, .45), (1.08, .6, .5)]),
    5: ([(0.42, 0.86, "fire")], [(1.00, .5, .5), (1.15, .45, .45), (1.22, .55, .40), (1.08, .5, .5)]),
    6: ([(0.81, 0.66, "lamp")], [(1.10, .45, .55), (1.22, .45, .60), (1.08, .65, .5)]),
    7: ([(0.09, 0.56, "lamp")], [(1.02, .5, .5), (1.18, .35, .45), (1.22, .45, .40), (1.08, .5, .5)]),
    8: ([(0.09, 0.55, "lamp")], [(1.00, .5, .5), (1.20, .40, .40), (1.25, .65, .35), (1.10, .5, .5)]),
    9: ([(0.09, 0.55, "lamp")], [(1.05, .5, .5), (1.20, .65, .45), (1.10, .55, .5)]),
    10: ([(0.09, 0.55, "lamp")], [(1.05, .55, .5), (1.20, .70, .55)]),
    11: ([(0.23, 0.66, "lamp")], [(1.00, .5, .5), (1.15, .35, .55), (1.20, .55, .55)]),
    12: ([], [(1.00, .5, .5), (1.18, .65, .40), (1.25, .60, .35), (1.08, .5, .5)]),
    13: ([(0.85, 0.63, "lamp")], [(1.00, .5, .5), (1.18, .35, .40), (1.20, .62, .40), (1.06, .5, .5)]),
    14: ([(0.81, 0.63, "lamp")], [(1.02, .5, .5), (1.15, .70, .45), (1.06, .5, .5)]),
    15: ([(0.65, 0.62, "lamp")], [(1.05, .45, .55), (1.20, .40, .60), (1.10, .55, .5)]),
    16: ([], [(1.00, .5, .5), (1.15, .45, .40), (1.22, .45, .45), (1.06, .5, .5)]),
    17: ([(0.71, 0.36, "fire")], [(1.05, .55, .5), (1.20, .60, .45)]),
    18: ([(0.80, 0.71, "lamp"), (0.07, 0.89, "fire")], [(1.00, .5, .5), (1.18, .35, .45), (1.08, .6, .5)]),
    19: ([(0.89, 0.77, "fire")], [(1.00, .5, .5), (1.18, .45, .55), (1.10, .6, .55)]),
    20: ([(0.72, 0.68, "fire")], [(1.05, .5, .5), (1.20, .55, .45)]),
    21: ([(0.32, 0.63, "fire")], [(1.00, .5, .5), (1.18, .60, .55), (1.06, .45, .5)]),
    22: ([(0.56, 0.58, "fire")], [(1.00, .5, .5), (1.15, .35, .55), (1.18, .70, .55), (1.05, .5, .5)]),
    23: ([], [(1.00, .5, .5), (1.18, .35, .45)]),
    24: ([], [(1.05, .5, .5), (1.20, .55, .45)]),
    25: ([(0.80, 0.70, "fire")], [(1.00, .5, .5), (1.18, .55, .50)]),
    26: ([(0.50, 0.55, "fire")], [(1.00, .5, .5), (1.20, .5, .55)]),
    27: ([(0.68, 0.55, "lamp"), (0.93, 0.64, "fire")], [(1.00, .5, .5), (1.18, .70, .55)]),
    28: ([(0.82, 0.80, "fire")], [(1.00, .5, .5), (1.18, .55, .40)]),
    29: ([(0.10, 0.83, "fire")], [(1.00, .5, .5), (1.15, .50, .45), (1.06, .5, .5)]),
    30: ([], [(1.05, .5, .5), (1.20, .5, .45)]),
    31: ([(0.83, 0.80, "fire")], [(1.00, .5, .5), (1.18, .45, .50), (1.10, .7, .6)]),
    32: ([(0.25, 0.56, "fire")], [(1.00, .5, .5), (1.18, .55, .50), (1.25, .55, .45)]),
    33: ([(0.17, 0.56, "fire")], [(1.00, .5, .5), (1.18, .58, .48)]),
    34: ([(0.17, 0.56, "fire")], [(1.05, .5, .5), (1.20, .45, .45)]),
    35: ([(0.17, 0.56, "fire")], [(1.00, .5, .5), (1.18, .65, .50)]),
    36: ([(0.21, 0.52, "fire")], [(1.00, .5, .5), (1.18, .40, .55)]),
    37: ([(0.50, 0.62, "fire")], [(1.00, .5, .5), (1.20, .5, .50)]),
    38: ([], [(1.00, .5, .5), (1.18, .40, .40)]),
    39: ([], [(1.00, .5, .5), (1.15, .60, .55)]),
    40: ([], [(1.00, .5, .5), (1.18, .45, .60)]),
    41: ([(0.17, 0.56, "fire")], [(1.05, .5, .5), (1.20, .55, .48)]),
    42: ([(0.59, 0.48, "lamp"), (0.69, 0.42, "lamp")], [(1.00, .5, .5), (1.18, .48, .45)]),
    43: ([(0.17, 0.56, "fire")], [(1.05, .5, .5), (1.20, .40, .50)]),
    44: ([(0.59, 0.48, "lamp"), (0.69, 0.42, "lamp")], [(1.00, .5, .5), (1.18, .40, .50)]),
    45: ([(0.59, 0.48, "lamp"), (0.69, 0.42, "lamp")], [(1.00, .5, .5), (1.20, .62, .48)]),
    46: ([(0.59, 0.48, "lamp"), (0.69, 0.42, "lamp")], [(1.00, .5, .5), (1.18, .45, .50)]),
    47: ([(0.51, 0.40, "lamp")], [(1.00, .5, .5), (1.15, .5, .45), (1.25, .5, .45)]),
    48: ([(0.44, 0.66, "lamp")], [(1.00, .5, .5), (1.12, .45, .55), (1.20, .45, .55)]),
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
         "On the chair beside the bed, Mochi the cat opened one eye, as if to say, it is far too early for all this stretching."]),
    (7, ["Yuna had come to stay with her grandparents for the autumn holidays.",
         "At home, in the city, mornings were always in a hurry. Alarms, and toast, and shoes, and running for the bus.",
         "But here, mornings came slowly. And this morning, the rain had made them even slower."]),
    (8, ["Yuna pulled the soft patchwork quilt over her knees and rested her chin in her hands.",
         "Outside, the rain was falling over the fields and the mountains.",
         "The trees on the hills had turned orange and red and gold, and the rain made all the colors shine."]),
    (8, ["Raindrops ran down the window glass in long, wobbly lines.",
         "Some of them raced each other. Some of them joined together and became one bigger drop.",
         "Yuna watched them, one after another, and did not think about anything at all."]),
    (9, ["Grandma had left a cup of warm tea on the windowsill, as she did every morning.",
         "A thin line of steam rose from it, curling slowly in the cool air.",
         "Mochi jumped down from the chair, walked across the quilt with very careful paws, and went to inspect the tea."]),
    (10, ["Mochi sniffed the steam. Then she decided that tea was not for cats, and climbed back onto her chair with great dignity.",
          "Yuna laughed softly.",
          "Then, from downstairs, came a smell. Warm, and sweet, and toasty. Fresh bread."]),
    # the window in the hall
    (28, ["Yuna put on her soft cream cardigan over her star pajamas, and padded down the hallway in her socks.",
          "In the big room downstairs, a little fire was already crackling in the hearth.",
          "She stopped by the tall window and pressed her hand against the cool glass."]),
    (30, ["The glass was cold, and a little foggy from the warm air inside.",
          "When she took her hand away, a small misty handprint stayed behind for a moment.",
          "Then it faded slowly, like a secret only the window knew."]),
    # grandpa in the garden
    (3, ["Outside, in the garden, Grandpa was walking slowly along the stone path, holding his old red umbrella.",
         "He wore his straw hat even in the rain. He said it kept his thoughts dry.",
         "Every morning, rain or shine, he walked around the garden to check on the old stone lantern and the persimmon tree."]),
    (24, ["Today, the wind was playful.",
          "It tugged at Grandpa's umbrella and swirled the orange leaves all around him, like tiny dancers.",
          "Grandpa held his collar with one hand and leaned into the wind, but he was smiling. He always said that rain was simply the sky taking care of the garden."]),
    # grandma in the kitchen
    (5, ["In the kitchen, Grandma was standing by the old stone stove.",
         "A fire crackled softly inside it, and its orange light flickered through the little iron door.",
         "Good morning, sleepy one, she said, lifting the heavy black kettle onto the hottest spot. Grandma always knew who was coming."]),
    (5, ["The kitchen smelled of woodsmoke and dried herbs, which hung in little bundles from the wooden beams.",
         "Soon the kettle began to whisper, and then to hum, and then to sing.",
         "A cloud of white steam rose up and drifted toward the window, where the rain kept falling."]),
    (6, ["On the wooden counter, a round loaf of bread was waiting, still warm from the oven.",
         "Grandma took her old bread knife and began to slice it, slowly and carefully. The crust crackled under the blade.",
         "Her hands had baked this same bread for more than fifty years. They moved the way the rain fell. Calm, and steady, and sure."]),
    (4, ["The rain grew heavier, and the kitchen became darker, so Grandma lit the lamp on the big table.",
         "She struck a match, and for a moment, its little flame danced in the air.",
         "Then she touched it to the wick, and a warm golden light bloomed across the old wooden table."]),
    (4, ["There, said Grandma. Now it is a proper rainy day.",
         "Through the window, Yuna could see the misty hills, and thin grey smoke rising from the chimneys of the other houses in the valley.",
         "Everyone in the valley was staying inside today, warm and dry, listening to the same rain."]),
    (11, ["On the kitchen windowsill, Grandma had set out breakfast in a row.",
          "A cup of tea. A round, golden loaf of bread. A jar of dark blueberry jam with a wooden spoon in it.",
          "And the little lamp, glowing beside them, its reflection shining in the wet glass. Yuna thought it looked like a painting."]),
    # drawing on the window
    (12, ["While the kettle boiled again, Yuna climbed onto the wooden stool by the window.",
          "The glass was misty, so she reached out with one finger, and began to draw.",
          "A round sun, with little lines all around it. A fluffy cloud. And a small house with a pointed roof and one little window."]),
    (12, ["That is our house, she said. And the sun is for tomorrow.",
          "Grandma came to look, and nodded seriously, as if she were looking at a very important plan.",
          "A good plan, she said. But today, I think, belongs to the rain."]),
    # tea together
    (13, ["They sat together at the table by the window, and Grandma poured the tea.",
          "Grandma, said Yuna, what did you do on rainy days when you were little?",
          "Grandma smiled, and her eyes became small and crinkly. Oh, the same as you, she said. I watched the rain. I drew on the windows. And I drank tea with my own grandmother, right here, at this very table."]),
    (13, ["Yuna looked at the old wooden table.",
          "It was scratched and worn and smooth from so many years of cups and plates and elbows.",
          "She tried to imagine Grandma as a little girl, sitting in this same spot, listening to this same rain. It made her feel warm inside."]),
    (14, ["Then Grandma brought the bread, and the jar of blueberry jam.",
          "In the garden, the persimmon tree was glowing orange through the rain, and the old stone lantern wore a little cap of wet leaves.",
          "For a long while, nobody said anything at all, and that was perfectly fine."]),
    (15, ["Yuna took a thick slice of the warm bread, and spread the dark blueberry jam slowly across it, all the way to the edges.",
          "The jam was made from blueberries they had picked together on the hill, at the very end of summer.",
          "She took a bite. It tasted like sunshine that had been saved in a jar for a rainy day."]),
    (16, ["Grandma held her teacup in both hands, the way you hold something precious.",
          "She breathed in the steam, and took a slow, quiet sip, and smiled a small, contented smile.",
          "You know, she said softly, when I was young, I always wanted to be somewhere exciting. But now I think the best moments are the quiet ones."]),
    # the fire
    (25, ["After breakfast, Grandma went to the big room and knelt by the fireplace.",
          "She chose a log of white birch from the pile, and laid it gently on the fire.",
          "Birch burns sweetly, she said. It sings a little when it burns. Listen."]),
    (26, ["And Yuna listened.",
          "The fire crackled and popped, and tiny golden sparks floated up into the air and disappeared.",
          "The new log caught slowly, and the flames curled around it, orange and yellow and soft."]),
    (21, ["Mochi had found the warmest place in the whole house.",
          "She was curled up on a blue cushion, right next to the hearth, her tail wrapped around her nose.",
          "Every now and then, one of her ears twitched at the sound of the fire. But she did not wake up."]),
    # reading and embroidery
    (19, ["Yuna fetched her favorite book, a big one, full of pictures of forests and rivers and animals.",
          "She lay down on the soft rug, with her feet in the air, close to the warm fire.",
          "She turned the pages slowly, looking at every little picture, as if each one were a window into another world."]),
    (20, ["Later, she sat up and held the book open on her lap.",
          "On one page, a family of bears was walking through a quiet green forest. On another, a little deer was drinking from a stream.",
          "Yuna wondered if animals liked rainy days too. She decided that the bears probably did."]),
    (18, ["By the window, Grandma sat on her cushion with her embroidery hoop.",
          "She was stitching flowers onto a white cloth. Pink ones, with little green leaves.",
          "The lamp on the table glowed beside her, and the rain whispered on the glass."]),
    (17, ["Her needle went in, and out. In, and out.",
          "The thread pulled through the cloth with a tiny sound, softer than a breath.",
          "Slowly, slowly, petal by petal, a flower appeared, as if it were growing right there in her hands."]),
    (38, ["Every now and then, Grandma rested the hoop in her lap and looked out at the rain.",
          "Out in the courtyard, the big clay jars stood shining wet, and the drops bounced on their lids like tiny drums.",
          "She watched for a while, and smiled, as if the rain had told her something kind."]),
    (22, ["For a long time, the three of them stayed like that.",
          "Grandma with her stitching. Yuna with her book. And Mochi, asleep on her cushion between them.",
          "The fire crackled. The rain fell. And the old house held them all, safe and warm."]),
    (22, ["Every so often, Grandma looked up from her embroidery and smiled at Yuna.",
          "And every so often, Yuna looked up from her book and smiled back.",
          "They did not need to say anything. Some days are like that. Quiet, and full."]),
    # watching the rain
    (23, ["In the afternoon, the wind picked up a little.",
          "Through the big window, the last orange leaves spun down from the maple tree and landed on the wet stones of the garden.",
          "The stone lantern stood quietly in the rain, as it had for a hundred years."]),
    (29, ["Grandma took Yuna's hand, and they stood together by the window.",
          "Far away, the mountains were wrapped in soft grey clouds, and the rain fell in long silver threads.",
          "Look, said Grandma. The mountains are wearing their winter scarves already."]),
    (29, ["Yuna leaned against Grandma's side.",
          "Behind them, the fire crackled in the hearth, warm on the backs of their legs.",
          "In front of them, the whole cool, grey, beautiful world was getting a long, gentle bath."]),
    # nap
    (32, ["After a while, Yuna curled up on the old green sofa by the window, under a soft checked blanket.",
          "She only meant to rest her eyes for a moment.",
          "But the rain was so steady, and the blanket was so warm, that she fell asleep almost at once."]),
    (33, ["A little later, Mochi padded over, jumped up onto the sofa, and settled down at Yuna's feet.",
          "She kneaded the blanket twice with her paws, curled into a ball, and closed her eyes too.",
          "Now there were two sleepers by the rainy window."]),
    (34, ["Grandma came over quietly, in her soft slippers.",
          "She tucked the blanket a little higher, around Yuna's shoulders, the way she had once tucked it around Yuna's mother.",
          "She did not wake her. On a rainy day, she whispered, a nap is the most important thing of all."]),
    (37, ["Then she hung the little iron kettle over the hearth, to keep the water warm.",
          "The fire below it was small now, just a few glowing embers and one gentle flame.",
          "A thin ribbon of steam rose from the spout and drifted slowly up toward the dark wooden beams."]),
    (35, ["Grandma sat down on a cushion beside the sofa, with a cup of tea, and watched her granddaughter sleep.",
          "Yuna's cheeks were pink, and her breathing was slow and even.",
          "Outside, the rain kept falling, and Grandma was in no hurry at all."]),
    (36, ["On the windowsill, a cup of tea sat cooling in the grey afternoon light.",
          "In the glass, you could just see the reflection of the fire, flickering softly behind the raindrops.",
          "The whole house was so quiet that you could hear every single drop."]),
    (39, ["Late in the afternoon, something surprising happened.",
          "The clouds thinned, just for a moment, and a soft golden light came through the window and fell across the old table.",
          "It lit up the steam from a cup of tea, and the dark jam in its jar, and the raindrops on the glass shone like tiny beads."]),
    (39, ["The rain did not stop. It simply let the sun peek in, to say hello.",
          "Just for a few minutes, the room was full of warm gold.",
          "Then the clouds closed again, gently, like a curtain, and the soft grey came back."]),
    (41, ["When the light began to fade, the room turned warm and amber.",
          "The fire glowed in the hearth, and Grandma reached over and stroked Yuna's hair, very lightly.",
          "Yuna stirred, and sighed, and smiled in her sleep."]),
    (43, ["Mochi woke first.",
          "She stood up on the blanket and stretched, long and slow, with her front paws reaching forward and her tail high in the air.",
          "Then she gave a big yawn, as if to say, well, that was an excellent nap. And Yuna opened her eyes."]),
    (31, ["Then the door opened, and Grandpa came in, shaking the rain from his red umbrella.",
          "The garden says hello, he announced. The persimmons are ripe, and the snails are very happy.",
          "Grandma laughed, and went to sit by the fireplace with him, and Mochi settled on her little mat in front of the flames, round as a loaf of bread."]),
    (40, ["Outside, evening came softly.",
          "The last grey light faded from the window, and the rain kept tapping on the glass.",
          "A forgotten cup of tea sat on the sill, keeping the window company."]),
    (27, ["From the garden, the old house looked like a lantern.",
          "Rain dripped from the edge of the roof and ran along the wet wooden sill.",
          "And through the misty glass, you could see the warm glow of the fire inside, golden and still."]),
    # night
    (42, ["When it was dark, Grandma struck a match and lit the oil lamp on the low table.",
          "Then she lit a tall white candle beside it, too.",
          "Two little flames, she said. One for the people, and one for the rain."]),
    (44, ["Yuna came and sat beside her at the table, still a little sleepy.",
          "The lamplight made everything golden. Grandma's silver hair. The old wood. Yuna's cheeks.",
          "Behind them, the window was deep blue, and the rain ran down it in long silver lines."]),
    (46, ["Mochi climbed into Yuna's lap and curled up there, purring like a tiny engine.",
          "Grandma poured one last cup of tea, and told stories.",
          "About the winter when the snow reached the windows. About Yuna's mother, when she was small. About the summer when a family of hedgehogs lived under the porch."]),
    (46, ["Yuna listened, and stroked Mochi's soft fur, and her eyes grew heavier and heavier.",
          "The candle flickered. The lamp hummed softly. The rain kept falling.",
          "And Grandma's voice was the gentlest sound of all."]),
    (45, ["Later, when everyone had gone to bed, the lamp and the candle still glowed on the empty table for a little while.",
          "A box of matches lay beside them, waiting for tomorrow.",
          "And the house was quiet, except for the rain."]),
    # sleep
    (2, ["Upstairs, Yuna climbed back into her little bed, under the soft patchwork quilt.",
         "The lamp on the bedside table glowed low and golden.",
         "Mochi jumped onto her chair, curled into a perfect round ball, and tucked her nose under her tail."]),
    (2, ["Yuna lay on her side and listened.",
         "The rain was still falling on the roof. Tap, tap, tap.",
         "The old house creaked softly, settling down for the night, like a big friendly animal getting comfortable."]),
    (2, ["She thought about the day.",
         "The warm bread. The blueberry jam. Grandpa's red umbrella in the wind. The birch log singing in the fire.",
         "Grandma's needle, going in and out, as a little pink flower slowly bloomed. And the golden light, just for a moment, through the rain."]),
    (47, ["Her eyes grew heavy. Her breathing grew slow.",
          "In... and out.",
          "On the windowsill, a single candle burned quietly, and the rain kept falling, covering the valley like a soft grey blanket.",
          "There was nowhere to go. Nothing to do. Nothing to worry about."]),
    (2, ["And you can rest now too.",
         "Let your forehead soften. Let your jaw relax.",
         "Let your shoulders sink down, heavy and warm, as if they were melting slowly into the bed.",
         "Feel your arms grow heavy. Your hands. Your fingers. Your legs, all the way down to your toes."]),
    (47, ["Somewhere, in a quiet valley, there is an old house made of wood and stone.",
          "The rain is falling softly on it now.",
          "A little flame is glowing. A cat is sleeping. A little girl is dreaming of tomorrow's sun.",
          "All is well. All is quiet.",
          "Good night."]),
    (48, ["Thank you for spending this quiet time with me.",
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
