# Sleepy Cosmos, episode 2: "Fall Asleep Exploring the Moons of Our Solar System" (narrated, ElevenLabs).
from episodes.solar_journey import EL_VOICE, EL_SETTINGS, _with_pauses as _pauses_ep1

SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
XFADE = 2.5
OVERLAY_FX = (("shooting_star", 0.7),)
CHAPTER_STYLE = "letters"
CHAPTER_PAIR = "classic"
FINAL = "hevc1440"
FADE = 0.001
GAP, TAIL = 0.0, 6.0
PRON = {"Io": "Eye-oh", "Charon": "Karon", "Iapetus": "Eye-app-et-us", "Enceladus": "En-sell-a-dus",
        "Mimas": "My-mas", "Huygens": "Hoy-gens", "Kraken Mare": "Kraken Mar-ay"}


def seg(scene, text, chapter=None, **args):
    return dict(scene=scene, text=[text], chapter=chapter, args=args)


LONG = [
    seg("title", "Hello, and welcome back to Sleepy Cosmos. Tonight, we're going to visit some of the quiet companions of the planets. "
        "The moons. Small worlds of ice and rock, of volcanoes and hidden oceans, circling patiently in the dark. "
        "So settle in, get comfortable, and let your breathing slow down. In... and out. "
        "There's nothing to remember, and nothing to do. Just listen, and drift.", chapter="Welcome", subtitle="The Moons of Our Solar System"),
    # --- our Moon
    seg("moon", "We begin with the Moon we know best. Our own. On a clear night, it hangs above the rooftops and the trees, "
        "silver and calm, the same Moon that people have looked up at for as long as there have been people. "
        "Scientists think it was born about four and a half billion years ago, when a planet about the size of Mars crashed into the young Earth. "
        "The debris from that collision gathered together in orbit, and slowly became the Moon.",
        chapter="Our Moon", body="moon", parent="earth", size=320, parent_size=620, px=0.12, py=0.85),
    seg("moon", "The Moon is about three thousand five hundred kilometers across, a little more than a quarter of the Earth's width. "
        "Its gravity is gentle, only about one sixth of what we feel here. "
        "If you jumped on the Moon, you would float upward slowly, and drift back down, as if in a dream. "
        "Its dark patches, the ones that make the face of the man in the Moon, are ancient seas of cooled lava.",
        body="moon", parent="earth", size=360, parent_size=620, px=0.12, py=0.85, x=0.55),
    seg("moon", "Between nineteen sixty nine and nineteen seventy two, twelve people walked on its surface. "
        "Because there is no wind and no rain on the Moon, their footprints are still there, almost exactly as they left them. "
        "They will probably remain for millions of years, small marks in the grey dust, "
        "quietly remembering the day we first stepped onto another world.",
        body="moon", parent="earth", size=400, parent_size=620, px=0.12, py=0.85, x=0.6, night=0.15),
    # --- Mars moons
    seg("moon", "Next, the tiny moons of Mars. Phobos and Deimos. In the old Greek stories, their names mean fear and dread. "
        "But there's nothing frightening about them. They're small, lumpy, and grey, like potatoes floating in space. "
        "Phobos circles very close to Mars, going around it three times every single day. "
        "From the surface of Mars, it would rise in the west and set in the east.",
        chapter="Phobos and Deimos", body="phobos", parent="mars", size=200, parent_size=650, px=0.1, py=0.8),
    seg("moon", "Phobos is slowly spiraling inward, a few centimeters closer every year. "
        "In tens of millions of years, it will come so close that Mars' gravity will pull it apart. "
        "Its pieces may form a thin ring around Mars, for a while. "
        "Deimos, smaller and farther away, will go on circling, quiet and alone, long after Phobos is gone.",
        body="deimos", parent="mars", size=150, parent_size=650, px=0.1, py=0.8, x=0.55),
    # --- Io
    seg("moon", "Now we travel out to Jupiter, and its four great moons. The first is Io. "
        "Io is the most volcanic place in the entire Solar System. It has hundreds of active volcanoes. "
        "Some of them send fountains of lava high into the sky, and plumes of gas that rise hundreds of kilometers above the surface, "
        "before falling back down as a gentle frost.",
        chapter="Io", body="io", parent="jupiter", size=300, parent_size=760, px=0.08, py=0.82),
    seg("moon", "Io's colors come from sulfur. Yellow, orange, red, white, and black, like a painter's palette. "
        "But why is Io so active? It's because of Jupiter's enormous gravity, and the steady tug of its neighboring moons. "
        "As Io travels around Jupiter, it is squeezed and stretched, again and again. "
        "Its rocks flex like a ball being squeezed in your hand, and that constant kneading keeps its insides hot and molten.",
        body="io", parent="jupiter", size=330, parent_size=760, px=0.08, py=0.82, x=0.58),
    # --- Europa
    seg("moon", "The next moon, Europa, is very different. It's smooth and pale, wrapped in a shell of ice, "
        "crossed by long reddish brown lines, like cracks in a frozen lake. "
        "Europa is a little smaller than our Moon. But beneath that icy crust, there is almost certainly an ocean. "
        "A real ocean, of liquid salty water, maybe a hundred kilometers deep.",
        chapter="Europa", body="europa", parent="jupiter", size=300, parent_size=760, px=0.08, py=0.82),
    seg("moon", "Europa's hidden ocean may hold about twice as much water as all the oceans of the Earth combined. "
        "It has stayed liquid for billions of years, warmed by the same gentle squeezing that heats Io. "
        "In the darkness at the bottom of that ocean, there might be warm vents, like the ones deep in Earth's seas, "
        "where strange and wonderful creatures live without ever seeing sunlight.",
        body="europa", parent="jupiter", size=330, parent_size=760, px=0.08, py=0.82, x=0.58),
    seg("moon", "A spacecraft called Europa Clipper is on its way there now. It launched in two thousand and twenty four, "
        "and will arrive at Jupiter around the year two thousand and thirty. "
        "It will fly past Europa dozens of times, studying its ice, and tasting the faint traces that drift up from below. "
        "It's a long journey. But the ocean has waited for billions of years. It can wait a little longer.",
        body="europa", parent="jupiter", size=360, parent_size=760, px=0.08, py=0.82, x=0.6, night=0.1),
    # --- Ganymede & Callisto
    seg("moon", "Ganymede is the largest moon in the Solar System. It's even bigger than the planet Mercury. "
        "Its surface is a patchwork of dark, ancient regions, and lighter areas, crossed by long grooves and ridges. "
        "And Ganymede is the only moon we know of that has its own magnetic field. "
        "Because of that, it has faint auroras of its own, glowing softly around its poles.",
        chapter="Ganymede and Callisto", body="ganymede", parent="jupiter", size=330, parent_size=760, px=0.08, py=0.82),
    seg("moon", "Like Europa, Ganymede probably hides a deep ocean under its ice, perhaps sandwiched between layers of ice, "
        "like a cool, dark filling. A European spacecraft, called JUICE, is traveling there now, "
        "and will one day settle into orbit around Ganymede, the first spacecraft ever to orbit a moon other than our own.",
        body="ganymede", parent="jupiter", size=360, parent_size=760, px=0.08, py=0.82, x=0.58),
    seg("moon", "Farther out circles Callisto, dark and quiet. It's one of the most heavily cratered places we know. "
        "Its surface has hardly changed in billions of years, so it's like a calm, old diary of everything that ever struck it. "
        "One of its craters, called Valhalla, is surrounded by rings of ripples, "
        "frozen in place, like the circles that spread out when you drop a stone into a still pond.",
        body="callisto", parent="jupiter", size=320, parent_size=760, px=0.08, py=0.82, x=0.6),
    # --- Titan
    seg("moon", "We drift onward now, to Saturn, and its largest moon, Titan. "
        "Titan is wrapped in a thick, golden orange haze, so thick that we can't see its surface in ordinary light. "
        "It's the only moon in the Solar System with a dense atmosphere. "
        "Standing on Titan, the air would press on you about one and a half times as much as the air on Earth.",
        chapter="Titan", body="titan", parent="saturn", size=320, parent_size=560, px=0.12, py=0.78),
    seg("moon", "Beneath that haze is a strange and quiet world. It has rivers, lakes, and seas, and it has rain. "
        "But it's far too cold for water to flow. Instead, the rivers and seas are filled with liquid methane and ethane. "
        "Rain drops on Titan are larger than on Earth, and they fall very slowly, drifting down like snowflakes. "
        "Its largest sea, Kraken Mare, is bigger than the Caspian Sea on Earth.",
        body="titan", parent="saturn", size=350, parent_size=560, px=0.12, py=0.78, x=0.58),
    seg("moon", "In two thousand and five, a small probe called Huygens parachuted down through Titan's haze. "
        "It landed on a damp plain scattered with smooth, rounded pebbles of ice, under a soft orange sky. "
        "It's still the most distant landing ever made. "
        "And one day, a flying robot called Dragonfly will travel there, gliding from place to place, through the thick, calm air.",
        body="titan", parent="saturn", size=380, parent_size=560, px=0.12, py=0.78, x=0.6, night=0.1),
    # --- Enceladus, Mimas, Iapetus
    seg("moon", "Not far from Titan is a tiny, shining moon called Enceladus. It's only about five hundred kilometers across. "
        "It's one of the brightest objects in the Solar System, because its surface is covered in fresh, clean ice. "
        "And from cracks near its south pole, which scientists call tiger stripes, it sprays tall fountains of water into space.",
        chapter="The Icy Moons of Saturn", body="enceladus", parent="saturn", size=300, parent_size=560, px=0.12, py=0.78),
    seg("moon", "That water comes from an ocean hidden beneath the ice. The Cassini spacecraft flew right through those fountains, "
        "and tasted salt, and minerals, and even some of the chemical ingredients that life on Earth depends on. "
        "Some of the ice drifts away from Enceladus and spreads out around Saturn, forming one of its faint outer rings. "
        "So a little piece of this small moon is always shining in Saturn's rings.",
        body="enceladus", parent="saturn", size=330, parent_size=560, px=0.12, py=0.78, x=0.58),
    seg("moon", "Saturn has many other moons with their own small surprises. "
        "Mimas has one enormous crater, so large compared to the moon itself that it looks like a giant eye. "
        "And Iapetus is two toned. One side is as dark as coal, and the other is bright as snow. "
        "Around its middle runs a long, tall ridge of mountains, like a seam around a walnut.",
        body="iapetus", parent="saturn", size=300, parent_size=560, px=0.12, py=0.78, x=0.6),
    # --- Uranus & Neptune
    seg("moon", "Far out, at Uranus, there's a small moon called Miranda. It looks as though it was broken apart and put back together, "
        "with grooves and ridges and patchwork regions that don't quite match. "
        "Miranda has the tallest cliff we know of in the Solar System, a sheer wall of ice about twenty kilometers high. "
        "In Miranda's weak gravity, if you stepped off the top, it would take you around ten minutes to drift down to the bottom.",
        chapter="Miranda and Triton", body="miranda", parent="uranus", size=280, parent_size=520, px=0.12, py=0.78),
    seg("moon", "And at Neptune, there's Triton. Pale pink and white, it's one of the coldest places ever measured, "
        "around minus two hundred and thirty five degrees. "
        "Triton circles Neptune backwards, against the planet's spin, which tells us it was probably captured long ago, "
        "a small wandering world from the Kuiper Belt that came too close, and never left.",
        body="triton", parent="neptune", size=300, parent_size=560, px=0.12, py=0.8, x=0.58),
    seg("moon", "Slowly, over billions of years, Triton is spiraling closer to Neptune. "
        "One day, far in the future, it will be pulled apart, and its pieces may form a beautiful set of rings. "
        "But for now, it glides on, with small dark geysers rising from its frozen surface, into a sky where the Sun is just a bright star.",
        body="triton", parent="neptune", size=330, parent_size=560, px=0.12, py=0.8, x=0.6, night=0.15),
    # --- Charon
    seg("moon", "Our last stop is far beyond Neptune. Pluto and its largest moon, Charon. "
        "Charon is about half the size of Pluto, so large that the two of them circle around a point in the space between them, "
        "like two dancers holding hands. They always show each other the same face. "
        "From one side of Pluto, Charon hangs in the sky, never rising and never setting.",
        chapter="Charon", body="charon", parent="pluto", size=300, parent_size=430, px=0.15, py=0.78),
    seg("moon", "When New Horizons flew past in two thousand and fifteen, it saw that Charon has a dark, reddish cap at its north pole. "
        "Scientists think the red comes from gas that escapes from Pluto, drifts across to Charon, and freezes there. "
        "So, in a quiet way, Pluto is always painting its moon.",
        body="charon", parent="pluto", size=330, parent_size=430, px=0.15, py=0.78, x=0.58),
    # --- home
    seg("moon", "And now, slowly, we drift back home, past the icy moons and the great planets, past the asteroid belt and the red sands of Mars, "
        "to our own grey, gentle Moon. It's rising now, over a sleeping world. "
        "The same Moon that lights the sea at night, that pulls the tides in and out, that keeps the Earth steady as it turns.",
        chapter="Goodnight, Moon", body="moon", parent="earth", size=300, parent_size=620, px=0.12, py=0.85, x=0.6, night=0.2),
    seg("travel", "There are hundreds of moons in our Solar System. Fiery ones, frozen ones, small ones and great ones. "
        "Each one circling quietly, never in a hurry, following the same patient path, night after night. "
        "Let your thoughts circle slowly too, and settle. Your body is heavy. Your breathing is slow. "
        "Everything is calm, and everything is exactly where it should be.", neb=5, slow=True),
    seg("outro", "Thank you for spending this quiet time with me. If you enjoyed it, you can subscribe to Sleepy Cosmos "
        "for a new calm journey through space every week. Sleep well, and sweet dreams.", subtitle="Goodnight"),
]

LONG = _pauses_ep1(LONG)
SHORT = []


def thumb(S, c):
    import space_art as A
    S.draw_backdrop(c, 3, 50.0, 0)
    A.rings(c, 1650, 860, 420, tilt=0.18, angle=-0.2, front=False)
    S.paint_sphere(c, "saturn", 1650, 860, 420, 0.3, light=(-0.6, -0.3, 0.72), night=0.2)
    A.rings(c, 1650, 860, 420, tilt=0.18, angle=-0.2, front=True)
    A.glow(c, 1260, 430, 230, (1.0, 0.7, 0.35), 0.4)
    S.paint_sphere(c, "titan", 1260, 430, 200, 0.2, light=(-0.6, -0.3, 0.72))
    S.paint_sphere(c, "europa", 980, 760, 95, 0.1, light=(-0.6, -0.3, 0.72))
    A.crescent(c, 170, 170, 60)
    A.text(c, "Fall Asleep", 470, 420, 115, (1, 1, 1))
    A.text(c, "Exploring the", 470, 540, 86, (1, 1, 1))
    A.text(c, "Moons", 470, 680, 150, (1, 0.88, 0.62))
    c.set_source_rgba(0.08, 0.06, 0.2, 0.85)
    c.new_path()
    c.arc(320, 800, 50, 1.5708, 4.7124)
    c.arc(620, 800, 50, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    A.text(c, "SLEEP STORY", 470, 818, 44, (1, 1, 1), family="Inter", spacing=2)
