#!/usr/bin/env python3
"""Build rounding worksheets for the nearest 10 and the nearest 100.

Each page has four labeled groups. The instruction is printed once
for the group. Write-in groups use four columns. Both-sides groups
use two wider columns.
"""

import random
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "math" / "rounding"
STUDENT_PDF = OUT_DIR / "rounding-10-and-100.pdf"
ANSWER_KEY_PDF = OUT_DIR / "rounding-10-and-100-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 36
RIGHT = 36
PAGES = 50
WRITE_COLS = 4
WRITE_ROWS = 6
CIRCLE_COLS = 3
CIRCLE_ROWS = 3
WRITE_COUNT = WRITE_COLS * WRITE_ROWS
CIRCLE_COUNT = CIRCLE_COLS * CIRCLE_ROWS
SEED = 20260923

GROUPS = (
    ("nearest_10", "Nearest 10.", "Round each number.", "write", 10),
    ("nearest_100", "Nearest 100.", "Round each number.", "write", 100),
    (
        "circle_10",
        "Both sides, nearest 10.",
        "Write the numbers on each side and circle the correct one.",
        "circle",
        10,
    ),
    (
        "circle_100",
        "Both sides, nearest 100.",
        "Write the numbers on each side and circle the correct one.",
        "circle",
        100,
    ),
)


def bounds(number, place):
    lower = (number // place) * place
    upper = lower + place
    if number % place == 0:
        raise ValueError(f"{number} is already a multiple of {place}")
    if number - lower < upper - number:
        answer = lower
    else:
        answer = upper
    return lower, upper, answer


def make_number(rng, seen, place, two_digit):
    for _ in range(400):
        if two_digit:
            number = rng.randint(11, 99)
        else:
            number = rng.randint(101, 999)
        if number % place == 0 or number in seen:
            continue
        seen.add(number)
        lower, upper, answer = bounds(number, place)
        return {
            "number": number,
            "place": place,
            "lower": lower,
            "upper": upper,
            "answer": answer,
        }
    raise RuntimeError(f"Could not build a nearest-{place} problem")


def fill_group(rng, seen, place, count, two_digit_count):
    if two_digit_count > count:
        raise RuntimeError("More 2-digit problems than the group can hold")
    flags = [True] * two_digit_count + [False] * (count - two_digit_count)
    rng.shuffle(flags)
    return [make_number(rng, seen, place, flag) for flag in flags]


def build_pages():
    rng = random.Random(SEED)
    pages = []
    for _ in range(PAGES):
        seen = set()
        page = {
            "nearest_10": fill_group(rng, seen, 10, WRITE_COUNT, 6),
            "nearest_100": fill_group(rng, seen, 100, WRITE_COUNT, 0),
            "circle_10": fill_group(rng, seen, 10, CIRCLE_COUNT, 2),
            "circle_100": fill_group(rng, seen, 100, CIRCLE_COUNT, 0),
        }
        if len(seen) != WRITE_COUNT * 2 + CIRCLE_COUNT * 2:
            raise RuntimeError("A number was repeated on the page")
        pages.append(page)
    return pages


def content_width():
    return PAGE_W - LEFT - RIGHT


def draw_header(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, PAGE_H - 32, "Rounding to the Nearest 10 and 100")
    y = PAGE_H - 54
    c.setFont("Helvetica", 14)
    c.drawString(LEFT, y, "Name:")
    name_x = LEFT + pdfmetrics.stringWidth("Name: ", "Helvetica", 14)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_x, y - 2, name_x + 180, y - 2)
    date_x = name_x + 206
    c.drawString(date_x, y, "Date:")
    date_line = date_x + pdfmetrics.stringWidth("Date: ", "Helvetica", 14)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)


def draw_footer(c, page, total):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_W / 2, 20, f"Page {page} of {total}")


def column_width(columns):
    gaps = COL_GAP * (columns - 1) if columns > 1 else 0
    return (content_width() - gaps) / columns


COL_GAP = 12


def group_pitches():
    """Leave a clear gap under each direction, and give both-sides rows more air."""
    content_top = PAGE_H - 78
    content_bottom = 40
    head_gap = 40
    group_gap = 34
    write_pitch = 22
    available = content_top - content_bottom
    used = (
        2 * (head_gap + (WRITE_ROWS - 1) * write_pitch)
        + 2 * head_gap
        + 3 * group_gap
    )
    circle_gaps = 2 * (CIRCLE_ROWS - 1)
    circle_pitch = (available - used) / circle_gaps
    if write_pitch < 20 or circle_pitch < 44 or head_gap < 36:
        raise RuntimeError(
            f"Rows are too tight: write {write_pitch:.1f}, circle {circle_pitch:.1f}"
        )
    return content_top, write_pitch, circle_pitch, head_gap, group_gap


def draw_group_heading(c, y, title, instruction):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(LEFT, y, title)
    title_w = pdfmetrics.stringWidth(title + " ", "Helvetica-Bold", 13)
    c.setFont("Helvetica", 12)
    c.drawString(LEFT + title_w, y, instruction)
    rule_y = y - 4
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(LEFT, rule_y, PAGE_W - RIGHT, rule_y)
    used = title_w + pdfmetrics.stringWidth(instruction, "Helvetica", 12)
    if used > content_width():
        raise RuntimeError(f"Group heading is too wide: {title} {instruction}")


def draw_write_cell(c, x, y, width, number, problem, show_answer):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    c.drawRightString(x + 18, y, f"{number}.")
    c.setFont("Helvetica", 14)
    value = str(problem["number"])
    value_w = pdfmetrics.stringWidth("999", "Helvetica", 14)
    c.drawRightString(x + 22 + value_w, y, value)
    line_x = x + 28 + value_w
    line_w = width - (line_x - x) - 4
    if line_w < 36:
        raise RuntimeError("Answer line is too short")
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(line_x, y - 2, line_x + line_w, y - 2)
    if show_answer:
        c.setFont("Helvetica", 12)
        c.drawString(line_x + 3, y + 1, str(problem["answer"]))


def draw_circle_cell(c, x, y, width, number, problem, show_answer):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    c.drawRightString(x + 14, y, f"{number}.")
    inner_x = x + 18
    inner_w = width - 20
    c.setFont("Helvetica-Bold", 13)
    value = str(problem["number"])
    value_w = pdfmetrics.stringWidth(value, "Helvetica-Bold", 13)
    gap = 6
    line_w = (inner_w - value_w - 2 * gap) / 2
    if line_w < 46:
        raise RuntimeError("Benchmark line is too short")
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.9)
    c.line(inner_x, y - 2, inner_x + line_w, y - 2)
    right_x = inner_x + line_w + gap + value_w + gap
    c.line(right_x, y - 2, right_x + line_w, y - 2)
    c.drawString(inner_x + line_w + gap, y, value)
    if not show_answer:
        return
    c.setFont("Helvetica", 11)
    for side, side_value, side_x in (
        ("left", problem["lower"], inner_x),
        ("right", problem["upper"], right_x),
    ):
        label = str(side_value)
        label_w = pdfmetrics.stringWidth(label, "Helvetica", 11)
        label_x = side_x + (line_w - label_w) / 2
        c.drawString(label_x, y + 2, label)
        if side_value == problem["answer"]:
            c.setLineWidth(1.1)
            c.ellipse(label_x - 5, y - 3, label_x + label_w + 5, y + 14, stroke=1, fill=0)


def draw_group(c, top, key, problems, show_answer, pitch, head_gap):
    title, instruction, style, _place = next(
        (title, instruction, style, place)
        for group_key, title, instruction, style, place in GROUPS
        if group_key == key
    )
    draw_group_heading(c, top, title, instruction)
    columns = WRITE_COLS if style == "write" else CIRCLE_COLS
    col_w = column_width(columns)
    rows = (len(problems) + columns - 1) // columns
    last_y = top
    for index, problem in enumerate(problems):
        row, col = divmod(index, columns)
        x = LEFT + col * (col_w + COL_GAP)
        y = top - head_gap - row * pitch
        last_y = y
        if style == "write":
            draw_write_cell(c, x, y, col_w, index + 1, problem, show_answer)
        else:
            draw_circle_cell(c, x, y, col_w, index + 1, problem, show_answer)
    if rows != (WRITE_ROWS if style == "write" else CIRCLE_ROWS):
        raise RuntimeError(f"{key} has an unexpected row count")
    return last_y


def write_student_packet(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Rounding to the Nearest 10 and 100")
    content_top, write_pitch, circle_pitch, head_gap, group_gap = group_pitches()
    for page_index, page in enumerate(pages):
        if page_index:
            c.showPage()
        draw_header(c)
        draw_footer(c, page_index + 1, PAGES)
        y = content_top
        last_y = y
        for key, _title, _instruction, style, _place in GROUPS:
            pitch = write_pitch if style == "write" else circle_pitch
            last_y = draw_group(c, y, key, page[key], False, pitch, head_gap)
            y = last_y - group_gap
        if last_y < 32:
            raise RuntimeError("Student page ran into the footer")
    c.save()


def answer_line(problems, start, per_line, kind):
    chunk = problems[start:start + per_line]
    parts = []
    for offset, problem in enumerate(chunk):
        number = start + offset + 1
        if kind == "write":
            parts.append(f"{number}. {problem['answer']}")
        else:
            parts.append(
                f"{number}. {problem['lower']}  {problem['number']}  "
                f"{problem['upper']}  circle {problem['answer']}"
            )
    return "    ".join(parts)


def write_answer_key(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Answer Key: Rounding to the Nearest 10 and 100")
    per_key = 2
    key_pages = (len(pages) + per_key - 1) // per_key
    width = content_width()
    for key_index in range(key_pages):
        if key_index:
            c.showPage()
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(LEFT, PAGE_H - 32, "Answer Key")
        c.setFont("Helvetica", 12)
        c.drawString(LEFT, PAGE_H - 50, "Rounding to the Nearest 10 and 100")
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, PAGE_H - 58, PAGE_W - RIGHT, PAGE_H - 58)
        draw_footer(c, key_index + 1, key_pages)
        chunk = pages[key_index * per_key:(key_index + 1) * per_key]
        y = PAGE_H - 78
        for offset, page in enumerate(chunk):
            page_number = key_index * per_key + offset + 1
            c.setFont("Helvetica-Bold", 12)
            c.drawString(LEFT, y, f"Page {page_number}")
            y -= 15
            for key, title, _instruction, style, _place in GROUPS:
                c.setFont("Helvetica-Bold", 11)
                c.drawString(LEFT, y, title)
                y -= 14
                problems = page[key]
                per_line = 8 if style == "write" else 2
                font = "Helvetica"
                size = 11 if style == "write" else 10
                for start in range(0, len(problems), per_line):
                    text = answer_line(problems, start, per_line, style)
                    if pdfmetrics.stringWidth(text, font, size) > width:
                        raise RuntimeError(f"Answer key line is too wide: {text}")
                    c.setFont(font, size)
                    c.drawString(LEFT + 8, y, text)
                    y -= 13
                y -= 6
            y -= 8
        if y < 30:
            raise RuntimeError("Answer key ran into the footer")
    c.save()
    return key_pages


def check_samples():
    samples = [
        (64, 10, 60, 70, 60),
        (45, 10, 40, 50, 50),
        (348, 100, 300, 400, 300),
        (350, 100, 300, 400, 400),
        (249, 100, 200, 300, 200),
    ]
    for number, place, lower, upper, answer in samples:
        got = bounds(number, place)
        if got != (lower, upper, answer):
            raise RuntimeError(f"{number} to nearest {place} -> {got}, expected {(lower, upper, answer)}")


def main():
    check_samples()
    pages = build_pages()
    if len(pages) != PAGES:
        raise RuntimeError("Expected 50 pages")
    for page in pages:
        for key, _title, _instruction, style, place in GROUPS:
            expected = WRITE_COUNT if style == "write" else CIRCLE_COUNT
            problems = page[key]
            if len(problems) != expected:
                raise RuntimeError(f"{key} should have {expected} problems")
            for problem in problems:
                if problem["place"] != place:
                    raise RuntimeError(f"{key} has the wrong place")
                got = bounds(problem["number"], problem["place"])
                if got != (problem["lower"], problem["upper"], problem["answer"]):
                    raise RuntimeError(f"Answer does not match the rounding rule: {problem}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, pages)
    key_pages = write_answer_key(ANSWER_KEY_PDF, pages)
    total = PAGES * (WRITE_COUNT * 2 + CIRCLE_COUNT * 2)
    print(f"Wrote {STUDENT_PDF} ({PAGES} pages, {total} problems)")
    print(f"Wrote {ANSWER_KEY_PDF} ({key_pages} pages)")
    print(f"Each page: {WRITE_COUNT} nearest 10, {WRITE_COUNT} nearest 100, "
          f"{CIRCLE_COUNT} both-sides 10, {CIRCLE_COUNT} both-sides 100")


if __name__ == "__main__":
    main()
