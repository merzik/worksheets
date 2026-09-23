#!/usr/bin/env python3
"""Build reading-comprehension story-map PDFs for grades 1, 2, and 3.

Each student page is one passage plus boxes for setting, character,
beginning, three middle events, and ending. A compact answer key is
written beside each packet.
"""

import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "reading-comp"

PAGE_W, PAGE_H = letter
LEFT = 40
RIGHT = 40
GAP = 8
LABEL_SIZE = 14
PASSAGE_COUNT = 20
CONTENT_TOP = PAGE_H - 76
CONTENT_BOTTOM = 40

HEART_WORDS = {
    "the",
    "a",
    "to",
    "said",
    "was",
    "of",
    "you",
    "have",
    "they",
    "she",
    "he",
    "are",
    "for",
    "her",
    "what",
}
VOWEL_TEAMS = (
    "eigh",
    "igh",
    "ai",
    "ay",
    "ea",
    "ee",
    "oa",
    "ow",
    "ou",
    "oo",
    "oi",
    "oy",
    "au",
    "aw",
    "ew",
    "ie",
    "ei",
    "ui",
    "ue",
)
CONSONANTS = set("bcdfghjklmnpqrstvwxz")
VOWELS = set("aeiou")


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


def words_in(text):
    return re.findall(r"[A-Za-z']+", text)


def word_count(text):
    return len(words_in(text))


def _prep(word):
    return word.replace("qu", "q")


def _vowels(token):
    return [i for i, ch in enumerate(token) if ch in VOWELS]


def is_silent_e(word):
    token = _prep(word)
    if len(token) < 3 or not token.endswith("e") or "y" in token:
        return False
    body = token[:-1]
    vowels = _vowels(body)
    if len(vowels) != 1:
        return False
    between = len(body) - vowels[0] - 1
    if not 1 <= between <= 2:
        return False
    return all(ch in CONSONANTS or ch in VOWELS for ch in token)


def is_closed_syllable(word):
    token = _prep(word)
    if not token or "y" in token:
        return False
    vowels = _vowels(token)
    if len(vowels) != 1 or vowels[0] == len(token) - 1:
        return False
    return all(ch in CONSONANTS or ch in VOWELS for ch in token)


def rejected_word(word):
    """Return the word if it is outside the grade 1 decodable pattern."""
    cleaned = word.lower()
    if not cleaned:
        return None
    if "'" in cleaned:
        return cleaned
    if cleaned in HEART_WORDS:
        return None
    if not re.fullmatch(r"[a-z]+", cleaned):
        return cleaned
    # y is a consonant at the start of yell or yes. Anywhere else it is a vowel.
    if "y" in cleaned[1:]:
        return cleaned
    token = "q" + cleaned[1:] if cleaned.startswith("y") else cleaned
    for team in VOWEL_TEAMS:
        if team in cleaned:
            return cleaned
    if re.search(r"[aeiou]r", cleaned):
        return cleaned
    if is_silent_e(token) or is_closed_syllable(token):
        return None
    return cleaned


def passage_lines(text, size, width):
    lines = []
    for index, paragraph in enumerate(text.strip().split("\n\n")):
        if index:
            lines.append("")
        lines.extend(wrap_text(paragraph.replace("\n", " "), "Helvetica", size, width))
    return lines


def passage_box_height(line_count, size):
    leading = size + 4
    if line_count <= 0:
        return leading + 18
    return 8 + size + (line_count - 1) * leading + 10


def validate(spec):
    errors = []
    passages = spec["passages"]
    if len(passages) != PASSAGE_COUNT:
        errors.append(f"{spec['label']}: expected {PASSAGE_COUNT} passages, got {len(passages)}")
    for index, passage in enumerate(passages, start=1):
        title = passage["title"]
        for field in ("title", "text", "setting", "character", "problem", "solution"):
            if not str(passage.get(field, "")).strip():
                errors.append(f"{spec['label']} {index} {title!r} is missing {field}")
        events = passage.get("events", [])
        if len(events) != 3 or not all(str(event).strip() for event in events):
            errors.append(f"{spec['label']} {index} {title!r} needs exactly 3 events")
        count = word_count(passage["text"])
        if not spec["min_words"] <= count <= spec["max_words"]:
            errors.append(
                f"{spec['label']} {index} {title!r} has {count} words "
                f"(need {spec['min_words']}-{spec['max_words']})"
            )
        if passage["character"].split()[0].lower() not in passage["text"].lower():
            errors.append(f"{spec['label']} {index} {title!r} does not name {passage['character']}")
        if spec["decodable"]:
            bad = []
            for word in words_in(f"{passage['title']} {passage['text']}"):
                problem = rejected_word(word)
                if problem and problem not in bad:
                    bad.append(problem)
            if bad:
                errors.append(f"{spec['label']} {index} {title!r} rejected: {', '.join(bad)}")
    return errors


def draw_header(c, title, grade_label):
    y = PAGE_H - 34
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, title)
    c.setFont("Helvetica", 12)
    grade_width = pdfmetrics.stringWidth(grade_label, "Helvetica", 12)
    c.drawString(PAGE_W - RIGHT - grade_width, y + 1, grade_label)
    y -= 26
    c.setFont("Helvetica", LABEL_SIZE)
    c.drawString(LEFT, y, "Name:")
    name_line = LEFT + pdfmetrics.stringWidth("Name: ", "Helvetica", LABEL_SIZE)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(name_line, y - 2, name_line + 200, y - 2)
    date_x = name_line + 224
    c.drawString(date_x, y, "Date:")
    date_line = date_x + pdfmetrics.stringWidth("Date: ", "Helvetica", LABEL_SIZE)
    c.line(date_line, y - 2, PAGE_W - RIGHT, y - 2)


def draw_footer(c, number, total):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_W / 2, 22, f"Passage {number} of {total}")


def draw_box(c, x, top, width, height):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.25)
    c.rect(x, top - height, width, height, stroke=1, fill=0)


def draw_label(c, x, top, label):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", LABEL_SIZE)
    c.drawString(x + 8, top - 8 - LABEL_SIZE, label)


def draw_passage_box(c, top, width, height, lines, size):
    draw_box(c, LEFT, top, width, height)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", size)
    leading = size + 4
    y = top - 8 - size
    for line in lines:
        if line:
            c.drawString(LEFT + 8, y, line)
        y -= leading


def draw_middle(c, x, top, width, height):
    draw_box(c, x, top, width, height)
    draw_label(c, x, top, "Middle (Three Events)")
    label_baseline = top - 8 - LABEL_SIZE
    # Leave a clear gap under the heading, and sit line 3 close to the box edge.
    first_baseline = label_baseline - 34
    last_baseline = (top - height) + 12
    slot = (first_baseline - last_baseline) / 2
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", LABEL_SIZE)
    number_width = pdfmetrics.stringWidth("3. ", "Helvetica", LABEL_SIZE)
    for index in range(3):
        baseline = first_baseline - index * slot
        c.drawString(x + 10, baseline, f"{index + 1}.")
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.7)
        c.line(x + 12 + number_width, baseline - 2, x + width - 12, baseline - 2)


def layout_for(spec, passages):
    width = PAGE_W - LEFT - RIGHT
    text_width = width - 16
    size = spec["font_size"]
    longest = 0
    for passage in passages:
        longest = max(longest, len(passage_lines(passage["text"], size, text_width)))
    passage_h = passage_box_height(longest, size)
    span = CONTENT_TOP - CONTENT_BOTTOM
    remaining = span - passage_h - 4 * GAP
    weights = [1.0, 1.05, 1.55, 1.0]
    unit = remaining / sum(weights)
    setting_h, begin_h, middle_h, _end_h = [unit * weight for weight in weights]
    end_h = span - passage_h - setting_h - begin_h - middle_h - 4 * GAP
    minimums = {
        "setting": (setting_h, 76),
        "beginning": (begin_h, 76),
        "middle": (middle_h, 116),
        "ending": (end_h, 76),
    }
    for name, (height, minimum) in minimums.items():
        if height < minimum:
            raise RuntimeError(
                f"{spec['label']} {name} box is {height:.0f} pt (need {minimum}). "
                "Shorten the longest passage."
            )
    return {
        "width": width,
        "text_width": text_width,
        "passage_h": passage_h,
        "setting_h": setting_h,
        "begin_h": begin_h,
        "middle_h": middle_h,
        "end_h": end_h,
    }


def write_student_packet(path, spec, passages, boxes):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(f"{spec['label']} Reading Passages")
    width = boxes["width"]
    for index, passage in enumerate(passages, start=1):
        if index > 1:
            c.showPage()
        draw_header(c, passage["title"], spec["label"])
        draw_footer(c, index, len(passages))
        top = CONTENT_TOP
        lines = passage_lines(passage["text"], spec["font_size"], boxes["text_width"])
        draw_passage_box(c, top, width, boxes["passage_h"], lines, spec["font_size"])
        top -= boxes["passage_h"] + GAP
        half = (width - GAP) / 2
        draw_box(c, LEFT, top, half, boxes["setting_h"])
        draw_label(c, LEFT, top, "Setting")
        draw_box(c, LEFT + half + GAP, top, half, boxes["setting_h"])
        draw_label(c, LEFT + half + GAP, top, "Character")
        top -= boxes["setting_h"] + GAP
        draw_box(c, LEFT, top, width, boxes["begin_h"])
        draw_label(c, LEFT, top, "Beginning (State Problem)")
        top -= boxes["begin_h"] + GAP
        draw_middle(c, LEFT, top, width, boxes["middle_h"])
        top -= boxes["middle_h"] + GAP
        draw_box(c, LEFT, top, width, boxes["end_h"])
        draw_label(c, LEFT, top, "Ending (Solution)")
    c.save()


def key_entries(passages, width):
    entries = []
    for number, passage in enumerate(passages, start=1):
        raw_lines = [
            (True, f"{number}. {passage['title']}"),
            (False, f"Setting: {passage['setting']}"),
            (False, f"Character: {passage['character']}"),
            (False, f"Beginning: {passage['problem']}"),
            (False, f"1. {passage['events'][0]}"),
            (False, f"2. {passage['events'][1]}"),
            (False, f"3. {passage['events'][2]}"),
            (False, f"Ending: {passage['solution']}"),
        ]
        lines = []
        for bold, text in raw_lines:
            font = "Helvetica-Bold" if bold else "Helvetica"
            wrapped = wrap_text(text, font, 12, width)
            for line_index, line in enumerate(wrapped):
                lines.append((bold and line_index == 0, line))
        entries.append(lines)
    return entries


def pack_key_pages(entries):
    leading = 15
    usable = PAGE_H - 108 - 42
    pages = []
    current = []
    used = 0
    for lines in entries:
        height = len(lines) * leading + 12
        if current and used + height > usable:
            pages.append(current)
            current = []
            used = 0
        current.append(lines)
        used += height
    if current:
        pages.append(current)
    return pages


def write_answer_key(path, spec, passages):
    width = PAGE_W - LEFT - RIGHT
    pages = pack_key_pages(key_entries(passages, width))
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
        y -= 20
        c.setFont("Helvetica", 14)
        c.drawString(LEFT, y, spec["key_title"])
        y -= 12
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.line(LEFT, y, PAGE_W - RIGHT, y)
        y -= 20
        for lines in entries:
            for bold, line in lines:
                c.setFont("Helvetica-Bold" if bold else "Helvetica", 12)
                c.drawString(LEFT, y, line)
                y -= 15
            y -= 12
        c.setFont("Helvetica", 12)
        c.drawCentredString(PAGE_W / 2, 22, f"Page {page_index + 1} of {total}")
    c.save()
    return total


def story(title, text, setting, character, problem, events, solution):
    return {
        "title": title,
        "text": text.strip(),
        "setting": setting,
        "character": character,
        "problem": problem,
        "events": events,
        "solution": solution,
    }


GRADE_1 = [
    story(
        "The Red Cap",
        "Sam had a red cap. He left it on a bench at the bus stop. The cap slid off and fell in the mud. Sam did not spot it. He got on his hands and did check the grass. At last he did spot the red cap. Sam did grab it and rub the mud off. He set the cap back on. Sam was glad he had his cap.",
        "the bus stop",
        "Sam",
        "Sam lost his red cap in the mud.",
        [
            "Sam checked the grass on his hands.",
            "He spotted the cap in the mud.",
            "He rubbed the mud off the cap.",
        ],
        "Sam set the cap back on.",
    ),
    story(
        "Jen and the Bun",
        "Jen went to the pond with a bun in a sack. A big dog ran up and did grab the bun. Jen did chase the dog, but the dog was fast. The dog did drop the bun in the mud. Jen did pick it up and toss it in the trash. She did pat the dog, and the dog sat still. Jen was not mad. She and the dog went on up the path.",
        "the pond",
        "Jen",
        "A dog grabbed Jen's bun.",
        [
            "Jen chased the dog.",
            "The dog dropped the bun in the mud.",
            "Jen tossed the bun in the trash and patted the dog.",
        ],
        "Jen was not mad, and she and the dog went up the path.",
    ),
    story(
        "The Lost Bolt",
        "Mike went on a bike ride to the lake. He hit a big rock on the path, and the bike did stop. A bolt fell off in the grass. Mike did hunt and hunt. At last he did spot the bolt. He did twist it back on. Then Mike did ride the rest of the path to the lake. He was glad the bike did not stop.",
        "the path to the lake",
        "Mike",
        "A bolt fell off Mike's bike.",
        [
            "The bike stopped when Mike hit a rock.",
            "Mike hunted in the grass for the bolt.",
            "He twisted the bolt back on.",
        ],
        "Mike rode the rest of the path to the lake.",
    ),
    story(
        "The Hot Cake",
        "Kate did bake a cake at home. She set the hot cake on a shelf. The cat did jump up and hit it. The cake fell on the rug with a splat. Kate did grab a mop and did scrub the rug. Then she did mix a fresh cake. She set this cake in a tin with a lid. The cat did not get the cake. Kate was glad.",
        "Kate's home",
        "Kate",
        "The cat knocked Kate's cake onto the rug.",
        [
            "Kate scrubbed the rug.",
            "She mixed a fresh cake.",
            "She set the new cake in a tin with a lid.",
        ],
        "The cat did not get the new cake.",
    ),
    story(
        "Tim and the Frog",
        "Tim had a pet frog in a tank on his desk. The lid was off. The frog slid past the rim and hid. Tim did check the desk. He did check the bed. He did check the rug. At last he did spot the frog on the lamp. Tim did cup it in his hands and set it back in the tank. He did snap the lid on. The frog sat on a rock.",
        "Tim's desk",
        "Tim",
        "Tim's frog got out of the tank.",
        [
            "Tim checked the desk, the bed, and the rug.",
            "He spotted the frog on the lamp.",
            "He set the frog back in the tank and snapped the lid on.",
        ],
        "The frog sat on a rock in the tank.",
    ),
    story(
        "Deb and the Bus",
        "Deb ran to the bus stop, but the bus had left. She did sit on the bench and sulk. She did kick a stone. Then a black truck did stop. It was Dad. Dad did wave, and Deb got in. Dad did drive her to class. Deb was glad she was not late. She did thank Dad and ran in to class.",
        "the bus stop",
        "Deb",
        "Deb missed the bus.",
        [
            "Deb sat on the bench.",
            "Dad stopped in a black truck.",
            "Dad drove Deb to class.",
        ],
        "Deb was not late and thanked Dad.",
    ),
    story(
        "The Wet Sock",
        "Nick had to get to a game, but a sock was lost. He did check the bed. He did check the rug. He did check the bin. At last he did spot the sock in the tub. It was wet. Nick did tug it on and did run to the game. He was not late. Nick did grin and hop on the grass.",
        "Nick's home",
        "Nick",
        "Nick could not find a sock before his game.",
        [
            "Nick checked the bed, the rug, and the bin.",
            "He found the wet sock in the tub.",
            "He tugged it on and ran to the game.",
        ],
        "Nick was not late.",
    ),
    story(
        "A Bug in the Tent",
        "Jake slept in a tent at camp. A bug bit his neck. He did slap at it. The bug hid in his pack. Jake did dump the pack on the mat. The bug fell off a sock. Jake did flick it off the mat and zip the flap. Then he slept. The bug did not get back in the tent. Jake was glad.",
        "a tent at camp",
        "Jake",
        "A bug bit Jake and hid in his pack.",
        [
            "Jake dumped the pack on the mat.",
            "The bug fell off a sock.",
            "Jake flicked the bug off and zipped the flap.",
        ],
        "The bug did not get back in, and Jake slept.",
    ),
    story(
        "Hope and the Fox",
        "Hope had a bone for the dog. She set it on a plate and went to get the dog. A fox slid in and stole the bone. Hope did chase the fox to the gate. The fox did drop the bone in a hole. Hope did dig it up and rub the mud off. She did hand the bone to the dog. The dog was glad, and Hope did grin.",
        "Hope's home",
        "Hope",
        "A fox stole the dog's bone.",
        [
            "Hope chased the fox to the gate.",
            "The fox dropped the bone in a hole.",
            "Hope dug it up and rubbed the mud off.",
        ],
        "Hope handed the bone to the dog.",
    ),
    story(
        "Cole and the Kite",
        "Cole went up a hill with a kite. A gust hit, and the kite got stuck in a shrub. Cole did tug the line, but the line did snap. He did sit and mend the line with a bit of tape. Then he did send the kite up. The kite rose in the sun. Cole did grin and run with it as it swept past.",
        "a hill",
        "Cole",
        "Cole's kite got stuck and the line snapped.",
        [
            "The kite got stuck in a shrub.",
            "Cole mended the line with tape.",
            "He sent the kite up again.",
        ],
        "The kite rose, and Cole ran with it.",
    ),
    story(
        "The Shed",
        "Max left a red top in the shed. A gust bent the flap, and mud got in. The top sank in a wet box. Max did not spot it. He did check the shelf. He did check the bin. At last he did drag the box to the mat. He did rub the top. Then it was not wet. Max did spin the top on the step. Max was glad he had the top.",
        "the shed",
        "Max",
        "Mud got on Max's top and he could not find it.",
        [
            "Max checked the shelf and the bin.",
            "He dragged the wet box to the mat.",
            "He rubbed the top until it was dry.",
        ],
        "Max spun the top on the step.",
    ),
    story(
        "The Gull and the Chips",
        "Liz had a sack of chips at lunch. She set the sack on a bench and went to get a drink. A gull swept in and stole the chips. Liz did chase the gull, but it fled to a pole. The sack split, and the chips fell in the sand. Liz did pick them up and toss them in the trash. Then she and a pal did split a bun. Liz was not mad.",
        "the lunch bench",
        "Liz",
        "A gull stole Liz's chips.",
        [
            "Liz chased the gull to a pole.",
            "The chips fell in the sand.",
            "Liz tossed them in the trash and split a bun with a pal.",
        ],
        "Liz was not mad.",
    ),
    story(
        "The Class Skit",
        "Ben had a skit to tell at class, but he lost the list. He did blush and stand still. A pal did hiss the next bit to him. Then Ben did tell the rest of the skit. The class did clap. Ben did grin at his pal. He was glad a pal did help him. Ben did a fine job.",
        "class",
        "Ben",
        "Ben lost the list for his skit.",
        [
            "Ben blushed and stood still.",
            "A pal hissed the next bit.",
            "Ben told the rest of the skit.",
        ],
        "The class clapped, and Ben was glad his pal helped.",
    ),
    story(
        "At the Lake",
        "Pete and Jade went to the lake. They had a plan to swim. Pete did jump off a rock and got a cramp in his leg. He did yell and flap his hands. Jade did hold a long stick to him. Pete did grip the stick. Jade did tug him in to the sand. Pete sat and did rest. He did thank Jade for the help. He was glad she was at the lake.",
        "the lake",
        "Pete",
        "Pete got a cramp after he jumped off a rock.",
        [
            "Pete yelled and flapped his hands.",
            "Jade held a long stick out for him.",
            "Jade tugged Pete in to the sand.",
        ],
        "Pete rested and thanked Jade.",
    ),
    story(
        "The Tent at Dusk",
        "Shane set up a tent on the grass. At dusk a gust hit, and the flap slid off. The tent did tilt. Shane did grab the flap and clip it back on. He did check the pegs and tap them in. Then he got in the tent. The flap held. Shane slept, and the tent did not rip. He was glad he did check the pegs.",
        "the grass",
        "Shane",
        "The tent flap slid off in a gust.",
        [
            "The tent tilted.",
            "Shane clipped the flap back on.",
            "He tapped the pegs in.",
        ],
        "The flap held, and Shane slept.",
    ),
    story(
        "The Lost Chick",
        "Mom had a chick that was lost in the shed. Seth did hunt for it. He did check the pen. He did check the bin. He did check a pile of sticks. The chick was in a tub. Seth did lift it up and set it back with the hen. The chick did peck at a snack. Seth did grin. He was glad the chick was back with the hen.",
        "the shed",
        "Seth",
        "A chick was lost in the shed.",
        [
            "Seth checked the pen, the bin, and a pile of sticks.",
            "He found the chick in a tub.",
            "He set the chick back with the hen.",
        ],
        "The chick pecked at a snack, and Seth was glad.",
    ),
    story(
        "The Note in the Crack",
        "Eve left a note on the desk for Dad. The note slid off and fell in a crack. Dad did not spot it. Eve did check the shelf. She did check the trash. At last she did spot a bit of the note in the crack. She did tug it up and hand it to Dad. The note said she had fed the dog. Dad did smile and thank Eve. Eve was glad.",
        "the desk",
        "Eve",
        "Eve's note fell into a crack.",
        [
            "Dad did not spot the note.",
            "Eve checked the shelf and the trash.",
            "She tugged the note out of the crack.",
        ],
        "Dad smiled and thanked Eve for feeding the dog.",
    ),
    story(
        "Tam and the Cap",
        "A gust swept the cap off Tam. The cap fled to the top of a bush. Tam did jump, but she did not grab it. She did get a stick and tap the cap. The cap fell in the grass. Tam did pick it up and clip it on. The next gust did not lift the cap. Tam did grin and run on the path.",
        "the path",
        "Tam",
        "A gust blew Tam's cap into a bush.",
        [
            "Tam jumped but could not grab the cap.",
            "She tapped the cap with a stick.",
            "The cap fell in the grass and she clipped it on.",
        ],
        "The next gust did not lift the cap.",
    ),
    story(
        "Rod and the Milk",
        "Rod did tip a glass of milk. The milk ran on the desk and did drip on the rug. Rod did gasp. He did get a mop and a rag. He did scrub the desk, and he did scrub the rug. The milk was off the desk and off the rug. Mom did thank Rod for the help. Rod was glad he did scrub the mess.",
        "the desk",
        "Rod",
        "Rod spilled milk on the desk and the rug.",
        [
            "The milk dripped on the rug.",
            "Rod got a mop and a rag.",
            "He scrubbed the desk and the rug.",
        ],
        "Mom thanked Rod, and the milk was gone.",
    ),
    story(
        "Blocks in the Sand",
        "Luke and Dale did dig in the sand. They did pack a pan with sand and tip it. A block of sand sat up. They did make five blocks in a line. A wave hit, but it did not smash the blocks. Luke did slap the next wave back with a stick. Dale did grin. They did grin at the blocks as the sun set.",
        "the sand",
        "Luke",
        "Luke and Dale wanted the waves not to smash their sand blocks.",
        [
            "They packed a pan with sand and tipped it.",
            "They made five blocks in a line.",
            "Luke slapped the next wave back with a stick.",
        ],
        "The wave did not smash the blocks.",
    ),
]


GRADE_2 = [
    story(
        "The Library Book",
        """Maya's library book was due the next morning. She checked her backpack, her desk, and the couch. She looked in the kitchen and by the front door. The book was not in any of those places.

Before bed, Maya got on the floor and looked under the bed. The book was beside a stuffed dog. She brushed off the dust and slid the book into her backpack so she would not forget it.

At school, Maya gave the book to the librarian before class began. The librarian smiled and said it was right on time. Maya felt proud as she walked to class.""",
        "Maya's bedroom",
        "Maya",
        "Maya could not find her library book, and it was due.",
        [
            "She looked in her backpack, on her desk, and around the house.",
            "She found the book under the bed.",
            "She put it in her backpack.",
        ],
        "Maya returned the book on time.",
    ),
    story(
        "The Popped Ball",
        """Leo was practicing shots in the gym when his kick sent the ball into a chair leg. The ball popped and hissed. Leo froze. He knew the class needed that ball for games.

Leo picked up the flat ball and walked it to Coach Ramirez. He told the truth and said he was sorry. Coach handed him tape, and Leo pressed it over the hole so the class could still roll the ball. After school, Coach brought a new ball from the office.

Leo thanked him and promised to aim away from the chairs. The next shot stayed on the gym floor.""",
        "the gym",
        "Leo",
        "Leo popped the class ball.",
        [
            "Leo told Coach Ramirez the truth.",
            "He taped the hole so the class could still use the ball.",
            "Coach brought a new ball from the office.",
        ],
        "Leo aimed away from the chairs, and his next shot stayed on the floor.",
    ),
    story(
        "Ruby Gets Out",
        """Nina was the class helper for Ruby the rabbit. She latched the hutch, or so she thought. At reading time, a student whispered that Ruby was on the rug.

Nina closed the classroom door so Ruby could not hop into the hall. She looked under the reading shelves and behind the paint jars. At last she found Ruby sitting in a box of paper scraps. Nina lifted her gently and set her back in the hutch. This time she checked the latch twice.

Ruby nibbled her hay. Nina told the teacher what had happened, and they added a second clip to the door.""",
        "the classroom",
        "Nina",
        "Ruby the rabbit got out of the hutch.",
        [
            "Nina closed the classroom door.",
            "She looked under the shelves and behind the paint jars.",
            "She found Ruby in a box of paper scraps.",
        ],
        "Nina put Ruby back and they added a second clip to the hutch.",
    ),
    story(
        "The Forgotten Lunch",
        """Jay sat down at lunch and unzipped his backpack. His lunch bag was not there. His stomach growled, and the cafeteria line was already closed.

His friend Elena opened her lunch and split the sandwich and the apple slices. Jay ate slowly and said thank you. At recess he helped Elena carry the ball bag out to the field.

The next morning Jay packed his own lunch and put an extra cheese stick on top for Elena. He zipped the backpack and checked the pocket twice before he left home. Elena smiled at lunch when she saw the extra snack in her hand.""",
        "the cafeteria",
        "Jay",
        "Jay forgot his lunch.",
        [
            "Elena shared her sandwich and apple slices.",
            "Jay helped Elena carry the ball bag at recess.",
            "The next morning he packed an extra cheese stick for Elena.",
        ],
        "Jay brought lunch and a thank-you snack for Elena.",
    ),
    story(
        "The Drooping Plant",
        """Priya's bean plant sat on a high shelf in the classroom. One Monday the stem bent over and the leaves looked soft. Priya was afraid the plant was dying.

She asked the teacher if they could move it. Together they set the pot on the sunny windowsill. Priya gave the soil a small drink of water, but she did not flood it. She wrote the date on a card beside the pot.

By Wednesday the stem had lifted and the leaves felt firmer. Priya smiled and kept the plant in the sun. She checked the soil with her finger each morning.""",
        "the classroom",
        "Priya",
        "Priya's bean plant was drooping.",
        [
            "She and the teacher moved the pot to the sunny windowsill.",
            "Priya gave the soil a small drink of water.",
            "She wrote the date on a card and checked the soil each morning.",
        ],
        "The stem lifted and the leaves felt firmer.",
    ),
    story(
        "The Paper Crown",
        """Omar was the king in the class play. Five minutes before the show, the paper crown was not on the prop table. He checked the costume bin and the music stand. No crown.

His partner, Lila, grabbed yellow paper and tape. They cut a band, taped it to fit Omar's head, and drew three paper jewels. It was simple, but it looked bright under the lights.

Omar walked on stage wearing the new crown. He remembered his lines, and the class clapped. After the play he saved the crown in his folder. He showed it to his family at home that night.""",
        "the school stage",
        "Omar",
        "The paper crown for the play was missing.",
        [
            "Omar checked the costume bin and the music stand.",
            "Lila helped him cut and tape a new crown.",
            "They drew three paper jewels on it.",
        ],
        "Omar wore the new crown, remembered his lines, and saved it.",
    ),
    story(
        "Mixed-Up Puzzle",
        """Ana had almost finished a puzzle of a red barn. Her little brother Mateo ran through the room and bumped the table. Pieces slid onto the rug and mixed with the ones still in the box.

Ana took a breath instead of yelling. She and Mateo picked up every piece. Ana sorted the edge pieces into a pile, and Mateo stacked the red ones. They rebuilt the border first.

They worked until the barn door clicked into place. Mateo clapped. Ana let him put in the last piece. They left the finished barn on the table for the rest of the day.""",
        "the living room",
        "Ana",
        "Mateo bumped the table and mixed up Ana's puzzle.",
        [
            "Ana and Mateo picked up every piece.",
            "They sorted edges and red pieces.",
            "They rebuilt the border first.",
        ],
        "They finished the puzzle, and Mateo put in the last piece.",
    ),
    story(
        "Ants at the Picnic",
        """Diego and his uncle spread a blanket in the park and set out watermelon, rolls, and cheese. A line of ants crossed the blanket and headed for the watermelon.

Diego waved his hands, but more ants came. His uncle said they should move. They packed the food into closed tubs, shook the blanket, and carried everything to a picnic table in the sun.

Diego wiped the table, and they ate there. The ants stayed in the grass. Diego kept the tubs shut between bites. His uncle said the picnic table had been the better spot all along, and Diego agreed with him.""",
        "the park",
        "Diego",
        "Ants crawled onto the picnic blanket.",
        [
            "Waving his hands did not stop the ants.",
            "They packed the food into closed tubs and shook the blanket.",
            "They carried everything to a picnic table.",
        ],
        "They ate at the table, and the ants stayed in the grass.",
    ),
    story(
        "The Slipped Chain",
        """Rosa was riding home when her bike chain slipped off the front gears. The pedals spun, but the bike would not move. She walked it to the sidewalk so cars could pass.

Her neighbor, Mr. Brooks, was washing his car. He showed Rosa how to lift the chain with a stick and set it back on the small gear. Rosa tried once and missed. She tried again, slowly, and the chain caught.

She pedaled down the driveway and back. The chain stayed on. Rosa thanked Mr. Brooks and rode the rest of the way home. She checked the chain once more at the corner.""",
        "the sidewalk by Rosa's street",
        "Rosa",
        "Rosa's bike chain slipped off.",
        [
            "She walked the bike to the sidewalk.",
            "Mr. Brooks showed her how to set the chain with a stick.",
            "Rosa tried again slowly, and the chain caught.",
        ],
        "The chain stayed on, and Rosa rode home.",
    ),
    story(
        "The Cloudy Tank",
        """The classroom fish tank looked like fog. Ben could barely see the three fish. He noticed extra flakes floating on top, left from a feeding he had done at lunch.

Ben told Ms. Patel. She said too much food can make the water cloudy. Ben scooped out the extra flakes with a net. Then Ms. Patel helped him replace some of the water with fresh water from a bucket.

The next morning the tank was clearer, and the fish swam near the glass. Ben taped a feeding chart on the tank so no one would feed them twice. The fish kept swimming in the clear water.""",
        "the classroom",
        "Ben",
        "The fish tank was cloudy from too much food.",
        [
            "Ben told Ms. Patel about the extra flakes.",
            "He scooped the flakes out with a net.",
            "They replaced some of the water.",
        ],
        "The tank cleared, and Ben taped up a feeding chart.",
    ),
    story(
        "Lost Glasses",
        """Elena could not read the board. Her glasses were gone. She checked her desk, the library bin, and the gym office. She was starting to worry she would miss the spelling test.

At recess she pulled on her hoodie because of the wind. Something hard tapped her elbow. She reached into the front pocket and felt the case. The glasses were inside, folded and safe.

Elena put them on and the trees looked sharp again. She went back to class, told her teacher, and finished the test. From then on she clipped the case to her backpack. She did not want to hunt for them again.""",
        "school",
        "Elena",
        "Elena lost her glasses before a spelling test.",
        [
            "She checked her desk, the library bin, and the gym office.",
            "She felt the case in her hoodie pocket.",
            "She put the glasses on and went back to class.",
        ],
        "Elena finished the test and clipped the case to her backpack.",
    ),
    story(
        "Kite in the Tree",
        """Malik was flying a red kite at the park when a gust dropped it into an oak tree. The string tangled in the branches. Malik tugged, and the kite only tipped sideways.

His older sister, Noor, found a long lightweight pole by the garden shed. She lifted the string, and Malik held the kite so it would not rip. The loop slid free.

They walked to the open field, away from the trees. Malik sent the kite up again. This time he kept his eyes on the branches and let out string slowly. The kite stayed high in the open sky.""",
        "the park",
        "Malik",
        "Malik's kite was stuck in a tree.",
        [
            "Tugging the string did not free the kite.",
            "Noor lifted the string with a long pole while Malik held the kite.",
            "The loop slid free.",
        ],
        "They flew the kite in the open field, away from the trees.",
    ),
    story(
        "A Cold Hamster",
        """Lucy noticed that Pip the hamster was curled in a tight ball. His cage sat under the heating vent, and cold air poured on the bedding whenever the fan clicked on.

Lucy told Mr. Chen. They moved the cage to a quiet shelf away from the vent. Lucy added a handful of soft bedding and a cardboard hut. Pip crept inside and his breathing looked calmer.

Lucy checked him after lunch. Pip was running on the wheel. Mr. Chen wrote "Keep away from the vent" on a card and taped it above the shelf. Pip stayed warm for the rest of the day.""",
        "the classroom",
        "Lucy",
        "Pip the hamster was cold under the heating vent.",
        [
            "Lucy told Mr. Chen.",
            "They moved the cage away from the vent.",
            "Lucy added bedding and a cardboard hut.",
        ],
        "Pip ran on his wheel, and they posted a sign about the vent.",
    ),
    story(
        "The Smudged Painting",
        """Andre had spent all art class on a painting of the playground. As he carried the wet paper to the drying rack, his sleeve dragged across the sky. A gray smear covered the sun.

Andre wanted to throw it away. Ms. Brooks said to wait until it dried and then decide. When the paper was dry, Andre looked again. The smear could be a cloud.

He painted soft edges around it and added two smaller clouds. The playground looked stormy and interesting. Andre hung the painting in the hall with his name on a card. Classmates stopped to look at the stormy sky.""",
        "the art room",
        "Andre",
        "Andre's sleeve smudged the sun on his wet painting.",
        [
            "Ms. Brooks told him to wait until the paper dried.",
            "Andre decided the smear could be a cloud.",
            "He painted soft edges and two smaller clouds.",
        ],
        "Andre hung the painting in the hall.",
    ),
    story(
        "The Permission Slip",
        """Sofia's class was going to the science museum, but her permission slip was missing on the day it was due. She dumped her folder on the kitchen table. Old drawings fell out. No slip.

She and her dad checked the backpack pockets and the mail pile. Dad opened the kitchen drawer where they kept pencils. The slip was under a pad of paper, still blank.

Dad signed it. Sofia put it in a folder and zipped that folder into the front pocket. The next morning she handed it to her teacher and got her name on the trip list. Sofia grinned.""",
        "Sofia's kitchen",
        "Sofia",
        "Sofia's permission slip was missing on the day it was due.",
        [
            "She dumped her folder and found only old drawings.",
            "She and her dad checked the backpack and the mail.",
            "They found the blank slip in the kitchen drawer.",
        ],
        "Dad signed the slip, and Sofia's name went on the trip list.",
    ),
    story(
        "A Seat at the Game",
        """Noah was new and sat alone on the bench at recess. Camila's team needed another player for kickball. She walked over and asked if he wanted to play.

Noah said he did not know the rules. Camila explained them in three short steps: kick, run, and tag the base. She let him bat second so he could watch once.

Noah kicked a soft ground ball and reached first base. His team cheered. The next day he came to the bench smiling, and Camila saved him a spot in the line. Noah said the game was the best part of his school day.""",
        "the playground",
        "Camila",
        "Noah was new and sitting alone at recess.",
        [
            "Camila asked Noah to play kickball.",
            "She explained kick, run, and tag the base.",
            "She let him bat second so he could watch once.",
        ],
        "Noah reached first base, and Camila saved him a spot the next day.",
    ),
    story(
        "Boxes Behind the Counter",
        """Hector was in charge of the cookie sale. He counted the boxes on the table and came up two short. The customers in line were waiting, and he did not want to sell treats he could not hand over.

He checked the supply closet and the teacher's desk. Then he looked behind the counter. Two boxes had slid against the wall, hidden by a poster board.

Hector set them on the table and counted again. The number matched his list. He sold the cookies, wrote the total, and pushed the extra boxes forward so none could hide. The line moved, and no one left without a box.""",
        "the cookie sale table",
        "Hector",
        "Hector was two boxes short at the cookie sale.",
        [
            "He checked the supply closet and the teacher's desk.",
            "He found two boxes behind the counter.",
            "He counted again and the number matched his list.",
        ],
        "Hector sold the cookies and moved the extra boxes where he could see them.",
    ),
    story(
        "Vacuum Day",
        """Amina's dog, Bean, ran and hid whenever the vacuum started. On Saturday Amina needed to clean her room, but Bean was shaking behind the bed.

Amina turned the vacuum off. She let Bean sniff the silent machine and gave him a calm pat. Then she turned it on in the hall, far from him, and tossed his ball so he had something else to think about.

Bean stayed in the doorway instead of running. Amina vacuumed a small square of rug and stopped. The next Saturday Bean watched from his bed. He still disliked the noise, but he did not hide.""",
        "Amina's room",
        "Amina",
        "Bean hid and shook when Amina tried to vacuum.",
        [
            "Amina turned the vacuum off and let Bean sniff it.",
            "She turned it on in the hall and tossed his ball.",
            "Bean stayed in the doorway while she vacuumed a small square.",
        ],
        "The next Saturday Bean watched from his bed and did not hide.",
    ),
    story(
        "The Empty Feeder",
        """Jonah looked out at the backyard and saw the bird feeder hanging empty. The chickadees landed, peeked in, and flew off. He had forgotten to fill it after the last storm.

He poured seed into a cup, carried it outside, and filled the feeder to the line his mom had marked. He latched the lid so squirrels would have a harder time. Then he stood back by the window.

Within a few minutes the chickadees returned. Jonah watched them take turns on the perch. He wrote "Fill feeder" on the family calendar so it would not sit empty again. Jonah smiled at the full perch.""",
        "Jonah's backyard",
        "Jonah",
        "The bird feeder was empty, so the birds flew off.",
        [
            "Jonah filled the feeder to the marked line.",
            "He latched the lid.",
            "He watched the chickadees come back.",
        ],
        "Jonah wrote a reminder on the family calendar.",
    ),
    story(
        "The Ripped Poster",
        """Lila's group had finished a poster about the water cycle. On the morning of the presentation, she found a rip through the sentence about clouds. The corner of the poster had caught on a chair.

Lila did not try to hide it. She turned the poster over, and her partners held it flat while she pressed tape along the rip. Then she wrote the torn sentence again in neat letters above the tape.

When they presented, the poster stayed together. The class could read every word. Lila kept a roll of tape in the project box after that. The group felt ready to present.""",
        "the classroom",
        "Lila",
        "The water-cycle poster ripped before the presentation.",
        [
            "Lila showed her partners the rip instead of hiding it.",
            "They taped the back of the poster.",
            "Lila wrote the torn sentence again.",
        ],
        "The poster stayed together during the presentation.",
    ),
]


GRADE_3 = [
    story(
        "The Closed Blind",
        """Amira's science project compared two bean plants. She set both pots in the same corner and gave them the same water. After four days, the plant beside the bookshelf had wilted. Its stem curved toward the glass.

Amira examined the corner and noticed the blind was pulled down each afternoon. The bookshelf plant spent those hours in shadow. She wrote in her log that the plants had the same water but different light.

With her teacher's permission, she raised the blind after lunch and turned both pots a little each day. She did not add extra water, so light would be the only change. Three days later the wilted stem had straightened.

Amira added a sentence to her board: the plant was not sick. It had been searching for sun. She left the blind raised for the rest of the week and still checked both plants every morning before class.""",
        "the classroom science corner",
        "Amira",
        "One bean plant wilted while the other stayed sturdy.",
        [
            "Amira noticed the blind shaded the bookshelf plant each afternoon.",
            "She raised the blind and turned both pots.",
            "She kept the water the same so only the light changed.",
        ],
        "The wilted stem straightened, and Amira recorded that the plant had been searching for sun.",
    ),
    story(
        "The Blocked Drain",
        """After a hard rain, the path beside the creek was a long puddle. Jordan was walking to the bridge when he saw leaves packed against a metal drain. Water had nowhere to go, so it spread across the gravel.

Jordan did not pull the grate up by himself. He found the park worker, Ms. Alvarez, and showed her the clog. Together they lifted the grate. Jordan raked leaves into a bucket while Ms. Alvarez cleared the mud with a shovel.

The water began to drop. Jordan stayed until the path showed again. Ms. Alvarez thanked him and set the bucket of leaves by the compost bin.

On the way home, Jordan told his family why the puddle had not been just a puddle. A blocked drain had turned the path into a pond. He said he would check that grate after the next storm. Jordan waved as he left the path.""",
        "the creek path",
        "Jordan",
        "A clogged drain flooded the path after the rain.",
        [
            "Jordan found leaves packed against the drain.",
            "He got Ms. Alvarez instead of lifting the grate alone.",
            "They raked the leaves and cleared the mud.",
        ],
        "The water dropped and the path showed again.",
    ),
    story(
        "The Understudy",
        """The class play was that afternoon, and the lead, Priya, could barely speak. She had cheered too loudly at the morning game. Ms. Brooks looked at the cast and asked who knew the part.

Camila had listened from the side during every practice, mouthing the lines while she waited for her small scene. She hesitated, then said she could try. At lunch she walked the stage alone and spoke the opening three times.

When the curtain opened, Camila's hands shook. She looked at Priya in the front row, took a breath, and began. She missed one word, paused, and kept going. The class followed the story anyway.

After the bow, Priya whispered that the pause had sounded like part of the line. Camila smiled. Watching had been practice, even when she was not in the spotlight. She kept the script in her folder for the next show. She was glad she had tried.""",
        "the school stage",
        "Camila",
        "The lead lost her voice just before the play.",
        [
            "Camila said she could try because she had mouthed the lines in practice.",
            "She practiced the opening alone at lunch.",
            "On stage she missed a word, paused, and kept going.",
        ],
        "The class followed the story, and Camila realized watching had been practice.",
    ),
    story(
        "The Switched Backpacks",
        """On the bus home, Malik grabbed a blue backpack from the seat and did not look at the tag. At his kitchen table he unzipped it and found a math folder with another name: Andre Ellis. His own backpack, with the tablet the class used for reading, was still on the bus.

Malik called the number written inside Andre's folder. Andre had made the same mistake and was standing in his own kitchen with Malik's bag. They agreed to meet at the school office before it locked.

Ms. Nguyen watched them trade bags and checked the tablet. The screen lit up, and nothing was cracked. Malik slid his reading folder back into the right pocket.

He looped a bright ribbon through his zipper that night. The next afternoon he checked the tag before he stepped off the bus. Andre did the same with his own bag. Both boys laughed with relief.""",
        "the bus and the school office",
        "Malik",
        "Malik took Andre's backpack and left his own, with the class tablet, on the bus.",
        [
            "Malik found Andre's name in the math folder.",
            "He called the number inside and learned Andre had his bag.",
            "They met at the office and traded bags.",
        ],
        "The tablet was safe, and Malik marked his zipper so he would check the tag.",
    ),
    story(
        "The Collar Tag",
        """A small cry came from the storm drain by the playground. Elena knelt and saw a kitten pressed against the metal, too scared to climb the wet side. She did not reach in. She ran for Mr. Cole, the custodian.

Mr. Cole brought a towel and a flashlight. He lay on the sidewalk, spoke softly, and slid the towel down like a ramp. The kitten crept up and into Elena's arms. A collar sat under the wet fur, and the tag was still readable: "Pip. Call Rosa."

Elena used the office phone. Rosa arrived out of breath and scooped Pip up, explaining that the kitten had slipped out during the rain. She thanked them both.

Elena washed her hands and wrote the afternoon in her journal. Asking for help had been faster than trying to be brave alone. She told her class about the towel ramp the next day too.""",
        "the playground storm drain",
        "Elena",
        "A kitten was trapped in the storm drain.",
        [
            "Elena got Mr. Cole instead of reaching in.",
            "Mr. Cole used a towel as a ramp and a flashlight.",
            "They read the collar tag and called Rosa.",
        ],
        "Rosa came for Pip, and Elena learned that getting help was the brave choice.",
    ),
    story(
        "Notes on the Gym Floor",
        """The math team met in the gym to explain a puzzle at the assembly. Ten minutes before they went on, their note cards were gone. A draft from the open door had blown the stack off the bleachers.

Noah dropped to his knees and found two cards under the bottom row. The other three were smeared from a wet shoe print. He could read the titles but not the middle steps.

His partner, Lila, said they still remembered the puzzle because they had built it. They whispered the steps in order: draw the chart, test one change, and check the result. Noah wrote fresh cards in big letters.

On stage, the chart made sense. A younger student even asked a question they could answer. The lost cards had been a scare, not the end of the explanation. Noah clipped the new cards into his folder before he left the gym.""",
        "the gym",
        "Noah",
        "The math team's note cards blew away and some were ruined.",
        [
            "Noah found two cards under the bleachers.",
            "The other cards were smeared, so the middle steps were gone.",
            "He and Lila rebuilt the steps from memory and wrote new cards.",
        ],
        "They explained the puzzle on stage and answered a question.",
    ),
    story(
        "Tomatoes After the Rain",
        """The community garden tomatoes had split overnight. Heavy rain had soaked the ripe fruit, and the skins had burst in pale lines. If the class waited until Friday's harvest, many of the tomatoes would spoil on the vine.

Sofia, the garden helper, brought a basket and a pair of scissors. She showed the group how to clip only the split ones, leaving the firm green tomatoes to finish. Juice stained her hands, but the basket filled quickly.

At lunch the class rinsed the pieces and set them out with salt on a tray. Students who usually skipped tomatoes took a cup. Sofia wrote "Pick ripe fruit after heavy rain" on the garden clipboard.

The plants looked thinner, but they were healthier. The next rain would not have so much soft fruit waiting to break. Sofia checked the vines again before she went inside. She was glad they had not waited.""",
        "the community garden",
        "Sofia",
        "Ripe tomatoes split after heavy rain and would spoil if left on the vine.",
        [
            "Sofia brought a basket and scissors.",
            "The group clipped only the split tomatoes.",
            "They rinsed the pieces and served them at lunch.",
        ],
        "The class ate the tomatoes, and Sofia wrote a note to pick ripe fruit after heavy rain.",
    ),
    story(
        "Fish at the Surface",
        """During quiet reading, Andre noticed the classroom fish hanging near the top of the tank. Their mouths broke the surface again and again. The filter, which usually hummed, was silent.

He did not tap the glass. He told Mr. Chen, who lifted the filter lid and found it packed with gray gunk. The fish were not playing. They were hunting for air.

Mr. Chen rinsed the filter in tank water, not soap, and Andre held the bucket steady. When the filter clicked back on, a stream of bubbles rolled through the tank. By the end of reading, the fish had dropped to the middle of the water.

Andre added "Check the hum" to the tank job list. A quiet filter was a problem, not a peaceful sound. Andre listened for the hum every morning after that. The fish stayed in the middle of the tank, and the water stayed clear too.""",
        "the classroom",
        "Andre",
        "The fish stayed at the surface because the filter had stopped.",
        [
            "Andre told Mr. Chen instead of tapping the glass.",
            "They found the filter packed with gunk.",
            "Mr. Chen rinsed it in tank water and turned it back on.",
        ],
        "The fish swam lower, and Andre added a filter check to the job list.",
    ),
    story(
        "The Missing Trumpet",
        """The concert started in twenty minutes, and Diego's trumpet was not in the band room cubby. He had practiced that morning and was sure he had set the case on the bench. Now the bench held only a stack of music.

Diego checked the practice rooms and the office. Then he opened the closet where extra stands were stored. His case was on the floor, shoved back when someone rolled a cart inside. The latch was still closed.

He had just enough time to warm up in the hall. His first notes wobbled, then settled. When the band entered, Diego watched the director's hands and came in on the beat.

After the concert he slid the case onto the cubby shelf, not the bench. A shelf could not be cleared by a rolling cart. Diego checked the cubby again before he left the band room. His case was still there.""",
        "the band room",
        "Diego",
        "Diego's trumpet case vanished before the concert.",
        [
            "He checked the practice rooms and the office.",
            "He found the case on the closet floor.",
            "He warmed up in the hall and entered on the beat.",
        ],
        "Diego played, then stored the case on the shelf so a cart could not shove it away.",
    ),
    story(
        "Juice on the Library Book",
        """Lila's little brother borrowed her library book and set a cup too close to the page. By the time Lila saw it, apple juice had soaked the chapter about bridges. The paper buckled and the ink blurred.

She did not try to hide the book in her backpack. At the library desk she showed Ms. Ortiz the stain and said it was an accident at home. Ms. Ortiz nodded and explained that damaged books have to be replaced.

Lila used money she had saved from feeding a neighbor's cat. She paid for the copy, and Ms. Ortiz ordered another one. Lila checked out a different bridges book so she could finish her report.

That night she gave her brother a plastic cup with a lid. The next book stayed on the table, far from any drink. Lila finished her bridges report with the new copy. She turned it in on time.""",
        "home and the library",
        "Lila",
        "Juice ruined a chapter of Lila's library book.",
        [
            "Lila showed the stain to Ms. Ortiz instead of hiding it.",
            "She paid for a replacement with chore money.",
            "She checked out a different book to finish her report.",
        ],
        "A new copy was ordered, and drinks at home got lids.",
    ),
    story(
        "A Plan for the Mud",
        """The soccer field was mud from sideline to sideline. Passes that usually skimmed the grass stopped dead. Hector's team was down by one, and long kicks kept the ball with the other side.

Hector called his teammates into a huddle. He said they should pass short, to the nearest foot, and stay out of the deep puddle by the goal. The keeper, Amina, would roll the ball instead of punting it into the mess.

The plan was slower, but the ball stayed with them. Hector tapped a pass to Jonah, who slid it into the corner. The game ended tied. Nobody cheered like it was a championship, but they shook hands standing up instead of slipping.

Hector thanked Amina for the calm rolls. Mud had changed the game, so they had changed the plan. Hector wrote the short-pass idea in his notebook that night. He wanted to remember it.""",
        "the muddy soccer field",
        "Hector",
        "Long passes stopped in the mud, and Hector's team was losing.",
        [
            "Hector told the team to pass short.",
            "He told them to avoid the deep puddle.",
            "Amina rolled the ball instead of punting it.",
        ],
        "The short passes led to a tying goal.",
    ),
    story(
        "The Creek as a Guide",
        """The trail map had slipped out of Rosa's pocket somewhere on the switchbacks. The group stopped at a split where both paths looked the same. Voices got quick and worried.

Mr. Ellis reminded them not to scatter. Rosa remembered the ranger's morning talk: the creek stayed on the left all the way to the meadow. They listened and heard water over rocks. Rosa pointed left, and the group walked single file, watching for the blue trail marks she had forgotten until then.

The marks appeared again beside a fallen log. Ten minutes later the ranger met them at the meadow, already walking back to check on slow groups. Rosa told him about the map.

He handed her a spare and showed her the zip pocket on her pack. She put the map there before she took another step. The group stayed together for the rest of the walk. Rosa led them.""",
        "the hiking trail",
        "Rosa",
        "The group lost the trail map at a fork in the path.",
        [
            "Mr. Ellis kept the group from scattering.",
            "Rosa remembered that the creek stayed on the left.",
            "They followed the water and found the blue trail marks.",
        ],
        "The ranger met them and Rosa zipped the spare map into her pack.",
    ),
    story(
        "Bread That Would Not Rise",
        """The dough for family dinner sat in the bowl like a pale stone. Sam had followed the card, but the kitchen was cold because a window was open. An hour passed, and the dough had barely moved.

Sam's grandmother pressed it with a finger and shook her head. She did not throw it out. She set the bowl on a rack above the warm stove, covered it with a damp towel, and told Sam to wait without peeking every minute.

The next time they looked, the dough had domed over the rim. Sam shaped it into a pan. While it baked, the kitchen smelled like the bakery down the street.

At dinner the bread was not perfect, but it was theirs. Sam wrote "warm spot, damp towel" on the recipe card so the next cold day would not stop the rise. He left the card where the family could see it.""",
        "Sam's kitchen",
        "Sam",
        "The bread dough would not rise in the cold kitchen.",
        [
            "Sam's grandmother saw that the window had chilled the room.",
            "She set the bowl above the warm stove.",
            "She covered it with a damp towel and told Sam to wait.",
        ],
        "The dough rose, they baked it, and Sam added the trick to the recipe card.",
    ),
    story(
        "Before the Copies",
        """The school paper was ready for the copier, stacked in the office. Jade read her article one last time and felt her stomach drop. She had written that the garden club met on Thursday. The club met on Tuesday. Fifty copies would spread the mistake.

Jade did not wait for someone else to notice. She told Mr. Patel, who ran the copier, and showed him the sentence. He had not started the machine. Together they opened the file, changed Thursday to Tuesday, and printed a single test page.

Jade checked the date, the names, and the lunch menu before she nodded. Then the copier began its steady shuffle. Students would arrive at the garden on the right day.

She kept a pencil in her pocket after that and read every article backward, sentence by sentence, once more. The Tuesday meeting was full. Many students arrived with garden tools and smiles.""",
        "the school office",
        "Jade",
        "Jade's article listed the wrong day for the garden club, and copies were about to be made.",
        [
            "She told Mr. Patel before he started the copier.",
            "They changed Thursday to Tuesday in the file.",
            "Jade checked a test page before the full stack was printed.",
        ],
        "The paper had the right day, and Jade made a habit of reading each article once more.",
    ),
    story(
        "A Ramp for the Cart",
        """The garden gate had a step that was only as high as a brick, but it stopped the supply cart. Wheels bumped, jars rattled, and water sloshed onto Priya's shoes. Carrying everything by hand took three trips.

Priya asked the garden lead, Ms. Brooks, if they could build a ramp. They measured the step and found a spare board in the shed. It was long enough to slope gently, not steeply. Priya sanded the rough edge while Ms. Brooks braced the board so it would not slide.

They tested the cart with one empty tub first. It rolled up without a jolt. Then they tried the full water jug. Priya kept one hand on the rail and one on the cart.

The next work day, the whole club used the ramp. The step was still there for people who wanted it. The cart finally had a way in. Priya left the board by the gate for the next work day.""",
        "the garden gate",
        "Priya",
        "A small step blocked the supply cart.",
        [
            "Priya asked Ms. Brooks about a ramp.",
            "They measured the step and sanded a spare board.",
            "They tested an empty tub, then the full water jug.",
        ],
        "The cart rolled up the ramp, and the club used it on the next work day.",
    ),
    story(
        "The Damp Lid",
        """The class time capsule would not latch. The wooden lid had swollen after a night in a damp closet, and the metal clasp missed its loop by a finger's width. Inside were letters the students wanted opened in ten years.

Owen suggested forcing it. Mr. Ellis said force would crack the wood. Instead they set the box, lid open, in the sunny hallway and aimed a fan across it. Every hour someone checked that the papers stayed inside and dry.

By the end of the day the lid sat flat. The clasp clicked. Owen still worried about another wet night, so he wrapped a piece of twine around the box as a backup and tucked the knot underneath.

They stored the capsule on a high shelf in the dry office. The letters could wait. The box could finally close. Owen wrote the shelf number on a class note so no one would move it.""",
        "the school hallway",
        "Owen",
        "The damp time-capsule lid had swollen and would not latch.",
        [
            "Mr. Ellis stopped Owen from forcing the lid.",
            "They dried the open box in the sunny hall with a fan.",
            "The clasp clicked, and Owen added twine as a backup.",
        ],
        "The capsule closed and was stored on a dry office shelf.",
    ),
    story(
        "Field Day Under the Awning",
        """Thunder rolled just as the relay teams lined up. The sky that had been pale all morning turned the color of a bruise. Ms. Alvarez blew a whistle and pointed to the wide awning beside the gym.

Students groaned about the canceled races. Then Ms. Alvarez said they were not canceled, only moved. She marked a shorter track with cones under the awning, away from the metal poles. The relay would be two legs instead of four, so nobody would crowd the dry strip.

Jonah's team complained, then practiced the handoff twice in the small space. When they ran, the baton did not drop. They did not win, but they finished. Rain tapped the awning like drums.

Jonah was soaked only at the edges of his sleeves. Field day had shrunk, but it had not disappeared. Jonah still talked about the handoff on the ride home. He was proud of it.""",
        "the field beside the gym",
        "Jonah",
        "A thunderstorm stopped the relay before it started.",
        [
            "Ms. Alvarez moved everyone under the awning.",
            "She marked a shorter track away from the metal poles.",
            "Jonah's team practiced the handoff in the small space.",
        ],
        "The team finished the shorter relay without dropping the baton.",
    ),
    story(
        "The Wallet on the Bench",
        """A brown wallet sat on the park bench where Elena had tied her shoe. She looked around the playground, but the family who had been there was gone. The wallet was fat with cards, and leaving it felt wrong.

Elena carried it to the rec center desk instead of digging through it on the sidewalk. The worker, Mr. Shah, opened it with her watching. A student ID from the middle school showed a name: Luis Ortega. The office phone list had his house.

Luis and his dad arrived before Elena finished her water bottle. Luis checked the cards and let out a long breath. Nothing was missing. His dad thanked Elena and Mr. Shah for not leaving the wallet on the bench.

Elena walked home lighter. She had not saved a fortune. She had kept a stranger's afternoon from getting worse. Mr. Shah said the desk was always the right place for a found wallet.""",
        "the park",
        "Elena",
        "Elena found a wallet and the owner was gone.",
        [
            "She took it to the rec center instead of searching it on the sidewalk.",
            "Mr. Shah found a student ID for Luis Ortega.",
            "They called his house.",
        ],
        "Luis and his dad picked up the wallet, and nothing was missing.",
    ),
    story(
        "The Wilting Lettuce",
        """The lettuce bed looked tired. Outer leaves drooped even though the morning had been cool. Andre knelt and pushed a finger into the soil. It was dry a knuckle down. The sprinkler had been aimed at the path, not the bed, for three days.

Andre told the garden club at lunch. They did not flood the plants all at once. He showed them how to water at the roots, slowly, until the soil held together without turning to mud. Then they moved the sprinkler and set a can on the path as a marker.

The next afternoon the leaves had lifted. Andre wrote a watering map: lettuce on odd days, tomatoes on even days, and a check of where the sprinkler actually pointed.

A map was a small thing. It kept the next dry week from sneaking up on the bed. Andre posted the map where the whole club could read it.""",
        "the school garden",
        "Andre",
        "The lettuce wilted because the sprinkler missed the bed.",
        [
            "Andre felt dry soil and saw that the sprinkler hit the path.",
            "The club watered slowly at the roots.",
            "They moved the sprinkler and marked the path with a can.",
        ],
        "The leaves lifted, and Andre wrote a watering map.",
    ),
    story(
        "The Morning Announcement",
        """The morning announcements were usually quick, but today the script was Camila's. She had written three sentences about the book drive. Standing by the office microphone, she felt her mouth go dry. The first practice, alone in the hall, had come out in a rush.

Mr. Patel let her try twice more before the bell. The second time she still stumbled on "donations." The third time she paused after each sentence, the way he showed her, and the word came out whole. He nodded and set the speaker on.

Camila heard her own voice in the hall. It was smaller than she expected and clearer than she feared. When she sat down in class, two students asked where to bring books.

She taped the script into her notebook with the pauses marked. The next announcement would still make her nervous. She would not meet it for the first time at the microphone.""",
        "the school office",
        "Camila",
        "Camila froze up when she practiced the morning announcement.",
        [
            "Her first practice came out in a rush.",
            "She stumbled on the word donations the second time.",
            "The third time she paused after each sentence and the word came out whole.",
        ],
        "She gave the announcement, students asked about the book drive, and she saved the marked script.",
    ),
]


SPECS = [
    {
        "folder": "grade-1",
        "label": "Grade 1",
        "key_title": "Grade 1 Decodable Passages",
        "student_name": "decodable-passages.pdf",
        "key_name": "decodable-passages-answer-key.pdf",
        "font_size": 16,
        "min_words": 60,
        "max_words": 90,
        "decodable": True,
        "passages": GRADE_1,
    },
    {
        "folder": "grade-2",
        "label": "Grade 2",
        "key_title": "Grade 2 Passages",
        "student_name": "passages.pdf",
        "key_name": "passages-answer-key.pdf",
        "font_size": 14,
        "min_words": 100,
        "max_words": 140,
        "decodable": False,
        "passages": GRADE_2,
    },
    {
        "folder": "grade-3",
        "label": "Grade 3",
        "key_title": "Grade 3 Instructional Passages",
        "student_name": "instructional-passages.pdf",
        "key_name": "instructional-passages-answer-key.pdf",
        "font_size": 12,
        "min_words": 150,
        "max_words": 190,
        "decodable": False,
        "passages": GRADE_3,
    },
]


def main():
    errors = []
    for spec in SPECS:
        errors.extend(validate(spec))
    if errors:
        raise SystemExit("\n".join(errors))
    for spec in SPECS:
        passages = spec["passages"]
        boxes = layout_for(spec, passages)
        folder = OUT_ROOT / spec["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        student_path = folder / spec["student_name"]
        key_path = folder / spec["key_name"]
        write_student_packet(student_path, spec, passages, boxes)
        key_pages = write_answer_key(key_path, spec, passages)
        print(f"Wrote {student_path} ({len(passages)} pages)")
        print(f"Wrote {key_path} ({key_pages} pages)")


if __name__ == "__main__":
    main()
