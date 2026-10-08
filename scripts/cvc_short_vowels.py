#!/usr/bin/env python3
"""Build mixed short-vowel CVC worksheets.

Each worksheet is two pages with five sections: spell from picture,
unscramble, minimal-pair sentences, code breakers, and rhyme match.
Pictures are PNG clipart in reading/short-vowels/images/.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reading" / "short-vowels"
IMAGE_DIR = OUT_DIR / "images"
STUDENT_PDF = OUT_DIR / "cvc-mixed.pdf"
ANSWER_KEY_PDF = OUT_DIR / "cvc-mixed-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 36
RIGHT = 36
SEED = 20261007
WORKSHEETS = 30
PAGES_PER_WORKSHEET = 2

SPELL_COUNT = 6
UNSCRAMBLE_COUNT = 8
MINIMAL_COUNT = 5
CODE_COUNT = 10
RHYME_COUNT = 5


def load_picture_words():
    words = sorted(p.stem for p in IMAGE_DIR.glob("*.png") if len(p.stem) == 3)
    if len(words) < SPELL_COUNT + UNSCRAMBLE_COUNT:
        raise RuntimeError(
            f"Need at least {SPELL_COUNT + UNSCRAMBLE_COUNT} clipart PNGs in {IMAGE_DIR}"
        )
    for word in words:
        if word[1] not in "aeiou":
            raise RuntimeError(f"Clipart word is not CVC short-vowel: {word}")
    return tuple(words)


PICTURE_WORDS = load_picture_words()

# (answer, distractor, sentence_with_blank) - blank is "___"
MINIMAL_PAIRS = (
    ("rug", "rag", "The big brown dog sat on the soft ___."),
    ("cat", "cot", "The ___ drank milk from a bowl."),
    ("pig", "peg", "The pink ___ rolled in the mud."),
    ("hat", "hit", "Put on your ___ before you go out."),
    ("bus", "bun", "We rode the yellow ___ to school."),
    ("pen", "pan", "I write with a blue ___."),
    ("cup", "cap", "Fill the ___ with cold water."),
    ("bed", "bad", "I sleep in my ___ at night."),
    ("mop", "map", "Use the ___ to clean the floor."),
    ("sun", "run", "The ___ is hot in the sky."),
    ("dog", "dig", "The ___ barked at the gate."),
    ("box", "fox", "Put the toys in the ___."),
    ("net", "nut", "The fish swam into the ___."),
    ("log", "leg", "The frog sat on a wet ___."),
    ("jam", "ham", "Mom put ___ on the bread."),
    ("fan", "fin", "Turn on the ___ to cool off."),
    ("hut", "hat", "The man lived in a small ___."),
    ("bug", "bag", "A little ___ crawled on the leaf."),
    ("pin", "pan", "She used a ___ to hold the paper."),
    ("tub", "cub", "Fill the ___ with warm water."),
    ("can", "cap", "Open the ___ of soup."),
    ("hen", "pen", "The ___ laid an egg."),
    ("jet", "wet", "The ___ flew high in the sky."),
    ("mug", "rug", "Sip hot cocoa from the ___."),
    ("van", "fan", "Dad drove the big ___."),
    ("web", "wed", "The spider spun a ___."),
    ("pot", "pit", "The soup cooked in the ___."),
    ("lid", "lip", "Put the ___ on the jar."),
    ("hop", "hot", "Watch the bunny ___."),
    ("kid", "kit", "The little ___ ran to mom."),
    ("pop", "pod", "I like to eat ___."),
    ("ram", "rag", "The ___ has curved horns."),
    ("yak", "yam", "The shaggy ___ lives in the hills."),
    ("cob", "cub", "Eat the corn on the ___."),
    ("bin", "bun", "Toss the scrap in the ___."),
    ("mad", "mud", "He got ___ when he lost."),
    ("sad", "mad", "She felt ___ when it rained."),
    ("top", "tap", "Spin the ___ on the floor."),
    ("wax", "tax", "The candle is made of ___."),
    ("mix", "six", "Please ___ the cake batter."),
)

RHYME_PAIRS = (
    ("cat", "hat"),
    ("dog", "log"),
    ("sun", "bun"),
    ("pig", "wig"),
    ("cup", "pup"),
    ("bed", "red"),
    ("map", "cap"),
    ("fox", "box"),
    ("hen", "pen"),
    ("mug", "bug"),
    ("net", "jet"),
    ("pan", "can"),
    ("fin", "pin"),
    ("hut", "nut"),
    ("rat", "bat"),
    ("mop", "top"),
    ("tub", "cub"),
    ("jam", "ham"),
    ("fan", "man"),
    ("lid", "kid"),
    ("hop", "pop"),
    ("big", "dig"),
    ("hot", "pot"),
    ("sit", "kit"),
    ("win", "bin"),
    ("rug", "bug"),
    ("van", "can"),
    ("web", "deb"),  # invalid - remove
    ("leg", "peg"),
    ("mad", "sad"),
    ("tag", "bag"),
    ("ram", "ham"),
    ("yak", "back"),  # back not CVC short - remove
    ("cob", "job"),
    ("rod", "pod"),
    ("ten", "hen"),
    ("six", "mix"),
    ("gum", "sum"),
    ("jug", "bug"),
    ("lab", "cab"),
    ("mom", "tom"),
    ("dad", "mad"),
    ("wax", "tax"),
    ("lip", "sip"),
    ("sub", "tub"),
    ("rag", "bag"),
    ("pad", "mad"),
    ("gas", "has"),
)

# Keep only true short-vowel CVC rhymes with real words.
_KNOWN_CVC = {
    "cat", "hat", "bat", "rat", "mat", "sat", "pat",
    "dog", "log", "fog", "hog",
    "sun", "bun", "run", "fun",
    "pig", "wig", "big", "dig", "fig",
    "cup", "pup",
    "bed", "red", "led", "fed", "wed",
    "map", "cap", "tap", "nap", "lap",
    "fox", "box",
    "hen", "pen", "ten", "men", "den",
    "mug", "bug", "rug", "jug", "hug", "dug", "tug",
    "net", "jet", "wet", "pet", "set", "met",
    "pan", "can", "man", "fan", "van", "ran",
    "fin", "pin", "bin", "win", "tin",
    "hut", "nut", "cut", "gut",
    "tub", "cub",
    "jam", "ham",
    "hot", "pot", "cot", "tot", "lot",
    "pop", "hop", "top", "mop",
    "kid", "lid",
    "cob", "job",
    "rod", "pod",
    "mom", "dad", "mad", "sad", "bad", "pad",
    "gum", "sum",
    "lab", "cab",
    "wax", "tax",
    "lip", "sip", "tip", "rip",
    "sub", "rag", "bag", "tag",
    "gas", "six", "mix", "leg", "peg", "web", "ram", "yak",
    "bus", "cup", "dog", "cat", "pig", "sun", "hut", "bug",
}
_VALID_RHYMES = []
for _a, _b in RHYME_PAIRS:
    if (
        _a in _KNOWN_CVC
        and _b in _KNOWN_CVC
        and _a[1] == _b[1]
        and _a[2] == _b[2]
        and _a != _b
    ):
        _VALID_RHYMES.append((_a, _b))
RHYME_PAIRS = tuple(_VALID_RHYMES)

# Text-only CVC words allowed in code/rhyme/minimal when not pictured.
TEXT_WORDS = sorted(
    {
        w
        for pair in MINIMAL_PAIRS
        for w in (pair[0], pair[1])
    }
    | {a for a, b in RHYME_PAIRS}
    | {b for a, b in RHYME_PAIRS}
    | set(PICTURE_WORDS)
)

SYMBOL_NAMES = (
    "star",
    "circle",
    "triangle",
    "square",
    "diamond",
    "heart",
    "cross",
    "hexagon",
    "arrow",
    "moon",
    "oval",
    "plus",
)

_IMAGE_CACHE: dict[str, ImageReader] = {}


def content_width():
    return PAGE_W - LEFT - RIGHT


def image_path(word):
    path = IMAGE_DIR / f"{word}.png"
    if not path.is_file():
        raise FileNotFoundError(f"Missing clipart: {path}")
    return path


def get_image(word):
    if word not in _IMAGE_CACHE:
        _IMAGE_CACHE[word] = ImageReader(str(image_path(word)))
    return _IMAGE_CACHE[word]


def scramble_word(rng, word):
    letters = list(word)
    for _ in range(40):
        rng.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled != word:
            return scrambled
    return word[1:] + word[0]


def take_least_used(rng, pool, count, used, usage):
    """Pick `count` items, preferring those used least often so far."""
    available = [w for w in pool if w not in used]
    if len(available) < count:
        raise RuntimeError(
            f"Need {count} unused items, only {len(available)} left in pool"
        )
    available = sorted(available, key=lambda w: (usage[w], rng.random()))
    # Prefer from the least-used tier, with enough room to sample.
    min_use = usage[available[0]]
    tier = [w for w in available if usage[w] <= min_use + 1]
    if len(tier) < count:
        tier = available[: max(count * 3, count)]
    chosen = rng.sample(tier, count)
    for w in chosen:
        usage[w] += 1
    used.update(chosen)
    return chosen


def pick_code_words(rng, pool, count):
    if len(pool) < count:
        raise RuntimeError("Code-breaker pool is too small")
    for _ in range(300):
        candidate = rng.sample(list(pool), count)
        if len(set("".join(candidate))) <= len(SYMBOL_NAMES):
            return candidate
    chosen = []
    letters = set()
    shuffled = list(pool)
    rng.shuffle(shuffled)
    for word in shuffled:
        nxt = letters | set(word)
        if len(nxt) <= len(SYMBOL_NAMES):
            chosen.append(word)
            letters = nxt
        if len(chosen) == count:
            return chosen
    raise RuntimeError("Could not build a code-breaker set")


def build_worksheet(rng, picture_usage, rhyme_usage, minimal_usage):
    used = set()

    spell = take_least_used(
        rng, PICTURE_WORDS, SPELL_COUNT, used, picture_usage
    )
    unscramble_words = take_least_used(
        rng, PICTURE_WORDS, UNSCRAMBLE_COUNT, used, picture_usage
    )
    unscramble = [
        {"word": w, "scrambled": scramble_word(rng, w)} for w in unscramble_words
    ]

    # Prefer least-used minimal pair templates that avoid already-used words.
    ranked = sorted(
        MINIMAL_PAIRS,
        key=lambda p: (minimal_usage[p[0] + "|" + p[1]], rng.random()),
    )
    minimal = []
    for answer, distractor, sentence in ranked:
        if answer in used or distractor in used:
            continue
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
        used.add(answer)
        used.add(distractor)
        minimal_usage[answer + "|" + distractor] += 1
        if len(minimal) == MINIMAL_COUNT:
            break
    if len(minimal) < MINIMAL_COUNT:
        # Fall back allowing overlap with prior sections.
        leftover = [p for p in ranked if p not in [
            (m["answer"], m["distractor"], m["sentence"]) for m in minimal
        ]]
        for answer, distractor, sentence in leftover:
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
            minimal_usage[answer + "|" + distractor] += 1
            if len(minimal) == MINIMAL_COUNT:
                break
    if len(minimal) < MINIMAL_COUNT:
        raise RuntimeError("Not enough minimal-pair sentences")

    code_pool = [w for w in TEXT_WORDS if w not in used]
    if len(code_pool) < CODE_COUNT:
        code_pool = list(TEXT_WORDS)
    code_words = pick_code_words(rng, code_pool, CODE_COUNT)
    used.update(code_words)
    letters_needed = sorted(set("".join(code_words)))
    symbols = list(SYMBOL_NAMES)
    rng.shuffle(symbols)
    legend = {letter: symbols[i] for i, letter in enumerate(letters_needed)}
    code = {
        "legend": legend,
        "words": [
            {"word": w, "symbols": [legend[ch] for ch in w]} for w in code_words
        ],
    }

    ranked_rhymes = sorted(
        RHYME_PAIRS,
        key=lambda p: (rhyme_usage[p[0] + "|" + p[1]], rng.random()),
    )
    rhyme_pairs = []
    for a, b in ranked_rhymes:
        if a in used or b in used:
            continue
        rhyme_pairs.append((a, b))
        used.add(a)
        used.add(b)
        rhyme_usage[a + "|" + b] += 1
        if len(rhyme_pairs) == RHYME_COUNT:
            break
    if len(rhyme_pairs) < RHYME_COUNT:
        for a, b in ranked_rhymes:
            if (a, b) in rhyme_pairs:
                continue
            rhyme_pairs.append((a, b))
            rhyme_usage[a + "|" + b] += 1
            if len(rhyme_pairs) == RHYME_COUNT:
                break
    if len(rhyme_pairs) < RHYME_COUNT:
        raise RuntimeError("Not enough rhyme pairs")

    left = [a for a, _b in rhyme_pairs]
    right = [b for _a, b in rhyme_pairs]
    rng.shuffle(right)
    if right == [b for _a, b in rhyme_pairs] and RHYME_COUNT > 1:
        right[0], right[1] = right[1], right[0]
    rhyme = {"left": left, "right": right, "pairs": list(rhyme_pairs)}

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
    worksheets = []
    for _ in range(WORKSHEETS):
        worksheets.append(
            build_worksheet(rng, picture_usage, rhyme_usage, minimal_usage)
        )
    return worksheets, picture_usage


# --- Symbol drawing for code breakers ---------------------------------------


def _stroke(c, width=1.2):
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.setLineJoin(1)


def draw_symbol(c, name, cx, cy, size):
    _stroke(c, 1.1)
    s = size
    if name == "star":
        pts = []
        for i in range(5):
            ang = -math.pi / 2 + i * 2 * math.pi / 5
            pts.append((cx + math.cos(ang) * s * 0.45, cy + math.sin(ang) * s * 0.45))
        for i in range(5):
            j = (i + 2) % 5
            c.line(pts[i][0], pts[i][1], pts[j][0], pts[j][1])
    elif name == "circle":
        c.circle(cx, cy, s * 0.35, stroke=1, fill=0)
    elif name == "triangle":
        path = c.beginPath()
        path.moveTo(cx, cy + s * 0.4)
        path.lineTo(cx - s * 0.38, cy - s * 0.32)
        path.lineTo(cx + s * 0.38, cy - s * 0.32)
        path.close()
        c.drawPath(path, stroke=1, fill=0)
    elif name == "square":
        c.rect(cx - s * 0.32, cy - s * 0.32, s * 0.64, s * 0.64, stroke=1, fill=0)
    elif name == "diamond":
        path = c.beginPath()
        path.moveTo(cx, cy + s * 0.4)
        path.lineTo(cx + s * 0.32, cy)
        path.lineTo(cx, cy - s * 0.4)
        path.lineTo(cx - s * 0.32, cy)
        path.close()
        c.drawPath(path, stroke=1, fill=0)
    elif name == "heart":
        c.circle(cx - s * 0.14, cy + s * 0.08, s * 0.16, stroke=1, fill=0)
        c.circle(cx + s * 0.14, cy + s * 0.08, s * 0.16, stroke=1, fill=0)
        path = c.beginPath()
        path.moveTo(cx - s * 0.3, cy + s * 0.05)
        path.lineTo(cx, cy - s * 0.35)
        path.lineTo(cx + s * 0.3, cy + s * 0.05)
        c.drawPath(path, stroke=1, fill=0)
    elif name == "cross":
        c.line(cx - s * 0.28, cy - s * 0.28, cx + s * 0.28, cy + s * 0.28)
        c.line(cx - s * 0.28, cy + s * 0.28, cx + s * 0.28, cy - s * 0.28)
    elif name == "hexagon":
        path = c.beginPath()
        for i in range(6):
            ang = i * math.pi / 3
            x = cx + math.cos(ang) * s * 0.35
            y = cy + math.sin(ang) * s * 0.35
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.close()
        c.drawPath(path, stroke=1, fill=0)
    elif name == "arrow":
        c.line(cx - s * 0.35, cy, cx + s * 0.2, cy)
        path = c.beginPath()
        path.moveTo(cx + s * 0.1, cy + s * 0.2)
        path.lineTo(cx + s * 0.38, cy)
        path.lineTo(cx + s * 0.1, cy - s * 0.2)
        c.drawPath(path, stroke=1, fill=0)
    elif name == "moon":
        path = c.beginPath()
        path.moveTo(cx + s * 0.05, cy + s * 0.35)
        path.curveTo(
            cx - s * 0.45,
            cy + s * 0.35,
            cx - s * 0.45,
            cy - s * 0.35,
            cx + s * 0.05,
            cy - s * 0.35,
        )
        path.curveTo(
            cx - s * 0.15,
            cy - s * 0.2,
            cx - s * 0.15,
            cy + s * 0.2,
            cx + s * 0.05,
            cy + s * 0.35,
        )
        path.close()
        c.drawPath(path, stroke=1, fill=0)
    elif name == "oval":
        c.ellipse(
            cx - s * 0.22, cy - s * 0.35, cx + s * 0.22, cy + s * 0.35, stroke=1, fill=0
        )
    elif name == "plus":
        c.setLineWidth(2.0)
        c.line(cx - s * 0.28, cy, cx + s * 0.28, cy)
        c.line(cx, cy - s * 0.28, cx, cy + s * 0.28)
        c.setLineWidth(1.1)
    elif name == "bolt":
        c.line(cx, cy + s * 0.38, cx - s * 0.12, cy + s * 0.02)
        c.line(cx - s * 0.12, cy + s * 0.02, cx + s * 0.12, cy - s * 0.02)
        c.line(cx + s * 0.12, cy - s * 0.02, cx, cy - s * 0.38)
    elif name == "wave":
        path = c.beginPath()
        path.moveTo(cx - s * 0.36, cy)
        path.curveTo(cx - s * 0.24, cy + s * 0.28, cx - s * 0.12, cy + s * 0.28, cx, cy)
        path.curveTo(cx + s * 0.12, cy - s * 0.28, cx + s * 0.24, cy - s * 0.28, cx + s * 0.36, cy)
        c.drawPath(path, stroke=1, fill=0)
    elif name == "dots":
        for dx in (-0.22, 0, 0.22):
            c.circle(cx + dx * s, cy, s * 0.08, stroke=1, fill=1)
    elif name == "check":
        c.setLineWidth(1.6)
        c.line(cx - s * 0.28, cy, cx - s * 0.06, cy - s * 0.22)
        c.line(cx - s * 0.06, cy - s * 0.22, cx + s * 0.32, cy + s * 0.28)
        c.setLineWidth(1.1)
    elif name == "slash":
        c.setLineWidth(1.8)
        c.line(cx - s * 0.22, cy - s * 0.32, cx + s * 0.22, cy + s * 0.32)
        c.setLineWidth(1.1)
    elif name == "tee":
        c.setLineWidth(1.8)
        c.line(cx - s * 0.28, cy + s * 0.28, cx + s * 0.28, cy + s * 0.28)
        c.line(cx, cy + s * 0.28, cx, cy - s * 0.32)
        c.setLineWidth(1.1)
    elif name == "hook":
        c.setLineWidth(1.8)
        c.line(cx + s * 0.1, cy + s * 0.34, cx + s * 0.1, cy - s * 0.05)
        path = c.beginPath()
        path.moveTo(cx + s * 0.1, cy - s * 0.05)
        path.curveTo(cx + s * 0.1, cy - s * 0.36, cx - s * 0.34, cy - s * 0.36, cx - s * 0.34, cy - s * 0.08)
        c.drawPath(path, stroke=1, fill=0)
        c.setLineWidth(1.1)
    elif name == "sun":
        c.circle(cx, cy, s * 0.16, stroke=1, fill=0)
        for ang in (0, 45, 90, 135, 180, 225, 270, 315):
            rad = math.radians(ang)
            c.line(
                cx + math.cos(rad) * s * 0.24,
                cy + math.sin(rad) * s * 0.24,
                cx + math.cos(rad) * s * 0.40,
                cy + math.sin(rad) * s * 0.40,
            )
    else:
        c.circle(cx, cy, s * 0.3, stroke=1, fill=0)


# --- Page chrome and sections -----------------------------------------------

CONTENT_TOP = PAGE_H - 68
CONTENT_BOTTOM = 40
SECTION_HEAD = 18  # heading text + rule + gap under rule


def draw_clipart(c, word, cx, cy, size):
    """Draw clipart centered at (cx, cy) inside a size x size box."""
    img = get_image(word)
    c.drawImage(
        img,
        cx - size / 2,
        cy - size / 2,
        width=size,
        height=size,
        preserveAspectRatio=True,
        mask="auto",
    )


def draw_header(c, worksheet_index, total_worksheets, title="CVC Short Vowels"):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 15)
    heading = title
    if total_worksheets > 1:
        heading = f"{title} - Worksheet {worksheet_index + 1}"
    c.drawString(LEFT, PAGE_H - 30, heading)
    y = PAGE_H - 50
    c.setFont("Helvetica", 12)
    c.drawString(LEFT, y, "Name:")
    name_x = LEFT + pdfmetrics.stringWidth("Name: ", "Helvetica", 12)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_x, y - 2, name_x + 200, y - 2)
    date_x = name_x + 220
    c.drawString(date_x, y, "Date:")
    date_line = date_x + pdfmetrics.stringWidth("Date: ", "Helvetica", 12)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)


def draw_footer(c, page, total):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, 18, f"Page {page} of {total}")


def draw_section_heading(c, y, title, instruction):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, title)
    title_w = pdfmetrics.stringWidth(title + "  ", "Helvetica-Bold", 12)
    c.setFont("Helvetica", 11)
    c.drawString(LEFT + title_w, y, instruction)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.7)
    c.line(LEFT, y - 4, PAGE_W - RIGHT, y - 4)
    return y - SECTION_HEAD


def draw_letter_boxes(c, x, y, box=18, gap=3, count=3, letters=None):
    _stroke(c, 1.0)
    for i in range(count):
        bx = x + i * (box + gap)
        c.rect(bx, y, box, box, stroke=1, fill=0)
        if letters and i < len(letters):
            c.setFont("Helvetica-Bold", 12)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(bx + box / 2, y + 4, letters[i].upper())


def page1_layout():
    """Split page 1 between Spell and Unscramble."""
    available = CONTENT_TOP - CONTENT_BOTTOM
    gap = 20
    body = available - 2 * SECTION_HEAD - gap
    spell_h = body * 0.50
    unscramble_h = body - spell_h
    return {
        "spell_top": CONTENT_TOP,
        "spell_h": spell_h,
        "unscramble_top": CONTENT_TOP - SECTION_HEAD - spell_h - gap,
        "unscramble_h": unscramble_h,
    }


def page2_layout():
    """Split page 2 across Choose / Code / Rhyme."""
    available = CONTENT_TOP - CONTENT_BOTTOM
    gaps = 18 * 2
    body = available - 3 * SECTION_HEAD - gaps
    choose_h = body * 0.30
    code_h = body * 0.34
    rhyme_h = body - choose_h - code_h
    choose_top = CONTENT_TOP
    code_top = choose_top - SECTION_HEAD - choose_h - 18
    rhyme_top = code_top - SECTION_HEAD - code_h - 18
    return {
        "choose_top": choose_top,
        "choose_h": choose_h,
        "code_top": code_top,
        "code_h": code_h,
        "rhyme_top": rhyme_top,
        "rhyme_h": rhyme_h,
    }


def spell_box_metrics(nlet_max):
    if nlet_max <= 3:
        return 22, 5
    if nlet_max <= 4:
        return 18, 4
    if nlet_max <= 5:
        return 16, 3
    return 14, 2


def code_box_metrics(nlet_max):
    # box, gap, number width, symbol step, symbol size
    if nlet_max <= 3:
        return 16, 3, 20, 20, 14
    if nlet_max <= 4:
        return 14, 2, 24, 17, 14
    if nlet_max <= 5:
        return 13, 2, 22, 16, 13
    if nlet_max <= 6:
        return 12, 2, 20, 15, 12
    return 11, 1, 18, 14, 11


def draw_spell_section(c, top, height, words):
    y = draw_section_heading(
        c, top, "Spell the Word.", "Write one letter in each box."
    )
    cols = 3
    rows = 2
    col_w = content_width() / cols
    cell_h = height / rows
    box, box_gap = spell_box_metrics(max(len(word) for word in words))
    gap_ib = 10  # icon to boxes
    icon_size = min(72, cell_h - box - gap_ib - 12)
    for index, word in enumerate(words):
        row, col = divmod(index, cols)
        cx = LEFT + col * col_w + col_w / 2
        cell_top = y - row * cell_h
        cluster_h = icon_size + gap_ib + box
        pad = max(4, (cell_h - cluster_h) / 2)
        icon_cy = cell_top - pad - icon_size / 2
        draw_clipart(c, word, cx, icon_cy, icon_size)
        nlet = len(word)
        total_w = nlet * box + (nlet - 1) * box_gap
        boxes_y = icon_cy - icon_size / 2 - gap_ib - box
        draw_letter_boxes(
            c, cx - total_w / 2, boxes_y, box=box, gap=box_gap, count=nlet
        )


def draw_unscramble_section(c, top, height, items):
    y = draw_section_heading(
        c, top, "Unscramble.", "Look at the picture. Unscramble the letters."
    )
    cols = 4
    col_w = content_width() / cols
    # Pictures sit close under the heading. A wide gap between the scrambled
    # letters and the answer line leaves room to write.
    top_pad = 2
    icon_size = 46
    letter_drop = 13
    line_gap = 36
    row_gap = 12
    row_h = icon_size + letter_drop + line_gap
    for index, item in enumerate(items):
        row, col = divmod(index, cols)
        cx = LEFT + col * col_w + col_w / 2
        row_top = y - top_pad - row * (row_h + row_gap)
        icon_cy = row_top - icon_size / 2
        draw_clipart(c, item["word"], cx, icon_cy, icon_size)
        scrambled = " ".join(ch.upper() for ch in item["scrambled"])
        font_size = 12
        while (
            font_size > 8
            and pdfmetrics.stringWidth(scrambled, "Helvetica-Bold", font_size) > col_w - 12
        ):
            font_size -= 1
        c.setFont("Helvetica-Bold", font_size)
        c.setFillColorRGB(0, 0, 0)
        letters_y = icon_cy - icon_size / 2 - letter_drop
        c.drawCentredString(cx, letters_y, scrambled)
        line_w = col_w - 28
        line_y = letters_y - line_gap
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.8)
        c.line(cx - line_w / 2, line_y, cx + line_w / 2, line_y)


def draw_minimal_section(c, top, height, items):
    y = draw_section_heading(
        c,
        top,
        "Choose the Word.",
        "Circle the word that completes each sentence.",
    )
    n = len(items)
    pitch = height / n
    font = "Helvetica"
    size = 12
    for index, item in enumerate(items):
        # One line per item, centered in the band so questions stay spaced out.
        band_top = y - index * pitch
        sent_y = band_top - pitch / 2
        c.setFillColorRGB(0, 0, 0)
        c.setFont(font, size)
        c.drawString(LEFT, sent_y, f"{index + 1}.")
        text_x = LEFT + 18
        c.drawString(text_x, sent_y, item["sentence"])
        opt_x = text_x + pdfmetrics.stringWidth(item["sentence"], font, size) + 16
        for choice in item["choices"]:
            c.circle(opt_x + 6, sent_y + 3, 6.5, stroke=1, fill=0)
            c.drawString(opt_x + 16, sent_y, choice)
            word_w = pdfmetrics.stringWidth(choice, font, size)
            opt_x += 16 + word_w + 14
        if opt_x > PAGE_W - RIGHT:
            raise RuntimeError(f"Choose-the-word line is too wide: {item['sentence']}")


def draw_code_section(c, top, height, code):
    y = draw_section_heading(
        c, top, "Code Breakers.", "Use the key. Write each word."
    )
    legend = code["legend"]
    letters = sorted(legend.keys())
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(LEFT, y, "Key:")
    key_x = LEFT + 28
    sym_size = 12
    cell_w = 44
    legend_top = y
    for letter in letters:
        if key_x + cell_w > PAGE_W - RIGHT:
            key_x = LEFT + 28
            y -= 20
        draw_symbol(c, legend[letter], key_x + 7, y + 3, sym_size)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(key_x + 16, y, f"= {letter.upper()}")
        key_x += cell_w
    legend_h = (legend_top - y) + 28
    y = legend_top - legend_h

    words = code["words"]
    cols = 2
    rows = (len(words) + cols - 1) // cols
    col_w = content_width() / cols
    remaining = max(60, height - legend_h)
    pitch = remaining / rows
    nlet_max = max(len(item["word"]) for item in words)
    box, gap, num_w, sym_step, sym_size = code_box_metrics(nlet_max)
    for index, item in enumerate(words):
        nlet = len(item["word"])
        col, row = divmod(index, rows)
        x = LEFT + col * col_w
        band_top = y - row * pitch
        row_y = band_top - min(12, pitch * 0.35)
        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, row_y, f"{index + 1}.")
        sx = x + num_w
        sym_dx = 7 if nlet_max <= 4 else sym_step / 2
        for sym in item["symbols"]:
            draw_symbol(c, sym, sx + sym_dx, row_y + 3, sym_size)
            sx += sym_step
        draw_letter_boxes(c, sx + 6, row_y - 3, box=box, gap=gap, count=nlet)
        end_x = sx + 6 + nlet * box + (nlet - 1) * gap
        if end_x > x + col_w - 2:
            raise RuntimeError(f"Code word does not fit: {item['word']}")


def draw_rhyme_section(c, top, height, rhyme):
    y = draw_section_heading(
        c, top, "Rhyme Match.", "Draw a line to match each rhyming pair."
    )
    left = rhyme["left"]
    right = rhyme["right"]
    left_x = LEFT + 150
    right_x = PAGE_W - RIGHT - 150
    n = len(left)
    pitch = height / n
    for i, word in enumerate(left):
        yy = y - (i + 0.5) * pitch
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawRightString(left_x, yy, word)
        c.circle(left_x + 14, yy + 4, 3.5, stroke=1, fill=1)
    for i, word in enumerate(right):
        yy = y - (i + 0.5) * pitch
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0, 0, 0)
        c.circle(right_x - 14, yy + 4, 3.5, stroke=1, fill=1)
        c.drawString(right_x, yy, word)


def draw_worksheet_pages(
    c, worksheet, worksheet_index, total_pages, page_offset,
    title="CVC Short Vowels", worksheet_total=None,
):
    total_worksheets = WORKSHEETS if worksheet_total is None else worksheet_total
    draw_header(c, worksheet_index, total_worksheets, title)
    draw_footer(c, page_offset + 1, total_pages)
    layout1 = page1_layout()
    draw_spell_section(
        c, layout1["spell_top"], layout1["spell_h"], worksheet["spell"]
    )
    draw_unscramble_section(
        c,
        layout1["unscramble_top"],
        layout1["unscramble_h"],
        worksheet["unscramble"],
    )

    c.showPage()
    draw_header(c, worksheet_index, total_worksheets, title)
    draw_footer(c, page_offset + 2, total_pages)
    layout2 = page2_layout()
    draw_minimal_section(
        c, layout2["choose_top"], layout2["choose_h"], worksheet["minimal"]
    )
    draw_code_section(
        c, layout2["code_top"], layout2["code_h"], worksheet["code"]
    )
    draw_rhyme_section(
        c, layout2["rhyme_top"], layout2["rhyme_h"], worksheet["rhyme"]
    )
    return page_offset + 2


def write_student_packet(path, worksheets, title="CVC Short Vowels"):
    total_pages = len(worksheets) * PAGES_PER_WORKSHEET
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(title)
    page_offset = 0
    for index, worksheet in enumerate(worksheets):
        if index:
            c.showPage()
        page_offset = draw_worksheet_pages(
            c, worksheet, index, total_pages, page_offset,
            title=title, worksheet_total=len(worksheets),
        )
    c.save()


def write_answer_key(path, worksheets, title="CVC Short Vowels - Answer Key"):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(title)
    y = PAGE_H - 40
    page = 1

    def ensure(need=50):
        nonlocal y, page
        if y < 40 + need:
            c.setFont("Helvetica", 10)
            c.drawCentredString(PAGE_W / 2, 18, f"Answer Key - page {page}")
            c.showPage()
            page += 1
            y = PAGE_H - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, title)
    y -= 28

    for wi, ws in enumerate(worksheets):
        ensure(120)
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(LEFT, y, f"Worksheet {wi + 1}")
        y -= 18

        c.setFont("Helvetica-Bold", 11)
        c.drawString(LEFT, y, "Spell the Word:")
        y -= 14
        c.setFont("Helvetica", 11)
        c.drawString(LEFT + 12, y, ", ".join(ws["spell"]))
        y -= 16

        c.setFont("Helvetica-Bold", 11)
        c.drawString(LEFT, y, "Unscramble:")
        y -= 14
        c.setFont("Helvetica", 11)
        parts = [f"{item['scrambled']} -> {item['word']}" for item in ws["unscramble"]]
        line = ""
        for part in parts:
            candidate = f"{line}, {part}" if line else part
            if pdfmetrics.stringWidth(candidate, "Helvetica", 11) > content_width() - 12:
                c.drawString(LEFT + 12, y, line)
                y -= 14
                ensure(40)
                line = part
            else:
                line = candidate
        if line:
            c.drawString(LEFT + 12, y, line)
            y -= 16

        ensure(40)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(LEFT, y, "Choose the Word:")
        y -= 14
        c.setFont("Helvetica", 11)
        for i, item in enumerate(ws["minimal"]):
            ensure(20)
            c.drawString(LEFT + 12, y, f"{i + 1}. {item['answer']}")
            y -= 14

        ensure(40)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(LEFT, y, "Code Breakers:")
        y -= 14
        c.setFont("Helvetica", 11)
        legend_bits = [
            f"{sym}={let.upper()}"
            for let, sym in sorted(ws["code"]["legend"].items(), key=lambda x: x[0])
        ]
        key_line = "Key: "
        for bit in legend_bits:
            candidate = key_line + ("" if key_line.endswith("Key: ") else ", ") + bit
            if pdfmetrics.stringWidth(candidate, "Helvetica", 11) > content_width() - 12:
                c.drawString(LEFT + 12, y, key_line)
                y -= 14
                ensure(30)
                key_line = bit
            else:
                key_line = candidate
        if key_line:
            c.drawString(LEFT + 12, y, key_line)
            y -= 14
        parts = [
            f"{i + 1}. {item['word']}" for i, item in enumerate(ws["code"]["words"])
        ]
        line = ""
        for part in parts:
            candidate = f"{line}, {part}" if line else part
            if pdfmetrics.stringWidth(candidate, "Helvetica", 11) > content_width() - 12:
                c.drawString(LEFT + 12, y, line)
                y -= 14
                ensure(30)
                line = part
            else:
                line = candidate
        if line:
            c.drawString(LEFT + 12, y, line)
            y -= 16

        ensure(50)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(LEFT, y, "Rhyme Match:")
        y -= 14
        c.setFont("Helvetica", 11)
        matches = ", ".join(f"{a}-{b}" for a, b in ws["rhyme"]["pairs"])
        c.drawString(LEFT + 12, y, matches)
        y -= 22

    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_W / 2, 18, f"Answer Key - page {page}")
    c.save()


def main():
    missing = [w for w in PICTURE_WORDS if not image_path(w).is_file()]
    if missing:
        raise RuntimeError(f"Missing clipart files: {missing}")

    worksheets, picture_usage = build_packet()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, worksheets)
    write_answer_key(ANSWER_KEY_PDF, worksheets)
    uses = sorted(picture_usage.values())
    print(f"Wrote {STUDENT_PDF} ({WORKSHEETS} worksheets, {WORKSHEETS * 2} pages)")
    print(f"Wrote {ANSWER_KEY_PDF}")
    print(
        f"Picture bank: {len(PICTURE_WORDS)} words; "
        f"uses per word min={uses[0]} max={uses[-1]}"
    )


if __name__ == "__main__":
    main()
