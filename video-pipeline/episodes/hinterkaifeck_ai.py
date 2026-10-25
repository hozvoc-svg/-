# Stickman Unsolved long-form, channel style: AI illustrations (made by the channel owner in Flow,
# images/hinterkaifeck/NN.png) + ElevenLabs narration + bold word-group captions.
# `python3 episodes/hinterkaifeck_ai.py` writes the Flow prompt list.
import os

SCENES_MODULE = "photo_scenes"
FADE = 0.001
XFADE = 0.5
CAPTION_STYLE = "punch"
VERTICAL_FILL = True
EL_SETTINGS = dict(stability=0.45, similarity_boost=0.75, style=0.15, speed=0.95)
PRON = {
    "Hinterkaifeck": "Hinter-kai-feck", "Kaifeck": "Kai-feck", "Cäzilia": "Tseh-tsee-lia",
    "Schlittenbauer": "Shlitten-bower", "Schrobenhausen": "Shroben-how-zen", "Baumgartner": "Bowm-gartner",
    "Reingruber": "Rine-grooba", "Fürstenfeldbruck": "Feersten-feld-brook", "Gruber": "Grooba",
}

STYLE = ("Gritty hand-drawn graphic novel illustration, heavy black ink outlines, muted desaturated colors, "
         "cinematic lighting, detailed textured background, 16:9 widescreen. ")
STICK = ("a simple stick figure with a thick glowing white outline, hollow round head, no face")

# (image no., what the picture shows, narration sentences)
SHOTS = [
    (1, f"A lonely old 1920s Bavarian farmhouse with a barn under one long roof, at the edge of a dark pine forest, snowy spring evening, thin smoke rising from the chimney, one warm window", [
        "Bavaria, Germany. Spring, 1922.",
        "On a lonely farm at the edge of a forest, smoke is rising from the chimney."]),
    (2, "Inside a dark old barn, cows eating fresh hay from a wooden trough, a lantern on a beam, nobody visible, eerie quiet", [
        "The cattle are being fed. Someone is eating the food in the kitchen.",
        "But the family who lives here... has been dead for days."]),
    (3, f"{STICK} stands in a snowy field at dusk, looking down at a line of human footprints coming out of a dark pine forest toward an old farmhouse", [
        "A few days earlier, the farmer had found something strange in the fresh snow."]),
    (4, "Low angle close-up of deep footprints in fresh snow leading to a dark wooden farmhouse door, no footprints coming back, moonlight, eerie", [
        "A line of footprints, coming out of the forest, and leading straight to his house.",
        "But no footprints going back."]),
    (5, "Title-card style wide shot: the farmhouse at night under a full moon, snow, dark forest, ominous red glow in one small attic window, empty space at the top for a title", [
        "This is the mystery of Hinterkaifeck.",
        "One of the strangest unsolved murder cases in history.",
        "A case that, even after a hundred years, raises more questions than answers."]),
    (6, "Old hand-drawn paper map of southern Bavaria with Munich, Ingolstadt and Schrobenhausen, a red ink circle marking a tiny farm in the countryside, candle light on the map", [
        "Hinterkaifeck was a small farmstead about seventy kilometers north of Munich, between the towns of Ingolstadt and Schrobenhausen.",
        "It stood on its own, a few hundred meters from the nearest hamlet, with a forest right behind it."]),
    (7, "Cutaway view of an old farmhouse where the living quarters and the barn are joined under one long roof, an inner door connecting the kitchen to the barn, warm and cold light", [
        "The house and the barn were built together, under one long roof.",
        "You could walk from the kitchen into the barn without ever stepping outside.",
        "Remember that. It matters later."]),
    (8, f"A family portrait of five stick figures, each {STICK}: an old man, an old woman, a woman, a young girl and a toddler, standing in front of an old farmhouse, sepia tones like an old photograph", [
        "In 1922, five people lived on the farm.",
        "Andreas Gruber, sixty-three, and his wife Cäzilia, seventy-two.",
        "Their widowed daughter, Viktoria, thirty-five.",
        "And Viktoria's two children. Little Cäzilia, seven, and Josef, just two years old."]),
    (9, f"Villagers as stick figures, each {STICK}, whispering to each other at a village well, glancing toward a distant farmhouse, grey sky", [
        "To the neighbors, the Grubers were hard-working, but cold. They kept to themselves.",
        "They were also known to be fairly well off. And there were rumors about them."]),
    (10, f"A 1915 courtroom, a stern judge at a high wooden bench, two stick figures, each {STICK}, standing in the dock, dramatic light through tall windows", [
        "In 1915, Andreas and Viktoria were convicted by a court of having an incestuous relationship, and both were sent to prison."]),
    (11, f"World War One trenches in France, mud and barbed wire, a stick figure soldier, {STICK}, wearing a spiked German helmet, smoke and grey sky", [
        "Viktoria's husband, Karl Gabriel, had gone to fight in the First World War.",
        "In 1914, he was reported killed in France. But his body was never identified."]),
    (12, f"A stick figure man, {STICK}, standing by a wooden fence between two farms, looking toward a woman stick figure holding a toddler, tense mood, autumn", [
        "Then there was the neighbor, Lorenz Schlittenbauer, a widower from the hamlet.",
        "He had a relationship with Viktoria, and he wanted to marry her."]),
    (13, f"An old wooden crib with a toddler stick figure, {STICK}, sleeping, two shadows of grown men falling over the crib from opposite sides", [
        "When little Josef was born in 1919, Schlittenbauer first accepted that he was the father.",
        "Then he accused Andreas of being the father. Then he took it back.",
        "Andreas was against the marriage."]),
    (14, f"A maid stick figure, {STICK}, wearing a headscarf, walking away from the farmhouse along a muddy road carrying a suitcase, looking back over her shoulder in fear", [
        "About six months before the murders, the family's maid quit her job.",
        "She told people the house was haunted."]),
    (15, f"A maid stick figure, {STICK}, lying awake in a small bed in a dark room, staring up at the wooden ceiling, dust falling from the planks", [
        "At night, she heard footsteps, and strange noises coming from the attic.",
        "Nobody took her seriously."]),
    (16, f"{STICK} with a farmer's hat, crouching in the snow next to footprints, looking at the dark forest edge, cold blue morning light", [
        "But in the weeks before the crime, Andreas himself began to notice things.",
        "The footprints in the snow, coming from the forest, and never leaving."]),
    (17, "A folded 1922 Munich newspaper lying on a rustic farmhouse kitchen table next to an oil lamp, ominous lighting", [
        "A Munich newspaper on the farm that no one in the family had bought."]),
    (18, "An empty iron key hook on a wooden wall, the dusty outline where a ring of old keys used to hang, candle light", [
        "A set of house keys that went missing."]),
    (19, "A wooden tool shed door at night with a heavy old padlock, fresh scratch marks and pry damage around the lock, moonlight", [
        "And someone had tried to break the lock of the tool shed."]),
    (20, f"{STICK} lying awake in an old wooden bed in a dark farmhouse bedroom, staring at the ceiling, a candle, deep shadows", [
        "One night, Andreas heard footsteps above him. In the attic."]),
    (21, f"{STICK} climbing a wooden ladder up through a hatch into a dark attic, holding an oil lantern, dusty rafters and hay", [
        "He climbed up with a lantern, and searched."]),
    (22, "Inside a dark farmhouse attic lit by an oil lantern on the floor, rafters, hay, old crates, in the far dark corner a barely visible black human silhouette", [
        "He found nothing."]),
    (23, f"{STICK} with a farmer's hat talking to two neighbor stick figures at a farm gate, one neighbor offering a hand, the farmer shaking his head, grey day", [
        "He told his neighbors about all of it, and they offered to help.",
        "But Andreas refused. He said he could handle it himself."]),
    (24, f"Two women stick figures, each {STICK}, walking along a country road toward a lonely farmhouse on a cold afternoon, one carrying a small suitcase", [
        "On Friday, March 31st, 1922, a new maid arrived at the farm.",
        "Her name was Maria Baumgartner. She was forty-four years old."]),
    (25, f"A woman stick figure, {STICK}, waving goodbye and walking away down the road, the other stays at the farmhouse door, sunset turning to dusk", [
        "Her sister walked with her to Hinterkaifeck, said goodbye, and left in the afternoon.",
        "Maria would spend only a few hours there."]),
    (26, "The farmhouse at night, the big barn door slightly open with orange light spilling onto the snow, dark forest, full moon, ominous, no people", [
        "What happened that night was later pieced together from the evidence.",
        "Late in the evening, one by one, four members of the family were lured into the barn."]),
    (27, "Inside the dark barn at night, a lantern swinging on a hook, long shadows, a pile of hay, an old mattock leaning against a wooden post, no people, no blood", [
        "Andreas, his wife, Viktoria, and little Cäzilia.",
        "Each of them was killed there, with a farm tool called a mattock."]),
    (28, "A dark farmhouse corridor at night, a door to a small bedroom slightly open, faint moonlight, a long shadow of a figure on the wall, no gore", [
        "Then the killer went into the house.",
        "Maria, the new maid, was killed in her small room.",
        "And two-year-old Josef, in his cot in his mother's bedroom."]),
    (29, "The farmhouse windows going dark one by one at night, snow, deep blue tones, very still and silent", [
        "Six people. In one night."]),
    (30, "The same farmhouse on a grey snowy morning, smoke rising from the chimney, crows on the fence, unsettling calm", [
        "And then comes the strangest part. The killer did not run.",
        "For the next few days, someone stayed at Hinterkaifeck.",
        "Not for an hour. Not for one night. For days."]),
    (31, "A rustic farmhouse kitchen table with a half-eaten loaf of bread, a knife, a plate of meat and a burning candle, one chair pulled out, empty room", [
        "The cattle were fed. Bread and meat were eaten from the kitchen.",
        "And people passing by saw smoke rising from the chimney."]),
    (32, f"A 1920s village school classroom, rows of wooden desks with child stick figures, each {STICK}, one empty desk in the middle, chalkboard", [
        "On Saturday, little Cäzilia did not come to school.",
        "On Sunday, the family did not come to church."]),
    (33, f"A mailman stick figure, {STICK}, with a 1920s postal cap, putting letters into an overflowing mailbox at the farm gate", [
        "The mail piled up. Nobody came to collect it."]),
    (34, f"A mechanic stick figure, {STICK}, with a flat cap, repairing an old engine of a feed cutting machine next to a farmhouse wall, toolbox, grey daylight", [
        "On Monday, a mechanic named Albert Hofner came to repair the engine of a feed cutting machine.",
        "He knocked. No one answered. All he heard was the dog, barking."]),
    (35, "The farmhouse seen from below, a small dark attic window, two faint eyes barely visible in the darkness behind the glass, grey daylight", [
        "He worked on the machine alone for about four and a half hours, and then went home.",
        "He saw nothing. But the killer may still have been on the farm that day.",
        "And we will never know whether someone was watching him."]),
    (36, f"Three stick figure men, each {STICK}, walking through the snow toward the farmhouse barn door, determined, cold morning", [
        "On Tuesday, April 4th, a group of neighbors finally went to check.",
        "Among them was Lorenz Schlittenbauer."]),
    (37, f"A stick figure man, {STICK}, frozen in shock in the open barn doorway, looking at a pile of hay inside, light from behind, no bodies or gore shown", [
        "In the barn, under a pile of hay, they found four bodies. In the house, two more."]),
    (38, f"1920s police officers as stick figures, each {STICK}, in uniforms and peaked caps, arriving at the farm in a vintage car, snow", [
        "Police from Munich arrived the next day.",
        "The autopsies were carried out right there, on the farm.",
        "Robbery looked like the obvious motive."]),
    (39, "An open wooden chest in a farmhouse bedroom full of old German banknotes and coins, lit by a lamp, untouched", [
        "But a large amount of money was found in the house, untouched.",
        "Whoever did this, was not here for money."]),
    (40, f"A 1920s detective stick figure, {STICK}, wearing a hat and coat, in front of a cork board with old photos, maps and notes connected with red string, desk lamp", [
        "The investigation was led by Inspector Georg Reingruber.",
        "Over the following years, more than one hundred people were questioned."]),
    (41, "A 1920s fortune teller's table with a glowing crystal ball, tarot cards and candles, purple and gold light, mysterious", [
        "In a desperate attempt, the police even turned to clairvoyants in Munich, hoping they could name the killer.",
        "Nothing worked."]),
    (42, f"Police lineup style: a stick figure man, {STICK}, standing in front of a height chart wall, harsh spotlight, a case number board", [
        "The main suspect was the neighbor, Lorenz Schlittenbauer.",
        "He had a motive. The fight over Viktoria, and over little Josef."]),
    (43, f"A stick figure man, {STICK}, walking confidently alone through a pitch-dark farmhouse hallway without a light, other figures hesitating at the door behind him", [
        "When the bodies were found, he went into the house alone, and found his way in the dark, as if he knew it well.",
        "He also moved the bodies, destroying evidence.",
        "Later, he said he was only searching for his son, little Josef."]),
    (44, f"A 1920s courtroom, a stick figure man, {STICK}, pointing at another man, a judge's gavel coming down, he is winning the case", [
        "But he always denied it. He was never charged.",
        "He even won lawsuits against people who called him a murderer."]),
    (45, f"A ghostly stick figure soldier, {STICK}, in a worn WWI uniform, standing at the edge of the dark forest looking at the farmhouse, fog", [
        "Another theory points to Viktoria's husband, Karl Gabriel. What if he never died in the war?",
        "Years later, there were rumors that German soldiers held as prisoners in Russia had met him, alive.",
        "But nothing was ever proven."]),
    (46, f"Two shady stick figure men, {STICK}, in flat caps, hiding behind a tree at night watching a farmhouse", [
        "Germany in 1922 was poor and chaotic. Thousands of former soldiers and drifters wandered the countryside, looking for work, or food.",
        "Others suspected thieves from the area.",
        "In the nineteen fifties, a woman claimed that her two brothers, Adolf and Anton Gump, were the killers.",
        "Anton was arrested, but released for lack of evidence."]),
    (47, f"Workers as stick figures, each {STICK}, tearing down the old farmhouse with crowbars, beams falling, dust, grey sky", [
        "In 1923, the farm was torn down.",
        "During the demolition, the murder weapon, the mattock, was found hidden in the attic."]),
    (48, "Close-up of an old rusty mattock lying among dusty attic floorboards and hay, a beam of light falling on it", [
        "The same attic where the old maid had heard footsteps.",
        "Some believe the killer had been hiding on the farm for weeks, or even months, taking food at night.",
        "That would explain the footsteps, the missing keys, and the strange newspaper.",
        "And many key pieces of evidence were later lost, some of them during the Second World War."]),
    (49, f"A modern classroom of a police academy, stick figure students, each {STICK}, studying old case files and photographs, one file with a name covered by a black bar", [
        "In 2007, students at the Bavarian Police Academy in Fürstenfeldbruck re-examined the case with modern methods.",
        "They believe they identified the most likely killer.",
        "But they never published the name, out of respect for the suspect's living relatives."]),
    (50, "An old case file folder stamped UNSOLVED in red, lying on a dark desk with old photographs of a farmhouse, dust, single lamp", [
        "The case was officially closed in 1955. The last suspect was questioned in 1986.",
        "Today, more than a hundred years later, the case is still unsolved.",
        "It inspired books, documentaries, and even a German film.",
        "Who was walking in the attic? Why did the killer stay for days?",
        "Why was the money left behind? And who did it?"]),
    (51, "An empty snowy field at the edge of a pine forest at dawn, a small wooden memorial cross, pink and grey sky, quiet and sad", [
        "Nothing is left of Hinterkaifeck today. Just fields, the edge of a forest, and a small memorial nearby.",
        "Six names. And a story that still has no ending."]),
    (52, "The farmhouse at night seen from the snowy field, the small attic window glowing orange with a dark human silhouette standing in it, full moon, snow falling", [
        "So, who do you think did it? The neighbor? The husband who never came home? Or a stranger in the attic?",
        "Tell me in the comments. And if you like unsolved mysteries, subscribe."]),
]

_IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "hinterkaifeck")
_MOVES = [((1.00, .5, .5), (1.14, .5, .46)), ((1.12, .42, .5), (1.12, .58, .5)),
          ((1.16, .5, .45), (1.02, .5, .5)), ((1.12, .58, .5), (1.12, .42, .52))]


def _img(n):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(_IMG, f"{n:02d}.{ext}")
        if os.path.exists(p):
            return p
    return os.path.join(_IMG, f"{n:02d}.png")


LONG = [dict(scene="photo", args=dict(img=_img(n), cam=_MOVES[n % 4]), text=txt) for n, _, txt in SHOTS]
# Short cut from the same pictures: (image no., horizontal centre of the 9:16 window, narration)
SHORT_SHOTS = [
    (3, 0.5, ["In 1922, a farmer in Germany found footprints in the snow."]),
    (4, 0.5, ["They came out of the forest, to his house... and never went back."]),
    (20, 0.5, ["Then, at night, he heard footsteps. In his attic."]),
    (21, 0.5, ["He went up with a lantern."]),
    (22, 0.5, ["Nothing."]),
    (26, 0.5, ["A few days later, all six people on the farm were dead."]),
    (30, 0.5, ["But here's the strangest part. The killer never left."]),
    (2, 0.5, ["For days, someone kept feeding the cows..."]),
    (31, 0.5, ["...eating their food, and lighting the fire."]),
    (50, 0.5, ["More than a hundred years later, no one knows who it was."]),
    (52, 0.5, ["Who was in the attic? The full story is on the channel."]),
]
SHORT = [dict(scene="photo", args=dict(img=_img(n), cam=_MOVES[n % 4], vx=vx), text=txt) for n, vx, txt in SHORT_SHOTS]


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", "hinterkaifeck_long_PROMPTS.md")
    words = sum(len(" ".join(t).split()) for _, _, t in SHOTS)
    with open(out, "w") as fh:
        fh.write("# Hinterkaifeck (лонг): промпти для Flow\n\n")
        fh.write(f"**{len(SHOTS)} картинок, 16:9.** Озвучка ≈ {words} слів (~{words / 150:.1f} хв).\n")
        fh.write("Назви файли за номерами (01.png, 02.png …) або просто надсилай по порядку.\n")
        fh.write("Стиль уже всередині кожного промпту — копіюй повністю.\n\n")
        for n, desc, txt in SHOTS:
            fh.write(f"**{n:02d}** — _{txt[0]}_\n```\n{STYLE}{desc[0].upper() + desc[1:]}.\n```\n\n")
    print(out, words)
