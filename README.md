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
python scripts/word_problems.py
python scripts/reading_comp.py
```

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
