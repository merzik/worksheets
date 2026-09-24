#!/usr/bin/env python3
"""Build intermediate reading-comprehension packets for grades 1 through 5.

Each student page is one story on the top half and three multiple-choice
questions on the bottom half. Stories have a problem, three events, and
a solution. A compact answer key is written beside each packet.
"""

import random
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT_ROOT = ROOT / "reading-comp"

PAGE_W, PAGE_H = letter
LEFT = 40
RIGHT = 40
PASSAGE_COUNT = 30
STORY_TOP = 714
STORY_BOTTOM = 420
STORY_H = STORY_TOP - STORY_BOTTOM
QUESTION_TOP = 390
QUESTION_BOTTOM = 32
QUESTION_GAP = 6
LETTERS = "ABCD"


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


def passage_lines(text, size, width):
    lines = []
    for index, paragraph in enumerate(text.strip().split("\n\n")):
        if index:
            lines.append("")
        lines.extend(wrap_text(paragraph.replace("\n", " "), "Helvetica", size, width))
    return lines


def content_width():
    return PAGE_W - LEFT - RIGHT


def question_box_height():
    span = QUESTION_TOP - QUESTION_BOTTOM
    return (span - 2 * QUESTION_GAP) / 3


def story_line_target(font_size):
    leading = font_size + 5
    inner = STORY_H - 22 - font_size
    return int(inner / leading) + 1


def place_answers(passages, seed):
    """Spread correct answers across A-D, and shuffle the other choices."""
    rng = random.Random(seed)
    count = len(passages)
    for question_index in range(3):
        letters = []
        for letter_index, letter in enumerate(LETTERS):
            extra = 1 if letter_index < count % 4 else 0
            letters.extend([letter] * (count // 4 + extra))
        rng.shuffle(letters)
        for passage, letter in zip(passages, letters):
            question = passage["questions"][question_index]
            wrongs = question["wrongs"][:]
            rng.shuffle(wrongs)
            choices = [None, None, None, None]
            slot = LETTERS.index(letter)
            choices[slot] = question["correct"]
            wrong_index = 0
            for index in range(4):
                if choices[index] is None:
                    choices[index] = wrongs[wrong_index]
                    wrong_index += 1
            question["choices"] = choices
            question["answer"] = letter
    _break_uniform_rows(passages)


def _break_uniform_rows(passages):
    for index, passage in enumerate(passages):
        answers = [question["answer"] for question in passage["questions"]]
        if len(set(answers)) != 1:
            continue
        for other in range(len(passages)):
            if other == index:
                continue
            other_questions = passages[other]["questions"]
            if other_questions[2]["answer"] == answers[2]:
                continue
            swapped = [question["answer"] for question in other_questions]
            swapped[2] = answers[2]
            if len(set(swapped)) == 1:
                continue
            first = passage["questions"][2]
            second = other_questions[2]
            first["answer"], second["answer"] = second["answer"], first["answer"]
            _pin_correct(first)
            _pin_correct(second)
            break


def _pin_correct(question):
    slot = LETTERS.index(question["answer"])
    current = question["choices"].index(question["correct"])
    if current == slot:
        return
    question["choices"][slot], question["choices"][current] = (
        question["choices"][current],
        question["choices"][slot],
    )


def validate(spec):
    errors = []
    passages = spec["passages"]
    label = spec["label"]
    if len(passages) != PASSAGE_COUNT:
        errors.append(f"{label}: expected {PASSAGE_COUNT} passages, got {len(passages)}")
        return errors

    width = content_width()
    text_width = width - 16
    target = story_line_target(spec["font_size"])
    line_counts = []
    titles = set()
    longest_correct = 0
    question_total = 0

    for number, passage in enumerate(passages, start=1):
        title = passage["title"]
        where = f"{label} {number} {title!r}"
        if title in titles:
            errors.append(f"{where} repeats a title")
        titles.add(title)
        if not _fits(title, "Helvetica-Bold", 16, width - 170):
            errors.append(f"{where} title is too long for the header")
        character = passage["character"].split()[0]
        if character.lower() not in passage["text"].lower():
            errors.append(f"{where} does not name {character}")
        paragraphs = [part for part in passage["text"].split("\n\n") if part.strip()]
        if not 2 <= len(paragraphs) <= 4:
            errors.append(f"{where} has {len(paragraphs)} paragraphs (need 2-4)")
        lines = passage_lines(passage["text"], spec["font_size"], text_width)
        line_counts.append(len(lines))
        if not target - 4 <= len(lines) <= target + 1:
            errors.append(
                f"{where} wraps to {len(lines)} lines (need {target - 4}-{target + 1})"
            )
        if len(passage["questions"]) != 3:
            errors.append(f"{where} needs 3 questions")
            continue
        for q_index, question in enumerate(passage["questions"], start=1):
            question_total += 1
            stem = question["stem"].strip()
            if not stem.endswith("?"):
                errors.append(f"{where} question {q_index} does not end with ?")
            choices = question["choices"]
            if len(choices) != 4 or len(set(choices)) != 4:
                errors.append(f"{where} question {q_index} needs 4 different choices")
                continue
            if question["correct"] not in choices:
                errors.append(f"{where} question {q_index} lost its correct choice")
            if question["answer"] not in LETTERS:
                errors.append(f"{where} question {q_index} has a bad answer letter")
            pinned = choices[LETTERS.index(question["answer"])]
            if pinned != question["correct"]:
                errors.append(f"{where} question {q_index} key does not match {pinned!r}")
            stem_lines = wrap_text(f"{q_index}. {stem}", "Helvetica-Bold", spec["question_size"], text_width - 8)
            if len(stem_lines) > 2:
                errors.append(f"{where} question {q_index} stem wraps past 2 lines")
            choice_width = text_width - 62
            for letter, choice in zip(LETTERS, choices):
                if not _fits(choice, "Helvetica", spec["question_size"], choice_width):
                    errors.append(
                        f"{where} choice {letter} does not fit on one line: {choice}"
                    )
            lengths = [len(choice) for choice in choices]
            correct_len = len(question["correct"])
            others = [len(choice) for choice in choices if choice != question["correct"]]
            if others and correct_len >= max(others) + 10:
                longest_correct += 1
            if not _question_fits(q_index, question, spec["question_size"], text_width):
                errors.append(f"{where} question {q_index} does not fit in its box")

    if line_counts:
        longest = max(line_counts)
        leading = _leading_for(spec["font_size"], longest)
        if leading < spec["font_size"] + 3:
            errors.append(
                f"{label}: longest story needs leading {leading:.1f} "
                f"(minimum is {spec['font_size'] + 3})"
            )
        shortest = min(line_counts)
        used = _text_height(spec["font_size"], shortest, leading)
        if used < STORY_H * 0.78:
            errors.append(
                f"{label}: shortest story fills only {used / STORY_H:.0%} of the half page"
            )
    if longest_correct:
        errors.append(
            f"{label}: {longest_correct} correct choices are 10 or more "
            "characters longer than every wrong choice"
        )
    return errors


def _fits(text, font, size, width):
    return pdfmetrics.stringWidth(text, font, size) <= width


def _text_height(font_size, line_count, leading):
    if line_count <= 0:
        return 0
    return 10 + font_size + (line_count - 1) * leading + 12


def _leading_for(font_size, line_count):
    if line_count <= 1:
        return font_size + 5
    room = STORY_H - 10 - 12 - font_size
    return room / (line_count - 1)


def _question_block_height(q_index, question, size, text_width):
    stem_lines = wrap_text(
        f"{q_index}. {question['stem']}",
        "Helvetica-Bold",
        size,
        text_width - 8,
    )
    choice_leading = size + 3
    stem_leading = size + 3
    height = 8 + size + (len(stem_lines) - 1) * stem_leading
    height += 6
    height += size + (len(question["choices"]) - 1) * choice_leading
    height += 8
    return height


def _question_fits(q_index, question, size, text_width):
    return _question_block_height(q_index, question, size, text_width) <= question_box_height()


def draw_header(c, title, grade_label):
    y = PAGE_H - 34
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, title)
    c.setFont("Helvetica", 11)
    grade_width = pdfmetrics.stringWidth(grade_label, "Helvetica", 11)
    c.drawString(PAGE_W - RIGHT - grade_width, y + 1, grade_label)
    y -= 26
    c.setFont("Helvetica", 13)
    c.drawString(LEFT, y, "Name:")
    name_line = LEFT + pdfmetrics.stringWidth("Name: ", "Helvetica", 13)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_line, y - 2, name_line + 210, y - 2)
    date_x = name_line + 230
    c.drawString(date_x, y, "Date:")
    date_line = date_x + pdfmetrics.stringWidth("Date: ", "Helvetica", 13)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)


def draw_footer(c, number, total):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, 20, f"Passage {number} of {total}")


def draw_story(c, text, font_size, leading):
    width = content_width()
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.25)
    c.rect(LEFT, STORY_BOTTOM, width, STORY_H, stroke=1, fill=0)
    lines = passage_lines(text, font_size, width - 16)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", font_size)
    y = STORY_TOP - 10 - font_size
    for line in lines:
        if line:
            c.drawString(LEFT + 8, y, line)
        y -= leading


def draw_direction(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(LEFT, STORY_BOTTOM - 16, "Fill in the circle next to the best answer.")


def draw_questions(c, questions, size):
    width = content_width()
    box_h = question_box_height()
    text_width = width - 16
    top = QUESTION_TOP
    for index, question in enumerate(questions, start=1):
        _draw_question(c, LEFT, top, width, box_h, index, question, size, text_width)
        top -= box_h + QUESTION_GAP


def _draw_question(c, x, top, width, height, number, question, size, text_width):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.1)
    c.rect(x, top - height, width, height, stroke=1, fill=0)
    stem_leading = size + 3
    choice_leading = size + 3
    stem_lines = wrap_text(
        f"{number}. {question['stem']}",
        "Helvetica-Bold",
        size,
        text_width - 8,
    )
    block = _question_block_height(number, question, size, text_width)
    y = top - max(8, (height - block) / 2) - size
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", size)
    for line in stem_lines:
        c.drawString(x + 8, y, line)
        y -= stem_leading
    y -= 6 - (stem_leading - size)
    number_width = pdfmetrics.stringWidth("A. ", "Helvetica-Bold", size)
    for letter, choice in zip(LETTERS, question["choices"]):
        circle_x = x + 22
        circle_y = y + size * 0.32
        c.setLineWidth(1.2)
        c.circle(circle_x, circle_y, 5.4, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x + 34, y, f"{letter}.")
        c.setFont("Helvetica", size)
        c.drawString(x + 38 + number_width, y, choice)
        y -= choice_leading


def write_student_packet(path, spec):
    passages = spec["passages"]
    width = content_width()
    text_width = width - 16
    longest = max(
        len(passage_lines(passage["text"], spec["font_size"], text_width))
        for passage in passages
    )
    leading = min(spec["font_size"] + 6, _leading_for(spec["font_size"], longest))
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(f"{spec['label']} Intermediate Reading")
    for index, passage in enumerate(passages, start=1):
        if index > 1:
            c.showPage()
        draw_header(c, passage["title"], spec["header"])
        draw_story(c, passage["text"], spec["font_size"], leading)
        draw_direction(c)
        draw_questions(c, passage["questions"], spec["question_size"])
        draw_footer(c, index, len(passages))
    c.save()
    return leading


def key_entries(passages, width):
    entries = []
    for number, passage in enumerate(passages, start=1):
        raw = [(True, f"{number}. {passage['title']}")]
        for index, question in enumerate(passage["questions"], start=1):
            letter = question["answer"]
            choice = question["choices"][LETTERS.index(letter)]
            raw.append((False, f"{index}. {question['stem']}"))
            raw.append((False, f"     {letter}. {choice}"))
        lines = []
        for bold, text in raw:
            font = "Helvetica-Bold" if bold else "Helvetica"
            wrapped = wrap_text(text, font, 11, width)
            for line_index, line in enumerate(wrapped):
                lines.append((bold and line_index == 0, line))
        entries.append(lines)
    return entries


def pack_key_pages(entries):
    leading = 14
    usable = PAGE_H - 108 - 36
    pages = []
    current = []
    used = 0
    for lines in entries:
        height = len(lines) * leading + 10
        if current and used + height > usable:
            pages.append(current)
            current = []
            used = 0
        current.append(lines)
        used += height
    if current:
        pages.append(current)
    return pages


def write_answer_key(path, spec):
    width = content_width()
    pages = pack_key_pages(key_entries(spec["passages"], width))
    total = len(pages)
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(f"Answer Key: {spec['key_title']}")
    for page_index, entries in enumerate(pages):
        if page_index:
            c.showPage()
        y = PAGE_H - 36
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(LEFT, y, "Answer Key")
        y -= 18
        c.setFont("Helvetica", 13)
        c.drawString(LEFT, y, spec["key_title"])
        y -= 10
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, y, PAGE_W - RIGHT, y)
        y -= 18
        for lines in entries:
            for bold, line in lines:
                c.setFont("Helvetica-Bold" if bold else "Helvetica", 11)
                c.drawString(LEFT, y, line)
                y -= 14
            y -= 10
        c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W / 2, 20, f"Page {page_index + 1} of {total}")
    c.save()
    return total


SPECS = [
    {
        "folder": "grade-1",
        "label": "Grade 1",
        "header": "Grade 1 Intermediate",
        "key_title": "Grade 1 Intermediate Passages",
        "student_name": "intermediate-passages.pdf",
        "key_name": "intermediate-passages-answer-key.pdf",
        "font_size": 16,
        "question_size": 13,
        "seed": 11,
        "module": "passages_mc.grade1",
    },
    {
        "folder": "grade-2",
        "label": "Grade 2",
        "header": "Grade 2 Intermediate",
        "key_title": "Grade 2 Intermediate Passages",
        "student_name": "intermediate-passages.pdf",
        "key_name": "intermediate-passages-answer-key.pdf",
        "font_size": 15,
        "question_size": 12,
        "seed": 22,
        "module": "passages_mc.grade2",
    },
    {
        "folder": "grade-3",
        "label": "Grade 3",
        "header": "Grade 3 Intermediate",
        "key_title": "Grade 3 Intermediate Passages",
        "student_name": "intermediate-passages.pdf",
        "key_name": "intermediate-passages-answer-key.pdf",
        "font_size": 13,
        "question_size": 12,
        "seed": 33,
        "module": "passages_mc.grade3",
    },
    {
        "folder": "grade-4",
        "label": "Grade 4",
        "header": "Grade 4 Intermediate",
        "key_title": "Grade 4 Intermediate Passages",
        "student_name": "intermediate-passages.pdf",
        "key_name": "intermediate-passages-answer-key.pdf",
        "font_size": 12,
        "question_size": 11,
        "seed": 44,
        "module": "passages_mc.grade4",
    },
    {
        "folder": "grade-5",
        "label": "Grade 5",
        "header": "Grade 5 Intermediate",
        "key_title": "Grade 5 Intermediate Passages",
        "student_name": "intermediate-passages.pdf",
        "key_name": "intermediate-passages-answer-key.pdf",
        "font_size": 12,
        "question_size": 11,
        "seed": 55,
        "module": "passages_mc.grade5",
    },
]


def load_specs(only):
    import importlib

    specs = []
    for spec in SPECS:
        if only and spec["folder"] not in only and spec["label"].lower() not in only:
            continue
        module = importlib.import_module(spec["module"])
        loaded = dict(spec)
        loaded["passages"] = module.PASSAGES
        specs.append(loaded)
    if not specs:
        names = ", ".join(spec["folder"] for spec in SPECS)
        raise SystemExit(f"No matching grade. Choose from: {names}")
    return specs


def main():
    only = set(sys.argv[1:])
    specs = load_specs(only)
    for spec in specs:
        place_answers(spec["passages"], spec["seed"])
    errors = []
    for spec in specs:
        errors.extend(validate(spec))
    if errors:
        raise SystemExit("\n".join(errors))
    for spec in specs:
        folder = OUT_ROOT / spec["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        student_path = folder / spec["student_name"]
        key_path = folder / spec["key_name"]
        leading = write_student_packet(student_path, spec)
        key_pages = write_answer_key(key_path, spec)
        target = story_line_target(spec["font_size"])
        print(
            f"Wrote {student_path} ({PASSAGE_COUNT} pages, "
            f"story leading {leading:.1f}, line target {target})"
        )
        print(f"Wrote {key_path} ({key_pages} pages)")


if __name__ == "__main__":
    main()
