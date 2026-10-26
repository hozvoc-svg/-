# Stickman Unsolved: The Mary Celeste (1872). Long-form, ElevenLabs narration, channel-style captions.
SCENES_MODULE = "sea_scenes"
XFADE = 0.6
FADE = 0.001
OVERLAY_FX = (("film_grain", 0.6),)
CHAPTER_STYLE = "typewriter"
CHAPTER_PAIR = "editorial"
CHAPTER_Y = 0.075
CAPTION_STYLE = "punch"
VERTICAL_FILL = True
EL_SETTINGS = dict(stability=0.45, similarity_boost=0.75, style=0.15, speed=0.95)

PRON = {
    "Morehouse": "More-house",
    "Dei Gratia": "Day-ee Grah-tsia",
    "Solly-Flood": "Solly Flood",
    "Habakuk Jephson": "Haba-kuk Jefson",
    "Sella": "Sella",
}

LONG = [
    dict(scene="open_sea", text=[
        "December 1872. The middle of the Atlantic Ocean.",
        "The crew of a small ship spots another vessel on the horizon, drifting strangely, its sails half torn.",
        "They shout. Nobody answers.",
    ]),
    dict(scene="boarding", text=[
        "When they climb aboard, they find the ship in good condition.",
        "There is food for six months. Fresh water. Clothes, personal belongings, even the captain's family things.",
        "But there is no one on board. Not a single person.",
    ]),
    dict(scene="title", text=[
        "This is the Mary Celeste. The most famous ghost ship in history.",
        "And after one hundred and fifty years, nobody knows what happened to the ten people on board.",
        "Ten people, a ship that could still sail, and no explanation.",
    ]),
    dict(scene="ship_profile", chapter="The ship", text=[
        "The Mary Celeste was a two-masted merchant ship, about thirty one meters long.",
        "She was built in Nova Scotia, Canada, in 1861, under a different name: the Amazon.",
        "And from the very start, sailors said she was unlucky.",
    ]),
    dict(scene="bad_luck", text=[
        "Her first captain fell ill and died just days after taking command.",
        "Over the next years, she collided with other ships, ran aground in a storm, and passed from owner to owner.",
        "In 1868 she was repaired, sold to American owners, and soon given a new name. Mary Celeste.",
    ]),
    dict(scene="family", chapter="The voyage", text=[
        "In 1872, her new captain was Benjamin Briggs, thirty seven years old.",
        "He was an experienced sailor, known as a serious, religious and fair man.",
        "For this voyage, he brought his wife Sarah, and their two-year-old daughter, Sophia.",
        "Their seven-year-old son, Arthur, stayed at home with his grandmother.",
        "Sarah even brought her melodeon, a small organ, so she could play music during the long weeks at sea.",
    ]),
    dict(scene="crew", text=[
        "Together with seven crew members, there were ten people on board.",
        "The first mate, Albert Richardson, was a respected officer. Most of the sailors were Germans, described as quiet and reliable men.",
        "Briggs wrote to his mother that he had a good crew, and expected a pleasant journey.",
    ]),
    dict(scene="cargo", text=[
        "The cargo was one thousand seven hundred and one barrels of raw alcohol, bound for Genoa, in Italy.",
        "Remember those barrels. They matter later.",
    ]),
    dict(scene="map", args=dict(stage=0), text=[
        "On November 7th, 1872, the Mary Celeste left New York harbor and sailed east, across the Atlantic.",
        "About a week later, another ship left New York on a similar route. A Canadian ship, the Dei Gratia.",
        "Her captain, David Morehouse, is said to have known Briggs.",
    ]),
    dict(scene="logbook", text=[
        "The voyage started normally. The weather was rough, but nothing unusual for winter.",
        "On November 25th, at eight in the morning, someone made the last entry on the ship's log slate.",
        "The ship was near the island of Santa Maria, in the Azores.",
        "After that, nothing. No more entries.",
        "The log book itself would later be found on board, in the mate's cabin.",
    ]),
    dict(scene="open_sea", args=dict(found=True), chapter="The discovery", text=[
        "On December 4th, the Dei Gratia spotted the Mary Celeste, about seven hundred kilometers east of the Azores.",
        "She was moving slowly, and in an odd way, as if no one was steering.",
        "For two hours, Captain Morehouse watched her through his telescope. No one appeared on deck.",
    ]),
    dict(scene="boarding", args=dict(detail=True), text=[
        "He sent his first mate, Oliver Deveau, and two men across in a small boat.",
        "What they found would be argued about for the next century.",
    ]),
    dict(scene="evidence", text=[
        "The single lifeboat was gone.",
        "The ship's papers were missing, and so were the captain's navigation tools: the sextant, and the chronometer.",
        "There was about one meter of water in the hold. A lot, but not enough to sink her.",
        "One of the pumps had been taken apart. The compass stand on deck was knocked over, its glass broken.",
        "And some of the hatches were open.",
    ]),
    dict(scene="cabin", text=[
        "In the captain's cabin, everything was still there. Clothes, books, a sewing machine, the child's toys.",
        "The crew had left behind their boots, their pipes, and their sea chests.",
        "Whoever left this ship left in a hurry, and took almost nothing with them.",
    ]),
    dict(scene="tow", text=[
        "Deveau and two other men sailed the Mary Celeste hundreds of kilometers, all the way to Gibraltar.",
        "The Dei Gratia's crew hoped for a big reward for saving the ship and her cargo.",
    ]),
    dict(scene="court", chapter="The investigation", text=[
        "But in Gibraltar, the case got strange.",
        "The man in charge, Frederick Solly-Flood, was convinced that this was a crime.",
        "He thought the crew had gotten drunk on the alcohol, murdered the captain and his family, and escaped.",
        "Or that the crew of the Dei Gratia had done it, to claim the reward.",
    ]),
    dict(scene="sword", text=[
        "He pointed to stains on a sword found in the cabin, and to cut marks on the ship's bow.",
        "But tests showed the stains were not blood.",
        "The alcohol was undrinkable. And there were no signs of a fight anywhere on board.",
    ]),
    dict(scene="reward", text=[
        "In the end, the court gave the Dei Gratia's crew a reward, but only about a sixth of the ship's value.",
        "Many saw this as a sign that the court still did not fully trust them.",
        "The ten people of the Mary Celeste were never found.",
    ]),
    dict(scene="doyle", chapter="The legend", text=[
        "Twelve years later, a young doctor wrote a short story inspired by the case.",
        "His name was Arthur Conan Doyle. Later, he would create Sherlock Holmes.",
        "His story called the ship the Marie Celeste, and invented dramatic details, like half-eaten breakfasts and warm cups of tea.",
        "Many people believed it was true. And those myths are still repeated today.",
    ]),
    dict(scene="theories", chapter="The theories", text=[
        "So what really happened? Over the years, people have suggested almost everything.",
        "Sea monsters. Pirates. A giant waterspout. An earthquake under the sea.",
        "But pirates would have taken the cargo. And a monster leaves no explanation for the missing lifeboat.",
    ]),
    dict(scene="fraud", text=[
        "Some believed Briggs and Morehouse planned it together, as an insurance fraud.",
        "But Briggs owned part of the ship himself. He would have lost money, and he would have had to disappear forever, with his wife and child.",
    ]),
    dict(scene="barrels", text=[
        "One theory takes us back to the cargo.",
        "When the barrels were unloaded in Genoa, nine of them were empty. They were made of red oak, a wood that can leak.",
        "Alcohol vapor may have built up in the hold.",
    ]),
    dict(scene="flame", text=[
        "In 2006, a chemist at University College London, Andrea Sella, tested this with a model of the hold.",
        "He filled it with gas and lit it. The result was a sudden burst of blue flame, that passed over without burning anything.",
        "If something similar happened on the Mary Celeste, it could have terrified the crew, without leaving a single mark.",
    ]),
    dict(scene="pump", text=[
        "Another theory focuses on the pump that was taken apart.",
        "On its previous voyage, the ship had carried coal. Coal dust could have clogged the pumps.",
        "And if the chronometer was wrong, Briggs might have believed he was farther from land than he was.",
        "Seeing water rising in the hold, and land in sight, he may have ordered everyone into the lifeboat, to wait and see if the ship would sink.",
    ]),
    dict(scene="lifeboat", text=[
        "But the ship did not sink.",
        "Perhaps the rope tying the lifeboat to the ship snapped, in a sudden gust of wind.",
        "And ten people watched their ship sail away, without them, in the middle of the ocean.",
        "Nobody knows how long they survived out there.",
    ]),
    dict(scene="wreck", chapter="The end of the ship", text=[
        "As for the Mary Celeste, her bad luck never ended.",
        "In 1885, her captain deliberately ran her onto a reef near Haiti, to collect insurance money.",
        "The fraud was discovered. The ghost ship ended her life as a crime scene, once again.",
    ]),
    dict(scene="unsolved", chapter="Still unsolved", text=[
        "Today, more than one hundred and fifty years later, the mystery is still unsolved.",
        "Why did ten people leave a ship that could still float? Where did they go?",
        "Why was nothing taken, except the lifeboat, the papers, and the navigation tools?",
        "And what made an experienced captain abandon his ship, with his own wife and child?",
        "In 2001, an expedition claimed to have found her wreck near Haiti. But tests on the wood later raised doubts. Even her final resting place is uncertain.",
    ]),
    dict(scene="outro", text=[
        "So what do you think happened? Alcohol vapor? A broken pump? Or something we still have not imagined?",
        "And if you were the captain, would you have made the same choice?",
        "Tell me in the comments. And if you like unsolved mysteries, subscribe. There are many more to come.",
    ]),
]

# 9:16 cut of the same scenes; vx = horizontal centre of the vertical window in the 16:9 frame
SHORT = [
    dict(scene="open_sea", args=dict(found=True, vx=0.68), text=[
        "In 1872, sailors found a ship drifting in the middle of the Atlantic."]),
    dict(scene="cabin", args=dict(vx=0.5), text=[
        "Food for six months. Clothes. Even a child's toys.",
        "But not a single person on board."]),
    dict(scene="boarding", args=dict(detail=True, vx=0.33), text=[
        "The lifeboat was gone. The ship could still float."]),
    dict(scene="lifeboat", args=dict(vx=0.33), text=[
        "Ten people vanished. They were never found."]),
    dict(scene="open_sea", args=dict(vx=0.68), text=[
        "This is the Mary Celeste. What happened? Full story on the channel."]),
]


def thumb(S, c):
    """The empty ship drifting on a grey sea, torn sails, a lifeboat-shaped gap and a big question."""
    S.sky(c, *S.GREY_SKY)
    S.sea(c, 3.0, 640, amp=18)
    S.ship(c, 1300, 760, 1.15, 3.0, torn=0.8, rock=0.0)
    S.vignette(c)
    S.text(c, "10 PEOPLE", 80, 230, 140, S.INK, align="left")
    S.text(c, "VANISHED", 80, 380, 150, S.RED, align="left")
    S.label(c, "FOOD FOR 6 MONTHS · NOBODY ON BOARD", 600, 1010, 46, (1.0, 0.66, 0.22))


def thumb_short(S, c):
    import cairo
    import build
    c.save()
    c.scale(1920 / 1080, 1920 / 1080)
    c.translate(-1300 + 540 * 1080 / 1920, 0)
    S.sky(c, *S.GREY_SKY)
    S.clouds(c, 3.0, a=0.35)
    S.sea(c, 3.0, 640, amp=18)
    S.ship(c, 1300, 760, 1.0, 3.0, torn=0.8, rock=0.0)
    c.restore()
    v = cairo.RadialGradient(540, 960, 500, 540, 960, 1150)
    v.add_color_stop_rgba(0, 0, 0, 0, 0)
    v.add_color_stop_rgba(1, 0, 0, 0, 0.6)
    c.set_source(v)
    c.paint()
    build.punch_caption(c, "10 PEOPLE", 1080, 300, 140, 1)
    c.save()
    c.select_font_face("Inter Display Black", 0, 1)
    c.set_font_size(150)
    s = "VANISHED"
    w = c.text_extents(s).x_advance
    c.move_to(540 - w / 2, 480)
    c.text_path(s)
    c.set_source_rgb(0, 0, 0); c.set_line_width(24); c.set_line_join(1); c.stroke_preserve()
    c.set_source_rgb(0.95, 0.18, 0.2); c.fill()
    c.restore()
    S.label(c, "1872  ·  GHOST SHIP", 540, 1560, 56, (1.0, 0.66, 0.22))
