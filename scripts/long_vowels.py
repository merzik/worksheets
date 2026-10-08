#!/usr/bin/env python3
"""Build mixed silent-e long-vowel worksheets.

Same five sections and page layout as the CVC packet. Each worksheet mixes
long a, i, o, and u (cake, bike, rose, flute).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phonics_mix as mix

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reading" / "long-vowels"
IMAGE_DIR = OUT_DIR / "images"
STUDENT_PDF = OUT_DIR / "long-vowels-mixed.pdf"
ANSWER_KEY_PDF = OUT_DIR / "long-vowels-mixed-answer-key.pdf"

SEED = 20261009
WORKSHEETS = 30
TITLE = "Long Vowels"

NOT_LONG = {
    "are", "were", "where", "there", "come", "some", "done", "gone",
    "love", "dove", "none", "have", "give", "live", "move", "prove",
    "one", "once", "sure", "eye",
}


def pattern(word):
    if word in NOT_LONG or not word.isalpha() or not word.islower():
        return None
    vowels = "aeiou"
    if word[-1] != "e":
        return None
    body = word[:-1]
    if not body or body[-1] in vowels:
        return None
    first = None
    for ch in body:
        if ch in vowels:
            first = ch
            break
        if ch not in "abcdefghijklmnopqrstuvwxyz":
            return None
    if first is None:
        return None
    after = body[body.index(first) + 1 :]
    if not after or any(ch in vowels for ch in after):
        return None
    return f"{first}_e"


def rime(word):
    if pattern(word) is None:
        return None
    return word[-3:]


def load_picture_words():
    words = []
    for path in sorted(IMAGE_DIR.glob("*.png")):
        if pattern(path.stem) is None:
            raise RuntimeError(f"Clipart is not a silent-e word: {path.name}")
        words.append(path.stem)
    if len(words) < mix.SPELL_COUNT + mix.UNSCRAMBLE_COUNT:
        raise RuntimeError(f"Need more silent-e pictures in {IMAGE_DIR}")
    return tuple(words)


PICTURE_WORDS = load_picture_words()

MINIMAL_PAIRS = (
    ("cake", "cape", "We ate the ___."),
    ("bike", "hike", "She rode her ___."),
    ("kite", "kit", "Fly the ___ in the sky."),
    ("bone", "bun", "The dog chewed a ___."),
    ("rose", "rope", "He held a red ___."),
    ("nose", "note", "Cover your ___ and sneeze."),
    ("note", "not", "Play the high ___."),
    ("phone", "cone", "Call Mom on the ___."),
    ("snake", "snack", "A ___ slid past the rock."),
    ("whale", "while", "The ___ is huge."),
    ("grape", "grip", "Pick a purple ___."),
    ("plane", "plan", "The ___ took off."),
    ("skate", "skit", "I can ___ on the ice."),
    ("wave", "save", "The ___ hit the sand."),
    ("game", "name", "We played a fun ___."),
    ("rake", "rack", "Get the ___ for the leaves."),
    ("tape", "tap", "Use ___ to hang the art."),
    ("vase", "case", "Put the rose in the ___."),
    ("stove", "store", "The pot is on the ___."),
    ("cube", "cub", "Six sides make a ___."),
    ("flute", "flat", "She plays a ___."),
    ("fire", "file", "The ___ is hot."),
    ("five", "fine", "I see ___ ducks."),
    ("nine", "line", "Count up to ___."),
    ("mice", "rice", "Three ___ ran to a hole."),
    ("dice", "dish", "Roll the ___."),
    ("slide", "sled", "Go down the ___."),
    ("hive", "have", "Bees live in a ___."),
    ("tire", "tile", "The car needs a new ___."),
    ("home", "hum", "I went ___ after school."),
    ("lake", "like", "We swam in the ___."),
    ("gate", "got", "Shut the ___."),
    ("mule", "mole", "The ___ carried the bags."),
    ("tune", "ton", "Hum a happy ___."),
    ("rule", "rail", "Follow the class ___."),
    ("june", "junk", "___ is a warm month."),
    ("cute", "cut", "The pup is ___."),
    ("huge", "hug", "The whale is ___."),
    ("shape", "ship", "A heart is a ___."),
    ("prize", "price", "She won a ___."),
    ("smile", "mile", "Give me a big ___."),
    ("ride", "rid", "We will ___ our bikes."),
    ("time", "tame", "What ___ is it?"),
    ("pipe", "pip", "Water runs in the ___."),
    ("rope", "rip", "Hold the ___ and climb."),
    ("cone", "can", "The ice cream is in a ___."),
    ("stone", "stand", "He sat on a big ___."),
    ("globe", "glad", "Spin the ___."),
    ("page", "peg", "Turn the ___."),
    ("safe", "save", "The cash is in a ___."),
    ("bake", "back", "We will ___ bread."),
    ("late", "let", "Do not be ___."),
    ("hole", "hall", "The mole dug a ___."),
    ("joke", "jack", "He told a ___."),
    ("hope", "hop", "I ___ we can play."),
    ("these", "this", "___ pens are blue."),
    ("close", "class", "Please ___ the door."),
    ("broke", "break", "The cup ___ when it fell."),
    ("drove", "drip", "Dad ___ the car home."),
    ("store", "star", "We shop at the ___."),
    ("more", "moon", "I want ___ cake."),
    ("place", "plain", "This is a good ___ to sit."),
    ("space", "spice", "The ship flew into ___."),
    ("white", "what", "The snow is ___."),
    ("bride", "braid", "The ___ wore a white dress."),
    ("wipe", "whip", "___ the desk."),
    ("hide", "hid", "___ behind the tree."),
    ("size", "sit", "What ___ hat do you need?"),
    ("dime", "dim", "I found one ___."),
    ("life", "lift", "A bug has a short ___."),
    ("use", "us", "___ a pencil."),
    ("tube", "tub", "Paste comes in a ___."),
)

RHYME_PAIRS = (
    ("cake", "make"),
    ("bake", "lake"),
    ("rake", "take"),
    ("snake", "wake"),
    ("game", "name"),
    ("same", "tame"),
    ("tape", "cape"),
    ("grape", "shape"),
    ("bike", "hike"),
    ("like", "spike"),
    ("kite", "bite"),
    ("white", "site"),
    ("five", "dive"),
    ("drive", "hive"),
    ("nine", "line"),
    ("mine", "pine"),
    ("fine", "dine"),
    ("mice", "rice"),
    ("dice", "nice"),
    ("fire", "tire"),
    ("wire", "hire"),
    ("slide", "ride"),
    ("hide", "side"),
    ("wide", "glide"),
    ("bone", "cone"),
    ("stone", "phone"),
    ("nose", "rose"),
    ("hose", "those"),
    ("note", "vote"),
    ("hole", "pole"),
    ("mole", "sole"),
    ("home", "dome"),
    ("robe", "globe"),
    ("hope", "rope"),
    ("joke", "poke"),
    ("cube", "tube"),
    ("flute", "cute"),
    ("mule", "rule"),
    ("tune", "june"),
    ("dune", "prune"),
    ("wave", "save"),
    ("cave", "gave"),
    ("plane", "cane"),
    ("lane", "mane"),
    ("gate", "late"),
    ("date", "rate"),
    ("vase", "case"),
    ("race", "face"),
    ("place", "space"),
    ("trace", "brace"),
    ("page", "cage"),
    ("stage", "age"),
    ("shade", "grade"),
    ("made", "wade"),
    ("skate", "plate"),
    ("state", "crate"),
    ("whale", "scale"),
    ("pale", "tale"),
    ("frame", "flame"),
    ("prize", "size"),
    ("time", "lime"),
    ("dime", "chime"),
    ("pipe", "ripe"),
    ("wipe", "gripe"),
    ("stove", "drove"),
    ("close", "rose"),
    ("broke", "spoke"),
    ("code", "rode"),
    ("eve", "steve"),
    ("theme", "scheme"),
    ("here", "mere"),
    ("care", "share"),
    ("more", "store"),
    ("score", "shore"),
    ("smile", "while"),
    ("bride", "glide"),
)

EXTRA_WORDS = (
    "make", "lake", "take", "wake", "same", "tame", "cape", "shape",
    "hike", "like", "spike", "bite", "site", "dive", "drive", "line",
    "mine", "pine", "fine", "dine", "rice", "nice", "wire", "hire",
    "ride", "side", "wide", "glide", "cone", "hose", "those", "vote",
    "pole", "sole", "dome", "robe", "poke", "tube", "cute", "rule",
    "june", "dune", "prune", "save", "cave", "gave", "cane", "lane",
    "mane", "late", "date", "rate", "case", "race", "face", "place",
    "space", "trace", "brace", "cage", "stage", "shade", "grade",
    "made", "wade", "plate", "state", "crate", "scale", "pale", "tale",
    "frame", "flame", "size", "lime", "chime", "ripe", "wipe", "drove",
    "spoke", "code", "rode", "eve", "theme", "scheme", "mere", "care",
    "share", "store", "score", "shore", "while", "home", "safe", "page",
    "bake", "hope", "joke", "tune", "mule", "huge", "use", "hide",
    "time", "dime", "pipe", "rope", "stone", "globe", "smile", "prize",
    "white", "bride", "life", "chore", "broke", "close", "more",
)


def main():
    mix.check_pairs(MINIMAL_PAIRS, RHYME_PAIRS, EXTRA_WORDS, pattern, rime)
    for word in PICTURE_WORDS:
        if pattern(word) is None:
            raise RuntimeError(word)
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
    print("Picture uses by vowel:", dict(sorted(kinds.items())))


if __name__ == "__main__":
    main()
