# Sleepy Cosmos, episode 1: "A Calm Journey Through the Solar System" (~1 hour, narrated with ElevenLabs).
# Each segment is one paragraph sent to the voice in a single request, so the delivery flows naturally.

SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 5.5
EL_VOICE = "JBFqnCBsd6RMkjVDRZzb"  # George: warm, calm British narrator
EL_SETTINGS = dict(stability=0.65, similarity_boost=0.75, style=0.0, use_speaker_boost=True, speed=0.88)
PRON = {"Io": "Eye-oh", "Charon": "Karon", "Arrokoth": "Arrow-koth", "Le Verrier": "Le Ver-yay"}


def seg(scene, text, chapter=None, **args):
    return dict(scene=scene, text=[text], chapter=chapter, args=args)


LONG = [
    seg("title", "Hello, and welcome to Sleepy Cosmos. Tonight, we're going on a long, slow journey through our Solar System, "
        "from the warm light of the Sun, all the way out to the quiet, frozen edge, where the Sun is just one more star. "
        "There's nothing you need to do, and nowhere you need to be. So get comfortable, let your body grow heavy, "
        "and take a slow breath in... and let it out. If you drift off before we reach the end, that's perfectly fine. "
        "The universe will still be here tomorrow.", chapter="Welcome"),
    seg("travel", "Imagine you're floating in a small, quiet ship, far above the Earth. The engines are silent. "
        "Outside the window, the stars don't twinkle the way they do at home. Out here, without air to blur them, "
        "they shine as steady, tiny points of light, in every direction, more of them than you could ever count. "
        "Our ship turns gently, slowly, toward the brightest light of all. And we begin to drift.", neb=1),
    seg("travel", "As we float, notice how quiet it is. There is no wind out here, no traffic, no voices. "
    "Sound needs air to travel, and between the planets there is almost none. "
    "The only sounds are the soft hum of our little ship, and your own slow breathing. "
    "Let that quiet settle over you, like a warm blanket. We have all the time in the world.", neb=2, slow=True),
    # --- the Sun
    seg("sun", "At the center of everything is the Sun. It's an ordinary star, really, one of hundreds of billions in our galaxy. "
        "But to us, it is everything. It is so large that about one point three million Earths could fit inside it. "
        "It holds more than ninety nine point eight percent of all the mass in the Solar System. "
        "Every planet, every moon, every grain of dust, together, is just a tiny remainder.", chapter="The Sun"),
    seg("sun", "The surface of the Sun is about five and a half thousand degrees Celsius. "
        "Deep in its core, it reaches around fifteen million degrees. There, under unimaginable pressure, "
        "hydrogen is slowly fused into helium. Every second, the Sun turns hundreds of millions of tonnes of hydrogen into light and heat. "
        "It has been doing this, quietly and steadily, for about four and a half billion years. "
        "And it will keep shining for billions of years more.", zoom=1.15),
    seg("sun", "The light leaving the Sun right now will take about eight minutes to reach the Earth. "
        "So when you step outside on a sunny afternoon, the sunlight touching your face left the Sun eight minutes earlier. "
        "But the journey inside the Sun is much slower. The energy made in the core bounces around for thousands of years, "
        "maybe even much longer, before it finally reaches the surface and escapes into space. "
        "The warmth you feel on a summer day began its journey before the first cities were built.", zoom=1.3),
    seg("sun", "Every so often, the Sun's surface becomes restless. Great loops of glowing gas rise up from it, "
    "arching thousands of kilometers into space, held in place by invisible magnetic fields. "
    "Sometimes, the Sun releases clouds of charged particles that travel all the way to the Earth. "
    "When they reach our sky near the poles, they make the air glow green and pink and violet. "
    "The northern and southern lights. A quiet gift, sent from the Sun, across a hundred and fifty million kilometers.", zoom=1.4),
    # --- Mercury
    seg("planet", "Let's drift away from the Sun now, toward the first planet. Mercury. "
        "It's the smallest planet in the Solar System, only a little larger than our Moon. "
        "Its grey surface is covered in craters, layer upon layer of them, from billions of years of quiet impacts. "
        "Mercury has almost no atmosphere at all, nothing to soften the light, nothing to hold in the warmth.",
        chapter="Mercury", body="mercury", size=330),
    seg("planet", "Mercury races around the Sun faster than any other planet. Its year lasts only eighty eight Earth days. "
        "But it turns on its axis very slowly. From sunrise to sunrise, a single day on Mercury lasts about one hundred and seventy six Earth days. "
        "So on Mercury, a day is longer than a year.", body="mercury", size=360, x=0.45),
    seg("planet", "In the daytime, the surface reaches more than four hundred degrees Celsius, hot enough to melt lead. "
        "But at night, with no atmosphere to hold the heat, it falls to around minus one hundred and eighty degrees. "
        "And strangely, in the deep craters near its poles, where sunlight never reaches, there is ice. "
        "Frozen water, hiding in permanent shadow, on the planet closest to the Sun.", body="mercury", size=390, x=0.6, night=0.4),
    seg("planet", "If you could stand on Mercury, the Sun would look about three times larger than it does from Earth, "
    "and far, far brighter. The sky would be black, even in the middle of the day, because there's no air to scatter the light. "
    "And because of Mercury's strange orbit, in some places the Sun would rise, pause, go backwards a little, "
    "and then continue across the sky again. A slow, hesitant sunrise, on a small and silent world.", body="mercury", size=300, x=0.5),
    # --- Venus
    seg("planet", "Our next stop is Venus. In the night sky on Earth, Venus is often the brightest thing after the Moon. "
        "People call it the morning star, or the evening star. From far away, it looks peaceful, wrapped in soft, pale yellow clouds. "
        "Venus is almost the same size as the Earth. For a long time, people imagined it might be a twin of our world, "
        "perhaps covered in warm oceans and tropical forests.", chapter="Venus", body="venus", size=380),
    seg("planet", "But underneath those clouds, Venus is the hottest planet in the Solar System, even hotter than Mercury. "
        "Its thick atmosphere of carbon dioxide traps the heat, and the surface stays at around four hundred and sixty five degrees, "
        "day and night. The air pressure on the ground is about ninety times stronger than on Earth. "
        "Standing there would feel like being nearly a kilometer deep in the ocean.", body="venus", size=400, x=0.45),
    seg("planet", "Venus also spins in the opposite direction to most planets, and incredibly slowly. "
        "One full turn takes two hundred and forty three Earth days, longer than its entire year around the Sun. "
        "If you could stand on Venus and see through the clouds, the Sun would rise in the west, and set in the east. "
        "But no one will stand there for a very long time. We'll simply watch it, glowing softly, and drift on.", body="venus", size=420, x=0.6),
    seg("planet", "Spacecraft have landed on Venus. Soviet probes called Venera reached the surface in the nineteen seventies and eighties. "
    "They sent back photographs of flat, cracked rocks under a dim, orange sky, before the heat and pressure overwhelmed them. "
    "The longest any of them survived was about two hours. "
    "Those few pictures are still the only views we have ever seen from the ground of another world so hostile.", body="venus", size=360, x=0.5),
    # --- Earth
    seg("earth", "And now, a world you know. Home. The Earth, about one hundred and fifty million kilometers from the Sun. "
        "Not too hot, and not too cold. Just right for liquid water to fill its oceans. "
        "From out here, it's mostly blue, with swirling white clouds and patches of green and brown. "
        "About seventy one percent of its surface is covered by water.", chapter="Earth and the Moon"),
    seg("earth", "Somewhere down there, right now, it is night, and people are sleeping. "
        "Somewhere else, the sun is rising, and someone is making their first cup of tea. "
        "Rain is falling on a forest. Waves are rolling onto a quiet beach. "
        "All of it, every story you have ever heard, has happened on that one small, blue world.", zoom=1.2),
    seg("earth", "Beside the Earth, our faithful companion, the Moon, travels around us about once a month. "
        "It's about three hundred and eighty four thousand kilometers away. "
        "It always shows us the same face, because it turns exactly once for every trip around the Earth. "
        "And every year, the Moon drifts about four centimeters farther away from us. Very slowly. Almost too slowly to notice. "
        "Like a friend taking one small step back, to see us a little better.", zoom=1.35, moon_focus=True),
    seg("earth", "The Moon does something gentle for us every day. Its gravity pulls on the oceans, "
    "lifting them into a slow bulge that sweeps around the planet. That's what makes the tides. "
    "Twice a day, the sea rises up a beach, and twice a day it slips away again. "
    "So every wave that ever reached your feet on the shore was guided, a little, by the Moon.", zoom=1.25, moon_focus=True),
    # --- Mars
    seg("planet", "We leave the Earth behind now, and drift outward, toward a small, rusty red world. Mars. "
        "Its color comes from iron in its rocks and dust, the same thing that gives rust its color. "
        "Mars is about half the size of the Earth. A day there is just a little longer than ours, "
        "about twenty four hours and thirty seven minutes. But its year lasts six hundred and eighty seven Earth days.",
        chapter="Mars", body="mars", size=360),
    seg("planet", "Mars is home to the tallest volcano in the Solar System. Olympus Mons. "
        "It rises about twenty two kilometers above the surrounding plains, around two and a half times the height of Mount Everest. "
        "It's so wide that if you stood on its slopes, it would stretch beyond the horizon in every direction. "
        "And not far away lies an enormous canyon, Valles Marineris, about four thousand kilometers long. "
        "On Earth, it would stretch across an entire continent.", body="mars", size=390, x=0.45),
    seg("planet", "Long ago, Mars was a very different world. Rivers once flowed across it, and lakes filled its craters. "
        "Today, the water is frozen in its polar caps and hidden under the ground. "
        "And there's something quietly beautiful about Mars. During the day, its sky is a dusty, butterscotch color. "
        "But at sunset, the sky around the Sun turns blue. A cool, soft, blue sunset, on a red planet.", body="mars", size=420, x=0.6),
    seg("planet", "Mars has two tiny moons, Phobos and Deimos. They aren't round like our Moon. "
        "They're small and lumpy, more like potatoes floating in space. "
        "Some scientists think they might be captured asteroids, or pieces thrown into space by an ancient impact. "
        "They circle quietly above the red deserts, as they have for millions of years.", body="mars", size=300, x=0.4, moons=2),
    seg("planet", "Right now, robots are exploring Mars for us. Rovers roll slowly across its red plains, "
    "studying rocks, taking pictures, and searching for signs that life might once have existed there. "
    "They move very carefully, sometimes only a few dozen meters in a whole day. "
    "Patient, lonely explorers, under a butterscotch sky, waiting for their next message from home.", body="mars", size=350, x=0.5),
    # --- asteroid belt
    seg("belt", "Beyond Mars, we pass through the asteroid belt. In films, asteroid fields are crowded and dangerous, "
        "full of tumbling rocks. But the real asteroid belt is mostly empty space. "
        "The asteroids are so far apart that, on average, they're separated by hundreds of thousands of kilometers. "
        "If you stood on one, you would probably not even see another with your own eyes.", chapter="The Asteroid Belt"),
    seg("belt", "There are millions of asteroids here, from small pebbles to rocky worlds hundreds of kilometers wide. "
        "And yet, if you gathered all of them together, they would weigh only a few percent of our Moon. "
        "The largest object here is Ceres, a small round dwarf planet, about nine hundred and forty kilometers across. "
        "Bright patches on its surface turned out to be salt, left behind by water that seeped up from below.", ceres=True),
    seg("belt", "As we glide through the belt, the asteroids drift past us slowly, tumbling end over end. "
    "Some are dark as coal. Some are made of metal, iron and nickel, shining faintly in the distant sunlight. "
    "They're leftovers, pieces that never came together to form a planet, "
    "because the strong pull of nearby Jupiter kept stirring them up. Fragments of a world that never was."),
    # --- Jupiter
    seg("planet", "And now, a giant appears ahead of us. Jupiter. The largest planet in the Solar System. "
        "It's so big that more than thirteen hundred Earths could fit inside it. "
        "Jupiter has no solid surface to stand on. It's a vast ball of hydrogen and helium, "
        "wrapped in long bands of clouds, cream and orange and brown, flowing in opposite directions.",
        chapter="Jupiter", body="jupiter", size=440),
    seg("planet", "Look closely, and you'll see the Great Red Spot. It's a storm, larger than the entire Earth, "
        "and it has been swirling for at least a hundred and fifty years, probably much longer. "
        "And Jupiter spins faster than any other planet. A full day there lasts only about ten hours. "
        "That fast spin stretches the clouds into those long, beautiful stripes.", body="jupiter", size=470, x=0.45),
    seg("planet", "Jupiter has dozens and dozens of moons, more than ninety that we know of. "
        "Four of them are large, and each one is a world of its own. "
        "Io is covered with active volcanoes, the most volcanic place in the Solar System. "
        "Europa is wrapped in a shell of ice, and beneath that ice, there is likely a deep ocean of liquid water, "
        "perhaps with more water than all of Earth's oceans combined.", body="jupiter", size=380, x=0.55, moons=4),
    seg("planet", "Ganymede is the largest moon in the Solar System, even larger than the planet Mercury. "
        "And Callisto, old and dark, is one of the most heavily cratered places we know. "
        "Long ago, in sixteen ten, Galileo pointed his small telescope at Jupiter and saw these four moons circling it. "
        "It was one of the first clues that not everything in the sky goes around the Earth.", body="jupiter", size=360, x=0.6, moons=4),
    seg("planet", "Jupiter also acts like a great protector. Its enormous gravity pulls in, or pushes away, "
    "many of the comets and asteroids that wander through the Solar System. "
    "In nineteen ninety four, astronomers watched as a broken comet, called Shoemaker Levy nine, crashed into Jupiter, "
    "leaving dark marks in its clouds larger than the Earth. Jupiter simply absorbed the blow, and kept turning.", body="jupiter", size=430, x=0.5),
    # --- Saturn
    seg("planet", "We drift on, deeper into the cold, and there, in the distance, is perhaps the most beautiful sight in the Solar System. "
        "Saturn, with its wide, shining rings. "
        "The rings stretch for hundreds of thousands of kilometers. But in most places, they're astonishingly thin, "
        "often only about ten meters thick, about the height of a three story building.",
        chapter="Saturn", body="saturn", size=300, rings=True),
    seg("planet", "The rings are made of countless pieces of ice and rock. Some are as small as grains of sand. "
        "Others are as large as houses. Each one follows its own quiet orbit around the planet, "
        "like an endless, frozen river of light. "
        "And Saturn itself is so light for its size that, if you could find a bathtub big enough, it would float.",
        body="saturn", size=330, x=0.45, rings=True),
    seg("planet", "Saturn has well over a hundred moons, and astronomers keep finding more. "
        "The largest, Titan, is bigger than Mercury, and it has a thick, orange, hazy atmosphere. "
        "It rains on Titan. But the rain isn't water. It's liquid methane, falling slowly through the haze, "
        "filling lakes and seas near its poles. It's the only place besides Earth where we know of liquid lying on the surface.",
        body="saturn", size=270, x=0.6, rings=True, moons=1),
    seg("planet", "Another small moon, Enceladus, is bright white, covered in fresh ice. "
        "From cracks near its south pole, it sprays great fountains of water vapor and ice into space. "
        "Beneath its frozen shell, there is an ocean. Deep, dark, and quiet, on a tiny moon far from the Sun. "
        "We'll watch Saturn's rings shimmer for a little while longer... and then, drift on.", body="saturn", size=310, x=0.5, rings=True),
    seg("planet", "A spacecraft called Cassini spent thirteen years circling Saturn, sending back thousands of beautiful pictures. "
    "It flew between the planet and its rings, and gave us our closest look at its moons. "
    "In two thousand and seventeen, at the end of its mission, Cassini was guided gently into Saturn's atmosphere, "
    "sending back information until the very last moment. It became a part of the planet it had studied for so long.", body="saturn", size=290, x=0.55, rings=True),
    # --- Uranus
    seg("planet", "It's getting colder and darker now. The Sun is smaller behind us, though still the brightest star in the sky. "
        "Ahead is a pale, blue green world. Uranus. "
        "It was the first planet discovered with a telescope, by William Herschel, in seventeen eighty one. "
        "Its soft color comes from methane in its atmosphere, which absorbs red light.",
        chapter="Uranus", body="uranus", size=330, rings=True, tilt=1.7),
    seg("planet", "Uranus is unusual. It's tipped over on its side, so it seems to roll around the Sun like a ball. "
        "Perhaps, long ago, something very large crashed into it, and knocked it over. "
        "Because of this tilt, each pole spends about forty two years in constant sunlight, "
        "followed by forty two years of darkness. A single, very long summer, and a single, very long winter.",
        body="uranus", size=360, x=0.45, rings=True, tilt=1.7),
    seg("planet", "A year on Uranus lasts eighty four Earth years. Someone born there at the start of spring "
        "might only see a handful of seasons in their entire life. "
        "And it's the coldest planetary atmosphere we know, falling to around minus two hundred and twenty degrees. "
        "Quiet, cold, and gently glowing, it turns slowly in the dark.", body="uranus", size=380, x=0.6, rings=True, tilt=1.7),
    seg("planet", "Uranus has thin, dark rings, and more than two dozen known moons. "
    "Many of them are named after characters from the plays of Shakespeare and the poems of Alexander Pope. "
    "Miranda, Ariel, Titania, Oberon. Little frozen worlds, with names from old stories, "
    "circling quietly in the cold, far from anyone who might call them by name.", body="uranus", size=340, x=0.5, rings=True, tilt=1.7, moons=3),
    # --- Neptune
    seg("planet", "The last of the planets is Neptune. A deep, beautiful blue. "
        "Neptune was found in an unusual way. Astronomers noticed that Uranus wasn't moving quite as expected, "
        "as if something unseen were gently pulling on it. In eighteen forty six, using only mathematics, "
        "Urbain Le Verrier predicted where this unseen planet should be. And when astronomers looked, there it was.",
        chapter="Neptune", body="neptune", size=340),
    seg("planet", "Neptune is so far away that one trip around the Sun takes one hundred and sixty five Earth years. "
        "Since its discovery, it has completed just one single orbit, finishing it in two thousand and eleven. "
        "And despite being so cold and so far from the Sun's warmth, Neptune has the fastest winds in the Solar System, "
        "racing at around two thousand kilometers an hour.", body="neptune", size=370, x=0.45),
    seg("planet", "Neptune's largest moon, Triton, travels around it backwards, in the opposite direction to the planet's spin. "
        "It was probably once a small world of its own, captured long ago by Neptune's gravity. "
        "Triton is one of the coldest places ever measured, and yet, on its surface, little geysers of nitrogen gas "
        "rise into its thin sky. Only one spacecraft has ever visited Neptune. Voyager two, in nineteen eighty nine.",
        body="neptune", size=330, x=0.6, moons=1),
    seg("planet", "From Neptune, the Sun is about nine hundred times dimmer than it looks from Earth. "
    "It would still be much brighter than the full Moon, but it would look like a small, sharp star, giving almost no warmth at all. "
    "Noon on Neptune would feel like a deep, blue twilight. "
    "And yet, here too, the Sun's gravity keeps hold, guiding Neptune on its long, slow path.", body="neptune", size=300, x=0.5),
    # --- Pluto & Kuiper belt
    seg("planet", "Beyond Neptune lies a wide, cold region called the Kuiper Belt, full of icy worlds. "
        "The most famous of them is Pluto. For many years, it was called the ninth planet. "
        "Since two thousand and six, it has been known as a dwarf planet. But it has never stopped being fascinating.",
        chapter="Pluto and the Kuiper Belt", body="pluto", size=300),
    seg("planet", "In two thousand and fifteen, the New Horizons spacecraft flew past Pluto, and sent back pictures no one expected. "
        "On its surface was a huge, bright plain of frozen nitrogen, shaped like a heart. "
        "Pluto has mountains made of water ice, as hard as rock in that deep cold, and a thin blue haze in its sky. "
        "Its largest moon, Charon, is about half its size. The two of them circle each other, like dancers, far out in the dark.",
        body="pluto", size=330, x=0.5, moons=1),
    seg("planet", "Out here, the Sun is just a very bright star. Its light takes more than five hours to arrive. "
        "And still, the Sun's gravity holds on, keeping these tiny frozen worlds in their slow, patient orbits, "
        "some of which take hundreds of years to complete. "
        "Beyond Pluto, New Horizons visited a small, snowman shaped object called Arrokoth. "
        "It is one of the oldest, most untouched objects ever seen, a leftover from the birth of the Solar System.",
        body="pluto", size=240, x=0.65),
    seg("planet", "The Kuiper Belt is home to many other dwarf planets too, with gentle, unfamiliar names. "
    "Eris, almost the same size as Pluto. Haumea, spinning so fast that it's stretched into the shape of an egg. "
    "Makemake, cold and bright, far from everything. "
    "They wander the outer dark, slowly, silently, taking centuries to complete a single journey around the Sun.", body="pluto", size=220, x=0.4),
    # --- Voyager & the edge
    seg("voyager", "Far beyond all of this, two small spacecraft are still traveling. Voyager one and Voyager two. "
        "They left Earth in nineteen seventy seven, and flew past the giant planets, sending back the first close pictures of them. "
        "Then, their main mission complete, they just kept going, outward, into the dark.", chapter="Voyager and the Edge"),
    seg("voyager", "Voyager one is now more than twenty four billion kilometers away. It is the most distant human made object. "
        "A radio message from Earth takes nearly a full day to reach it. "
        "In two thousand and twelve, it crossed the heliopause, the place where the wind from the Sun finally fades, "
        "and the space between the stars begins. Voyager two followed, in two thousand and eighteen.", zoom=1.2),
    seg("voyager", "Each Voyager carries a golden record. On it are sounds and pictures of the Earth. "
        "Greetings in fifty five languages. Music. The sound of rain, of wind, of a mother's kiss. "
        "A small message in a bottle, thrown into the cosmic ocean, just in case someone, someday, finds it. "
        "Even after their power fades, the Voyagers will keep drifting through the galaxy, silently, for billions of years.", zoom=1.35),
    seg("voyager", "Voyager one's power is slowly running down. Each year, the engineers on Earth carefully turn off another instrument, "
    "or another heater, to save energy, so the little spacecraft can keep talking to us just a bit longer. "
    "Its radio transmitter is only about as powerful as a refrigerator light bulb, and by the time its signal reaches us, it is unimaginably faint. "
    "And yet, giant antennas still listen, every day, for its quiet voice from the edge.", zoom=1.45),
    # --- Oort cloud
    seg("oort", "And far, far beyond them, there may be a vast, invisible shell of icy objects surrounding the entire Solar System. "
        "It's called the Oort Cloud. No one has ever seen it directly. "
        "But some comets fall toward the Sun from such enormous distances that astronomers believe they must come from there.",
        chapter="The Oort Cloud"),
    seg("oort", "The Oort Cloud may stretch more than a light year from the Sun, a quarter of the way to the nearest star. "
        "Even traveling as fast as it does, Voyager one will need about three hundred years just to reach its inner edge, "
        "and perhaps thirty thousand years to pass through it. "
        "Out there, the Sun is only a bright point of light, and the cold is deeper than anything we can imagine.", zoom=1.25),
    seg("oort", "Sometimes, a passing star, or the slow tides of our galaxy, gently nudge one of these distant icy objects. "
    "It begins to fall toward the Sun, a journey that can take thousands of years. "
    "As it comes closer, the Sun's warmth turns its ice into gas, and it grows a long, glowing tail. "
    "A comet. A visitor from the edge of the Solar System, passing through our sky, before slowly returning to the dark.", zoom=1.4),
    # --- Pale blue dot / return
    seg("dot", "Long before it left the planets behind, in nineteen ninety, Voyager one turned its camera back, one last time. "
        "From about six billion kilometers away, it took a picture of the Earth. "
        "In that picture, our whole world is just a tiny, pale blue dot, smaller than a single pixel, floating in a beam of sunlight.",
        chapter="Home"),
    seg("dot", "Everyone you have ever loved. Every sunrise, every song, every quiet evening. "
        "All of it, on that one small dot, suspended in the dark. "
        "It's a gentle reminder of how small we are, and how precious, and how lucky, to be here at all.", zoom=1.3),
    seg("dot", "Out here, at the edge of everything we know, there is no up and no down. No noise. No hurry. "
    "Just the soft light of distant stars, and the long, patient dance of worlds around the Sun. "
    "We are a part of that dance. Every atom in your body was once inside a star. "
    "In a quiet way, you are the universe, resting, and looking at itself.", zoom=1.4),
    seg("travel", "Slowly now, our little ship turns around. The stars drift past the window, steady and calm. "
        "We pass the frozen worlds of the Kuiper Belt, the deep blue of Neptune, the pale green of Uranus. "
        "Saturn's rings glimmer once more in the distance. Jupiter's bands slide by, cream and orange. "
        "The Sun grows brighter, and warmer, and closer.", neb=3, warp=0.6),
    seg("earth", "And there, ahead of us, is home. Blue and white, turning slowly in the sunlight. "
        "Somewhere down there is your bed, your pillow, your blanket, waiting for you. "
        "Let your eyes feel heavy now. Let your breathing slow down. In... and out.", zoom=1.05, night=0.3),
    seg("travel", "You don't need to remember all the numbers, or all the names. "
        "Just remember the feeling. The quiet. The slow turning of the planets. The soft light of the Sun, holding everything together. "
        "Everything is moving, gently, patiently, exactly as it should. "
        "And you can rest now, safe and warm, on our small blue world.", neb=5, slow=True),
    seg("outro", "Thank you for traveling with me tonight. If you enjoyed this journey, you can subscribe to Sleepy Cosmos "
        "for a new calm voyage through space every week. Sleep well, and sweet dreams.", fade_out=8.0),
]


def _with_pauses(segs):
    """Quiet, wordless drifts between chapters and a long calm tail after the goodbye."""
    out = []
    for i, s in enumerate(segs):
        if s.get("chapter") and i > 1:
            out.append(dict(scene="travel", args=dict(neb=i % 6, slow=True, warp=0.15), duration=28))
        out.append(s)
    out.append(dict(scene="travel", args=dict(neb=0, slow=True, warp=0.1, fade_out=20.0), duration=900))
    return out


LONG = _with_pauses(LONG)
SHORT = []


def thumb(S, c):
    """Saturn and a small Earth on a starry field, big calm title on the left."""
    import space_art as A
    S.draw_backdrop(c, 0, 50.0, 0)
    A.rings(c, 1350, 560, 300, front=False)
    S.paint_sphere(c, "saturn", 1350, 560, 300, 0.3, light=(-0.6, -0.3, 0.72), tilt=0.12)
    A.rings(c, 1350, 560, 300, front=True)
    A.glow(c, 1760, 900, 110, (0.4, 0.65, 1.0), 0.4)
    S.paint_sphere(c, "earth", 1760, 900, 80, 0.15, light=(-0.6, -0.3, 0.72), tilt=0.41, clouds_phase=0.3)
    A.crescent(c, 170, 170, 60)
    A.text(c, "Fall Asleep", 520, 420, 120, (1, 1, 1))
    A.text(c, "Traveling the", 520, 545, 92, (1, 1, 1))
    A.text(c, "Solar System", 520, 665, 110, (1, 0.88, 0.62))
    c.set_source_rgba(0.08, 0.06, 0.2, 0.85)
    c.new_path()
    c.arc(370, 790, 50, 1.5708, 4.7124)
    c.arc(670, 790, 50, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    A.text(c, "SLEEP STORY", 520, 808, 44, (1, 1, 1), family="Inter", spacing=2)
