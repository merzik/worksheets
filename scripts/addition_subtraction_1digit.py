#!/usr/bin/env python3
"""Build single-digit addition and subtraction worksheets.

Writes a 50-page student packet and a compact answer key into
math/addition-subtraction/. Each page has addition on the top half and
subtraction on the bottom half. Both numbers are single digits (0-9).
Answers may be one or two digits.
"""

import random
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "math" / "addition-subtraction"
STUDENT_PDF = OUT_DIR / "addition-subtraction-1-digit.pdf"
ANSWER_KEY_PDF = OUT_DIR / "addition-subtraction-1-digit-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 32
RIGHT = 32
COLS = 5
ROWS_PER_HALF = 3
PAGES = 50
PER_HALF = COLS * ROWS_PER_HALF
DIGIT_SIZE = 18
DIGIT_LEADING = 22
FIELD_DIGITS = 2
SEED = 20261004
SECTION_LABEL_H = 22


def answer_of(problem):
    if problem["op"] == "+":
        return problem["a"] + problem["b"]
    return problem["a"] - problem["b"]


def make_addition(rng, seen, need_carry):
    for _ in range(5000):
        a = rng.randint(0, 9)
        b = rng.randint(0, 9)
        total = a + b
        carries = total >= 10
        key = ("+", a, b)
        if key in seen or carries != need_carry:
            continue
        seen.add(key)
        return {"a": a, "b": b, "op": "+"}
    raise RuntimeError("Could not build a unique single-digit addition problem")


def make_subtraction(rng, seen):
    for _ in range(5000):
        a = rng.randint(0, 9)
        b = rng.randint(0, a)
        key = ("-", a, b)
        if key not in seen:
            seen.add(key)
            return {"a": a, "b": b, "op": "-"}
    raise RuntimeError("Could not build a unique single-digit subtraction problem")


def build_pages():
    rng = random.Random(SEED)
    pages = []
    for page in range(PAGES):
        seen = set()
        carry_count = 8 if page % 2 == 0 else 7
        plain_count = PER_HALF - carry_count
        addition = [make_addition(rng, seen, True) for _ in range(carry_count)]
        addition.extend(make_addition(rng, seen, False) for _ in range(plain_count))
        rng.shuffle(addition)
        subtraction = [make_subtraction(rng, seen) for _ in range(PER_HALF)]
        rng.shuffle(subtraction)
        if not any(answer_of(problem) >= 10 for problem in addition):
            raise RuntimeError(f"Page {page + 1} addition has no two-digit answers")
        if not any(answer_of(problem) < 10 for problem in addition):
            raise RuntimeError(f"Page {page + 1} addition has only two-digit answers")
        pages.append({"addition": addition, "subtraction": subtraction})
    return pages


def digit_slot():
    return pdfmetrics.stringWidth("0", "Helvetica", DIGIT_SIZE)


def draw_number(c, right, baseline, number, width=FIELD_DIGITS):
    slot = digit_slot()
    text = f"{number:>{width}}"
    for index, char in enumerate(text):
        if char == " ":
            continue
        char_width = pdfmetrics.stringWidth(char, "Helvetica", DIGIT_SIZE)
        x = right - (width - index) * slot
        c.drawString(x + (slot - char_width) / 2, baseline, char)


def draw_problem(c, cell_x, cell_top, cell_w, number, problem, show_answer):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 9)
    c.drawString(cell_x + 4, cell_top - 12, f"{number}.")

    slot = digit_slot()
    field = slot * FIELD_DIGITS
    right = cell_x + (cell_w + field) / 2 + 4
    block_top = cell_top - 28
    c.setFont("Helvetica", DIGIT_SIZE)
    draw_number(c, right, block_top, problem["a"])
    sub_y = block_top - DIGIT_LEADING
    c.drawRightString(right - field - 3, sub_y, problem["op"])
    draw_number(c, right, sub_y, problem["b"])
    line_y = sub_y - 5
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(right - field - 14, line_y, right + 2, line_y)
    if show_answer:
        c.setFont("Helvetica", DIGIT_SIZE)
        draw_number(c, right, line_y - DIGIT_LEADING, answer_of(problem))


def content_box():
    top = PAGE_H - 70
    bottom = 36
    return top, bottom, PAGE_W - LEFT - RIGHT


def draw_header(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, PAGE_H - 34, "Single-Digit Addition and Subtraction")
    y = PAGE_H - 56
    c.setFont("Helvetica", 14)
    c.drawString(LEFT, y, "Name:")
    name_x = LEFT + pdfmetrics.stringWidth("Name: ", "Helvetica", 14)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_x, y - 2, name_x + 190, y - 2)
    date_x = name_x + 214
    c.drawString(date_x, y, "Date:")
    date_line = date_x + pdfmetrics.stringWidth("Date: ", "Helvetica", 14)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)


def draw_footer(c, page, total):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_W / 2, 20, f"Page {page} of {total}")


def half_geometry():
    top, bottom, width = content_box()
    gap_x = 4
    gap_y = 6
    mid = (top + bottom) / 2
    cell_w = (width - gap_x * (COLS - 1)) / COLS
    half_h = mid - bottom - SECTION_LABEL_H
    cell_h = (half_h - gap_y * (ROWS_PER_HALF - 1)) / ROWS_PER_HALF
    return {
        "width": width,
        "cell_w": cell_w,
        "cell_h": cell_h,
        "gap_x": gap_x,
        "gap_y": gap_y,
        "add_label_y": top - 4,
        "add_grid_top": top - SECTION_LABEL_H,
        "sub_label_y": mid - 4,
        "sub_grid_top": mid - SECTION_LABEL_H,
    }


def draw_section_label(c, y, title):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, title)


def draw_grid(c, problems, grid_top, cell_w, cell_h, gap_x, gap_y, start_number):
    for index, problem in enumerate(problems):
        col = index % COLS
        row = index // COLS
        x = LEFT + col * (cell_w + gap_x)
        cell_top = grid_top - row * (cell_h + gap_y)
        draw_problem(c, x, cell_top, cell_w, start_number + index, problem, False)


def write_student_packet(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Single-Digit Addition and Subtraction")
    geom = half_geometry()
    for page_index, page in enumerate(pages):
        if page_index:
            c.showPage()
        draw_header(c)
        draw_footer(c, page_index + 1, PAGES)
        draw_section_label(c, geom["add_label_y"], "Addition")
        draw_grid(
            c,
            page["addition"],
            geom["add_grid_top"],
            geom["cell_w"],
            geom["cell_h"],
            geom["gap_x"],
            geom["gap_y"],
            1,
        )
        draw_section_label(c, geom["sub_label_y"], "Subtraction")
        draw_grid(
            c,
            page["subtraction"],
            geom["sub_grid_top"],
            geom["cell_w"],
            geom["cell_h"],
            geom["gap_x"],
            geom["gap_y"],
            PER_HALF + 1,
        )
    c.save()


def write_answer_key(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Answer Key: Single-Digit Addition and Subtraction")
    blocks_per_page = 3
    key_pages = (len(pages) + blocks_per_page - 1) // blocks_per_page
    width = PAGE_W - LEFT - RIGHT
    for key_index in range(key_pages):
        if key_index:
            c.showPage()
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(LEFT, PAGE_H - 34, "Answer Key")
        c.setFont("Helvetica", 12)
        c.drawString(LEFT, PAGE_H - 52, "Single-Digit Addition and Subtraction")
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, PAGE_H - 60, PAGE_W - RIGHT, PAGE_H - 60)
        draw_footer(c, key_index + 1, key_pages)
        chunk = pages[key_index * blocks_per_page:(key_index + 1) * blocks_per_page]
        y = PAGE_H - 78
        for offset, page in enumerate(chunk):
            page_number = key_index * blocks_per_page + offset + 1
            c.setFont("Helvetica-Bold", 11)
            c.drawString(LEFT, y, f"Page {page_number}")
            y -= 16
            cell_w = width / COLS
            cell_h = 16
            for label, problems, start in (
                ("Addition", page["addition"], 1),
                ("Subtraction", page["subtraction"], PER_HALF + 1),
            ):
                c.setFont("Helvetica-Bold", 10)
                c.drawString(LEFT, y, label)
                y -= 14
                c.setFont("Helvetica", 10)
                for index, problem in enumerate(problems):
                    col = index % COLS
                    row = index // COLS
                    text = f"{start + index}. {answer_of(problem)}"
                    c.drawString(LEFT + col * cell_w, y - row * cell_h, text)
                y -= ROWS_PER_HALF * cell_h + 10
            y -= 8
    c.save()
    return key_pages


def main():
    pages = build_pages()
    if len(pages) != PAGES:
        raise RuntimeError("Expected 50 pages")
    for page in pages:
        if len(page["addition"]) != PER_HALF or len(page["subtraction"]) != PER_HALF:
            raise RuntimeError("Expected 15 addition and 15 subtraction per page")
        for problem in page["addition"] + page["subtraction"]:
            a, b = problem["a"], problem["b"]
            if not (0 <= a <= 9 and 0 <= b <= 9):
                raise RuntimeError(f"Not a single-digit problem: {problem}")
            result = answer_of(problem)
            if problem["op"] == "+":
                if not (0 <= result <= 18):
                    raise RuntimeError(f"Bad addition answer: {problem} -> {result}")
            else:
                if b > a or not (0 <= result <= 9):
                    raise RuntimeError(f"Bad subtraction: {problem} -> {result}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, pages)
    key_pages = write_answer_key(ANSWER_KEY_PDF, pages)
    print(f"Wrote {STUDENT_PDF} ({PAGES} pages, {PAGES * PER_HALF * 2} problems)")
    print(f"Wrote {ANSWER_KEY_PDF} ({key_pages} pages)")


if __name__ == "__main__":
    main()
