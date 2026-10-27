from episodes._short_common import *
PRON = {"6EQUJ5": "six, E, Q, U, J, five", "Ehman": "Ee-man"}
SHORT_HOOK = [("72 SECONDS", (0.3, 0.93, 1.0), 92), ("from deep space", INK, 48)]
SHORT = shots([
    ("wow_dish", None, ["August 15th, 1977. A radio telescope in Ohio, called Big Ear, is listening to the sky."]),
    ("wow_print", None, ["Days later, astronomer Jerry Ehman checks the printouts, and sees this. 6EQUJ5."]),
    ("wow_print", dict(circle=True), ["A signal so strong, he circles it, and writes one word. Wow!"]),
    ("wow_sky", None, ["It lasted seventy-two seconds, and came from the direction of the constellation Sagittarius."]),
    ("wow_search", None, ["Astronomers have searched that spot again and again. It never came back. Follow for more."]),
])
