# Stickman Unsolved: The Hinterkaifeck Murders (1922). Long-form, ElevenLabs narration.
SCENES_MODULE = "farm_scenes"
XFADE = 0.6
FADE = 0.001
OVERLAY_FX = (("film_grain", 0.6),)
CHAPTER_STYLE = "typewriter"
CHAPTER_PAIR = "editorial"
CHAPTER_Y = 0.13
CAPTION_STYLE = "punch"
VERTICAL_FILL = True
EL_SETTINGS = dict(stability=0.45, similarity_boost=0.75, style=0.15, speed=0.95)

PRON = {
    "Hinterkaifeck": "Hinter-kai-feck",
    "Kaifeck": "Kai-feck",
    "Cäzilia": "Tseh-tsee-lia",
    "Schlittenbauer": "Shlitten-bower",
    "Schrobenhausen": "Shroben-how-zen",
    "Baumgartner": "Bowm-gartner",
    "Reingruber": "Rine-grooba",
    "Fürstenfeldbruck": "Feersten-feld-brook",
    "Gruber": "Grooba",
}

LONG = [
    dict(scene="farm_open", chapter=None, text=[
        "Bavaria, Germany. Spring, 1922.",
        "On a lonely farm at the edge of a forest, smoke is rising from the chimney.",
        "The cattle are being fed. Someone is eating the food in the kitchen.",
        "But the family who lives here... has been dead for days.",
    ]),
    dict(scene="tracks", text=[
        "A few days earlier, the farmer had found something strange in the fresh snow.",
        "A line of footprints, coming out of the forest, and leading straight to his house.",
        "But no footprints going back.",
    ]),
    dict(scene="title", text=[
        "This is the mystery of Hinterkaifeck. One of the strangest unsolved murder cases in history.",
        "A case that, even after a hundred years, raises more questions than answers.",
    ]),
    dict(scene="map", chapter="The farm", text=[
        "Hinterkaifeck was a small farmstead about seventy kilometers north of Munich, between the towns of Ingolstadt and Schrobenhausen.",
        "It stood on its own, a few hundred meters from the nearest hamlet, with a forest right behind it.",
    ]),
    dict(scene="layout", text=[
        "The house and the barn were built together, under one long roof.",
        "You could walk from the kitchen into the barn without ever stepping outside.",
        "Remember that. It matters later.",
    ]),
    dict(scene="family", text=[
        "In 1922, five people lived on the farm.",
        "Andreas Gruber, sixty-three, and his wife Cäzilia, seventy-two.",
        "Their widowed daughter, Viktoria, thirty-five.",
        "And Viktoria's two children. Little Cäzilia, seven, and Josef, just two years old.",
    ]),
    dict(scene="secret", chapter="A family with secrets", text=[
        "To the neighbors, the Grubers were hard-working, but cold. They kept to themselves.",
        "They were also known to be fairly well off. And there were rumors about them.",
        "In 1915, Andreas and Viktoria were convicted by a court of having an incestuous relationship, and both were sent to prison.",
    ]),
    dict(scene="secret", args=dict(war=True), text=[
        "Viktoria's husband, Karl Gabriel, had gone to fight in the First World War.",
        "In 1914, he was reported killed in France.",
        "But his body was never identified.",
    ]),
    dict(scene="neighbour", text=[
        "Then there was the neighbor, Lorenz Schlittenbauer, a widower from the hamlet.",
        "He had a relationship with Viktoria, and he wanted to marry her.",
        "When little Josef was born in 1919, Schlittenbauer first accepted that he was the father.",
        "Then he accused Andreas of being the father. Then he took it back.",
        "Andreas was against the marriage.",
    ]),
    dict(scene="maid_leaves", chapter="Strange signs", text=[
        "About six months before the murders, the family's maid quit her job.",
        "She told people the house was haunted. At night, she heard footsteps, and strange noises coming from the attic.",
        "Nobody took her seriously.",
    ]),
    dict(scene="signs", text=[
        "But in the weeks before the crime, Andreas himself began to notice things.",
        "The footprints in the snow, coming from the forest, and never leaving.",
        "A Munich newspaper on the farm that no one in the family had bought.",
        "A set of house keys that went missing.",
        "And someone had tried to break the lock of the tool shed.",
    ]),
    dict(scene="attic", text=[
        "One night, Andreas heard footsteps above him. In the attic.",
        "He climbed up with a lantern, and searched.",
        "He found nothing.",
    ]),
    dict(scene="refuse", text=[
        "He told his neighbors about all of it, and they offered to help.",
        "But Andreas refused.",
        "He said he could handle it himself.",
    ]),
    dict(scene="arrival", chapter="March 31st, 1922", text=[
        "On Friday, March 31st, 1922, a new maid arrived at the farm.",
        "Her name was Maria Baumgartner. She was forty-four years old.",
        "Her sister walked with her to Hinterkaifeck, said goodbye, and left in the afternoon.",
        "Maria would spend only a few hours there.",
    ]),
    dict(scene="barn_night", args=dict(n=4), text=[
        "What happened that night was later pieced together from the evidence.",
        "Late in the evening, one by one, four members of the family were lured into the barn.",
        "Andreas, his wife, Viktoria, and little Cäzilia.",
        "Each of them was killed there, with a farm tool called a mattock.",
    ]),
    dict(scene="house_dark", text=[
        "Then the killer went into the house.",
        "Maria, the new maid, was killed in her small room.",
        "And two-year-old Josef, in his cot in his mother's bedroom.",
        "Six people. In one night.",
    ]),
    dict(scene="days_after", chapter="The days after", text=[
        "And then comes the strangest part.",
        "The killer did not run.",
        "For the next few days, someone stayed at Hinterkaifeck.",
        "Not for an hour. Not for one night. For days.",
        "The cattle were fed. Bread and meat were eaten from the kitchen.",
        "And people passing by saw smoke rising from the chimney.",
    ]),
    dict(scene="absent", text=[
        "On Saturday, little Cäzilia did not come to school.",
        "On Sunday, the family did not come to church.",
        "The mail piled up. Nobody came to collect it.",
    ]),
    dict(scene="mechanic", text=[
        "On Monday, a mechanic named Albert Hofner came to repair the engine of a feed cutting machine.",
        "He knocked. No one answered. All he heard was the dog, barking.",
        "He worked on the machine alone for about four and a half hours, and then went home.",
        "He saw nothing. But the killer may still have been on the farm that day.",
        "And we will never know whether someone was watching him.",
    ]),
    dict(scene="discovery", text=[
        "On Tuesday, April 4th, a group of neighbors finally went to check.",
        "Among them was Lorenz Schlittenbauer.",
        "In the barn, under a pile of hay, they found four bodies. In the house, two more.",
    ]),
    dict(scene="money", chapter="The investigation", text=[
        "Police from Munich arrived the next day.",
        "The autopsies were carried out right there, on the farm.",
        "Robbery looked like the obvious motive.",
        "But a large amount of money was found in the house, untouched.",
        "Whoever did this, was not here for money.",
    ]),
    dict(scene="board", args=dict(seer=True), text=[
        "The investigation was led by Inspector Georg Reingruber.",
        "Over the following years, more than one hundred people were questioned.",
        "In a desperate attempt, the police even turned to clairvoyants in Munich, hoping they could name the killer.",
        "Nothing worked.",
    ]),
    dict(scene="suspect", chapter="The suspects", args=dict(
        name="Schlittenbauer", col=(1.0, 0.66, 0.22),
        points=["Motive: Viktoria and Josef", "Entered the house alone", "Moved the bodies", "Never charged"],
        verdict="DENIED IT"), text=[
        "The main suspect was the neighbor, Lorenz Schlittenbauer.",
        "He had a motive. The fight over Viktoria, and over little Josef.",
        "When the bodies were found, he went into the house alone, and found his way in the dark, as if he knew it well.",
        "He also moved the bodies, destroying evidence.",
        "Later, he said he was only searching for his son, little Josef.",
        "But he always denied it. He was never charged, and he even won lawsuits against people who called him a murderer.",
    ]),
    dict(scene="soldier", text=[
        "Another theory points to Viktoria's husband, Karl Gabriel.",
        "What if he never died in the war?",
        "Years later, there were rumors that German soldiers held as prisoners in Russia had met him, alive.",
        "But nothing was ever proven.",
    ]),
    dict(scene="stranger", text=[
        "Germany in 1922 was poor and chaotic. Thousands of former soldiers and drifters wandered the countryside, looking for work, or food.",
        "Others suspected thieves from the area.",
        "In the nineteen fifties, a woman claimed that her two brothers, Adolf and Anton Gump, were the killers.",
        "Anton was arrested, but released for lack of evidence.",
    ]),
    dict(scene="demolition", chapter="Lost evidence", text=[
        "In 1923, the farm was torn down.",
        "During the demolition, the murder weapon, the mattock, was found hidden in the attic.",
        "The same attic where the old maid had heard footsteps.",
        "Some believe the killer had been hiding on the farm for weeks, or even months, taking food at night.",
        "That would explain the footsteps, the missing keys, and the strange newspaper.",
        "And many key pieces of evidence were later lost, some of them during the Second World War.",
    ]),
    dict(scene="academy", text=[
        "In 2007, students at the Bavarian Police Academy in Fürstenfeldbruck re-examined the case with modern methods.",
        "They believe they identified the most likely killer.",
        "But they never published the name, out of respect for the suspect's living relatives.",
    ]),
    dict(scene="unsolved", chapter="Still unsolved", text=[
        "The case was officially closed in 1955. The last suspect was questioned in 1986.",
        "Today, more than a hundred years later, the case is still unsolved.",
        "It inspired books, documentaries, and even a German film.",
        "Who was walking in the attic? Why did the killer stay for days?",
        "Why was the money left behind? And who did it?",
    ]),
    dict(scene="memorial", text=[
        "Nothing is left of Hinterkaifeck today. Just fields, the edge of a forest, and a small memorial nearby.",
        "Six names. And a story that still has no ending.",
    ]),
    dict(scene="outro", text=[
        "So, who do you think did it? The neighbor? The husband who never came home? Or a stranger in the attic?",
        "Tell me in the comments. And if you like unsolved mysteries, subscribe. There are many more to come.",
    ]),
]
# 9:16 cut of the same scenes; vx = horizontal centre of the vertical window in the 16:9 frame
SHORT = [
    dict(scene="tracks", args=dict(vx=0.35), text=[
        "In 1922, a farmer in Germany found footprints in the snow.",
        "They came out of the forest, to his house... and never went back."]),
    dict(scene="attic", args=dict(vx=0.45), text=[
        "Then, at night, he heard footsteps. In his attic.",
        "He went up with a lantern.",
        "Nothing."]),
    dict(scene="barn_night", args=dict(n=4, vx=0.6), text=[
        "A few days later, all six people on the farm were dead."]),
    dict(scene="farm_open", args=dict(vx=0.38), text=[
        "But here's the strangest part. The killer never left."]),
    dict(scene="days_after", args=dict(vx=0.38), text=[
        "For days, someone kept feeding the cows...",
        "...eating their food, and lighting the fire."]),
    dict(scene="board", args=dict(vx=0.5), text=[
        "More than a hundred years later, no one knows who it was."]),
    dict(scene="stranger", args=dict(vx=0.6), text=[
        "Who was in the attic? The full story is on the channel."]),
]


def thumb(S, c):
    """Farm at night, one lit attic hatch, a trail of footprints from the forest, big red question."""
    c.save()
    c.translate(-150, -120)
    c.scale(1.25, 1.25)
    S.night(c, 2.0)
    S.treeline(c, 640, seed=6, scale=0.9)
    S.field(c, 700)
    S.farm(c, 900, 860, 1.0, T=2.0, attic=1.0, lights=(0, 0, 0))
    S.stick(c, 1355, 588, 0.36, col=(0.02, 0.01, 0.01))  # silhouette in the lit attic hatch
    S.snow_steps(c, [(120, 720), (420, 820), (700, 870), (950, 895)], 1.0, size=1.5, col=(0.55, 0.10, 0.12))
    c.restore()
    S.vignette(c)
    S.text(c, "SOMEONE WAS", 70, 190, 130, S.INK, align="left")
    S.text(c, "IN THE ATTIC", 70, 330, 130, S.RED, align="left")
    S.label(c, "6 DEAD · 1922 · UNSOLVED", 420, 1010, 52, S.AMBER)
