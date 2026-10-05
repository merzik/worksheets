#!/usr/bin/env python3
"""Build grade 2 fall worksheets for adding adjectives to nouns.

Each item gives a basic sentence with nouns marked. The student writes a
new sentence that adds a descriptive adjective before every marked noun.
A separate answer key lists several suggested adjectives for each noun.
"""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "writing" / "descriptive-sentences"
STUDENT_PDF = OUT_DIR / "add-adjectives-fall-grade-2.pdf"
ANSWER_KEY_PDF = OUT_DIR / "add-adjectives-fall-grade-2-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 48
RIGHT = 48
TOP = 42
BOTTOM = 40
TITLE_SIZE = 16
BODY_SIZE = 15
BODY_LEADING = 21
DIR_SIZE = 13
DIR_LEADING = 17
KEY_SIZE = 12
KEY_LEADING = 16
LINE_GAP = 28
WRITE_LINES = 2
ITEMS_PER_PAGE = 5
STUDENT_PAGES = 10
SUGGESTIONS_PER_NOUN = 4

# Nouns wrapped in {braces} are the ones the student should describe.
# Short fall sentences for grade 2. Suggestions are sample adjectives only.
RAW_ITEMS = [
    {
        "template": "The {leaf} fell from the {tree}.",
        "suggestions": {
            "leaf": ["red", "crunchy", "golden", "dry"],
            "tree": ["tall", "old", "maple", "oak"],
        },
    },
    {
        "template": "A {squirrel} hid an {acorn}.",
        "suggestions": {
            "squirrel": ["furry", "quick", "busy", "gray"],
            "acorn": ["brown", "tiny", "shiny", "round"],
        },
    },
    {
        "template": "The {girl} picked a {pumpkin}.",
        "suggestions": {
            "girl": ["happy", "little", "brave", "kind"],
            "pumpkin": ["huge", "orange", "round", "heavy"],
        },
    },
    {
        "template": "My {brother} raked the {leaves}.",
        "suggestions": {
            "brother": ["older", "strong", "helpful", "tired"],
            "leaves": ["colorful", "dry", "crispy", "fallen"],
        },
    },
    {
        "template": "The {cat} sat on the {porch}.",
        "suggestions": {
            "cat": ["fluffy", "sleepy", "orange", "quiet"],
            "porch": ["wooden", "sunny", "front", "creaky"],
        },
    },
    {
        "template": "A {crow} flew over the {field}.",
        "suggestions": {
            "crow": ["black", "loud", "clever", "large"],
            "field": ["open", "golden", "wide", "dusty"],
        },
    },
    {
        "template": "The {farmer} picked the {apples}.",
        "suggestions": {
            "farmer": ["kind", "busy", "strong", "cheerful"],
            "apples": ["red", "sweet", "ripe", "shiny"],
        },
    },
    {
        "template": "Our {class} made a {scarecrow}.",
        "suggestions": {
            "class": ["creative", "excited", "noisy", "proud"],
            "scarecrow": ["funny", "tall", "friendly", "ragged"],
        },
    },
    {
        "template": "The {boy} jumped in the {pile}.",
        "suggestions": {
            "boy": ["joyful", "young", "eager", "silly"],
            "pile": ["huge", "leafy", "soft", "colorful"],
        },
    },
    {
        "template": "An {owl} sat in the {barn}.",
        "suggestions": {
            "owl": ["wise", "quiet", "brown", "watchful"],
            "barn": ["old", "red", "dusty", "wooden"],
        },
    },
    {
        "template": "The {wind} blew the {hat}.",
        "suggestions": {
            "wind": ["cold", "strong", "autumn", "gusty"],
            "hat": ["wool", "blue", "floppy", "warm"],
        },
    },
    {
        "template": "My {sister} drank warm {cider}.",
        "suggestions": {
            "sister": ["thirsty", "smiling", "little", "cozy"],
            "cider": ["sweet", "spicy", "apple", "steamy"],
        },
    },
    {
        "template": "The {dog} chased the {leaves}.",
        "suggestions": {
            "dog": ["playful", "brown", "speedy", "happy"],
            "leaves": ["swirling", "dry", "yellow", "flying"],
        },
    },
    {
        "template": "A {wagon} rolled down the {hill}.",
        "suggestions": {
            "wagon": ["red", "wooden", "heavy", "creaky"],
            "hill": ["steep", "grassy", "long", "bumpy"],
        },
    },
    {
        "template": "The {cook} baked a {pie}.",
        "suggestions": {
            "cook": ["careful", "skilled", "busy", "cheerful"],
            "pie": ["pumpkin", "warm", "sweet", "golden"],
        },
    },
    {
        "template": "Our {family} visited the {orchard}.",
        "suggestions": {
            "family": ["happy", "large", "excited", "close"],
            "orchard": ["apple", "sunny", "quiet", "busy"],
        },
    },
    {
        "template": "The {pumpkin} sat on the {steps}.",
        "suggestions": {
            "pumpkin": ["plump", "orange", "carved", "round"],
            "steps": ["front", "stone", "wooden", "cold"],
        },
    },
    {
        "template": "A {goose} walked by the {pond}.",
        "suggestions": {
            "goose": ["white", "noisy", "proud", "fat"],
            "pond": ["still", "cool", "muddy", "small"],
        },
    },
    {
        "template": "The {kids} rode on a {hayride}.",
        "suggestions": {
            "kids": ["excited", "laughing", "bundled", "happy"],
            "hayride": ["bumpy", "fun", "long", "crowded"],
        },
    },
    {
        "template": "My {friend} wore a {sweater}.",
        "suggestions": {
            "friend": ["best", "kind", "funny", "new"],
            "sweater": ["cozy", "orange", "soft", "thick"],
        },
    },
    {
        "template": "The {corn} grew in the {field}.",
        "suggestions": {
            "corn": ["tall", "yellow", "sweet", "ripe"],
            "field": ["wide", "sunny", "dusty", "green"],
        },
    },
    {
        "template": "A {spider} spun a {web}.",
        "suggestions": {
            "spider": ["tiny", "busy", "black", "clever"],
            "web": ["sticky", "shiny", "delicate", "round"],
        },
    },
    {
        "template": "The {teacher} read a {story}.",
        "suggestions": {
            "teacher": ["kind", "patient", "cheerful", "calm"],
            "story": ["funny", "fall", "exciting", "short"],
        },
    },
    {
        "template": "Our {class} painted {leaves}.",
        "suggestions": {
            "class": ["artistic", "quiet", "proud", "busy"],
            "leaves": ["bright", "paper", "colorful", "pretty"],
        },
    },
    {
        "template": "The {moon} shone on the {farm}.",
        "suggestions": {
            "moon": ["bright", "full", "silver", "round"],
            "farm": ["quiet", "sleepy", "peaceful", "small"],
        },
    },
    {
        "template": "A {chipmunk} ran up the {tree}.",
        "suggestions": {
            "chipmunk": ["striped", "quick", "tiny", "nervous"],
            "tree": ["tall", "oak", "rough", "shady"],
        },
    },
    {
        "template": "The {bus} stopped at the {farm}.",
        "suggestions": {
            "bus": ["yellow", "noisy", "crowded", "big"],
            "farm": ["busy", "pumpkin", "friendly", "large"],
        },
    },
    {
        "template": "My {cousin} carved a {pumpkin}.",
        "suggestions": {
            "cousin": ["older", "careful", "silly", "talented"],
            "pumpkin": ["round", "orange", "heavy", "fresh"],
        },
    },
    {
        "template": "The {apple} hung on the {branch}.",
        "suggestions": {
            "apple": ["red", "juicy", "shiny", "ripe"],
            "branch": ["high", "thin", "sturdy", "leafy"],
        },
    },
    {
        "template": "A {rake} leaned on the {fence}.",
        "suggestions": {
            "rake": ["metal", "old", "long", "rusty"],
            "fence": ["wooden", "white", "garden", "broken"],
        },
    },
    {
        "template": "The {mud} covered my {boots}.",
        "suggestions": {
            "mud": ["thick", "brown", "sticky", "wet"],
            "boots": ["rain", "rubber", "new", "tall"],
        },
    },
    {
        "template": "Our {neighbors} hung a {wreath}.",
        "suggestions": {
            "neighbors": ["friendly", "kind", "new", "cheerful"],
            "wreath": ["autumn", "pretty", "leafy", "colorful"],
        },
    },
    {
        "template": "The {fox} ran through the {woods}.",
        "suggestions": {
            "fox": ["sly", "red", "quick", "quiet"],
            "woods": ["dark", "thick", "cool", "quiet"],
        },
    },
    {
        "template": "A {basket} held the {apples}.",
        "suggestions": {
            "basket": ["woven", "full", "brown", "sturdy"],
            "apples": ["crisp", "red", "fresh", "sweet"],
        },
    },
    {
        "template": "The {sun} warmed the {pumpkin}.",
        "suggestions": {
            "sun": ["bright", "warm", "afternoon", "golden"],
            "pumpkin": ["orange", "round", "plump", "smooth"],
        },
    },
    {
        "template": "My {grandma} made {soup}.",
        "suggestions": {
            "grandma": ["loving", "careful", "smiling", "busy"],
            "soup": ["hot", "squash", "tasty", "hearty"],
        },
    },
    {
        "template": "The {tractor} pulled the {wagon}.",
        "suggestions": {
            "tractor": ["green", "loud", "powerful", "old"],
            "wagon": ["full", "wooden", "hay", "heavy"],
        },
    },
    {
        "template": "A {mushroom} grew by the {stump}.",
        "suggestions": {
            "mushroom": ["tiny", "brown", "spotted", "soft"],
            "stump": ["old", "mossy", "wet", "rotting"],
        },
    },
    {
        "template": "The {kids} found {acorns}.",
        "suggestions": {
            "kids": ["curious", "excited", "young", "lucky"],
            "acorns": ["smooth", "brown", "fallen", "plump"],
        },
    },
    {
        "template": "Our {school} had a {parade}.",
        "suggestions": {
            "school": ["busy", "cheerful", "local", "proud"],
            "parade": ["fall", "noisy", "fun", "colorful"],
        },
    },
    {
        "template": "The {horse} ate fresh {hay}.",
        "suggestions": {
            "horse": ["brown", "gentle", "hungry", "tall"],
            "hay": ["dry", "golden", "sweet", "soft"],
        },
    },
    {
        "template": "A {mouse} hid under the {leaf}.",
        "suggestions": {
            "mouse": ["tiny", "brown", "shy", "quick"],
            "leaf": ["crumpled", "orange", "wide", "dry"],
        },
    },
    {
        "template": "The {baker} sold warm {bread}.",
        "suggestions": {
            "baker": ["friendly", "busy", "smiling", "kind"],
            "bread": ["fresh", "crusty", "soft", "brown"],
        },
    },
    {
        "template": "My {dad} lit the {fire}.",
        "suggestions": {
            "dad": ["careful", "strong", "helpful", "calm"],
            "fire": ["warm", "bright", "crackling", "safe"],
        },
    },
    {
        "template": "The {turkey} walked across the {yard}.",
        "suggestions": {
            "turkey": ["fat", "wild", "proud", "noisy"],
            "yard": ["leafy", "back", "grassy", "messy"],
        },
    },
    {
        "template": "A {bee} buzzed near the {flower}.",
        "suggestions": {
            "bee": ["busy", "striped", "tiny", "loud"],
            "flower": ["yellow", "late", "bright", "sweet"],
        },
    },
    {
        "template": "The {fog} covered the {road}.",
        "suggestions": {
            "fog": ["thick", "gray", "morning", "cool"],
            "road": ["winding", "quiet", "dirt", "empty"],
        },
    },
    {
        "template": "Our {class} picked {gourds}.",
        "suggestions": {
            "class": ["eager", "noisy", "curious", "happy"],
            "gourds": ["bumpy", "colorful", "odd", "small"],
        },
    },
    {
        "template": "The {shadow} stretched across the {lawn}.",
        "suggestions": {
            "shadow": ["long", "dark", "cool", "thin"],
            "lawn": ["green", "front", "leafy", "soft"],
        },
    },
    {
        "template": "A {picnic} waited under the {tree}.",
        "suggestions": {
            "picnic": ["tasty", "ready", "simple", "cozy"],
            "tree": ["shady", "maple", "wide", "tall"],
        },
    },
]


def parse_sentence(template):
    """Turn a braced template into (text, highlighted) parts."""
    parts = []
    i = 0
    while i < len(template):
        if template[i] == "{":
            end = template.find("}", i)
            if end < 0:
                raise RuntimeError(f"Unclosed brace in: {template}")
            noun = template[i + 1 : end]
            if not noun:
                raise RuntimeError(f"Empty noun in: {template}")
            parts.append((noun, True))
            i = end + 1
        else:
            end = template.find("{", i)
            if end < 0:
                end = len(template)
            text = template[i:end]
            if text:
                parts.append((text, False))
            i = end
    if not any(flag for _, flag in parts):
        raise RuntimeError(f"No highlighted nouns in: {template}")
    return parts


def nouns_in(parts):
    return [text for text, highlighted in parts if highlighted]


def plain_sentence(parts):
    return "".join(text for text, _ in parts)


def number_column_width():
    widest = f"{ITEMS_PER_PAGE * STUDENT_PAGES}. "
    return pdfmetrics.stringWidth(widest, "Helvetica-Bold", BODY_SIZE)


def wrap_parts(parts, font, bold_font, size, width):
    """Wrap mixed regular/bold parts into lines of (text, highlighted) chunks."""
    lines = []
    current = []
    current_width = 0

    tokens = []
    for text, highlighted in parts:
        face = bold_font if highlighted else font
        if highlighted:
            tokens.append((text, True, face))
            continue
        words = text.split(" ")
        for index, word in enumerate(words):
            if word:
                tokens.append((word, False, face))
            if index < len(words) - 1:
                tokens.append((" ", False, face))

    for text, highlighted, face in tokens:
        token_width = pdfmetrics.stringWidth(text, face, size)
        if text == " " and not current:
            continue
        if current and current_width + token_width > width and text != " ":
            lines.append(current)
            current = []
            current_width = 0
        if text == " " and current_width + token_width > width:
            lines.append(current)
            current = []
            current_width = 0
            continue
        current.append((text, highlighted, face))
        current_width += token_width

    if current:
        lines.append(current)
    return lines


def wrap_text(text, font, size, width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_mixed_line(c, x, y, chunks, size):
    cursor = x
    for text, highlighted, face in chunks:
        width = pdfmetrics.stringWidth(text, face, size)
        if highlighted and text.strip():
            pad = 1.5
            c.setFillColorRGB(1, 0.95, 0.55)
            c.rect(
                cursor - pad,
                y - 3,
                width + (pad * 2),
                size + 2,
                stroke=0,
                fill=1,
            )
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(0.9)
            c.line(cursor, y - 2, cursor + width, y - 2)
        c.setFillColorRGB(0, 0, 0)
        c.setFont(face, size)
        c.drawString(cursor, y, text)
        cursor += width
    return cursor


def draw_header(c):
    y = PAGE_H - TOP
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", TITLE_SIZE)
    c.drawString(LEFT, y, "Add Descriptive Adjectives")
    c.setFont("Helvetica", BODY_SIZE)
    c.drawRightString(PAGE_W - RIGHT, y, "Grade 2 - Fall")

    y -= 26
    c.setFont("Helvetica", BODY_SIZE)
    c.drawString(LEFT, y, "Name:")
    name_line = LEFT + c.stringWidth("Name: ", "Helvetica", BODY_SIZE)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_line, y - 2, name_line + 220, y - 2)

    date_label = name_line + 250
    c.drawString(date_label, y, "Date:")
    date_line = date_label + c.stringWidth("Date: ", "Helvetica", BODY_SIZE)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)

    y -= 14
    c.setLineWidth(1)
    c.line(LEFT, y, PAGE_W - RIGHT, y)
    return y - 12


def draw_directions(c, y):
    width = PAGE_W - LEFT - RIGHT
    directions = (
        "Each highlighted word is a noun. Add a descriptive adjective before "
        "each highlighted noun to make the sentence more interesting. Write "
        "your new sentence on the lines."
    )
    lines = wrap_text(directions, "Helvetica", DIR_SIZE, width)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", DIR_SIZE)
    for line in lines:
        c.drawString(LEFT, y, line)
        y -= DIR_LEADING

    y -= 4
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(0.8)
    c.line(LEFT, y, PAGE_W - RIGHT, y)
    return y - 14


def draw_item(c, number, parts, slot_top, slot_bottom):
    width = PAGE_W - LEFT - RIGHT
    number_label = f"{number}."
    number_width = number_column_width()
    text_width = width - number_width

    lines = wrap_parts(
        parts, "Helvetica", "Helvetica-Bold", BODY_SIZE, text_width
    )
    y = slot_top - BODY_SIZE
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", BODY_SIZE)
    c.drawString(LEFT, y, number_label)

    for line in lines:
        draw_mixed_line(c, LEFT + number_width, y, line, BODY_SIZE)
        y -= BODY_LEADING

    y -= 4
    c.setFont("Helvetica", BODY_SIZE)
    c.drawString(LEFT + number_width, y, "New sentence:")
    y -= 20

    c.setStrokeColorRGB(0.35, 0.35, 0.35)
    c.setLineWidth(0.8)
    for _ in range(WRITE_LINES):
        if y < slot_bottom + 4:
            raise RuntimeError(
                f"Item {number} does not fit with {WRITE_LINES} lines"
            )
        c.line(LEFT + number_width, y, PAGE_W - RIGHT, y)
        y -= LINE_GAP


def draw_page_number(c, page, total):
    label = f"Page {page} of {total}"
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", BODY_SIZE)
    c.drawCentredString(PAGE_W / 2, 24, label)


def write_student_packet(path, items):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Add Descriptive Adjectives - Grade 2 Fall")
    content_bottom = 46

    for page in range(STUDENT_PAGES):
        if page:
            c.showPage()
        y = draw_header(c)
        content_top = draw_directions(c, y)
        slot_height = (content_top - content_bottom) / ITEMS_PER_PAGE
        start = page * ITEMS_PER_PAGE
        for offset in range(ITEMS_PER_PAGE):
            number = start + offset + 1
            slot_top = content_top - offset * slot_height
            slot_bottom = slot_top - slot_height
            draw_item(
                c, number, items[number - 1]["parts"], slot_top, slot_bottom
            )
        draw_page_number(c, page + 1, STUDENT_PAGES)

    c.save()


def key_entry_lines(number, item, width):
    indent = "    "
    lines = []
    heading = f"{number}. {plain_sentence(item['parts'])}"
    lines.extend(wrap_text(heading, "Helvetica-Bold", KEY_SIZE, width))
    for noun in nouns_in(item["parts"]):
        suggestions = ", ".join(item["suggestions"][noun])
        text = f"{indent}{noun}: {suggestions}"
        lines.extend(wrap_text(text, "Helvetica", KEY_SIZE, width))
    return lines


def answer_key_pages(items):
    width = PAGE_W - LEFT - RIGHT
    entries = [key_entry_lines(n, item, width) for n, item in enumerate(items, 1)]
    usable = 642
    pages = []
    current = []
    used = 0
    for lines in entries:
        height = len(lines) * KEY_LEADING + 8
        if current and used + height > usable:
            pages.append(current)
            current = []
            used = 0
        current.append(lines)
        used += height
    if current:
        pages.append(current)
    return pages


def write_answer_key(path, items):
    pages = answer_key_pages(items)
    total = len(pages)
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Answer Key: Add Descriptive Adjectives - Grade 2 Fall")

    for page_index, entries in enumerate(pages):
        if page_index:
            c.showPage()
        y = PAGE_H - TOP
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", TITLE_SIZE)
        c.drawString(LEFT, y, "Answer Key")
        y -= 20
        c.setFont("Helvetica", BODY_SIZE)
        c.drawString(LEFT, y, "Add Descriptive Adjectives - Grade 2 Fall")
        y -= 18
        note = (
            "Suggested adjectives for each highlighted noun. "
            "Other fitting adjectives are also correct."
        )
        for line in wrap_text(note, "Helvetica-Oblique", KEY_SIZE, PAGE_W - LEFT - RIGHT):
            c.setFont("Helvetica-Oblique", KEY_SIZE)
            c.drawString(LEFT, y, line)
            y -= KEY_LEADING
        y -= 4
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, y, PAGE_W - RIGHT, y)
        y -= 18

        for lines in entries:
            for line in lines:
                if line[:1].isdigit():
                    c.setFont("Helvetica-Bold", KEY_SIZE)
                else:
                    c.setFont("Helvetica", KEY_SIZE)
                c.drawString(LEFT, y, line)
                y -= KEY_LEADING
            y -= 8

        draw_page_number(c, page_index + 1, total)

    c.save()
    return total


def build_items(raw):
    expected = ITEMS_PER_PAGE * STUDENT_PAGES
    if len(raw) != expected:
        raise RuntimeError(f"Expected {expected} items, got {len(raw)}")

    items = []
    width = PAGE_W - LEFT - RIGHT - number_column_width()
    for index, raw_item in enumerate(raw, start=1):
        parts = parse_sentence(raw_item["template"])
        nouns = nouns_in(parts)
        suggestions = raw_item["suggestions"]
        if set(suggestions) != set(nouns):
            raise RuntimeError(
                f"Item {index} suggestion nouns {sorted(suggestions)} "
                f"do not match sentence nouns {nouns}"
            )
        for noun in nouns:
            words = suggestions[noun]
            if len(words) != SUGGESTIONS_PER_NOUN:
                raise RuntimeError(
                    f"Item {index} noun {noun!r} needs "
                    f"{SUGGESTIONS_PER_NOUN} suggestions, got {len(words)}"
                )
            if any(" " in word or not word for word in words):
                raise RuntimeError(
                    f"Item {index} has a bad suggestion for {noun!r}: {words}"
                )
        lines = wrap_parts(
            parts, "Helvetica", "Helvetica-Bold", BODY_SIZE, width
        )
        if len(lines) > 2:
            raise RuntimeError(
                f"Sentence {index} wraps to {len(lines)} lines: "
                f"{plain_sentence(parts)}"
            )
        items.append(
            {
                "parts": parts,
                "suggestions": suggestions,
            }
        )
    return items


def main():
    items = build_items(RAW_ITEMS)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, items)
    key_pages = write_answer_key(ANSWER_KEY_PDF, items)
    print(
        f"Wrote {STUDENT_PDF} "
        f"({STUDENT_PAGES} pages, {len(items)} sentences)"
    )
    print(f"Wrote {ANSWER_KEY_PDF} ({key_pages} pages)")


if __name__ == "__main__":
    main()
