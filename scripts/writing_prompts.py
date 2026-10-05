#!/usr/bin/env python3
"""Build story-starter writing worksheets for seasonal themes.

Each page opens with a short story beginning and a matching image.
The rest of the page is lined writing space for the student to continue.
"""

import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "writing" / "prompts"
IMAGE_DIR = OUT_DIR / "images"

PAGE_W, PAGE_H = letter
LEFT = 48
RIGHT = 48
TOP = 42
BOTTOM = 40
TITLE_SIZE = 16
BODY_SIZE = 14
BODY_LEADING = 20
LINE_GAP = 32
PROMPT_COUNT = 5

PACKETS = {
    "fall": {
        "pdf_name": "fall-story-starters.pdf",
        "pdf_title": "Fall Story Starters",
        "prompts": [
            {
                "title": "The Perfect Pumpkin",
                "image": "fall-pumpkin-patch.jpg",
                "starter": (
                    "Maya walked between the rows of pumpkins. The air smelled "
                    "like dry leaves and warm dirt. Most of the pumpkins were "
                    "round and orange, but one little pumpkin near the fence "
                    "was different. It had a tiny green leaf still growing "
                    "from its stem, and when Maya touched it, the leaf "
                    "twitched. Maya leaned closer and whispered, \"Are you "
                    "trying to tell me something?\""
                ),
            },
            {
                "title": "The Leaf Pile Secret",
                "image": "fall-leaf-pile.jpg",
                "starter": (
                    "Jordan ran across the yard and jumped into the biggest "
                    "pile of leaves on the block. Red, gold, and brown leaves "
                    "flew up around him. Then he heard a soft rustle under "
                    "the pile that did not sound like leaves. Something small "
                    "scooted past his shoe. Jordan froze, held his breath, "
                    "and peeked into the leaves."
                ),
            },
            {
                "title": "The Highest Apple",
                "image": "fall-apple-orchard.jpg",
                "starter": (
                    "Sam stood under the tallest apple tree in the orchard. "
                    "A shiny red apple hung just out of reach, glowing in "
                    "the morning sun. When Sam finally stretched high enough "
                    "to touch it, the apple felt warm, not cool like the "
                    "others. A soft humming sound came from inside. Sam "
                    "looked around. No one else was nearby."
                ),
            },
            {
                "title": "The Friendly Scarecrow",
                "image": "fall-scarecrow.jpg",
                "starter": (
                    "At the edge of the cornfield stood a scarecrow in a "
                    "plaid shirt and a floppy straw hat. The wind moved "
                    "through the corn, but the scarecrow's head turned a "
                    "little farther than the wind could push it. One button "
                    "eye seemed to wink. \"You look like you need help,\" "
                    "the scarecrow said in a dry, friendly voice. \"I have "
                    "been waiting for someone brave.\""
                ),
            },
            {
                "title": "Follow That Squirrel",
                "image": "fall-squirrel-forest.jpg",
                "starter": (
                    "A gray squirrel sat on the path with an acorn in its "
                    "paws. When it saw a visitor coming, it flicked its tail "
                    "and darted into the woods. Every few steps it stopped "
                    "and looked back, as if it wanted to be followed. The "
                    "path wound between trees with red and gold leaves. "
                    "Somewhere ahead, the squirrel chattered again, louder "
                    "this time."
                ),
            },
        ],
    },
    "thanksgiving": {
        "pdf_name": "thanksgiving-story-starters.pdf",
        "pdf_title": "Thanksgiving Story Starters",
        "prompts": [
            {
                "title": "Kitchen Helpers",
                "image": "thanksgiving-kitchen.jpg",
                "starter": (
                    "The kitchen smelled like turkey, warm bread, and pumpkin "
                    "pie. Avery stood on a stool and stirred the mashed "
                    "potatoes while Grandpa checked the oven. Suddenly the "
                    "lights blinked, then went out. The room was quiet for "
                    "one second. Then Avery heard a soft knock coming from "
                    "inside the pantry."
                ),
            },
            {
                "title": "The Waiting Table",
                "image": "thanksgiving-table.jpg",
                "starter": (
                    "The long table was set with shiny plates, orange "
                    "napkins, and a cornucopia full of squash and apples. "
                    "Every chair was ready except one. A small envelope sat "
                    "on that empty plate. On the front, in careful letters, "
                    "it said, \"Open before dinner.\" No one knew who had "
                    "left it there."
                ),
            },
            {
                "title": "The Backyard Turkey",
                "image": "thanksgiving-turkey.jpg",
                "starter": (
                    "Casey looked out the back door and froze. A big turkey "
                    "was standing in the yard among the fallen leaves. It "
                    "tilted its head, as if it were listening. Then it "
                    "walked right up to the porch steps and dropped a shiny "
                    "acorn by Casey's shoe. The turkey waited, blinking "
                    "slowly, like it had something important to say."
                ),
            },
            {
                "title": "The Gratitude Card",
                "image": "thanksgiving-gratitude.jpg",
                "starter": (
                    "Riley had made a thank-you card with stickers, glitter, "
                    "and one careful sentence inside. Family members were "
                    "coming up the porch with covered dishes for dinner. "
                    "Riley planned to give the card to Grandma. But when "
                    "Riley opened it one more time to check the words, the "
                    "sentence had changed all by itself."
                ),
            },
            {
                "title": "Parade Day Surprise",
                "image": "thanksgiving-parade.jpg",
                "starter": (
                    "The Thanksgiving parade filled Main Street with music, "
                    "flags, and giant balloons. Morgan waved from the "
                    "sidewalk as a harvest float rolled by. On the float "
                    "stood a person in a corn costume, holding a small "
                    "wooden box. The person looked straight at Morgan and "
                    "tossed the box gently into Morgan's hands."
                ),
            },
        ],
    },
    "winter": {
        "pdf_name": "winter-story-starters.pdf",
        "pdf_title": "Winter Story Starters",
        "prompts": [
            {
                "title": "The First Snowflake",
                "image": "winter-first-snow.jpg",
                "starter": (
                    "The sky turned soft and gray, and the first snowflake "
                    "of the year landed on Jamie's mitten. It did not melt. "
                    "It glowed with a tiny blue light, then another flake "
                    "landed beside it. Soon Jamie's mitten held a little "
                    "path of glowing snowflakes, pointing toward the end "
                    "of the street."
                ),
            },
            {
                "title": "The Snowman Who Blinked",
                "image": "winter-snowman.jpg",
                "starter": (
                    "Taylor and Drew rolled the last snowball into place and "
                    "stepped back to look at their snowman. Scarf, hat, "
                    "carrot nose, and two dark eyes. Perfect. Then one of "
                    "the eyes blinked. The snowman leaned forward a little "
                    "and whispered, \"Thank you for building me. I need a "
                    "favor before the sun goes down.\""
                ),
            },
            {
                "title": "Across the Frozen Pond",
                "image": "winter-ice-skating.jpg",
                "starter": (
                    "The pond was smooth and clear, like a giant window over "
                    "the water. Skye glided across the ice, scarf flying "
                    "behind. Near the middle of the pond, Skye saw something "
                    "under the ice: a small silver key lying on the dark "
                    "water below. As Skye circled closer, the key slowly "
                    "began to rise toward the surface."
                ),
            },
            {
                "title": "Cocoa by the Window",
                "image": "winter-cabin-cocoa.jpg",
                "starter": (
                    "Snow covered the cabin roof and the pine trees outside. "
                    "Inside, a mug of hot cocoa sat by the window, still "
                    "steaming. Cameron picked it up and noticed a tiny "
                    "folded note stuck to the bottom of the mug. The note "
                    "said, \"Follow the fox tracks after the last marshmallow "
                    "melts.\" Outside, fresh tracks led into the trees."
                ),
            },
            {
                "title": "The Flying Sled",
                "image": "winter-sledding.jpg",
                "starter": (
                    "Alex climbed onto the wooden sled at the top of the "
                    "hill. One push, and the sled raced down through the "
                    "powder. Halfway down, the sled left the ground. It "
                    "did not bump. It floated. The pine trees slid past "
                    "below, and Alex realized the sled was not coming "
                    "down at all."
                ),
            },
        ],
    },
}


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


def draw_header(c):
    y = PAGE_H - TOP
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", TITLE_SIZE)
    c.drawString(LEFT, y, "Continue the Story")

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
    return y - 16


def draw_prompt_top(c, prompt, content_top):
    content_width = PAGE_W - LEFT - RIGHT
    image_width = 200
    image_height = 150
    gap = 16
    beside_width = content_width - image_width - gap

    y = content_top
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", BODY_SIZE + 1)
    c.drawString(LEFT, y, prompt["title"])
    y -= 10

    image_path = IMAGE_DIR / prompt["image"]
    if not image_path.exists():
        raise FileNotFoundError(f"Missing image: {image_path}")

    image_top = y
    image_bottom = image_top - image_height
    c.drawImage(
        ImageReader(str(image_path)),
        LEFT,
        image_bottom,
        width=image_width,
        height=image_height,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(0.8)
    c.rect(LEFT, image_bottom, image_width, image_height, stroke=1, fill=0)

    # Text starts beside the image, then continues full-width underneath.
    words = prompt["starter"].split()
    beside_lines = []
    current = ""
    remaining = list(words)
    max_beside_lines = max(1, int((image_height - 4) / BODY_LEADING))
    while remaining and len(beside_lines) < max_beside_lines:
        word = remaining[0]
        trial = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(trial, "Helvetica", BODY_SIZE) <= beside_width:
            current = trial
            remaining.pop(0)
        else:
            if current:
                beside_lines.append(current)
                current = ""
            else:
                beside_lines.append(word)
                remaining.pop(0)
    if current:
        if len(beside_lines) < max_beside_lines:
            beside_lines.append(current)
        else:
            remaining = current.split() + remaining

    text_x = LEFT + image_width + gap
    text_y = image_top - BODY_SIZE
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", BODY_SIZE)
    for line in beside_lines:
        c.drawString(text_x, text_y, line)
        text_y -= BODY_LEADING

    below_top = min(text_y, image_bottom - 8)
    if remaining:
        below_text = " ".join(remaining)
        below_lines = wrap_text(below_text, "Helvetica", BODY_SIZE, content_width)
        text_y = below_top - BODY_SIZE
        for line in below_lines:
            c.drawString(LEFT, text_y, line)
            text_y -= BODY_LEADING
        return text_y - 10

    return min(text_y, image_bottom) - 14


def draw_writing_lines(c, lines_top):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Oblique", BODY_SIZE)
    c.drawString(LEFT, lines_top, "Now finish the story.")

    y = lines_top - 28
    c.setStrokeColorRGB(0.35, 0.35, 0.35)
    c.setLineWidth(0.8)
    while y >= BOTTOM + 18:
        c.line(LEFT, y, PAGE_W - RIGHT, y)
        y -= LINE_GAP


def draw_page_number(c, page, total):
    label = f"Page {page} of {total}"
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", BODY_SIZE)
    c.drawCentredString(PAGE_W / 2, 24, label)


def write_student_packet(path, pdf_title, prompts):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle(pdf_title)

    for index, prompt in enumerate(prompts):
        if index:
            c.showPage()
        content_top = draw_header(c)
        lines_top = draw_prompt_top(c, prompt, content_top)
        draw_writing_lines(c, lines_top)
        draw_page_number(c, index + 1, len(prompts))

    c.save()


def build_packet(theme):
    if theme not in PACKETS:
        known = ", ".join(sorted(PACKETS))
        raise RuntimeError(f"Unknown theme {theme!r}. Choose from: {known}")

    packet = PACKETS[theme]
    prompts = packet["prompts"]
    if len(prompts) != PROMPT_COUNT:
        raise RuntimeError(
            f"Expected {PROMPT_COUNT} prompts for {theme}, got {len(prompts)}"
        )
    for prompt in prompts:
        image_path = IMAGE_DIR / prompt["image"]
        if not image_path.exists():
            raise FileNotFoundError(f"Missing image: {image_path}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / packet["pdf_name"]
    write_student_packet(path, packet["pdf_title"], prompts)
    print(f"Wrote {path} ({len(prompts)} pages)")
    return path


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    themes = args or sorted(PACKETS)
    for theme in themes:
        build_packet(theme)


if __name__ == "__main__":
    main()
