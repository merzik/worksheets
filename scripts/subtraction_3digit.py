#!/usr/bin/env python3
"""Build 3-digit subtraction worksheets, with and without regrouping mixed.

Writes a 50-page student packet (5 columns by 5 rows) and a compact
answer key into math/addition-subtraction/.
"""

import random
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "math" / "addition-subtraction"
STUDENT_PDF = OUT_DIR / "subtraction-3-digit.pdf"
ANSWER_KEY_PDF = OUT_DIR / "subtraction-3-digit-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 32
RIGHT = 32
COLS = 5
ROWS = 5
PAGES = 50
PER_PAGE = COLS * ROWS
DIGIT_SIZE = 18
DIGIT_LEADING = 22
SEED = 20260923


def regroups(minuend, subtrahend):
    for _ in range(3):
        if minuend % 10 < subtrahend % 10:
            return True
        minuend //= 10
        subtrahend //= 10
    return False


def make_no_regroup(rng, seen):
    for _ in range(2000):
        hundreds = rng.randint(1, 9)
        tens = rng.randint(0, 9)
        ones = rng.randint(0, 9)
        sub_hundreds = rng.randint(1, hundreds)
        sub_tens = rng.randint(0, tens)
        sub_ones = rng.randint(0, ones)
        minuend = hundreds * 100 + tens * 10 + ones
        subtrahend = sub_hundreds * 100 + sub_tens * 10 + sub_ones
        pair = (minuend, subtrahend)
        if minuend > subtrahend and pair not in seen and not regroups(minuend, subtrahend):
            seen.add(pair)
            return {"a": minuend, "b": subtrahend, "regroup": False}
    raise RuntimeError("Could not build a subtraction problem without regrouping")


def make_regroup(rng, seen):
    for _ in range(5000):
        minuend = rng.randint(101, 999)
        subtrahend = rng.randint(100, minuend - 1)
        pair = (minuend, subtrahend)
        if pair not in seen and regroups(minuend, subtrahend):
            seen.add(pair)
            return {"a": minuend, "b": subtrahend, "regroup": True}
    raise RuntimeError("Could not build a subtraction problem with regrouping")


def build_pages():
    rng = random.Random(SEED)
    seen = set()
    pages = []
    for page in range(PAGES):
        regroup_count = 13 if page % 2 == 0 else 12
        plain_count = PER_PAGE - regroup_count
        problems = [make_regroup(rng, seen) for _ in range(regroup_count)]
        problems.extend(make_no_regroup(rng, seen) for _ in range(plain_count))
        rng.shuffle(problems)
        if not any(problem["regroup"] for problem in problems):
            raise RuntimeError(f"Page {page + 1} has no regrouping problems")
        if all(problem["regroup"] for problem in problems):
            raise RuntimeError(f"Page {page + 1} has only regrouping problems")
        pages.append(problems)
    return pages


def digit_slot():
    return pdfmetrics.stringWidth("0", "Helvetica", DIGIT_SIZE)


def draw_number(c, right, baseline, number):
    slot = digit_slot()
    text = f"{number:>3}"
    for index, char in enumerate(text):
        if char == " ":
            continue
        char_width = pdfmetrics.stringWidth(char, "Helvetica", DIGIT_SIZE)
        x = right - (3 - index) * slot
        c.drawString(x + (slot - char_width) / 2, baseline, char)


def draw_problem(c, cell_x, cell_top, cell_w, cell_h, number, problem, show_answer):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 9)
    c.drawString(cell_x + 4, cell_top - 12, f"{number}.")

    slot = digit_slot()
    field = slot * 3
    right = cell_x + (cell_w + field) / 2 + 4
    block_top = cell_top - 28
    c.setFont("Helvetica", DIGIT_SIZE)
    draw_number(c, right, block_top, problem["a"])
    sub_y = block_top - DIGIT_LEADING
    c.drawRightString(right - field - 3, sub_y, "-")
    draw_number(c, right, sub_y, problem["b"])
    line_y = sub_y - 5
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(right - field - 14, line_y, right + 2, line_y)
    if show_answer:
        c.setFont("Helvetica", DIGIT_SIZE)
        draw_number(c, right, line_y - DIGIT_LEADING, problem["a"] - problem["b"])


def content_box():
    top = PAGE_H - 70
    bottom = 36
    return top, bottom, PAGE_W - LEFT - RIGHT


def draw_header(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, PAGE_H - 34, "3-Digit Subtraction")
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


def cell_geometry():
    top, bottom, width = content_box()
    gap_x = 4
    gap_y = 6
    cell_w = (width - gap_x * (COLS - 1)) / COLS
    cell_h = ((top - bottom) - gap_y * (ROWS - 1)) / ROWS
    return top, cell_w, cell_h, gap_x, gap_y


def write_student_packet(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("3-Digit Subtraction")
    top, cell_w, cell_h, gap_x, gap_y = cell_geometry()
    for page_index, problems in enumerate(pages):
        if page_index:
            c.showPage()
        draw_header(c)
        draw_footer(c, page_index + 1, PAGES)
        for index, problem in enumerate(problems):
            col = index % COLS
            row = index // COLS
            x = LEFT + col * (cell_w + gap_x)
            cell_top = top - row * (cell_h + gap_y)
            draw_problem(c, x, cell_top, cell_w, cell_h, index + 1, problem, False)
    c.save()


def write_answer_key(path, pages):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Answer Key: 3-Digit Subtraction")
    blocks_per_page = 4
    key_pages = (len(pages) + blocks_per_page - 1) // blocks_per_page
    width = PAGE_W - LEFT - RIGHT
    block_h = 150
    for key_index in range(key_pages):
        if key_index:
            c.showPage()
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(LEFT, PAGE_H - 34, "Answer Key")
        c.setFont("Helvetica", 12)
        c.drawString(LEFT, PAGE_H - 52, "3-Digit Subtraction")
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, PAGE_H - 60, PAGE_W - RIGHT, PAGE_H - 60)
        draw_footer(c, key_index + 1, key_pages)
        chunk = pages[key_index * blocks_per_page:(key_index + 1) * blocks_per_page]
        y = PAGE_H - 78
        for offset, problems in enumerate(chunk):
            page_number = key_index * blocks_per_page + offset + 1
            c.setFont("Helvetica-Bold", 11)
            c.drawString(LEFT, y, f"Page {page_number}")
            y -= 16
            cell_w = width / COLS
            cell_h = 22
            c.setFont("Helvetica", 11)
            for index, problem in enumerate(problems):
                col = index % COLS
                row = index // COLS
                answer = problem["a"] - problem["b"]
                text = f"{index + 1}. {answer}"
                c.drawString(LEFT + col * cell_w, y - row * cell_h, text)
            y -= ROWS * cell_h + 14
    c.save()
    return key_pages


def main():
    pages = build_pages()
    if len(pages) != PAGES or any(len(page) != PER_PAGE for page in pages):
        raise RuntimeError("Expected 50 pages of 25 problems")
    for page in pages:
        for problem in page:
            if not (100 <= problem["a"] <= 999 and 100 <= problem["b"] <= 999):
                raise RuntimeError(f"Not a 3-digit problem: {problem}")
            if problem["a"] < problem["b"]:
                raise RuntimeError(f"Negative answer: {problem}")
            if regroups(problem["a"], problem["b"]) != problem["regroup"]:
                raise RuntimeError(f"Regrouping flag does not match: {problem}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_student_packet(STUDENT_PDF, pages)
    key_pages = write_answer_key(ANSWER_KEY_PDF, pages)
    regroup_total = sum(problem["regroup"] for page in pages for problem in page)
    print(f"Wrote {STUDENT_PDF} ({PAGES} pages, {PAGES * PER_PAGE} problems)")
    print(f"Wrote {ANSWER_KEY_PDF} ({key_pages} pages)")
    print(f"{regroup_total} with regrouping, {PAGES * PER_PAGE - regroup_total} without")


if __name__ == "__main__":
    main()
