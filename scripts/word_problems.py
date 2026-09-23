#!/usr/bin/env python3
"""Build the multi-step addition and subtraction word-problem PDFs.

Writes a 10-page student packet (5 problems per page) and a separate
answer key into math/word-problems/.
"""

import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "math" / "word-problems"
STUDENT_PDF = OUT_DIR / "addition-subtraction-3-digit-multistep.pdf"
ANSWER_KEY_PDF = OUT_DIR / "addition-subtraction-3-digit-multistep-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 48
RIGHT = 48
STORY_SIZE = 14
STORY_LEADING = 18
PROBLEMS_PER_PAGE = 5
STUDENT_PAGES = 10

# Each item is one two-step story. {a}, {b}, and {c} are the only numbers.
RAW_PROBLEMS = [
    {
        "a": 248,
        "op1": "+",
        "b": 36,
        "op2": "-",
        "c": 75,
        "unit": "crayons",
        "template": (
            "Maya has {a} crayons. She buys {b} more. Then she gives {c} "
            "crayons to her class. How many crayons does Maya have left?"
        ),
    },
    {
        "a": 415,
        "op1": "-",
        "b": 128,
        "op2": "+",
        "c": 64,
        "unit": "books",
        "template": (
            "A shelf has {a} books. Students check out {b} books. Then {c} "
            "new books are added. How many books are on the shelf now?"
        ),
    },
    {
        "a": 186,
        "op1": "+",
        "b": 97,
        "op2": "+",
        "c": 45,
        "unit": "sandwiches",
        "template": (
            "The cafeteria made {a} cheese sandwiches and {b} turkey sandwiches. "
            "They also made {c} ham sandwiches. How many sandwiches did they make in all?"
        ),
    },
    {
        "a": 530,
        "op1": "-",
        "b": 145,
        "op2": "-",
        "c": 80,
        "unit": "points",
        "template": (
            "Jordan had {a} points. He used {b} points on a prize. Then he used "
            "{c} more points. How many points does Jordan have left?"
        ),
    },
    {
        "a": 162,
        "op1": "+",
        "b": 85,
        "op2": "-",
        "c": 47,
        "unit": "fish",
        "template": (
            "The pet store has {a} fish. A delivery brings {b} more fish. "
            "The store sells {c} fish. How many fish are left?"
        ),
    },
    {
        "a": 256,
        "op1": "+",
        "b": 119,
        "op2": "-",
        "c": 150,
        "unit": "cans",
        "template": (
            "A class collected {a} cans. They collected {b} more cans the next day. "
            "They gave {c} cans to a food bank. How many cans do they still have?"
        ),
    },
    {
        "a": 640,
        "op1": "-",
        "b": 275,
        "op2": "+",
        "c": 80,
        "unit": "bottles",
        "template": (
            "Field day started with {a} bottles of water. Students drank {b} bottles. "
            "The coach brought {c} more bottles. How many bottles are there now?"
        ),
    },
    {
        "a": 134,
        "op1": "+",
        "b": 87,
        "op2": "+",
        "c": 56,
        "unit": "balls",
        "template": (
            "The gym has {a} red balls and {b} blue balls. Then {c} green balls "
            "are added. How many balls are there in all?"
        ),
    },
    {
        "a": 810,
        "op1": "-",
        "b": 265,
        "op2": "-",
        "c": 178,
        "unit": "apples",
        "template": (
            "A store had {a} apples. It sold {b} apples in the morning and {c} "
            "apples in the afternoon. How many apples are left?"
        ),
    },
    {
        "a": 95,
        "op1": "+",
        "b": 128,
        "op2": "-",
        "c": 46,
        "unit": "stickers",
        "template": (
            "Lena has {a} stickers. Her brother gives her {b} stickers. She uses "
            "{c} stickers on a card. How many stickers does Lena have now?"
        ),
    },
    {
        "a": 450,
        "op1": "-",
        "b": 125,
        "op2": "-",
        "c": 60,
        "unit": "dollars",
        "template": (
            "Noah saved {a} dollars. He spent {b} dollars on a bike repair and "
            "{c} dollars on a helmet. How much money does Noah have left?"
        ),
    },
    {
        "a": 308,
        "op1": "+",
        "b": 146,
        "op2": "-",
        "c": 220,
        "unit": "carrots",
        "template": (
            "A farmer picked {a} carrots on Monday and {b} carrots on Tuesday. "
            "He sold {c} carrots. How many carrots does he have left?"
        ),
    },
    {
        "a": 500,
        "op1": "-",
        "b": 186,
        "op2": "-",
        "c": 74,
        "unit": "seats",
        "template": (
            "There are {a} seats in the auditorium. First, {b} students sit down. "
            "Then {c} more students sit down. How many seats are empty?"
        ),
    },
    {
        "a": 73,
        "op1": "+",
        "b": 150,
        "op2": "-",
        "c": 89,
        "unit": "marbles",
        "template": (
            "Priya had {a} marbles. She won {b} marbles in a game. Then she gave "
            "{c} marbles to her sister. How many marbles does Priya have?"
        ),
    },
    {
        "a": 267,
        "op1": "-",
        "b": 98,
        "op2": "+",
        "c": 140,
        "unit": "sheets",
        "template": (
            "The art room has {a} sheets of paper. Students use {b} sheets. "
            "The teacher puts out {c} more sheets. How many sheets are there now?"
        ),
    },
    {
        "a": 142,
        "op1": "+",
        "b": 88,
        "op2": "+",
        "c": 35,
        "unit": "treats",
        "template": (
            "The bake sale had {a} cookies and {b} brownies. There were also "
            "{c} cupcakes. How many treats were there in all?"
        ),
    },
    {
        "a": 360,
        "op1": "-",
        "b": 95,
        "op2": "+",
        "c": 40,
        "unit": "lunches",
        "template": (
            "The bus had {a} lunches. Students ate {b} lunches at the park. "
            "Then {c} more lunches were packed. How many lunches are there now?"
        ),
    },
    {
        "a": 720,
        "op1": "-",
        "b": 210,
        "op2": "-",
        "c": 155,
        "unit": "cards",
        "template": (
            "Diego had {a} baseball cards. He gave {b} cards to his cousin. "
            "Then he gave {c} cards to a friend. How many cards does Diego have left?"
        ),
    },
    {
        "a": 184,
        "op1": "+",
        "b": 96,
        "op2": "+",
        "c": 47,
        "unit": "flowers",
        "template": (
            "The garden club planted {a} flowers on Friday and {b} flowers on Saturday. "
            "They planted {c} more flowers on Sunday. How many flowers did they plant in all?"
        ),
    },
    {
        "a": 590,
        "op1": "-",
        "b": 134,
        "op2": "+",
        "c": 75,
        "unit": "puzzles",
        "template": (
            "A toy store had {a} puzzles. It sold {b} puzzles on Saturday. "
            "Then {c} new puzzles arrived. How many puzzles does the store have now?"
        ),
    },
    {
        "a": 215,
        "op1": "+",
        "b": 64,
        "op2": "-",
        "c": 90,
        "unit": "pencils",
        "template": (
            "Ms. Alvarez had {a} pencils. She bought {b} more pencils. She gave "
            "{c} pencils to her students. How many pencils does she have left?"
        ),
    },
    {
        "a": 480,
        "op1": "-",
        "b": 196,
        "op2": "+",
        "c": 85,
        "unit": "juice boxes",
        "template": (
            "The snack cart had {a} juice boxes. Students bought {b} juice boxes. "
            "Then {c} more juice boxes were stocked. How many juice boxes are on the cart now?"
        ),
    },
    {
        "a": 126,
        "op1": "+",
        "b": 203,
        "op2": "+",
        "c": 58,
        "unit": "books",
        "template": (
            "Room 12 read {a} books in September and {b} books in October. "
            "They read {c} books in November. How many books did they read in all?"
        ),
    },
    {
        "a": 750,
        "op1": "-",
        "b": 280,
        "op2": "-",
        "c": 165,
        "unit": "ears of corn",
        "template": (
            "A farm stand had {a} ears of corn. It sold {b} ears in the morning "
            "and {c} ears in the afternoon. How many ears of corn are left?"
        ),
    },
    {
        "a": 88,
        "op1": "+",
        "b": 147,
        "op2": "-",
        "c": 62,
        "unit": "rocks",
        "template": (
            "Kai collected {a} rocks. He found {b} more rocks at the creek. "
            "He gave {c} rocks to the science table. How many rocks does Kai have now?"
        ),
    },
    {
        "a": 154,
        "op1": "+",
        "b": 79,
        "op2": "+",
        "c": 42,
        "unit": "folders",
        "template": (
            "The choir has {a} red folders and {b} blue folders. They get {c} "
            "new black folders. How many folders does the choir have in all?"
        ),
    },
    {
        "a": 625,
        "op1": "-",
        "b": 240,
        "op2": "+",
        "c": 118,
        "unit": "cars",
        "template": (
            "A parking lot has {a} cars in the morning. Then {b} cars leave. "
            "Later, {c} more cars park. How many cars are in the lot now?"
        ),
    },
    {
        "a": 340,
        "op1": "-",
        "b": 127,
        "op2": "-",
        "c": 86,
        "unit": "bandages",
        "template": (
            "The nurse had {a} bandages. She used {b} bandages on Monday and "
            "{c} bandages on Tuesday. How many bandages are left?"
        ),
    },
    {
        "a": 173,
        "op1": "+",
        "b": 86,
        "op2": "+",
        "c": 54,
        "unit": "food items",
        "template": (
            "Students brought {a} cans of soup and {b} boxes of pasta. They also "
            "brought {c} jars of sauce. How many food items did they bring in all?"
        ),
    },
    {
        "a": 900,
        "op1": "-",
        "b": 375,
        "op2": "-",
        "c": 240,
        "unit": "beads",
        "template": (
            "Elena had {a} beads. She used {b} beads for a necklace. Then she used "
            "{c} beads for a bracelet. How many beads does Elena have left?"
        ),
    },
    {
        "a": 212,
        "op1": "+",
        "b": 68,
        "op2": "+",
        "c": 45,
        "unit": "items",
        "template": (
            "The book fair sold {a} posters and {b} bookmarks. It also sold "
            "{c} pencils. How many items did the book fair sell?"
        ),
    },
    {
        "a": 470,
        "op1": "-",
        "b": 195,
        "op2": "+",
        "c": 160,
        "unit": "visitors",
        "template": (
            "A zoo had {a} visitors in the morning. Then {b} visitors left at lunch. "
            "After lunch, {c} more visitors arrived. How many visitors are at the zoo now?"
        ),
    },
    {
        "a": 156,
        "op1": "+",
        "b": 89,
        "op2": "+",
        "c": 74,
        "unit": "papers",
        "template": (
            "Mr. Chen has {a} math papers and {b} reading papers. He also has "
            "{c} science papers. How many papers is that in all?"
        ),
    },
    {
        "a": 800,
        "op1": "-",
        "b": 245,
        "op2": "-",
        "c": 190,
        "unit": "gallons",
        "template": (
            "A tank holds {a} gallons of water. Workers drain {b} gallons. "
            "Then they drain {c} more gallons. How many gallons are left in the tank?"
        ),
    },
    {
        "a": 64,
        "op1": "+",
        "b": 119,
        "op2": "+",
        "c": 27,
        "unit": "stickers",
        "template": (
            "Sofia has {a} animal stickers and {b} sports stickers. She buys "
            "{c} star stickers. How many stickers does Sofia have in all?"
        ),
    },
    {
        "a": 555,
        "op1": "-",
        "b": 230,
        "op2": "+",
        "c": 145,
        "unit": "apples",
        "template": (
            "The lunchroom had {a} apples. Students ate {b} apples. The kitchen "
            "brought out {c} more apples. How many apples are there now?"
        ),
    },
    {
        "a": 128,
        "op1": "+",
        "b": 76,
        "op2": "+",
        "c": 95,
        "unit": "miles",
        "template": (
            "A scout troop hiked {a} miles in May and {b} miles in June. "
            "They hiked {c} miles in July. How many miles did they hike in all?"
        ),
    },
    {
        "a": 670,
        "op1": "-",
        "b": 285,
        "op2": "-",
        "c": 140,
        "unit": "erasers",
        "template": (
            "The school store had {a} erasers. It sold {b} erasers this week and "
            "{c} erasers last week. How many erasers are left?"
        ),
    },
    {
        "a": 92,
        "op1": "+",
        "b": 135,
        "op2": "-",
        "c": 48,
        "unit": "towers",
        "template": (
            "Jamal built {a} block towers. He built {b} more towers after school. "
            "Then {c} towers fell down. How many towers are still standing?"
        ),
    },
    {
        "a": 201,
        "op1": "+",
        "b": 144,
        "op2": "+",
        "c": 63,
        "unit": "pieces of art",
        "template": (
            "The art show has {a} drawings and {b} paintings. There are also "
            "{c} photos. How many pieces of art are in the show?"
        ),
    },
    {
        "a": 430,
        "op1": "-",
        "b": 175,
        "op2": "+",
        "c": 90,
        "unit": "passengers",
        "template": (
            "A train had {a} passengers. Then {b} passengers got off. Next, "
            "{c} passengers got on. How many passengers are on the train now?"
        ),
    },
    {
        "a": 260,
        "op1": "-",
        "b": 84,
        "op2": "-",
        "c": 57,
        "unit": "jump ropes",
        "template": (
            "The gym teacher had {a} jump ropes. Students took {b} jump ropes outside. "
            "Then they took {c} more jump ropes to the field. How many jump ropes are left in the gym?"
        ),
    },
    {
        "a": 157,
        "op1": "+",
        "b": 68,
        "op2": "+",
        "c": 42,
        "unit": "berries",
        "template": (
            "Nina picked {a} strawberries and {b} blueberries. She also picked "
            "{c} raspberries. How many berries did Nina pick in all?"
        ),
    },
    {
        "a": 315,
        "op1": "-",
        "b": 120,
        "op2": "+",
        "c": 48,
        "unit": "chairs",
        "template": (
            "A classroom had {a} chairs. Workers moved {b} chairs to the cafeteria. "
            "Then they moved {c} chairs back. How many chairs are in the classroom now?"
        ),
    },
    {
        "a": 188,
        "op1": "+",
        "b": 207,
        "op2": "+",
        "c": 96,
        "unit": "items",
        "template": (
            "The recycling club gathered {a} plastic bottles and {b} glass bottles. "
            "They also gathered {c} metal cans. How many items did they gather in all?"
        ),
    },
    {
        "a": 640,
        "op1": "-",
        "b": 255,
        "op2": "-",
        "c": 180,
        "unit": "tickets",
        "template": (
            "Owen had {a} tickets. He used {b} tickets for rides and {c} tickets "
            "for games. How many tickets does Owen have left?"
        ),
    },
    {
        "a": 109,
        "op1": "+",
        "b": 86,
        "op2": "-",
        "c": 70,
        "unit": "muffins",
        "template": (
            "A bakery made {a} muffins in the morning and {b} muffins in the afternoon. "
            "It sold {c} muffins. How many muffins are left?"
        ),
    },
    {
        "a": 512,
        "op1": "-",
        "b": 190,
        "op2": "+",
        "c": 75,
        "unit": "ducks",
        "template": (
            "The pond had {a} ducks. Then {b} ducks flew away. Later, {c} more "
            "ducks landed. How many ducks are at the pond now?"
        ),
    },
    {
        "a": 143,
        "op1": "+",
        "b": 98,
        "op2": "+",
        "c": 55,
        "unit": "paper cranes",
        "template": (
            "Students made {a} paper cranes on Monday and {b} paper cranes on Tuesday. "
            "They made {c} paper cranes on Wednesday. How many paper cranes did they make in all?"
        ),
    },
    {
        "a": 980,
        "op1": "-",
        "b": 420,
        "op2": "-",
        "c": 315,
        "unit": "boxes",
        "template": (
            "A warehouse had {a} boxes. Trucks took {b} boxes in the morning and "
            "{c} boxes in the afternoon. How many boxes are left?"
        ),
    },
]


def apply_op(left, op, right):
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    raise ValueError(f"Unknown operation: {op}")


def build_problems(raw_problems):
    if len(raw_problems) != STUDENT_PAGES * PROBLEMS_PER_PAGE:
        raise ValueError(
            f"Expected {STUDENT_PAGES * PROBLEMS_PER_PAGE} problems, got {len(raw_problems)}"
        )

    problems = []
    for index, raw in enumerate(raw_problems, start=1):
        a, b, c = raw["a"], raw["b"], raw["c"]
        op1, op2 = raw["op1"], raw["op2"]
        for label, value in (("a", a), ("b", b), ("c", c)):
            if not isinstance(value, int) or not 0 <= value <= 999:
                raise ValueError(f"Problem {index} {label}={value} is not a whole number up to 3 digits")

        mid = apply_op(a, op1, b)
        final = apply_op(mid, op2, c)
        for label, value in (("step 1", mid), ("answer", final)):
            if not 0 <= value <= 999:
                raise ValueError(f"Problem {index} {label}={value} is outside 0 to 999")

        text = raw["template"].format(a=a, b=b, c=c)
        for value in (a, b, c):
            if not re.search(rf"\b{value}\b", text):
                raise ValueError(f"Problem {index} text is missing {value}")

        problems.append(
            {
                "text": text,
                "steps": [f"{a} {op1} {b} = {mid}", f"{mid} {op2} {c} = {final}"],
                "answer": f"{final} {raw['unit']}",
            }
        )
    return problems


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


def draw_page_number(c, page, total):
    label = f"Page {page} of {total}"
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", STORY_SIZE)
    c.drawCentredString(PAGE_W / 2, 24, label)


def draw_student_header(c):
    y = PAGE_H - 42
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, "Addition and Subtraction Word Problems")

    y -= 28
    c.setFont("Helvetica", STORY_SIZE)
    c.drawString(LEFT, y, "Name:")
    name_line = LEFT + c.stringWidth("Name: ", "Helvetica", STORY_SIZE)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_line, y - 2, name_line + 210, y - 2)

    date_label = name_line + 240
    c.drawString(date_label, y, "Date:")
    date_line = date_label + c.stringWidth("Date: ", "Helvetica", STORY_SIZE)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)

    y -= 14
    c.setLineWidth(1)
    c.line(LEFT, y, PAGE_W - RIGHT, y)
    return y - 8


def number_column_width():
    return pdfmetrics.stringWidth("50. ", "Helvetica-Bold", STORY_SIZE)


def draw_problem(c, number, problem, slot_top, slot_height):
    number_label = f"{number}."
    number_width = number_column_width()
    text_width = PAGE_W - LEFT - RIGHT - number_width
    lines = wrap_text(problem["text"], "Helvetica", STORY_SIZE, text_width)

    y = slot_top - STORY_SIZE
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", STORY_SIZE)
    c.drawString(LEFT, y, number_label)
    c.setFont("Helvetica", STORY_SIZE)
    c.drawString(LEFT + number_width, y, lines[0])
    y -= STORY_LEADING
    for line in lines[1:]:
        c.drawString(LEFT + number_width, y, line)
        y -= STORY_LEADING

    answer_y = slot_top - slot_height + 18
    if answer_y > y - 10:
        raise RuntimeError(f"Problem {number} does not fit in its slot ({len(lines)} lines)")

    c.setFont("Helvetica", STORY_SIZE)
    c.drawString(LEFT + number_width, answer_y, "Answer:")
    answer_width = c.stringWidth("Answer: ", "Helvetica", STORY_SIZE)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(LEFT + number_width + answer_width, answer_y - 2, PAGE_W - RIGHT, answer_y - 2)


def write_student_packet(path, problems):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Addition and Subtraction Word Problems")
    content_bottom = 46

    for page in range(STUDENT_PAGES):
        if page:
            c.showPage()
        content_top = draw_student_header(c)
        slot_height = (content_top - content_bottom) / PROBLEMS_PER_PAGE
        start = page * PROBLEMS_PER_PAGE
        for offset in range(PROBLEMS_PER_PAGE):
            number = start + offset + 1
            slot_top = content_top - offset * slot_height
            draw_problem(c, number, problems[number - 1], slot_top, slot_height)
        draw_page_number(c, page + 1, STUDENT_PAGES)

    c.save()


def answer_key_pages(problems):
    width = PAGE_W - LEFT - RIGHT
    entries = []
    for number, problem in enumerate(problems, start=1):
        text = (
            f"{number:>2}. {problem['steps'][0]};  {problem['steps'][1]}.  "
            f"Answer: {problem['answer']}"
        )
        entries.append(wrap_text(text, "Helvetica", STORY_SIZE, width))

    # First answer baseline is near y=690. Keep the last line above the page number.
    usable = 642
    pages = []
    current = []
    used = 0
    for lines in entries:
        height = len(lines) * STORY_LEADING + 6
        if current and used + height > usable:
            pages.append(current)
            current = []
            used = 0
        current.append(lines)
        used += height
    if current:
        pages.append(current)
    return pages


def write_answer_key(path, problems):
    pages = answer_key_pages(problems)
    total = len(pages)
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Answer Key: Addition and Subtraction Word Problems")

    for page_index, entries in enumerate(pages):
        if page_index:
            c.showPage()
        y = PAGE_H - 42
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(LEFT, y, "Answer Key")
        y -= 22
        c.setFont("Helvetica", STORY_SIZE)
        c.drawString(LEFT, y, "Addition and Subtraction Word Problems")
        y -= 16
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, y, PAGE_W - RIGHT, y)
        y -= 22

        for lines in entries:
            for line in lines:
                c.setFont("Helvetica", STORY_SIZE)
                c.drawString(LEFT, y, line)
                y -= STORY_LEADING
            y -= 8

        draw_page_number(c, page_index + 1, total)

    c.save()
    return total


def main():
    problems = build_problems(RAW_PROBLEMS)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, problems)
    key_pages = write_answer_key(ANSWER_KEY_PDF, problems)
    print(f"Wrote {STUDENT_PDF} ({STUDENT_PAGES} pages, {len(problems)} problems)")
    print(f"Wrote {ANSWER_KEY_PDF} ({key_pages} pages)")


if __name__ == "__main__":
    main()
