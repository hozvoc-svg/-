# Sleepy Cosmos, episode 4: "Fall Asleep Drifting Through Galaxies" (narrated, ElevenLabs).
from episodes.solar_journey import EL_VOICE, EL_SETTINGS, _with_pauses

SCENES_MODULE = "space_scenes"
AMBIENT = "space"
CAPTIONS = False
FADE = 0.001
GAP, TAIL = 0.0, 6.0
PRON = {"Andromeda": "An-drom-eda"}


def seg(scene, text, chapter=None, **args):
    return dict(scene=scene, text=[text], chapter=chapter, args=args)


LONG = [
    seg("title", "Hello, and welcome back to Sleepy Cosmos. Tonight, we're going farther than ever before. "
        "Beyond the planets, beyond the nearby stars, out into the great ocean of galaxies. "
        "It's a very big journey, but you don't need to do anything at all. Just lie back, let your eyes close if you like, "
        "and breathe slowly. In... and out. Let's drift.", chapter="Welcome", subtitle="Drifting Through Galaxies"),
    # --- Milky Way
    seg("galaxy", "Every star you have ever seen in the night sky belongs to one great family. Our galaxy. The Milky Way. "
        "It's a vast, slowly turning spiral of stars, gas, and dust, about a hundred thousand light years across. "
        "It holds somewhere between one and four hundred billion stars. Our Sun is just one of them.",
        chapter="The Milky Way", seed=3, scale=520),
    seg("galaxy", "On a very dark night, far from city lights, you can see the Milky Way as a soft, glowing band stretched across the sky. "
        "That band is the disk of our galaxy, seen from the inside. Billions of distant stars, so many and so far away, "
        "that their light blends together into a gentle, milky haze. That's where its name comes from.",
        seed=3, scale=620, tilt=0.3),
    seg("galaxy", "Our Sun lives in one of the spiral arms, about twenty six thousand light years from the center. "
        "Not in the crowded middle, and not at the lonely edge. Somewhere calm, in between. "
        "And the whole galaxy is turning. The Sun carries us around the center once every two hundred and thirty million years or so. "
        "The last time the Earth was in this part of its journey, the very first dinosaurs were just appearing.",
        seed=3, scale=700, tilt=0.4, dx=-120),
    seg("blackhole", "At the very center of the Milky Way, hidden behind thick clouds of dust, there's a supermassive black hole, "
        "about four million times heavier than the Sun. Stars close to it race around it in tight, fast orbits. "
        "But out where we are, it's very far away. It's simply the quiet center of our great, turning home.", zoom=1.0),
    # --- neighbors
    seg("galaxy", "The Milky Way isn't alone. It has small companion galaxies, circling around it like moons around a planet. "
        "Two of them, the Large and Small Magellanic Clouds, can be seen from the southern half of the Earth "
        "as two faint, glowing smudges, as if pieces of the Milky Way had drifted off on their own.",
        chapter="Our Neighbors", seed=7, scale=260, dx=200, arms=1),
    seg("galaxy", "Our nearest large neighbor is the Andromeda Galaxy, about two and a half million light years away. "
        "On a dark autumn night, you can see it with your own eyes, as a small, faint oval of light. "
        "The light reaching your eyes from Andromeda left it two and a half million years ago, "
        "long before the first humans walked the Earth.", seed=5, scale=560, tilt=0.28),
    seg("galaxy", "Andromeda is larger than the Milky Way, with perhaps a trillion stars. "
        "And the two galaxies are slowly drifting toward each other. "
        "In several billion years, they may pass close, or even merge, swirling together into one great new galaxy. "
        "But even then, the stars are so far apart that they would almost never collide. "
        "They would simply drift past one another, like ships passing quietly in the night.", seed=5, scale=640, tilt=0.3),
    # --- kinds of galaxies
    seg("galaxy", "Galaxies come in many shapes. Some are spirals, like ours, with long, curving arms where new stars are born. "
        "Some have a straight bar of stars across their middle, with arms trailing from its ends. "
        "Some are huge, smooth ovals, full of old, golden stars, calm and quiet. "
        "And some are small and irregular, with no clear shape at all, like clouds drifting in the wind.",
        chapter="Many Kinds of Galaxies", seed=9, scale=480, arms=4),
    seg("galaxy", "Sometimes, galaxies come close to each other, and their gravity pulls them into new shapes. "
        "Long streams of stars stretch out between them, like taffy, or like ribbons in the wind. "
        "These meetings take hundreds of millions of years. From our point of view, they look completely still, "
        "frozen in a single, graceful moment of a very, very slow dance.", seed=11, scale=420, dx=-200, arms=2),
    # --- deep field
    seg("travel", "In nineteen ninety five, astronomers tried something unusual. They pointed the Hubble Space Telescope "
        "at a tiny, dark patch of sky, a patch that seemed completely empty, "
        "about the size of a grain of sand held at arm's length. And they kept looking at it, for days.",
        chapter="The Deep Field", neb=2, warp=0.2),
    seg("galaxy", "When the picture came back, that empty patch of sky was full of galaxies. Thousands of them. "
        "Spirals, ovals, tiny distant smudges, each one a whole galaxy, with billions of stars of its own. "
        "And that was just one tiny patch. The whole sky is like that, in every direction we look.",
        seed=13, scale=200, dx=-500),
    seg("galaxy", "Today, astronomers think there are hundreds of billions of galaxies in the part of the universe we can see. "
        "Maybe more. If you tried to count them, one every second, without ever stopping, "
        "it would take you thousands of years. And each one is full of stars, and many of those stars have planets of their own.",
        seed=17, scale=300, dx=420),
    # --- looking back in time
    seg("travel", "Because light takes time to travel, looking far away also means looking back in time. "
        "We see the Moon as it was a little over a second ago. The Sun, as it was eight minutes ago. "
        "The farthest galaxies, as they were billions of years ago, when the universe was young. "
        "Every time we look up, we are looking into the past.", chapter="Looking Back in Time", neb=4, warp=0.3),
    seg("galaxy", "The James Webb Space Telescope, launched in two thousand and twenty one, can see some of the very first galaxies, "
        "shining when the universe was only a few hundred million years old. "
        "They're small, and bright, and full of brand new stars. "
        "Their light has been traveling toward us for over thirteen billion years, just to land, at last, in a telescope's golden mirrors.",
        seed=19, scale=240, arms=3),
    seg("travel", "The universe itself is about thirteen point eight billion years old. And it's still growing. "
        "The space between the galaxies is slowly stretching, carrying them farther apart. "
        "The part we can see stretches tens of billions of light years in every direction. "
        "And beyond that, the universe may go on, much farther still, perhaps forever.", neb=0, warp=0.15),
    seg("travel", "Even the quiet darkness between the stars still holds a faint, gentle warmth. "
        "A soft glow left over from the very beginning, when the whole universe was hot and bright. "
        "Over billions of years, that glow has cooled, until now it's just a few degrees above absolute zero. "
        "But it's still there, everywhere, like the last warmth in a blanket after a long night.", neb=1, slow=True),
    # --- home
    seg("galaxy", "And now, slowly, we drift back. Past the distant galaxies, past Andromeda, "
        "toward our own spiral, glowing softly in the dark. Toward one ordinary star in one of its arms. "
        "Toward one small blue planet, turning gently in the sunlight.", chapter="Home", seed=3, scale=600, tilt=0.35),
    seg("earth", "Here we are. Home. Of all the hundreds of billions of galaxies, and all the stars inside them, "
        "this is the one small place where you are lying down right now, resting, safe and warm. "
        "Let that feeling settle over you. You belong to something very, very big, and very, very beautiful.", night=0.25),
    seg("travel", "Let your breathing slow. Let your shoulders sink. Let your thoughts drift away, like distant galaxies, "
        "slowly, gently, farther and farther. There's nowhere to go. Nothing to do. "
        "The universe is turning, quietly, exactly as it should. And you can rest now.", neb=5, slow=True),
    seg("outro", "Thank you for spending this quiet time with me. If you enjoyed it, you can subscribe to Sleepy Cosmos "
        "for a new calm journey through space every week. Sleep well, and sweet dreams.", subtitle="Goodnight"),
]

LONG = _with_pauses(LONG)
SHORT = []


def thumb(S, c):
    import space_art as A
    c.set_source_rgb(*S.BG1)
    c.paint()
    S.sc_galaxy(c, 10.0, 40.0, 100.0, dict(seed=3, scale=620, dx=380, tilt=0.42, neb=1))
    A.crescent(c, 170, 170, 60)
    A.text(c, "Fall Asleep", 470, 420, 115, (1, 1, 1))
    A.text(c, "Drifting Through", 470, 540, 80, (1, 1, 1))
    A.text(c, "Galaxies", 470, 680, 140, (1, 0.88, 0.62))
    c.set_source_rgba(0.08, 0.06, 0.2, 0.85)
    c.new_path()
    c.arc(320, 800, 50, 1.5708, 4.7124)
    c.arc(620, 800, 50, -1.5708, 1.5708)
    c.close_path()
    c.fill()
    A.text(c, "SLEEP STORY", 470, 818, 44, (1, 1, 1), family="Inter", spacing=2)
