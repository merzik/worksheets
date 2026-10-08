#!/usr/bin/env python3
"""Build mixed vowel-team worksheets.

Same five sections and page layout as the CVC packet. Each worksheet mixes
teams such as ai, ay, ea, ee, ie, oa, ow, oo, ue, and ui
(rain, crayon, beach, tree, pie, boat, snow, moon, blue, juice).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phonics_mix as mix

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reading" / "vowel-teams"
IMAGE_DIR = OUT_DIR / "images"
STUDENT_PDF = OUT_DIR / "vowel-teams-mixed.pdf"
ANSWER_KEY_PDF = OUT_DIR / "vowel-teams-mixed-answer-key.pdf"

SEED = 20261010
WORKSHEETS = 30
TITLE = "Vowel Teams"

TEAMS = ("ai", "ay", "ea", "ee", "ie", "oa", "oe", "ow", "ue", "ui", "oo")

# Spellings that are not the long-vowel team we are teaching.
NOT_TEAM = {
    "bread", "head", "dead", "lead", "read", "deaf", "meant", "spread",
    "steak", "break", "great", "bear", "wear", "pear", "swear",
    "said", "again", "against", "says",
    "friend", "chief", "thief", "field", "brief", "piece", "niece",
    "build", "built", "guide", "guilt", "guess", "guest",
    "book", "look", "cook", "foot", "good", "wood", "hook", "took",
    "wool", "hood", "stood", "blood", "flood", "floor", "door", "poor",
    "cow", "now", "how", "owl", "down", "town", "clown", "brown", "crown",
    "gown", "frown", "growl", "howl", "flower", "tower", "power", "shower",
    "shoe", "does",
}


def _hits(word):
    found = []
    for team in TEAMS:
        start = 0
        while True:
            index = word.find(team, start)
            if index < 0:
                break
            if team in ("ue", "ui") and index > 0 and word[index - 1] == "q":
                start = index + 1
                continue
            found.append((index, team))
            start = index + 1
    return found


def pattern(word):
    if word in NOT_TEAM or not word.isalpha() or not word.islower():
        return None
    found = _hits(word)
    if not found:
        return None
    found.sort()
    return found[-1][1]


def rime(word):
    if pattern(word) is None:
        return None
    found = _hits(word)
    found.sort()
    return word[found[-1][0] :]


def load_picture_words():
    words = []
    for path in sorted(IMAGE_DIR.glob("*.png")):
        if pattern(path.stem) is None:
            raise RuntimeError(f"Clipart is not a vowel-team word: {path.name}")
        words.append(path.stem)
    if len(words) < mix.SPELL_COUNT + mix.UNSCRAMBLE_COUNT:
        raise RuntimeError(f"Need more vowel-team pictures in {IMAGE_DIR}")
    return tuple(words)


PICTURE_WORDS = load_picture_words()

MINIMAL_PAIRS = (
    ("rain", "ran", "The ___ made the grass wet."),
    ("train", "truck", "We rode the ___."),
    ("mail", "mall", "The letter came in the ___."),
    ("snail", "snake", "The ___ is very slow."),
    ("chain", "chin", "The ___ is made of steel."),
    ("nail", "name", "Hit the ___ with the hammer."),
    ("paint", "pant", "___ the fence red."),
    ("tail", "tall", "The dog wagged its ___."),
    ("sail", "seal", "The ___ is up on the boat."),
    ("wait", "wet", "___ for me at the door."),
    ("day", "den", "It is a sunny ___."),
    ("play", "plan", "The kids ___ at the park."),
    ("stay", "step", "___ in your seat."),
    ("tray", "try", "Set the cups on the ___."),
    ("hay", "hat", "The horse ate the ___."),
    ("clay", "clap", "Make a pot from ___."),
    ("gray", "grab", "The clouds look ___."),
    ("way", "why", "Which ___ do we go?"),
    ("pay", "pat", "I will ___ for the book."),
    ("say", "sad", "What did she ___?"),
    ("crayon", "crown", "Color it with a ___."),
    ("bee", "bug", "A ___ sat on the rose."),
    ("tree", "three", "Climb the tall ___."),
    ("three", "tree", "I see ___ pigs."),
    ("sheep", "ship", "The ___ has thick wool."),
    ("feet", "fit", "My ___ got wet."),
    ("cheese", "chess", "The mouse ate the ___."),
    ("deer", "door", "A ___ ran past the tree."),
    ("green", "grin", "The grass is ___."),
    ("wheel", "while", "The ___ can spin."),
    ("sleep", "slip", "I ___ in a soft bed."),
    ("seed", "sad", "Plant a ___ in the pot."),
    ("queen", "quick", "The ___ wore a crown."),
    ("sweet", "sweat", "The cake is ___."),
    ("street", "start", "We live on this ___."),
    ("keep", "kept", "___ the dime in a safe."),
    ("see", "set", "I can ___ the moon."),
    ("leaf", "loaf", "A ___ fell off the tree."),
    ("beach", "bench", "We play in the sand at the ___."),
    ("peach", "pitch", "Eat the ripe ___."),
    ("tea", "tie", "Sip the hot ___."),
    ("seal", "sell", "A ___ can swim and bark."),
    ("heat", "hat", "I feel the ___ of the sun."),
    ("team", "tame", "Our ___ won the game."),
    ("bean", "bin", "The green ___ is in the pot."),
    ("clean", "clan", "Please ___ your desk."),
    ("dream", "drum", "I had a funny ___."),
    ("cream", "cram", "Ice ___ is cold."),
    ("speak", "spike", "Please ___ up."),
    ("eat", "ate", "We ___ lunch at noon."),
    ("seat", "set", "Please sit in this ___."),
    ("boat", "boot", "The ___ floats on the lake."),
    ("goat", "got", "The ___ ate the hay."),
    ("coat", "cat", "Zip up your ___."),
    ("soap", "soup", "Wash with ___."),
    ("road", "rod", "The ___ goes to town."),
    ("toad", "told", "A ___ sat on a log."),
    ("toast", "toss", "I ate ___ with jam."),
    ("float", "flat", "A boat can ___."),
    ("snow", "snap", "White ___ fell all night."),
    ("blow", "blue", "___ out the candle."),
    ("grow", "gray", "Plants ___ in the sun."),
    ("show", "shoe", "___ me your drawing."),
    ("slow", "slip", "A turtle is ___."),
    ("crow", "cry", "A black ___ sat in the tree."),
    ("bowl", "ball", "The soup is in a ___."),
    ("row", "raw", "We will ___ the boat."),
    ("low", "law", "The swing is too ___."),
    ("yellow", "yell", "The sun looks ___."),
    ("arrow", "arm", "Shoot the ___."),
    ("rainbow", "rain", "A ___ is in the sky."),
    ("moon", "man", "The ___ is full tonight."),
    ("boot", "boat", "He lost one ___."),
    ("spoon", "spin", "Eat soup with a ___."),
    ("broom", "brim", "Sweep with the ___."),
    ("tooth", "tool", "The dentist looked at my ___."),
    ("school", "scale", "I learn at ___."),
    ("pool", "pull", "We swim in the ___."),
    ("room", "ram", "My bed is in my ___."),
    ("roof", "root", "The ___ keeps the rain out."),
    ("tool", "tall", "A hammer is a ___."),
    ("zoo", "zip", "We saw a lion at the ___."),
    ("food", "foot", "We need ___ to eat."),
    ("cool", "coal", "The water is ___."),
    ("noon", "none", "We eat lunch at ___."),
    ("soon", "sun", "We will leave ___."),
    ("balloon", "ball", "Hold the red ___."),
    ("pie", "pay", "I want a slice of ___."),
    ("tie", "tea", "He wore a red ___."),
    ("blue", "blow", "The sky is ___."),
    ("glue", "glow", "Stick it with ___."),
    ("clue", "claw", "We found a ___."),
    ("true", "tree", "The story is ___."),
    ("juice", "just", "Pour the ___."),
    ("fruit", "front", "An apple is a ___."),
    ("suit", "sit", "He wore a blue ___."),
    ("toe", "top", "I stubbed my ___."),
)

RHYME_PAIRS = (
    ("rain", "train"),
    ("chain", "main"),
    ("gain", "pain"),
    ("mail", "snail"),
    ("tail", "nail"),
    ("sail", "pail"),
    ("wait", "bait"),
    ("paint", "faint"),
    ("day", "play"),
    ("stay", "clay"),
    ("tray", "hay"),
    ("way", "say"),
    ("gray", "may"),
    ("pay", "day"),
    ("bee", "tree"),
    ("see", "free"),
    ("three", "knee"),
    ("sheep", "jeep"),
    ("keep", "deep"),
    ("sleep", "beep"),
    ("feet", "sweet"),
    ("sheet", "street"),
    ("deer", "cheer"),
    ("wheel", "feel"),
    ("heel", "peel"),
    ("green", "queen"),
    ("seen", "green"),
    ("seed", "need"),
    ("feed", "weed"),
    ("beach", "peach"),
    ("teach", "reach"),
    ("tea", "sea"),
    ("pea", "tea"),
    ("meat", "seat"),
    ("heat", "neat"),
    ("beat", "wheat"),
    ("seal", "meal"),
    ("real", "deal"),
    ("team", "dream"),
    ("beam", "steam"),
    ("bean", "lean"),
    ("mean", "clean"),
    ("speak", "weak"),
    ("eat", "beat"),
    ("boat", "goat"),
    ("coat", "float"),
    ("throat", "boat"),
    ("road", "toad"),
    ("load", "road"),
    ("snow", "blow"),
    ("grow", "show"),
    ("slow", "crow"),
    ("know", "throw"),
    ("low", "row"),
    ("yellow", "pillow"),
    ("arrow", "rainbow"),
    ("own", "shown"),
    ("moon", "spoon"),
    ("soon", "noon"),
    ("balloon", "moon"),
    ("boot", "root"),
    ("hoot", "boot"),
    ("broom", "room"),
    ("tooth", "booth"),
    ("school", "pool"),
    ("tool", "cool"),
    ("food", "mood"),
    ("zoo", "moo"),
    ("pie", "tie"),
    ("cried", "fried"),
    ("dried", "tried"),
    ("blue", "glue"),
    ("true", "clue"),
    ("due", "blue"),
    ("fruit", "suit"),
    ("toe", "hoe"),
    ("doe", "toe"),
)

EXTRA_WORDS = (
    "main", "gain", "pain", "tail", "sail", "pail", "fail", "wait", "bait",
    "faint", "day", "play", "stay", "clay", "tray", "hay", "way", "say",
    "gray", "may", "pay", "see", "free", "knee", "jeep", "keep", "deep",
    "beep", "sleep", "sweet", "sheet", "street", "cheer", "feel", "heel",
    "peel", "queen", "seen", "need", "feed", "weed", "teach", "reach",
    "sea", "pea", "meat", "seat", "heat", "neat", "beat", "wheat", "meal",
    "real", "deal", "dream", "beam", "steam", "bean", "lean", "mean",
    "clean", "speak", "weak", "eat", "float", "throat", "toad", "load",
    "blow", "grow", "show", "slow", "crow", "know", "throw", "low", "row",
    "pillow", "own", "shown", "soon", "noon", "root", "hoot", "room",
    "booth", "pool", "tool", "cool", "food", "mood", "zoo", "moo", "cried",
    "fried", "dried", "tried", "true", "clue", "due", "fruit", "suit",
    "toe", "hoe", "doe", "sheep", "seed", "tea", "team", "toast", "bowl",
    "cream", "queen", "sweet", "street", "sleep", "keep", "see", "pay",
    "say", "way", "hay", "tray", "clay", "stay", "play", "day", "tail",
    "sail", "wait", "chain", "train", "rain", "green", "three", "tree",
    "feet", "deer", "beach", "peach", "leaf", "boat", "goat", "coat",
    "road", "snow", "moon", "spoon", "boot", "broom", "tooth", "school",
    "pie", "tie", "blue", "glue", "juice",
)


def main():
    mix.check_pairs(MINIMAL_PAIRS, RHYME_PAIRS, EXTRA_WORDS, pattern, rime)
    words = mix.text_pool(
        PICTURE_WORDS, MINIMAL_PAIRS, RHYME_PAIRS, EXTRA_WORDS, pattern
    )
    worksheets, picture_usage = mix.build_packet(
        SEED,
        PICTURE_WORDS,
        MINIMAL_PAIRS,
        RHYME_PAIRS,
        words,
        pattern,
        WORKSHEETS,
    )
    mix.write_packet(STUDENT_PDF, ANSWER_KEY_PDF, worksheets, TITLE, IMAGE_DIR)
    uses = sorted(picture_usage.values())
    kinds = Counter()
    for ws in worksheets:
        for word in ws["spell"]:
            kinds[pattern(word)] += 1
        for item in ws["unscramble"]:
            kinds[pattern(item["word"])] += 1
    print(f"Wrote {STUDENT_PDF} ({WORKSHEETS} worksheets, {WORKSHEETS * 2} pages)")
    print(f"Wrote {ANSWER_KEY_PDF}")
    print(
        f"Picture bank: {len(PICTURE_WORDS)} words; "
        f"uses per word min={uses[0]} max={uses[-1]}"
    )
    print("Picture uses by team:", dict(sorted(kinds.items())))


if __name__ == "__main__":
    main()
