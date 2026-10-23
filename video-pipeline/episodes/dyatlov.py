# Episode: The Dyatlov Pass Incident (long-form) + Short.
# Each segment: scene name, scene args, list of sentences (caption text).
# PRON maps caption spellings to spellings the TTS pronounces well.

PRON = {
    "Thibeaux-Brignolles": "Tee-bo Brin-yol",
    "Kholat Syakhl": "Holat See-akhl",
    "Krivonischenko": "Krivo-nee-shenko",
    "Kolmogorova": "Kolmo-gorova",
    "Zolotaryov": "Zolota-ryov",
    "Doroshenko": "Doro-shenko",
    "Dubinina": "Doo-bee-nina",
    "Kolevatov": "Kole-vatov",
    "Gaume": "Gome",
    "Puzrin": "Poo-zrin",
    "Otorten": "Otor-ten",
    "Mansi": "Mahn-see",
    "Yudin": "Yoo-din",
    "ETH": "E T H",
    "EPFL": "E P F L",
    "-30°C": "minus thirty degrees",
}

LONG = [
    dict(scene="tent_night", chapter="The tent", text=[
        "February 1959.",
        "A search team climbs a frozen slope in the northern Ural Mountains, and finds a tent.",
        "It has been cut open... from the inside.",
    ]),
    dict(scene="footprints", text=[
        "Leading away from it are footprints.",
        "Nine people, walking down the mountain at -30°C.",
        "Most of them in socks. Some of them barefoot.",
    ]),
    dict(scene="questions", text=[
        "Why would nine experienced hikers run from their only shelter, into a night that would almost certainly kill them?",
        "For sixty years, nobody could answer that question.",
        "Today, we finally can. Let's go back to the beginning.",
    ]),
    dict(scene="title", text=["This is the Dyatlov Pass incident."]),
    dict(scene="group", chapter="The expedition", text=[
        "In January 1959, ten students and graduates of the Ural Polytechnic Institute set out on a winter ski trek.",
        "Their leader was twenty-three year old Igor Dyatlov, a radio engineering student and an experienced hiker.",
    ]),
    dict(scene="map", text=[
        "Their goal was Otorten, a mountain deep in the northern Urals.",
        "The route was rated category three, the hardest level at the time.",
        "Every member had done tough trips before. This was not a group of amateurs.",
    ]),
    dict(scene="goodbye", text=[
        "On January 28th, one member, Yuri Yudin, fell ill and turned back.",
        "He said goodbye to his friends.",
        "He was the last person to ever see them alive.",
    ]),
    dict(scene="walking", text=[
        "The remaining nine pushed on.",
        "We know what happened next from their diaries and cameras, which were later recovered.",
        "They joked, they sang, they even made a camp newspaper called Evening Otorten.",
        "Everything looked normal.",
    ]),
    dict(scene="camp", text=[
        "On February 1st, they set up camp on the slope of a mountain the local Mansi people called Kholat Syakhl.",
        "In their language, that means Dead Mountain.",
        "Instead of camping in the shelter of the forest below, they pitched their tent on the open slope.",
        "They dug into the snow to make a flat platform, ate dinner, and went to sleep.",
    ]),
    dict(scene="calendar", chapter="The search", text=[
        "Dyatlov had promised to send a telegram by February 12th.",
        "The day came and went.",
        "Families were worried, but delays were common on winter trips.",
        "On February 20th, the first search teams set out.",
    ]),
    dict(scene="search", text=[
        "On February 26th, they found the tent.",
        "It was half collapsed and buried in snow.",
        "Inside were the group's boots, coats, food and equipment. Everything they needed to survive.",
        "But the tent wall had been sliced open with a knife... from the inside.",
    ]),
    dict(scene="footprints", args=dict(orderly=True), text=[
        "Footprints led down the slope toward the forest, about one and a half kilometers away.",
        "Eight or nine sets.",
        "And strangely, they were not the prints of people running in panic.",
        "The group walked, calmly, side by side, in a line.",
    ]),
    dict(scene="cedar", text=[
        "At the edge of the forest, under a tall cedar tree, searchers found the remains of a small fire.",
        "And next to it, the first two hikers. Yuri Doroshenko and Yuri Krivonischenko.",
        "They were wearing only their underwear.",
        "Branches on the cedar were broken off up to five meters high, as if someone had climbed it to look back toward the tent.",
    ]),
    dict(scene="between", text=[
        "Then, between the cedar and the tent, three more.",
        "Igor Dyatlov, Zinaida Kolmogorova, and Rustem Slobodin.",
        "Their positions suggested they died trying to climb back up to the tent.",
        "Slobodin had a small fracture in his skull.",
    ]),
    dict(scene="ravine", chapter="The last four", text=[
        "The last four would not be found for more than two months.",
        "In May, as the snow melted, searchers discovered them in a ravine near the cedar, under four meters of snow.",
    ]),
    dict(scene="injuries", text=[
        "And this is where the story gets truly strange.",
        "Nikolai Thibeaux-Brignolles had a severe skull fracture.",
        "Lyudmila Dubinina and Semyon Zolotaryov had massive chest fractures.",
        "One expert compared the force to a car crash. Yet there were almost no external wounds.",
        "Some of them wore clothing cut from their dead friends, and a few items showed traces of radiation.",
    ]),
    dict(scene="classified", chapter="The investigation", text=[
        "The Soviet investigation closed in May 1959.",
        "Its conclusion? The hikers died because of, quote, a compelling natural force.",
        "The files were classified, and the area was closed to hikers for years.",
    ]),
    dict(scene="theories", chapter="The theories", text=[
        "Of course, a vague answer like that created an explosion of theories.",
    ]),
    dict(scene="rocket", text=[
        "Some believed the group stumbled onto a secret military test.",
        "A parachute mine or a missile could explain the injuries and the radiation.",
        "And people in the region did report strange orange lights in the sky that winter.",
    ]),
    dict(scene="yeti", text=[
        "Others blamed the local Mansi people, or escaped prisoners.",
        "But there were no signs of a fight, and nothing was stolen.",
        "And yes, some people blamed a yeti.",
    ]),
    dict(scene="infrasound", text=[
        "A more scientific idea was infrasound.",
        "Wind around the mountain creating low frequency sound that can trigger panic.",
        "But that still does not explain the broken bones.",
    ]),
    dict(scene="objections", text=[
        "And then there was the avalanche theory. It explains why they fled.",
        "But skeptics had strong arguments against it.",
        "The slope seemed too gentle for an avalanche.",
        "Searchers found no clear avalanche debris.",
        "And why would an avalanche happen hours after they went to sleep?",
    ]),
    dict(scene="study", chapter="The 2021 study", text=[
        "In 2019, Russian prosecutors reopened the case.",
        "And in 2021, two scientists, Johan Gaume of EPFL and Alexander Puzrin of ETH Zurich, published a study in the journal Communications Earth and Environment.",
        "It answered all three objections.",
    ]),
    dict(scene="slab", args=dict(mode="build"), text=[
        "Here is what they think happened.",
        "To pitch the tent, the hikers cut a flat platform into the slope.",
        "That removed support for the snow above.",
        "Through the night, strong winds blew more snow down the mountain, piling it up above the tent.",
        "Slowly, the weight grew. Until, hours later, a small block of snow, a slab, broke loose.",
    ]),
    dict(scene="slab", args=dict(mode="hit"), text=[
        "It was not a huge avalanche. Just a slab of packed snow, a few meters long.",
        "Enough to crush part of the tent.",
        "Using computer models, including snow simulation code originally built for the animated movie Frozen, they showed that a slab like this could cause exactly the kind of chest and skull injuries found on the hikers.",
        "Especially if they were lying on their skis on the tent floor.",
    ]),
    dict(scene="flee", text=[
        "Waking up in the dark, under a crushing weight of snow, and fearing a bigger avalanche, the hikers cut their way out and walked down to the forest.",
        "They planned to come back.",
        "But the night was brutal.",
        "And by the time searchers arrived weeks later, wind and fresh snow had hidden the small slab completely.",
    ]),
    dict(scene="unsolved", chapter="What's still unsolved", text=[
        "Not everything is solved.",
        "The radiation traces may be linked to the fact that one of the hikers had worked at a nuclear facility, but that has never been proven.",
        "And some people still reject the avalanche explanation.",
        "But for the first time in sixty years, we have a theory that explains most of the evidence, without secret weapons or monsters.",
    ]),
    dict(scene="memorial", text=[
        "Just nine young people, a cold mountain, and a chain of small, tragic decisions.",
        "Today, the place where they died is called Dyatlov Pass, in their memory.",
    ]),
    dict(scene="outro", text=[
        "So what do you think happened that night?",
        "Was it really the snow, or is there something we are still missing? Tell me in the comments.",
        "And if you like unsolved mysteries, subscribe. Next time, we look at a case that even modern science cannot explain.",
    ]),
]

SHORT = [
    dict(scene="tent_night", text=[
        "In 1959, a search team found this tent on a frozen mountain in Russia.",
        "It had been cut open... from the inside.",
    ]),
    dict(scene="footprints", text=[
        "Footprints led down the slope. Nine hikers, at -30°C, most of them in socks.",
    ]),
    dict(scene="cedar", text=[
        "Two were found by a cedar tree, in their underwear.",
        "Three more died trying to climb back to the tent.",
    ]),
    dict(scene="injuries", text=[
        "The last four turned up months later, with crushed chests and skull fractures, but almost no external wounds.",
    ]),
    dict(scene="classified", text=[
        "The Soviets blamed a compelling natural force, and classified the files.",
    ]),
    dict(scene="slab", args=dict(mode="build"), text=[
        "In 2021, scientists finally modeled it.",
        "A small slab of snow broke loose hours after they cut into the slope, and crushed the tent in the dark.",
    ]),
    dict(scene="outro", args=dict(short=True), text=[
        "Would you have run? The full story is on the channel.",
    ]),
]
