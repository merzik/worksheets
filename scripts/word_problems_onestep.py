#!/usr/bin/env python3
"""Build single-step 3-digit addition and subtraction word-problem PDFs.

Writes a 20-page student packet (5 problems per page) and a separate
answer key into math/word-problems/. Stories are one operation only.
"""

import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "math" / "word-problems"
STUDENT_PDF = OUT_DIR / "addition-subtraction-3-digit.pdf"
ANSWER_KEY_PDF = OUT_DIR / "addition-subtraction-3-digit-answer-key.pdf"

PAGE_W, PAGE_H = letter
LEFT = 48
RIGHT = 48
STORY_SIZE = 14
STORY_LEADING = 18
PROBLEMS_PER_PAGE = 5
STUDENT_PAGES = 20

# Each item is one single-step story. {a} and {b} are the only numbers.
RAW_PROBLEMS = [
    {
        "a": 248,
        "op": "+",
        "b": 136,
        "unit": "crayons",
        "template": (
            "Maya has {a} crayons. She buys {b} more. How many crayons "
            "does Maya have now?"
        ),
    },
    {
        "a": 415,
        "op": "-",
        "b": 128,
        "unit": "books",
        "template": (
            "A shelf has {a} books. Students check out {b} books. How many "
            "books are on the shelf now?"
        ),
    },
    {
        "a": 186,
        "op": "+",
        "b": 297,
        "unit": "sandwiches",
        "template": (
            "The cafeteria made {a} cheese sandwiches and {b} turkey sandwiches. "
            "How many sandwiches did they make in all?"
        ),
    },
    {
        "a": 530,
        "op": "-",
        "b": 145,
        "unit": "points",
        "template": (
            "Jordan had {a} points. He used {b} points on a prize. How many "
            "points does Jordan have left?"
        ),
    },
    {
        "a": 162,
        "op": "+",
        "b": 385,
        "unit": "fish",
        "template": (
            "The pet store has {a} fish. A delivery brings {b} more fish. "
            "How many fish are there now?"
        ),
    },
    {
        "a": 456,
        "op": "-",
        "b": 219,
        "unit": "cans",
        "template": (
            "A class collected {a} cans. They gave {b} cans to a food bank. "
            "How many cans do they still have?"
        ),
    },
    {
        "a": 640,
        "op": "-",
        "b": 275,
        "unit": "bottles",
        "template": (
            "Field day started with {a} bottles of water. Students drank {b} "
            "bottles. How many bottles are left?"
        ),
    },
    {
        "a": 134,
        "op": "+",
        "b": 287,
        "unit": "balls",
        "template": (
            "The gym has {a} red balls and {b} blue balls. How many balls "
            "are there in all?"
        ),
    },
    {
        "a": 810,
        "op": "-",
        "b": 265,
        "unit": "apples",
        "template": (
            "A store had {a} apples. It sold {b} apples in the morning. "
            "How many apples are left?"
        ),
    },
    {
        "a": 195,
        "op": "+",
        "b": 328,
        "unit": "stickers",
        "template": (
            "Lena has {a} stickers. Her brother gives her {b} stickers. How many "
            "stickers does Lena have now?"
        ),
    },
    {
        "a": 450,
        "op": "-",
        "b": 185,
        "unit": "dollars",
        "template": (
            "Noah saved {a} dollars. He spent {b} dollars on a bike. How much "
            "money does Noah have left?"
        ),
    },
    {
        "a": 308,
        "op": "+",
        "b": 246,
        "unit": "carrots",
        "template": (
            "A farmer picked {a} carrots on Monday and {b} carrots on Tuesday. "
            "How many carrots did he pick in all?"
        ),
    },
    {
        "a": 500,
        "op": "-",
        "b": 186,
        "unit": "seats",
        "template": (
            "There are {a} seats in the auditorium. Then {b} students sit down. "
            "How many seats are empty?"
        ),
    },
    {
        "a": 173,
        "op": "+",
        "b": 250,
        "unit": "marbles",
        "template": (
            "Priya had {a} marbles. She won {b} marbles in a game. How many "
            "marbles does Priya have now?"
        ),
    },
    {
        "a": 367,
        "op": "-",
        "b": 198,
        "unit": "sheets",
        "template": (
            "The art room has {a} sheets of paper. Students use {b} sheets. "
            "How many sheets are left?"
        ),
    },
    {
        "a": 142,
        "op": "+",
        "b": 388,
        "unit": "cookies",
        "template": (
            "The bake sale had {a} chocolate cookies and {b} sugar cookies. "
            "How many cookies were there in all?"
        ),
    },
    {
        "a": 360,
        "op": "-",
        "b": 195,
        "unit": "lunches",
        "template": (
            "The bus had {a} lunches. Students ate {b} lunches at the park. "
            "How many lunches are left?"
        ),
    },
    {
        "a": 720,
        "op": "-",
        "b": 310,
        "unit": "cards",
        "template": (
            "Diego had {a} baseball cards. He gave {b} cards to his cousin. "
            "How many cards does Diego have left?"
        ),
    },
    {
        "a": 184,
        "op": "+",
        "b": 296,
        "unit": "flowers",
        "template": (
            "The garden club planted {a} flowers on Friday and {b} flowers on "
            "Saturday. How many flowers did they plant in all?"
        ),
    },
    {
        "a": 590,
        "op": "-",
        "b": 234,
        "unit": "puzzles",
        "template": (
            "A toy store had {a} puzzles. It sold {b} puzzles on Saturday. "
            "How many puzzles does the store have left?"
        ),
    },
    {
        "a": 215,
        "op": "+",
        "b": 164,
        "unit": "pencils",
        "template": (
            "Ms. Alvarez had {a} pencils. She bought {b} more pencils. How many "
            "pencils does she have now?"
        ),
    },
    {
        "a": 480,
        "op": "-",
        "b": 196,
        "unit": "juice boxes",
        "template": (
            "The snack cart had {a} juice boxes. Students bought {b} juice boxes. "
            "How many juice boxes are left?"
        ),
    },
    {
        "a": 126,
        "op": "+",
        "b": 403,
        "unit": "books",
        "template": (
            "Room 12 read {a} books in September and {b} books in October. "
            "How many books did they read in all?"
        ),
    },
    {
        "a": 750,
        "op": "-",
        "b": 280,
        "unit": "ears of corn",
        "template": (
            "A farm stand had {a} ears of corn. It sold {b} ears in the morning. "
            "How many ears of corn are left?"
        ),
    },
    {
        "a": 188,
        "op": "+",
        "b": 247,
        "unit": "rocks",
        "template": (
            "Kai collected {a} rocks. He found {b} more rocks at the creek. "
            "How many rocks does Kai have now?"
        ),
    },
    {
        "a": 254,
        "op": "+",
        "b": 179,
        "unit": "folders",
        "template": (
            "The choir has {a} red folders and {b} blue folders. How many "
            "folders does the choir have in all?"
        ),
    },
    {
        "a": 625,
        "op": "-",
        "b": 240,
        "unit": "cars",
        "template": (
            "A parking lot has {a} cars in the morning. Then {b} cars leave. "
            "How many cars are in the lot now?"
        ),
    },
    {
        "a": 340,
        "op": "-",
        "b": 127,
        "unit": "bandages",
        "template": (
            "The nurse had {a} bandages. She used {b} bandages on Monday. "
            "How many bandages are left?"
        ),
    },
    {
        "a": 173,
        "op": "+",
        "b": 286,
        "unit": "cans of soup",
        "template": (
            "Students brought {a} cans of soup and {b} more cans of soup. "
            "How many cans of soup did they bring in all?"
        ),
    },
    {
        "a": 900,
        "op": "-",
        "b": 375,
        "unit": "beads",
        "template": (
            "Elena had {a} beads. She used {b} beads for a necklace. How many "
            "beads does Elena have left?"
        ),
    },
    {
        "a": 212,
        "op": "+",
        "b": 168,
        "unit": "posters",
        "template": (
            "The book fair sold {a} posters and {b} more posters. How many "
            "posters did the book fair sell?"
        ),
    },
    {
        "a": 470,
        "op": "-",
        "b": 195,
        "unit": "visitors",
        "template": (
            "A zoo had {a} visitors in the morning. Then {b} visitors left at "
            "lunch. How many visitors are at the zoo now?"
        ),
    },
    {
        "a": 156,
        "op": "+",
        "b": 289,
        "unit": "papers",
        "template": (
            "Mr. Chen has {a} math papers and {b} reading papers. How many "
            "papers is that in all?"
        ),
    },
    {
        "a": 800,
        "op": "-",
        "b": 245,
        "unit": "gallons",
        "template": (
            "A tank holds {a} gallons of water. Workers drain {b} gallons. "
            "How many gallons are left in the tank?"
        ),
    },
    {
        "a": 164,
        "op": "+",
        "b": 319,
        "unit": "stickers",
        "template": (
            "Sofia has {a} animal stickers and {b} sports stickers. How many "
            "stickers does Sofia have in all?"
        ),
    },
    {
        "a": 555,
        "op": "-",
        "b": 230,
        "unit": "apples",
        "template": (
            "The lunchroom had {a} apples. Students ate {b} apples. How many "
            "apples are left?"
        ),
    },
    {
        "a": 128,
        "op": "+",
        "b": 276,
        "unit": "miles",
        "template": (
            "A scout troop hiked {a} miles in May and {b} miles in June. "
            "How many miles did they hike in all?"
        ),
    },
    {
        "a": 670,
        "op": "-",
        "b": 285,
        "unit": "erasers",
        "template": (
            "The school store had {a} erasers. It sold {b} erasers this week. "
            "How many erasers are left?"
        ),
    },
    {
        "a": 192,
        "op": "+",
        "b": 135,
        "unit": "block towers",
        "template": (
            "Jamal built {a} block towers. He built {b} more towers after school. "
            "How many towers did Jamal build in all?"
        ),
    },
    {
        "a": 301,
        "op": "+",
        "b": 244,
        "unit": "pieces of art",
        "template": (
            "The art show has {a} drawings and {b} paintings. How many pieces "
            "of art is that in all?"
        ),
    },
    {
        "a": 430,
        "op": "-",
        "b": 175,
        "unit": "passengers",
        "template": (
            "A train had {a} passengers. Then {b} passengers got off. How many "
            "passengers are on the train now?"
        ),
    },
    {
        "a": 260,
        "op": "-",
        "b": 184,
        "unit": "jump ropes",
        "template": (
            "The gym teacher had {a} jump ropes. Students took {b} jump ropes "
            "outside. How many jump ropes are left in the gym?"
        ),
    },
    {
        "a": 157,
        "op": "+",
        "b": 268,
        "unit": "berries",
        "template": (
            "Nina picked {a} strawberries and {b} blueberries. How many berries "
            "did Nina pick in all?"
        ),
    },
    {
        "a": 315,
        "op": "-",
        "b": 120,
        "unit": "chairs",
        "template": (
            "A classroom had {a} chairs. Workers moved {b} chairs to the cafeteria. "
            "How many chairs are in the classroom now?"
        ),
    },
    {
        "a": 188,
        "op": "+",
        "b": 307,
        "unit": "bottles",
        "template": (
            "The recycling club gathered {a} plastic bottles and {b} glass bottles. "
            "How many bottles did they gather in all?"
        ),
    },
    {
        "a": 640,
        "op": "-",
        "b": 255,
        "unit": "tickets",
        "template": (
            "Owen had {a} tickets. He used {b} tickets for rides. How many "
            "tickets does Owen have left?"
        ),
    },
    {
        "a": 209,
        "op": "+",
        "b": 186,
        "unit": "muffins",
        "template": (
            "A bakery made {a} muffins in the morning and {b} muffins in the "
            "afternoon. How many muffins did the bakery make?"
        ),
    },
    {
        "a": 512,
        "op": "-",
        "b": 190,
        "unit": "ducks",
        "template": (
            "The pond had {a} ducks. Then {b} ducks flew away. How many ducks "
            "are at the pond now?"
        ),
    },
    {
        "a": 143,
        "op": "+",
        "b": 298,
        "unit": "paper cranes",
        "template": (
            "Students made {a} paper cranes on Monday and {b} paper cranes on "
            "Tuesday. How many paper cranes did they make in all?"
        ),
    },
    {
        "a": 980,
        "op": "-",
        "b": 420,
        "unit": "boxes",
        "template": (
            "A warehouse had {a} boxes. Trucks took {b} boxes in the morning. "
            "How many boxes are left?"
        ),
    },
    {
        "a": 267,
        "op": "+",
        "b": 148,
        "unit": "markers",
        "template": (
            "The art cart has {a} markers. The teacher adds {b} more markers. "
            "How many markers are on the cart now?"
        ),
    },
    {
        "a": 735,
        "op": "-",
        "b": 268,
        "unit": "leaves",
        "template": (
            "Students collected {a} leaves. They used {b} leaves for a project. "
            "How many leaves are left?"
        ),
    },
    {
        "a": 119,
        "op": "+",
        "b": 354,
        "unit": "stamps",
        "template": (
            "Ava has {a} stamps. She buys {b} more stamps. How many stamps "
            "does Ava have now?"
        ),
    },
    {
        "a": 604,
        "op": "-",
        "b": 317,
        "unit": "shells",
        "template": (
            "Theo found {a} shells at the beach. He gave {b} shells to his sister. "
            "How many shells does Theo have left?"
        ),
    },
    {
        "a": 225,
        "op": "+",
        "b": 178,
        "unit": "buttons",
        "template": (
            "The craft box has {a} red buttons and {b} blue buttons. How many "
            "buttons are in the craft box?"
        ),
    },
    {
        "a": 891,
        "op": "-",
        "b": 456,
        "unit": "nails",
        "template": (
            "A builder had {a} nails. He used {b} nails on a fence. How many "
            "nails are left?"
        ),
    },
    {
        "a": 306,
        "op": "+",
        "b": 219,
        "unit": "seeds",
        "template": (
            "A class planted {a} sunflower seeds and {b} pumpkin seeds. How many "
            "seeds did they plant in all?"
        ),
    },
    {
        "a": 548,
        "op": "-",
        "b": 163,
        "unit": "toy cars",
        "template": (
            "The playroom had {a} toy cars. Children took {b} toy cars home. "
            "How many toy cars are left?"
        ),
    },
    {
        "a": 174,
        "op": "+",
        "b": 325,
        "unit": "postcards",
        "template": (
            "Mia wrote {a} postcards. Then she wrote {b} more postcards. How many "
            "postcards did Mia write in all?"
        ),
    },
    {
        "a": 762,
        "op": "-",
        "b": 409,
        "unit": "bricks",
        "template": (
            "Workers stacked {a} bricks. They used {b} bricks for a wall. How many "
            "bricks are left?"
        ),
    },
    {
        "a": 231,
        "op": "+",
        "b": 267,
        "unit": "balloons",
        "template": (
            "The party store had {a} red balloons and {b} yellow balloons. How many "
            "balloons is that in all?"
        ),
    },
    {
        "a": 685,
        "op": "-",
        "b": 294,
        "unit": "paper plates",
        "template": (
            "The kitchen had {a} paper plates. The cafeteria used {b} paper plates. "
            "How many paper plates are left?"
        ),
    },
    {
        "a": 108,
        "op": "+",
        "b": 392,
        "unit": "magnets",
        "template": (
            "Sam has {a} magnets. He finds {b} more magnets in a drawer. How many "
            "magnets does Sam have now?"
        ),
    },
    {
        "a": 917,
        "op": "-",
        "b": 538,
        "unit": "coins",
        "template": (
            "A jar held {a} coins. Someone took {b} coins out. How many coins "
            "are left in the jar?"
        ),
    },
    {
        "a": 246,
        "op": "+",
        "b": 153,
        "unit": "rulers",
        "template": (
            "The supply closet has {a} rulers. A new box adds {b} rulers. How many "
            "rulers are in the closet now?"
        ),
    },
    {
        "a": 573,
        "op": "-",
        "b": 286,
        "unit": "pairs of socks",
        "template": (
            "A clothing store had {a} pairs of socks. It sold {b} pairs. How many "
            "pairs of socks are left?"
        ),
    },
    {
        "a": 139,
        "op": "+",
        "b": 461,
        "unit": "pinecones",
        "template": (
            "Kids gathered {a} pinecones on Monday and {b} pinecones on Tuesday. "
            "How many pinecones did they gather in all?"
        ),
    },
    {
        "a": 824,
        "op": "-",
        "b": 357,
        "unit": "napkins",
        "template": (
            "The cafeteria had {a} napkins. Workers used {b} napkins at lunch. "
            "How many napkins are left?"
        ),
    },
    {
        "a": 205,
        "op": "+",
        "b": 194,
        "unit": "hats",
        "template": (
            "A winter drive collected {a} hats and {b} more hats. How many hats "
            "were collected in all?"
        ),
    },
    {
        "a": 658,
        "op": "-",
        "b": 271,
        "unit": "spoons",
        "template": (
            "The kitchen had {a} spoons. Helpers set out {b} spoons for dinner. "
            "How many spoons are left in the drawer?"
        ),
    },
    {
        "a": 312,
        "op": "+",
        "b": 287,
        "unit": "acorns",
        "template": (
            "Squirrels gathered {a} acorns and then gathered {b} more. How many "
            "acorns did they gather in all?"
        ),
    },
    {
        "a": 941,
        "op": "-",
        "b": 486,
        "unit": "paper clips",
        "template": (
            "The office had {a} paper clips. Staff used {b} paper clips. How many "
            "paper clips are left?"
        ),
    },
    {
        "a": 167,
        "op": "+",
        "b": 233,
        "unit": "key chains",
        "template": (
            "A craft fair sold {a} key chains in the morning and {b} key chains "
            "in the afternoon. How many key chains were sold?"
        ),
    },
    {
        "a": 706,
        "op": "-",
        "b": 319,
        "unit": "socks",
        "template": (
            "A store had {a} pairs of socks. It sold {b} pairs. How many pairs "
            "of socks are left?"
        ),
    },
    {
        "a": 284,
        "op": "+",
        "b": 156,
        "unit": "ribbons",
        "template": (
            "The craft room has {a} ribbons. Students bring {b} more ribbons. "
            "How many ribbons are there now?"
        ),
    },
    {
        "a": 539,
        "op": "-",
        "b": 162,
        "unit": "golf balls",
        "template": (
            "A coach had {a} golf balls. Players used {b} golf balls at practice. "
            "How many golf balls are left?"
        ),
    },
    {
        "a": 118,
        "op": "+",
        "b": 375,
        "unit": "buttons",
        "template": (
            "Lily sorted {a} buttons. Then she sorted {b} more buttons. How many "
            "buttons did Lily sort in all?"
        ),
    },
    {
        "a": 863,
        "op": "-",
        "b": 427,
        "unit": "straws",
        "template": (
            "The snack room had {a} straws. Students used {b} straws. How many "
            "straws are left?"
        ),
    },
    {
        "a": 249,
        "op": "+",
        "b": 301,
        "unit": "sentences",
        "template": (
            "A writing club wrote {a} sentences on Monday and {b} sentences on "
            "Tuesday. How many sentences did they write in all?"
        ),
    },
    {
        "a": 614,
        "op": "-",
        "b": 238,
        "unit": "stamps",
        "template": (
            "The mail room had {a} stamps. Workers used {b} stamps on letters. "
            "How many stamps are left?"
        ),
    },
    {
        "a": 175,
        "op": "+",
        "b": 426,
        "unit": "snap cubes",
        "template": (
            "A math tub has {a} snap cubes. The teacher adds {b} more snap cubes. "
            "How many snap cubes are in the tub now?"
        ),
    },
    {
        "a": 792,
        "op": "-",
        "b": 345,
        "unit": "postcards",
        "template": (
            "A gift shop had {a} postcards. It sold {b} postcards. How many "
            "postcards are left?"
        ),
    },
    {
        "a": 203,
        "op": "+",
        "b": 189,
        "unit": "baseballs",
        "template": (
            "The team has {a} baseballs. A new bag adds {b} baseballs. How many "
            "baseballs does the team have now?"
        ),
    },
    {
        "a": 457,
        "op": "-",
        "b": 208,
        "unit": "marbles",
        "template": (
            "A bag held {a} marbles. Kids took {b} marbles out to play. How many "
            "marbles are left in the bag?"
        ),
    },
    {
        "a": 326,
        "op": "+",
        "b": 274,
        "unit": "beads",
        "template": (
            "Students strung {a} beads in the morning and {b} beads in the "
            "afternoon. How many beads did they string in all?"
        ),
    },
    {
        "a": 881,
        "op": "-",
        "b": 493,
        "unit": "cups",
        "template": (
            "The cafeteria stacked {a} cups. Helpers set out {b} cups for lunch. "
            "How many cups are left in the stack?"
        ),
    },
    {
        "a": 152,
        "op": "+",
        "b": 348,
        "unit": "dice",
        "template": (
            "A game shelf has {a} dice. A new set adds {b} dice. How many dice "
            "are on the shelf now?"
        ),
    },
    {
        "a": 620,
        "op": "-",
        "b": 175,
        "unit": "stamps",
        "template": (
            "The stamp club had {a} stamps. Members traded {b} stamps. How many "
            "stamps does the club have left?"
        ),
    },
    {
        "a": 291,
        "op": "+",
        "b": 207,
        "unit": "bookmarks",
        "template": (
            "The library made {a} bookmarks and {b} more bookmarks. How many "
            "bookmarks did the library make?"
        ),
    },
    {
        "a": 954,
        "op": "-",
        "b": 568,
        "unit": "paper cups",
        "template": (
            "A picnic had {a} paper cups. Guests used {b} paper cups. How many "
            "paper cups are left?"
        ),
    },
    {
        "a": 134,
        "op": "+",
        "b": 265,
        "unit": "toy animals",
        "template": (
            "A shelf holds {a} toy animals. Children add {b} more toy animals. "
            "How many toy animals are on the shelf now?"
        ),
    },
    {
        "a": 713,
        "op": "-",
        "b": 286,
        "unit": "stickers",
        "template": (
            "Emma had {a} stickers. She used {b} stickers on a poster. How many "
            "stickers does Emma have left?"
        ),
    },
    {
        "a": 218,
        "op": "+",
        "b": 391,
        "unit": "rubber bands",
        "template": (
            "The science lab has {a} rubber bands. A new pack adds {b} rubber "
            "bands. How many rubber bands are there now?"
        ),
    },
    {
        "a": 846,
        "op": "-",
        "b": 379,
        "unit": "index cards",
        "template": (
            "A teacher had {a} index cards. Students used {b} index cards. How many "
            "index cards are left?"
        ),
    },
    {
        "a": 165,
        "op": "+",
        "b": 234,
        "unit": "paper boats",
        "template": (
            "Kids folded {a} paper boats. Then they folded {b} more paper boats. "
            "How many paper boats did they fold in all?"
        ),
    },
    {
        "a": 507,
        "op": "-",
        "b": 149,
        "unit": "push pins",
        "template": (
            "The office had {a} push pins. Staff used {b} push pins on a board. "
            "How many push pins are left?"
        ),
    },
    {
        "a": 273,
        "op": "+",
        "b": 316,
        "unit": "trading cards",
        "template": (
            "Ryan has {a} trading cards. He buys {b} more trading cards. How many "
            "trading cards does Ryan have now?"
        ),
    },
    {
        "a": 938,
        "op": "-",
        "b": 451,
        "unit": "paper clips",
        "template": (
            "A desk drawer held {a} paper clips. Someone used {b} paper clips. "
            "How many paper clips are left?"
        ),
    },
    {
        "a": 189,
        "op": "+",
        "b": 254,
        "unit": "foam shapes",
        "template": (
            "The art room has {a} foam shapes. A new bag adds {b} foam shapes. "
            "How many foam shapes are there now?"
        ),
    },
    {
        "a": 672,
        "op": "-",
        "b": 305,
        "unit": "tennis balls",
        "template": (
            "A coach had {a} tennis balls. Players used {b} tennis balls at practice. "
            "How many tennis balls are left?"
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
        a, b = raw["a"], raw["b"]
        op = raw["op"]
        for label, value in (("a", a), ("b", b)):
            if not isinstance(value, int) or not 0 <= value <= 999:
                raise ValueError(
                    f"Problem {index} {label}={value} is not a whole number up to 3 digits"
                )

        final = apply_op(a, op, b)
        if not 0 <= final <= 999:
            raise ValueError(f"Problem {index} answer={final} is outside 0 to 999")

        text = raw["template"].format(a=a, b=b)
        for value in (a, b):
            if not re.search(rf"\b{value}\b", text):
                raise ValueError(f"Problem {index} text is missing {value}")

        problems.append(
            {
                "text": text,
                "equation": f"{a} {op} {b} = {final}",
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
    return pdfmetrics.stringWidth("100. ", "Helvetica-Bold", STORY_SIZE)


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
        text = f"{number:>3}. {problem['equation']}.  Answer: {problem['answer']}"
        entries.append(wrap_text(text, "Helvetica", STORY_SIZE, width))

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
