# Worksheets

A library of printable worksheets for special education. Each sheet is written for a specific skill and a specific level, so a teacher can pull the right page without rewriting it for the student in front of them.

Worksheets will vary in difficulty inside every folder. A folder is a skill or a grade band, not a single level.

## Where things go

### Math — `math/`

Computation and applied math.

| Folder | What belongs here |
| --- | --- |
| `multiplication/` | Facts, arrays, and multi-digit multiplication |
| `addition-subtraction/` | Addition and subtraction, from facts through multi-digit work |
| `word-problems/` | Story problems that use the operations above |
| `rounding/` | Rounding to the nearest 10 and 100 |

### Reading — `reading/`

Phonics and oral reading. These pages target how words are decoded and read, not passage comprehension.

| Folder | What belongs here |
| --- | --- |
| `short-vowels/` | CVC and other short-vowel patterns |
| `long-vowels/` | Silent-e and other long-vowel patterns |
| `vowel-teams/` | Two-letter vowel spellings (ai, ea, oa, and so on) |
| `fluency/` | Repeated reading, phrase practice, and rate-building pages |

### Reading comprehension — `reading-comp/`

Passages with questions, organized by grade so the text and the questions match the student.

| Folder | What belongs here |
| --- | --- |
| `grade-1/` through `grade-5/` | Passages and questions written at that grade level |

## How we add a worksheet

Drop the finished file in the folder that matches its skill. Name the file so the skill and level are obvious from the filename, for example `multiplication-facts-2s-level-1.pdf`.

## Generating a worksheet

PDFs are generated from a Python script. Edit the script and run it again. Do not edit a PDF by hand, or the student pages and the answer key will drift apart.

Needs Python 3. ReportLab is listed in `requirements.txt`.

```
pip install -r requirements.txt
python scripts/word_problems_onestep.py
python scripts/word_problems.py
python scripts/subtraction_3digit.py
python scripts/rounding.py
python scripts/reading_comp.py
python scripts/reading_comp_mc.py
```

### Single-step addition and subtraction

| | |
| --- | --- |
| Script | `scripts/word_problems_onestep.py` |
| Student packet | `math/word-problems/addition-subtraction-3-digit.pdf` |
| Answer key | `math/word-problems/addition-subtraction-3-digit-answer-key.pdf` |

The student packet is US Letter, 20 pages, 5 problems per page (100 problems). Addition and subtraction are mixed. Each story is one step only.

- Stories are Helvetica at 14 pt, with an answer line under each problem
- Problems are numbered 1–100 and continue from page to page
- Each student page has a name line, a date line, and a page number such as “Page 3 of 20”
- The answer key is a separate PDF. Each line shows the problem number, the equation, and the final answer

Problems live in `RAW_PROBLEMS` in the script. Each one is a one-step story:

- `a` and `b` are whole numbers from 0 to 999. They are the only numbers in the story
- `op` is `+` or `-`
- `unit` is the word on the answer, such as `crayons`, so the key reads `384 crayons`
- `template` is the story. Write `{a}` and `{b}` where the numbers go. Do not type the digits into the sentence

```python
{
    "a": 248,
    "op": "+",
    "b": 136,
    "unit": "crayons",
    "template": (
        "Maya has {a} crayons. She buys {b} more. How many crayons "
        "does Maya have now?"
    ),
}
```

The script does the arithmetic. It stops without writing the PDFs if a problem breaks a rule:

- The list is not exactly 100 problems
- A number or the final answer is outside 0–999
- The story text does not contain `a` and `b`
- A story is too long to fit above its answer line

Keep a story to two short sentences so it fits.

### Multi-step addition and subtraction

| | |
| --- | --- |
| Script | `scripts/word_problems.py` |
| Student packet | `math/word-problems/addition-subtraction-3-digit-multistep.pdf` |
| Answer key | `math/word-problems/addition-subtraction-3-digit-multistep-answer-key.pdf` |

The student packet is US Letter, 10 pages, 5 problems per page (50 problems).

- Stories are Helvetica at 14 pt, with an answer line under each problem
- Problems are numbered 1–50 and continue from page to page
- Each student page has a name line, a date line, and a page number such as “Page 3 of 10”
- The answer key is a separate PDF. Each line shows the problem number, both steps, and the final answer

Problems live in `RAW_PROBLEMS` in the script. Each one is a two-step story:

- `a`, `b`, and `c` are whole numbers from 0 to 999. They are the only numbers in the story
- `op1` and `op2` are `+` or `-`, in the order the story happens
- `unit` is the word on the answer, such as `crayons`, so the key reads `209 crayons`
- `template` is the story. Write `{a}`, `{b}`, and `{c}` where the numbers go. Do not type the digits into the sentence

```python
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
}
```

The script does the arithmetic. It stops without writing the PDFs if a problem breaks a rule:

- The list is not exactly 50 problems
- A number, a middle step, or the final answer is outside 0–999
- The story text does not contain `a`, `b`, and `c`
- A story is too long to fit above its answer line

Keep a story to two or three short sentences so it fits.

### 3-digit subtraction

`python scripts/subtraction_3digit.py` writes a 50-page packet and a compact answer key.

| | |
| --- | --- |
| Script | `scripts/subtraction_3digit.py` |
| Student packet | `math/addition-subtraction/subtraction-3-digit.pdf` |
| Answer key | `math/addition-subtraction/subtraction-3-digit-answer-key.pdf` |

Each page is a 5 by 5 grid of vertical 3-digit problems. Problems that need regrouping are mixed with problems that do not. Both numbers are 3 digits, and the answer is never negative. Problems are numbered 1–25 on every page, and the pages are numbered, such as “Page 3 of 50.”

### Rounding

`python scripts/rounding.py` writes a 50-page packet and a compact answer key.

| | |
| --- | --- |
| Script | `scripts/rounding.py` |
| Student packet | `math/rounding/rounding-10-and-100.pdf` |
| Answer key | `math/rounding/rounding-10-and-100-answer-key.pdf` |

Each page has four labeled groups. The instruction is printed once, on the group.

- Nearest 10: 24 numbers in four columns. The student writes the rounded number.
- Nearest 100: 24 numbers in four columns.
- Both sides, nearest 10: 9 numbers in three columns. The student writes the tens on each side and circles the correct one.
- Both sides, nearest 100: 9 numbers in three columns.

A number that ends in 5, or 50, rounds up.

### Making the next set

1. Copy `scripts/word_problems.py` and give the copy a name that matches the skill.
2. Replace `RAW_PROBLEMS` and the two output filenames. Put the PDFs in the folder for that skill. Name the student file so the skill and level are obvious, and add `-answer-key` to the teacher file.
3. Keep this layout unless the skill needs a different one: letter size, 14 pt, name and date, numbered problems, numbered pages, an answer line, and a separate key.
4. Run the new script.

### Reading comprehension

`python scripts/reading_comp.py` writes a 20-page student packet and a compact answer key for each of grades 1, 2, and 3.

| Grade | Student packet | Answer key |
| --- | --- | --- |
| 1 | `reading-comp/grade-1/decodable-passages.pdf` | `reading-comp/grade-1/decodable-passages-answer-key.pdf` |
| 2 | `reading-comp/grade-2/passages.pdf` | `reading-comp/grade-2/passages-answer-key.pdf` |
| 3 | `reading-comp/grade-3/instructional-passages.pdf` | `reading-comp/grade-3/instructional-passages-answer-key.pdf` |

Each student page is one story. The boxes fill the page from top to bottom:

- A full-width box with the passage
- Setting and Character, side by side
- Beginning (State Problem)
- Middle (Three Events), with lines numbered 1, 2, and 3
- Ending (Solution)

The header has the story title, the grade, and a name and date line. The footer says which passage it is, such as “Passage 4 of 20.” Passage type is 16 pt in grade 1, 14 pt in grade 2, and 12 pt in grade 3. Labels are 14 pt. The answer boxes are blank writing space.

The answer key is separate. Each entry lists the passage number and title, then the setting, character, beginning, three events, and ending.

Passages live in `GRADE_1`, `GRADE_2`, and `GRADE_3` in `scripts/reading_comp.py`. Each one needs a title, the passage, and the story-map answers. The script stops if a grade does not have 20 passages, if a word count is outside its band, or if a grade 1 word is not decodable.

- Grade 1 is about 60–90 words. Words use short vowels, blends, digraphs (`sh`, `ch`, `th`, `ck`), and silent-e. No vowel teams. Heart words are only `the`, `a`, `to`, `said`, `was`, `of`, `you`, `have`, `they`, `she`, `he`, `are`, `for`, `her`, and `what`.
- Grade 2 is about 100–140 words, in two or three short paragraphs.
- Grade 3 is about 150–190 words, in three or four paragraphs, still short enough to leave room to write.

### Intermediate multiple choice

`python scripts/reading_comp_mc.py` writes a 30-page student packet and a compact answer key for each of grades 1 through 5. Pass an optional folder name, such as `grade-3`, to rebuild one grade.

| Grade | Student packet | Answer key |
| --- | --- | --- |
| 1 | `reading-comp/grade-1/intermediate-passages.pdf` | `reading-comp/grade-1/intermediate-passages-answer-key.pdf` |
| 2 | `reading-comp/grade-2/intermediate-passages.pdf` | `reading-comp/grade-2/intermediate-passages-answer-key.pdf` |
| 3 | `reading-comp/grade-3/intermediate-passages.pdf` | `reading-comp/grade-3/intermediate-passages-answer-key.pdf` |
| 4 | `reading-comp/grade-4/intermediate-passages.pdf` | `reading-comp/grade-4/intermediate-passages-answer-key.pdf` |
| 5 | `reading-comp/grade-5/intermediate-passages.pdf` | `reading-comp/grade-5/intermediate-passages-answer-key.pdf` |

Each page is one story at an intermediate level for that grade. The story fills the top half of the page. It has a problem, three events, and a solution. The bottom half has three multiple-choice questions, each with four answers. The student fills in a circle.

Type size steps down by grade: 16 pt in grade 1, 15 pt in grade 2, 13 pt in grade 3, and 12 pt in grades 4 and 5. The header has the title, the grade, a name line, and a date line. The footer says which passage it is, such as "Passage 4 of 30."

The answer key lists the passage number, the title, each question, and the correct choice.

Passages live in `scripts/passages_mc/`. Each one needs a title, the main character's name, the story, and three questions. A question stores the correct choice and three wrong choices. The script assigns the letters A through D so they stay spread out. It stops if a grade does not have 30 passages, if a story does not fill about half a page, or if a question does not fit in its box.
