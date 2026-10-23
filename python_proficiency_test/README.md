# Level test

A 30-question test that tells you where you stand in Python and where to start in this repository.

**Open it in Colab:** [`level_test.ipynb`](level_test.ipynb) (upload it or open it from your GitHub copy). It takes about 30 to 45 minutes. Please do it on your own, without AI or search: the result is only useful if it is honest.

At the end you get:

- a score from 0 to 100 and your level
- how many points you earned in each part (Basic, Intermediate, Advanced)
- the topics worth reviewing, with the matching lesson when it exists
- an explanation for every question you missed

## Levels

| Score | Level |
|---|---|
| 0 to 33 | Basic |
| 34 to 66 | Intermediate |
| 67 to 99 | Advanced |
| 100 | Perfect score, which unlocks the **Pro challenge** |

**Pro:** with a perfect 100, two harder problems at the end of the notebook (an LRU cache and an expression evaluator) decide whether you earn the **Pro** title. Both must pass every test case.

## How the points work

The test is worth 100 points, split into three parts that build on each other:

| Part | Questions | Points |
|---|---|---|
| Basic | 12 | 33 |
| Intermediate | 10 | 33 |
| Advanced | 8 | 34 |

- **Cumulative by design.** Mastering the basics is worth 33 points, basics plus intermediate 66. To reach Advanced you need most of the points from the first two parts *and* some of the advanced ones; knowing a few hard tricks is not enough.
- **Three question types.** *Multiple choice* (the only kind that can be guessed), *What is printed?* (typed, all or nothing) and *Write code* (checked by automatic test cases, with **partial credit** for each case that passes). Harder or ungessable questions are worth more points.
- **Guessing does not pay.** A wrong multiple choice answer costs a third of the question's points; a blank answer costs nothing. With four options, a pure guess is worth zero on average. In simulations, answering every multiple choice question at random gives about 3 points (it is above zero because each part is floored at 0).
- **Parts never cancel each other.** Each part is floored at 0 points before adding them up.
- **100 is only for a flawless test.** The score is rounded to the nearest whole number, but anything below 100 points is never rounded up to 100.
- **Honest feedback.** Scores within 3 points of a border are flagged, and uneven results (strong on hard questions, weak on basics) get a note.

Examples (these are checked by the automated tests):

| Answers | Score | Level |
|---|---|---|
| Everything blank | 0 | Basic |
| All Basic questions right, nothing else | 33 | Basic |
| All Basic and Intermediate right | 66 | Intermediate |
| Those, plus the two advanced multiple choice questions | 72 | Advanced |
| Everything right | 100 | Perfect score, Pro challenge unlocked |

## What this test is not

It is an informal self-assessment, not a certification. It has not been calibrated with real learners yet, so the difficulty of each question and the level borders are educated guesses. Well-known assessments such as the FCS1 were validated with interviews, statistics and exam scores; this one is not. The answer key is in this repository, so it works on the honor system.

## Files

| File | What it is |
|---|---|
| `level_test.ipynb` | The test, generated from `questions.json`. Self-contained: it carries its own grader. |
| `questions.json` | The question bank: prompts, answers, test cases, topics and weights. **Edit this one.** |
| `scoring.py` | The scoring rules and the result display. |
| `build_notebook.py` | Rebuilds `level_test.ipynb` from the two files above. |
| `tests/` | Automated tests for the bank and the scoring rules. |

## Changing or adding questions

1. Edit `questions.json`. Each question has a tier (`basic`, `intermediate`, `advanced`), a topic, a type (`mcq`, `output` or `code`) and a weight. The weights of each tier must add up to 330, 330 and 340 (tenths of a point).
2. For `code` questions add a reference `solution` and several `cases` (`call`, optional `setup`, and `expected` or `raises`). Make sure the empty `starter` code does **not** pass any case.
3. Check and rebuild:

```bash
pip install -r requirements-dev.txt
pytest placement/tests
python placement/build_notebook.py
```

The tests verify that every printed-output answer is what the code really prints, that every reference solution passes its cases, that starter code scores nothing, and that the scoring rules behave as described above.

## Ideas for later

- Calibrate difficulty with data: ask 30 to 50 people to take it, then look at the percentage of correct answers per question and adjust weights and borders.
- Draw questions randomly from a larger bank, and eventually make the test adaptive (shorter, with the same precision) once there is enough data to calibrate it.
- Add links to Level 2 and Level 3 lessons as they are written.
