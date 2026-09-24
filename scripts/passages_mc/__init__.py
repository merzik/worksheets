"""Passage helpers for the multiple-choice reading packets."""


def question(stem, correct, wrong1, wrong2, wrong3):
    return {
        "stem": stem,
        "correct": correct,
        "wrongs": [wrong1, wrong2, wrong3],
    }


def passage(title, character, text, questions):
    if len(questions) != 3:
        raise ValueError(f"{title!r} needs exactly 3 questions")
    return {
        "title": title,
        "character": character,
        "text": text.strip(),
        "questions": questions,
    }
