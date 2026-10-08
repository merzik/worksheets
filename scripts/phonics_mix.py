"""Shared builder for mixed phonics packets.

Each worksheet is two pages with the same five sections as the CVC packet:
spell from picture, unscramble, choose the word, code breakers, and rhyme match.
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cvc_short_vowels as base

from reportlab.pdfbase import pdfmetrics

SYMBOLS = base.SYMBOL_NAMES + (
    "bolt",
    "wave",
    "dots",
    "check",
    "slash",
    "tee",
    "hook",
    "sun",
)

SPELL_COUNT = 6
UNSCRAMBLE_COUNT = 8
MINIMAL_COUNT = 5
CODE_COUNT = 10
RHYME_COUNT = 5


def sentence_fits(sentence, choices):
    font = "Helvetica"
    size = 12
    opt_x = base.LEFT + 18 + pdfmetrics.stringWidth(sentence, font, size) + 16
    for choice in choices:
        word_w = pdfmetrics.stringWidth(choice, font, size)
        opt_x += 16 + word_w + 14
    return opt_x <= base.PAGE_W - base.RIGHT


def check_pairs(minimal_pairs, rhyme_pairs, extra_words, pattern, rime):
    for answer, distractor, sentence in minimal_pairs:
        if pattern(answer) is None:
            raise RuntimeError(f"Choose-the-word answer is off pattern: {answer}")
        if not distractor.isalpha() or distractor == answer:
            raise RuntimeError(f"Bad distractor for {answer}: {distractor}")
        if "___" not in sentence:
            raise RuntimeError(f"Sentence has no blank: {sentence}")
        if not sentence_fits(sentence, (answer, distractor)):
            raise RuntimeError(f"Choose-the-word line is too wide: {sentence}")
    for a, b in rhyme_pairs:
        if pattern(a) is None or pattern(b) is None:
            raise RuntimeError(f"Rhyme pair is off pattern: {a}/{b}")
        if rime(a) != rime(b) or a == b:
            raise RuntimeError(f"Not a rhyme: {a}/{b} ({rime(a)}/{rime(b)})")
    for word in extra_words:
        if pattern(word) is None:
            raise RuntimeError(f"Extra word is off pattern: {word}")


def text_pool(picture_words, minimal_pairs, rhyme_pairs, extra_words, pattern):
    words = set(picture_words) | set(extra_words)
    words |= {a for a, _b, _s in minimal_pairs}
    words |= {a for a, b in rhyme_pairs} | {b for a, b in rhyme_pairs}
    bad = [w for w in words if pattern(w) is None]
    if bad:
        raise RuntimeError(f"Text pool has off-pattern words: {bad}")
    return sorted(words)


def _swap_for_new_kind(words, pool, used, usage, pattern):
    have = {pattern(w) for w in words}
    options = [w for w in pool if pattern(w) not in have and w not in words]
    if not options:
        return False
    options.sort(key=lambda w: (usage[w],))
    counts = Counter(pattern(w) for w in words)
    pick = options[0]
    for index, word in enumerate(words):
        if counts[pattern(word)] > 1:
            usage[word] -= 1
            usage[pick] += 1
            used.discard(word)
            used.add(pick)
            words[index] = pick
            return True
    return False


def reinforce(spell, unscramble, pool, used, usage, pattern, min_kinds):
    guard = 0
    while guard < 8:
        kinds = {pattern(w) for w in spell + unscramble}
        if len(kinds) >= min_kinds:
            return
        guard += 1
        if _swap_for_new_kind(unscramble, pool, used, usage, pattern):
            continue
        if _swap_for_new_kind(spell, pool, used, usage, pattern):
            continue
        return


def pick_code_words(rng, pool, count, pattern):
    pool = list(pool)
    if len(pool) < count:
        raise RuntimeError("Code-breaker pool is too small")

    def fits(candidate, min_kinds):
        if len(set("".join(candidate))) > len(SYMBOLS):
            return False
        return len({pattern(w) for w in candidate}) >= min_kinds

    for min_kinds, tries in ((3, 500), (2, 250), (1, 200)):
        for _ in range(tries):
            candidate = rng.sample(pool, count)
            if fits(candidate, min_kinds):
                rng.shuffle(candidate)
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


def _take_labeled(rng, items, count, used, usage, label):
    def words_of(item):
        if label == "minimal":
            return item[0], item[1]
        return item[0], item[1]

    def usage_key(item):
        a, b = words_of(item)
        return f"{a}|{b}"

    ranked = sorted(items, key=lambda item: (usage[usage_key(item)], rng.random()))

    def grab(allow_used, picked, picked_words):
        for item in ranked:
            if item in picked:
                continue
            a, b = words_of(item)
            if a in picked_words or b in picked_words:
                continue
            if not allow_used and (a in used or b in used):
                continue
            picked.append(item)
            picked_words.add(a)
            picked_words.add(b)
            usage[usage_key(item)] += 1
            used.add(a)
            used.add(b)
            return True
        return False

    picked = []
    picked_words = set()
    for allow_used in (False, True):
        while len(picked) < count and grab(allow_used, picked, picked_words):
            pass
        if len(picked) == count:
            return picked
    raise RuntimeError(f"Not enough {label} items")


def build_worksheet(
    rng, picture_words, minimal_pairs, rhyme_pairs, text_words,
    pattern, picture_usage, rhyme_usage, minimal_usage,
):
    used = set()
    spell = base.take_least_used(
        rng, picture_words, SPELL_COUNT, used, picture_usage
    )
    unscramble_words = base.take_least_used(
        rng, picture_words, UNSCRAMBLE_COUNT, used, picture_usage
    )
    reinforce(
        spell, unscramble_words, picture_words, used, picture_usage, pattern, 3
    )
    rng.shuffle(spell)
    rng.shuffle(unscramble_words)
    kinds = {pattern(w) for w in spell + unscramble_words}
    if len(kinds) < 3:
        raise RuntimeError(f"Picture sections are not mixed: {sorted(kinds)}")
    unscramble = [
        {"word": w, "scrambled": base.scramble_word(rng, w)} for w in unscramble_words
    ]

    minimal_raw = _take_labeled(
        rng, minimal_pairs, MINIMAL_COUNT, used, minimal_usage, "minimal"
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

    code_pool = [w for w in text_words if w not in used]
    if len(code_pool) < CODE_COUNT:
        code_pool = list(text_words)
    code_words = pick_code_words(rng, code_pool, CODE_COUNT, pattern)
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

    rhyme_raw = _take_labeled(
        rng, rhyme_pairs, RHYME_COUNT, used, rhyme_usage, "rhyme"
    )
    left = [a for a, _b in rhyme_raw]
    right = [b for _a, b in rhyme_raw]
    order = [b for _a, b in rhyme_raw]
    rng.shuffle(right)
    if right == order and RHYME_COUNT > 1:
        right[0], right[1] = right[1], right[0]
    rhyme = {"left": left, "right": right, "pairs": list(rhyme_raw)}
    return {
        "spell": spell,
        "unscramble": unscramble,
        "minimal": minimal,
        "code": code,
        "rhyme": rhyme,
    }


def build_packet(
    seed, picture_words, minimal_pairs, rhyme_pairs, text_words, pattern, worksheets
):
    rng = random.Random(seed)
    picture_usage = Counter()
    rhyme_usage = Counter()
    minimal_usage = Counter()
    built = [
        build_worksheet(
            rng,
            picture_words,
            minimal_pairs,
            rhyme_pairs,
            text_words,
            pattern,
            picture_usage,
            rhyme_usage,
            minimal_usage,
        )
        for _ in range(worksheets)
    ]
    return built, picture_usage


def write_packet(student_pdf, answer_pdf, worksheets, title, image_dir):
    base.IMAGE_DIR = image_dir
    base._IMAGE_CACHE.clear()
    image_dir.parent.mkdir(parents=True, exist_ok=True)
    base.write_student_packet(student_pdf, worksheets, title=title)
    base.write_answer_key(answer_pdf, worksheets, title=f"{title} - Answer Key")
