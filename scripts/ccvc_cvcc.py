#!/usr/bin/env python3
"""Build mixed CCVC and CVCC worksheets.

Same five sections and page layout as the CVC packet, with four-letter
words. Each worksheet mixes consonant-consonant-vowel-consonant words
(frog, stop) and consonant-vowel-consonant-consonant words (milk, nest).
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cvc_short_vowels as base

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reading" / "short-vowels"
IMAGE_DIR = OUT_DIR / "images"
STUDENT_PDF = OUT_DIR / "ccvc-cvcc-mixed.pdf"
ANSWER_KEY_PDF = OUT_DIR / "ccvc-cvcc-mixed-answer-key.pdf"

SEED = 20261008
WORKSHEETS = 30
TITLE = "CCVC and CVCC"

SPELL_COUNT = 6
UNSCRAMBLE_COUNT = 8
MINIMAL_COUNT = 5
CODE_COUNT = 10
RHYME_COUNT = 5

VOWELS = set("aeiou")
SYMBOLS = base.SYMBOL_NAMES + ("bolt", "wave", "dots", "check")


def pattern(word):
    if len(word) != 4 or any(ch not in "abcdefghijklmnopqrstuvwxyz" for ch in word):
        return None
    cons = [ch not in VOWELS for ch in word]
    if cons[0] and cons[1] and not cons[2] and cons[3]:
        return "ccvc"
    if cons[0] and not cons[1] and cons[2] and cons[3]:
        return "cvcc"
    return None


def load_picture_words():
    words = []
    for path in sorted(IMAGE_DIR.glob("*.png")):
        kind = pattern(path.stem)
        if kind is None:
            continue
        words.append(path.stem)
    ccvc = sum(1 for w in words if pattern(w) == "ccvc")
    cvcc = sum(1 for w in words if pattern(w) == "cvcc")
    need = max(SPELL_COUNT, UNSCRAMBLE_COUNT) // 2 + 1
    if ccvc < need or cvcc < need:
        raise RuntimeError(f"Need more pictures of each pattern (ccvc={ccvc}, cvcc={cvcc})")
    return tuple(words)


PICTURE_WORDS = load_picture_words()

# (answer, distractor, sentence). The sentence forces the answer.
MINIMAL_PAIRS = (
    ("frog", "from", "A ___ can hop and swim."),
    ("stop", "step", "___ when the sign is red."),
    ("clap", "clip", "We ___ our hands for the song."),
    ("crab", "grab", "The ___ has two big claws."),
    ("flag", "flat", "Wave the red ___."),
    ("sled", "slid", "Ride the ___ on the snow."),
    ("swim", "slim", "Fish ___ in the pond."),
    ("plug", "plum", "Put the ___ in the wall."),
    ("drop", "drip", "One ___ of rain fell."),
    ("trap", "trip", "The mouse ran into the ___."),
    ("crib", "crab", "The baby sleeps in a ___."),
    ("plum", "plug", "Eat the sweet purple ___."),
    ("clip", "clap", "Hold the papers with a ___."),
    ("milk", "silk", "Pour the ___ into a glass."),
    ("gift", "lift", "Open the ___ in the box."),
    ("fist", "fish", "He made a tight ___."),
    ("fish", "fist", "The ___ swam in the lake."),
    ("hand", "sand", "Wave your ___ hello."),
    ("mask", "task", "Wear a ___ on your face."),
    ("tent", "dent", "We slept in a ___."),
    ("wind", "wand", "The ___ blew the leaves."),
    ("wolf", "golf", "The gray ___ howled."),
    ("duck", "dock", "The ___ says quack."),
    ("lock", "rock", "Turn the key in the ___."),
    ("sock", "rock", "Put a ___ on your foot."),
    ("rock", "sock", "Pick up the gray ___."),
    ("ship", "shop", "The big ___ sails away."),
    ("bath", "path", "I take a warm ___."),
    ("bell", "belt", "Ring the ___ at noon."),
    ("golf", "gulf", "He hit the ___ ball."),
    ("nest", "rest", "The bird sits in a ___."),
    ("belt", "bell", "Buckle your ___."),
    ("bulb", "bulk", "Change the light ___."),
    ("ring", "wing", "She wore a gold ___."),
    ("sand", "hand", "We played in the ___."),
    ("jump", "bump", "___ over the log."),
    ("camp", "damp", "We set up ___ by the lake."),
    ("best", "nest", "This is the ___ one."),
    ("must", "dust", "You ___ stop and look."),
)

RHYME_PAIRS = (
    ("stop", "drop"),
    ("clap", "flap"),
    ("clip", "slip"),
    ("trap", "snap"),
    ("swim", "trim"),
    ("flag", "brag"),
    ("plug", "slug"),
    ("crab", "grab"),
    ("spin", "grin"),
    ("skip", "flip"),
    ("spot", "trot"),
    ("step", "prep"),
    ("drip", "trip"),
    ("slim", "trim"),
    ("flap", "slap"),
    ("lamp", "camp"),
    ("nest", "rest"),
    ("jump", "bump"),
    ("belt", "melt"),
    ("hand", "sand"),
    ("tent", "went"),
    ("gift", "lift"),
    ("fist", "list"),
    ("sink", "wink"),
    ("bank", "tank"),
    ("duck", "luck"),
    ("lock", "rock"),
    ("sock", "dock"),
    ("fish", "wish"),
    ("ship", "chip"),
    ("bath", "math"),
    ("ring", "sing"),
    ("bell", "well"),
    ("milk", "silk"),
    ("fast", "last"),
    ("just", "must"),
    ("lost", "cost"),
    ("soft", "loft"),
    ("help", "yelp"),
    ("pond", "bond"),
    ("pink", "link"),
    ("mint", "hint"),
    ("dump", "lump"),
    ("land", "band"),
    ("best", "test"),
    ("dust", "rust"),
    ("wing", "king"),
    ("path", "math"),
    ("shop", "chop"),
    ("sent", "bent"),
    ("wish", "dish"),
    ("mask", "task"),
    ("left", "heft"),
    ("bend", "send"),
)

EXTRA_WORDS = (
    "brim", "grim", "plan", "clan", "plot", "slot", "snug", "slug",
    "crop", "trot", "grin", "flip", "brag", "grab", "snap", "trim",
    "flap", "slap", "slip", "drip", "trip", "skip", "spin", "spot",
    "step", "prep", "slim", "swam", "from", "flat", "slid", "grit",
    "camp", "damp", "ramp", "rest", "west", "test", "best", "bump",
    "dump", "lump", "melt", "felt", "sand", "land", "band", "went",
    "sent", "bent", "dent", "lift", "list", "mist", "wink", "link",
    "pink", "tank", "rank", "luck", "tuck", "dock", "wish", "dish",
    "chip", "whip", "shop", "chop", "path", "math", "wing", "sing",
    "king", "well", "tell", "silk", "gulf", "fast", "last", "past",
    "just", "must", "dust", "rust", "lost", "cost", "soft", "loft",
    "help", "yelp", "pond", "bond", "hint", "mint", "hunt", "bunt",
    "send", "bend", "heft", "left", "vest", "bulk", "task", "wand",
    "golf", "wolf", "sock", "rock", "lock", "duck", "fish", "ship",
)


def rime(word):
    kind = pattern(word)
    if kind == "ccvc":
        return word[2:]
    if kind == "cvcc":
        return word[1:]
    return None


def check_data():
    for answer, distractor, sentence in MINIMAL_PAIRS:
        if pattern(answer) is None or pattern(distractor) is None:
            raise RuntimeError(f"Minimal pair is not CCVC/CVCC: {answer}/{distractor}")
        if answer == distractor:
            raise RuntimeError(f"Minimal pair words match: {answer}")
        if "___" not in sentence:
            raise RuntimeError(f"Sentence has no blank: {sentence}")
    for a, b in RHYME_PAIRS:
        if pattern(a) is None or pattern(b) is None:
            raise RuntimeError(f"Rhyme pair is not CCVC/CVCC: {a}/{b}")
        if rime(a) != rime(b) or a == b:
            raise RuntimeError(f"Not a rhyme: {a}/{b}")
    for word in EXTRA_WORDS:
        if pattern(word) is None:
            raise RuntimeError(f"Extra word is not CCVC/CVCC: {word}")


check_data()

TEXT_WORDS = sorted(
    set(PICTURE_WORDS)
    | {a for a, _b, _s in MINIMAL_PAIRS}
    | {b for _a, b, _s in MINIMAL_PAIRS}
    | {a for a, b in RHYME_PAIRS}
    | {b for a, b in RHYME_PAIRS}
    | set(EXTRA_WORDS)
)


def take_mixed(rng, pool, count, used, usage):
    groups = {
        "ccvc": [w for w in pool if pattern(w) == "ccvc"],
        "cvcc": [w for w in pool if pattern(w) == "cvcc"],
    }
    n_ccvc = count // 2
    n_cvcc = count - n_ccvc
    free_ccvc = [w for w in groups["ccvc"] if w not in used]
    free_cvcc = [w for w in groups["cvcc"] if w not in used]
    if len(free_ccvc) < n_ccvc or len(free_cvcc) < n_cvcc:
        raise RuntimeError("Not enough unused CCVC and CVCC words")
    chosen = base.take_least_used(rng, groups["ccvc"], n_ccvc, used, usage)
    chosen += base.take_least_used(rng, groups["cvcc"], n_cvcc, used, usage)
    rng.shuffle(chosen)
    return chosen


def take_labeled(rng, items, count, used, usage, label):
    """Pick `count` records, mixing CCVC and CVCC answers."""
    def words_of(item):
        if label == "minimal":
            return (item[0], item[1])
        return item

    def usage_key(item):
        a, b = words_of(item)[:2]
        return f"{a}|{b}"

    ranked = sorted(items, key=lambda item: (usage[usage_key(item)], rng.random()))
    picked = []

    def grab(allow_used, want):
        for item in ranked:
            if item in picked:
                continue
            a, b = words_of(item)[:2]
            if pattern(a) != want:
                continue
            if not allow_used and (a in used or b in used):
                continue
            picked.append(item)
            usage[usage_key(item)] += 1
            used.add(a)
            used.add(b)
            return True
        return False

    for allow_used in (False, True):
        wants = ["ccvc", "cvcc", "ccvc", "cvcc", "ccvc", "cvcc"]
        for want in wants:
            if len(picked) == count:
                return picked
            grab(allow_used, want)
        if len(picked) == count:
            return picked
    if len(picked) < count:
        raise RuntimeError(f"Not enough {label} items")
    return picked


def pick_code_words(rng, pool, count):
    ccvc = [w for w in pool if pattern(w) == "ccvc"]
    cvcc = [w for w in pool if pattern(w) == "cvcc"]
    half = count // 2
    for _ in range(400):
        if len(ccvc) < half or len(cvcc) < count - half:
            break
        candidate = rng.sample(ccvc, half) + rng.sample(cvcc, count - half)
        if len(set("".join(candidate))) <= len(SYMBOLS):
            rng.shuffle(candidate)
            return candidate
    for _ in range(200):
        candidate = rng.sample(list(pool), count)
        if len(set("".join(candidate))) <= len(SYMBOLS):
            return candidate
    chosen = []
    letters = set()
    shuffled = list(pool)
    rng.shuffle(shuffled)
    for word in shuffled:
        nxt = letters | set(word)
        if len(nxt) <= len(SYMBOLS):
            chosen.append(word)
            letters = nxt
        if len(chosen) == count:
            return chosen
    raise RuntimeError("Could not build a code-breaker set")


def build_worksheet(rng, picture_usage, rhyme_usage, minimal_usage):
    used = set()
    spell = take_mixed(rng, PICTURE_WORDS, SPELL_COUNT, used, picture_usage)
    unscramble_words = take_mixed(
        rng, PICTURE_WORDS, UNSCRAMBLE_COUNT, used, picture_usage
    )
    unscramble = [
        {"word": w, "scrambled": base.scramble_word(rng, w)} for w in unscramble_words
    ]

    minimal_raw = take_labeled(
        rng, MINIMAL_PAIRS, MINIMAL_COUNT, used, minimal_usage, "minimal"
    )
    minimal = []
    for answer, distractor, sentence in minimal_raw:
        choices = [answer, distractor]
        rng.shuffle(choices)
        minimal.append(
            {
                "answer": answer,
                "distractor": distractor,
                "sentence": sentence,
                "choices": choices,
            }
        )

    code_pool = [w for w in TEXT_WORDS if w not in used]
    if len(code_pool) < CODE_COUNT:
        code_pool = list(TEXT_WORDS)
    code_words = pick_code_words(rng, code_pool, CODE_COUNT)
    used.update(code_words)
    letters_needed = sorted(set("".join(code_words)))
    symbols = list(SYMBOLS)
    rng.shuffle(symbols)
    legend = {letter: symbols[i] for i, letter in enumerate(letters_needed)}
    code = {
        "legend": legend,
        "words": [
            {"word": w, "symbols": [legend[ch] for ch in w]} for w in code_words
        ],
    }

    rhyme_raw = take_labeled(
        rng, RHYME_PAIRS, RHYME_COUNT, used, rhyme_usage, "rhyme"
    )
    left = [a for a, _b in rhyme_raw]
    right = [b for _a, b in rhyme_raw]
    rng.shuffle(right)
    if right == [b for _a, b in rhyme_raw] and RHYME_COUNT > 1:
        right[0], right[1] = right[1], right[0]
    rhyme = {"left": left, "right": right, "pairs": list(rhyme_raw)}
    return {
        "spell": spell,
        "unscramble": unscramble,
        "minimal": minimal,
        "code": code,
        "rhyme": rhyme,
    }


def build_packet():
    rng = random.Random(SEED)
    picture_usage = Counter()
    rhyme_usage = Counter()
    minimal_usage = Counter()
    worksheets = [
        build_worksheet(rng, picture_usage, rhyme_usage, minimal_usage)
        for _ in range(WORKSHEETS)
    ]
    return worksheets, picture_usage


def main():
    base.IMAGE_DIR = IMAGE_DIR
    base._IMAGE_CACHE.clear()
    worksheets, picture_usage = build_packet()
    # Both patterns show up in the picture sections of every worksheet.
    for index, ws in enumerate(worksheets, start=1):
        for key in ("spell", "unscramble"):
            words = ws[key] if key == "spell" else [item["word"] for item in ws[key]]
            kinds = {pattern(w) for w in words}
            if kinds != {"ccvc", "cvcc"}:
                raise RuntimeError(f"Worksheet {index} {key} is not mixed: {kinds}")
        if len(ws["code"]["words"]) != CODE_COUNT:
            raise RuntimeError(f"Worksheet {index} code count is wrong")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base.write_student_packet(STUDENT_PDF, worksheets, title=TITLE)
    base.write_answer_key(
        ANSWER_KEY_PDF, worksheets, title="CCVC and CVCC - Answer Key"
    )
    uses = sorted(picture_usage.values())
    print(f"Wrote {STUDENT_PDF} ({WORKSHEETS} worksheets, {WORKSHEETS * 2} pages)")
    print(f"Wrote {ANSWER_KEY_PDF}")
    print(
        f"Picture bank: {len(PICTURE_WORDS)} words; "
        f"uses per word min={uses[0]} max={uses[-1]}"
    )


if __name__ == "__main__":
    main()
