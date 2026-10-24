# Sleepy Cosmos, episode 3: "Fall Asleep Learning the Life of Stars" (narrated, ElevenLabs).
from episodes.solar_journey import EL_VOICE, EL_SETTINGS, _with_pauses

SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 6.0
PRON = {"Betelgeuse": "Beetle-juice", "Jocelyn Bell Burnell": "Jocelyn Bell Bur-nell", "Proxima": "Proxima"}


def seg(scene, text, chapter=None, **args):
    return dict(scene=scene, text=[text], chapter=chapter, args=args)


LONG = [
    seg("title", "Hello, and welcome back to Sleepy Cosmos. Tonight, we're going to follow the life of the stars. "
        "How they're born in great, glowing clouds. How they shine, quietly, for millions and billions of years. "
        "And how, one day, they fade, or burst, or fold into the deepest darkness in the universe. "
        "So get comfortable, and let your body relax. Breathe in slowly... and out. Let's drift among the stars.",
        chapter="Welcome", subtitle="The Life of Stars"),
    # --- birth
    seg("nursery", "Every star begins inside a cloud. A vast, cold, dark cloud of gas and dust, drifting between the stars. "
        "Some of these clouds are so large that light would take hundreds of years to cross them. "
        "They're made mostly of hydrogen, the simplest element in the universe, mixed with fine grains of dust, like soot or sand.",
        chapter="Where Stars Are Born", seed=11),
    seg("nursery", "For a long time, the cloud just floats, calm and still. Then, something disturbs it. "
        "Perhaps a nearby star explodes, or the cloud drifts through a crowded part of the galaxy. "
        "Here and there, the gas begins to gather into denser knots. And once a knot is dense enough, gravity takes over. "
        "Slowly, it starts to pull itself together, tighter and tighter.", seed=11),
    seg("nursery", "As it collapses, the center of the knot grows hotter and hotter. "
        "After many thousands of years, the core reaches around ten million degrees. "
        "And then, something wonderful happens. Hydrogen atoms begin to fuse together, making helium, and releasing light. "
        "A new star switches on. Its light pushes away the remaining dust around it, and it begins to shine into the dark.", seed=12),
    seg("nursery", "On a clear winter night, you can see a place like this with your own eyes. "
        "Below the three bright stars of Orion's belt, there's a small, fuzzy patch of light. That's the Orion Nebula, "
        "about thirteen hundred light years away. Inside it, thousands of young stars are being born, right now. "
        "Some of them may already be gathering planets of their own.", seed=12),
    seg("nursery", "In another cloud, called the Eagle Nebula, there are tall, dark columns of gas and dust that astronomers call "
        "the Pillars of Creation. Each one is several light years tall. Inside them, new stars are slowly taking shape, "
        "hidden from view, wrapped in dust, like seeds sleeping in the soil, waiting for spring.", seed=13),
    # --- red dwarfs
    seg("star", "Stars come in many sizes, and their size decides almost everything about their lives. "
        "The smallest true stars are red dwarfs. They're cool, dim, and gentle, glowing a deep orange red. "
        "Red dwarfs are by far the most common stars in our galaxy. About three out of every four stars are red dwarfs. "
        "And yet, not a single one of them is bright enough to see from Earth with your eyes alone.",
        chapter="Red Dwarfs", body="star_red", size=150),
    seg("star", "The nearest star to the Sun is a red dwarf called Proxima Centauri, a little over four light years away. "
        "Red dwarfs burn their fuel so slowly and so carefully that they can shine for trillions of years. "
        "That's far longer than the universe has existed so far. "
        "Not one red dwarf has ever burned out. Every single one ever born is still glowing, quietly, somewhere in the dark.",
        body="star_red", size=180, x=0.55),
    # --- Sun-like
    seg("star", "Then there are stars like our Sun. Yellow, steady, and middle sized. "
        "A star like the Sun can shine for about ten billion years, fusing hydrogen into helium deep in its core. "
        "Our Sun is roughly halfway through that life. It's in the calm middle years, "
        "shining steadily, giving light and warmth to the planets that circle it.",
        chapter="Stars Like the Sun", body="sun", size=260),
    seg("star", "Inside a star like the Sun, there is a quiet balance. Gravity is always trying to squeeze the star smaller. "
        "And the heat from fusion in the core is always pushing outward. "
        "For billions of years, these two forces hold each other perfectly still, like two friends leaning against each other, back to back. "
        "That balance is what keeps the Sun shining so evenly, day after day, for all of human history.",
        body="sun", size=290, x=0.55),
    # --- blue giants
    seg("star", "At the other end are the giants. Huge, heavy stars, many times the mass of the Sun. "
        "They burn incredibly hot, so hot that they glow blue white, and they shine thousands, or even hundreds of thousands of times brighter than the Sun. "
        "In the constellation of Orion, the bright star Rigel is one of these brilliant blue giants.",
        chapter="Blue Giants", body="star_blue", size=300),
    seg("star", "But burning so brightly comes at a cost. Giant stars use up their fuel very quickly. "
        "Instead of living for billions of years, they may live for only a few million. "
        "On the scale of the universe, that's just a brief, brilliant moment. "
        "Like a firework, compared to a candle.", body="star_blue", size=330, x=0.55),
    # --- red giants
    seg("star", "What happens when a star like the Sun begins to run low on hydrogen in its core? "
        "In about five billion years, our Sun will find out. Its core will shrink and heat up, and its outer layers will swell, "
        "growing hundreds of times larger. It will become a red giant, glowing a soft, deep orange.",
        chapter="Red Giants", body="star_orange", size=480),
    seg("star", "As a red giant, the Sun may grow so large that it reaches out past the orbits of Mercury and Venus, "
        "and perhaps all the way to the Earth's orbit. "
        "But that is an unimaginably long time from now, far longer than the whole story of life on Earth so far. "
        "For billions of years to come, the Sun will go on shining just as it does today.", body="star_orange", size=560, x=0.55),
    seg("star", "Some red giants are already shining in our sky. In Orion's shoulder, there's a reddish star called Betelgeuse. "
        "It's a red supergiant, so large that if it took the place of our Sun, it would stretch out beyond the orbit of Mars. "
        "A few years ago, Betelgeuse grew noticeably dimmer, and people wondered if it was about to explode. "
        "It turned out to be a great cloud of dust it had breathed out, drifting across its face. It's shining as usual again.",
        body="star_orange", size=620, x=0.6),
    # --- planetary nebula & white dwarf
    seg("shell", "At the very end of its life, a star like the Sun gently lets go of its outer layers. "
        "They drift away into space, forming a glowing shell of gas, lit up from within. "
        "Astronomers call these planetary nebulae, although they have nothing to do with planets. "
        "Through a small telescope, they looked round, like planets, and the name simply stayed.",
        chapter="A Gentle Ending", kind="ring"),
    seg("shell", "One of the most famous is the Ring Nebula, a soft, colorful halo in the constellation of Lyra. "
        "Its colors come from different gases glowing in the light of the dying star. "
        "These shells slowly spread out and fade over tens of thousands of years, "
        "returning their gas to the galaxy, where one day it may help to form new stars and planets.", kind="ring"),
    seg("star", "At the center, what's left behind is a white dwarf. The bare, glowing core of the old star. "
        "It's about the size of the Earth, but so dense that a single teaspoon of it would weigh several tonnes. "
        "A white dwarf no longer makes any new energy. It simply shines with the heat it has left, "
        "cooling very, very slowly, over billions and billions of years.", body="star_white", size=55),
    seg("star", "Eventually, a white dwarf will cool all the way down, and fade into a cold, dark ember. A black dwarf. "
        "But that takes so long that the universe isn't old enough for even one black dwarf to exist yet. "
        "Every white dwarf that has ever formed is still glowing, softly, like the last warm coals of a fire, long after everyone has gone to bed.",
        body="star_white", size=70, x=0.55),
    # --- supernova
    seg("shell", "The giant stars end their lives very differently. When a massive star runs out of fuel, "
        "its core suddenly collapses, in less than a second. And the star explodes. A supernova. "
        "For a few weeks, a single exploding star can shine brighter than an entire galaxy of billions of stars.",
        chapter="Supernovae", kind="nova"),
    seg("shell", "In the year ten fifty four, astronomers in China noticed a new star appear in the sky. "
        "It was so bright that it could be seen in daylight for weeks. "
        "Today, when we point our telescopes at that same spot, we see the Crab Nebula, "
        "the glowing, tangled remains of that explosion, still spreading outward, nearly a thousand years later.", kind="nova"),
    seg("shell", "Supernovae are not only endings. They're also beginnings. "
        "Inside stars, and in their explosions, the elements that make up our world were created. "
        "The calcium in your bones. The iron in your blood. The oxygen you're breathing right now. "
        "All of it was made inside stars, long before the Sun was born. In a very real way, you are made of stardust.", kind="nova"),
    # --- neutron stars
    seg("pulsar", "Sometimes, after a supernova, the core that's left behind is crushed into something extraordinary. A neutron star. "
        "It holds more mass than the Sun, squeezed into a ball only about twenty kilometers across, the size of a city. "
        "A single teaspoon of a neutron star would weigh about as much as a mountain.", chapter="Neutron Stars"),
    seg("pulsar", "Many neutron stars spin incredibly fast, some of them hundreds of times every second. "
        "As they spin, they send out beams of radio waves, sweeping across space like the light of a lighthouse. "
        "When those beams sweep past the Earth, we see them as regular, steady pulses. We call these stars pulsars.", zoom=1.2),
    seg("pulsar", "The first pulsar was discovered in nineteen sixty seven by a young astronomer named Jocelyn Bell Burnell. "
        "She noticed a strange, perfectly regular signal in her data, ticking like a clock. "
        "At first, it was so regular that it was jokingly nicknamed Little Green Men. "
        "But it turned out to be something just as wonderful. A dead star, still spinning, still keeping time.", zoom=1.3),
    # --- black holes
    seg("blackhole", "And the very largest stars may collapse even further, into a black hole. "
        "A place where gravity is so strong that nothing, not even light, can escape. "
        "Around a black hole is a boundary called the event horizon. Anything that crosses it can never come back out.",
        chapter="Black Holes"),
    seg("blackhole", "We can't see a black hole itself, because it gives off no light. "
        "But we can see what's around it. Gas and dust swirling in toward it form a flat, glowing disk, "
        "heated to millions of degrees as it spins. And the black hole's gravity bends the light from behind it, "
        "wrapping it around in glowing rings.", zoom=1.15),
    seg("blackhole", "In two thousand and nineteen, astronomers shared the first ever picture of a black hole, "
        "in the center of a giant galaxy called M eighty seven. A dark shadow, surrounded by a ring of orange light. "
        "And in two thousand and twenty two, they shared a picture of the black hole at the center of our own galaxy, the Milky Way. "
        "It's called Sagittarius A star, and it's about four million times heavier than the Sun.", zoom=1.3),
    seg("blackhole", "It's very far away from us, about twenty six thousand light years, so there's nothing to worry about. "
        "It sits quietly at the heart of our galaxy, while hundreds of billions of stars, including our Sun, "
        "circle around it, slowly, over hundreds of millions of years. Like a great, dark, still center, around which everything turns.",
        zoom=1.4),
    # --- the cycle
    seg("nursery", "And so the story of the stars comes back to where it began. "
        "The gas that dying stars send out into space drifts through the galaxy, mixing with the clouds. "
        "Over time, those clouds gather, and collapse, and new stars are born, richer in the elements made by the stars before them. "
        "Our own Sun, and the Earth, and you, are part of that long, quiet cycle.", chapter="The Cycle of Stars", seed=14),
    seg("galaxy", "Right now, all across our galaxy, stars are being born, and stars are quietly fading. "
        "Some are just beginning to glow. Some are in the long, calm middle of their lives, like our Sun. "
        "And some are gently letting go, returning what they've made to the stars of tomorrow. "
        "There is no hurry in any of it. Just a slow, patient rhythm, like breathing.", seed=3),
    seg("travel", "So let yourself breathe slowly now, in that same rhythm. In... and out. "
        "Let your body be heavy and warm, like a star resting in its long, quiet middle years. "
        "Above you, beyond the ceiling and the clouds, the stars are shining, as they always have. "
        "They'll still be shining when you wake. Rest now.", neb=5, slow=True),
    seg("outro", "Thank you for spending this quiet time with me. If you enjoyed it, you can subscribe to Sleepy Cosmos "
        "for a new calm journey through space every week. Sleep well, and sweet dreams.", subtitle="Goodnight"),
]

LONG = _with_pauses(LONG)
SHORT = []


def thumb(S, c):
    import space_art as A
    c.set_source_rgb(*S.BG1)
    c.paint()
    S.sc_nursery(c, 10.0, 40.0, 100.0, dict(seed=11))
    A.glow(c, 1450, 560, 700, (1.0, 0.45, 0.2), 0.3)
    S.paint_sphere(c, "star_orange", 1450, 560, 330, 0.2, emissive=True)
    A.glow(c, 1080, 860, 120, (0.6, 0.75, 1.0), 0.6)
    S.paint_sphere(c, "star_blue", 1080, 860, 60, 0.1, emissive=True)
    A.crescent(c, 170, 170, 60)
    A.text(c, "Fall Asleep", 470, 420, 115, (1, 1, 1))
    A.text(c, "Learning the", 470, 540, 86, (1, 1, 1))
    A.text(c, "Life of Stars", 470, 670, 120, (1, 0.88, 0.62))
    c.set_source_rgba(0.08, 0.06, 0.2, 0.85)
    c.new_path()
    c.arc(320, 800, 50, 1.5708, 4.7124)
    c.arc(620, 800, 50, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    A.text(c, "SLEEP STORY", 470, 818, 44, (1, 1, 1), family="Inter", spacing=2)
