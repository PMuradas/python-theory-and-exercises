"""Builds placement/level_test.ipynb from questions.json and scoring.py.

Usage:
    python build_notebook.py                      # writes level_test.ipynb (what learners get)
    python build_notebook.py --solved out.ipynb   # notebook with every answer filled in (used by the tests)
"""
import json
import os
import sys

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scoring  # noqa: E402

TIER_TITLES = {"basic": "Part 1: Basic", "intermediate": "Part 2: Intermediate", "advanced": "Part 3: Advanced"}
KIND_LABELS = {"mcq": "Multiple choice", "output": "What is printed?", "code": "Write code"}

INTRO = """# Python level test

Find out where you stand and where to start in this repository. The test has **30 questions** in three parts (Basic, Intermediate, Advanced) and takes about 30 to 45 minutes. At the end you get a score from 0 to 100, your level, the topics worth reviewing and an explanation for every question you missed.

**Please do it on your own, without AI or search.** Nothing is at stake: the result is only useful if it is honest. This is an informal self-assessment, not a certification.

## How to answer

- **Multiple choice:** set the variable to `"a"`, `"b"`, `"c"` or `"d"`. If you do not know, leave it empty (or use `"?"`).
- **What is printed?** Write the exact output between the triple quotes (one line per printed line). Leave it empty if you do not know.
- **Write code:** complete the function or class in the cell. Run the cell so it is defined.

Run each cell after answering. When you finish, run the two cells in the **Get your result** section at the end.

## How the score works

| Level | Score |
|---|---|
| Basic | 0 to 33 |
| Intermediate | 34 to 66 |
| Advanced | 67 to 99 |
| **Perfect score** | 100 (unlocks the **Pro challenge**) |

- Each part is worth about a third of the score: the levels build on each other, so you cannot reach Advanced by skipping the fundamentals.
- Questions are worth different amounts of points (shown in each question). Code questions give **partial credit** for every test case that passes.
- On multiple choice, a **wrong answer costs a third of the question's points** and a blank answer costs nothing, so guessing does not pay off on average. When you are unsure, leave it blank.
- 100 is only possible with a flawless test. It is never reached by rounding.
- With a perfect 100, two harder problems (the Pro challenge) at the end of the notebook decide whether you earn the **Pro** title."""


def points_text(weight):
    return f"{weight / 10:g} pts"


def question_cells(q, solved):
    cells = []
    n = q["number"]
    head = f"### Question {n} · {KIND_LABELS[q['type']]} · {points_text(q['weight'])}\n\n{q['prompt']}"
    if q.get("code"):
        head += f"\n\n```python\n{q['code']}\n```"
    if q["type"] == "mcq":
        head += "\n\n" + "\n".join(f"- **{k})** {v}" for k, v in q["options"].items())
        head += f"\n\n*A wrong answer costs {q['weight'] / 30:.2g} pts; leave it empty if you do not know.*"
    cells.append(nbf.v4.new_markdown_cell(head))

    var = f"answer_{n:02d}"
    if q["type"] == "mcq":
        value = q["answer"] if solved else ""
        cells.append(nbf.v4.new_code_cell(f'{var} = "{value}"  # "a", "b", "c" or "d"; leave empty if you do not know'))
    elif q["type"] == "output":
        value = q["answer"] if solved else ""
        cells.append(nbf.v4.new_code_cell(f'{var} = """\n{value}\n"""  # the exact output, one line per printed line'))
    else:
        cells.append(nbf.v4.new_code_cell((q["solution"] if solved else q["starter"]).rstrip("\n")))
    return cells


def build(solved=False):
    with open(os.path.join(HERE, "questions.json"), encoding="utf-8") as f:
        bank = json.load(f)

    number = 0
    for q in bank["questions"]:
        number += 1
        q["number"] = number

    cells = [nbf.v4.new_markdown_cell(INTRO)]
    counts = {t: sum(1 for q in bank["questions"] if q["tier"] == t) for t in scoring.TIERS}
    for tier in scoring.TIERS:
        cells.append(nbf.v4.new_markdown_cell(f"## {TIER_TITLES[tier]} ({counts[tier]} questions)"))
        for q in bank["questions"]:
            if q["tier"] == tier:
                cells.extend(question_cells(q, solved))

    cells.append(nbf.v4.new_markdown_cell(
        "## Pro challenge\n\nOnly counts if you scored a perfect **100** on the main test. Two harder problems: "
        "every test case of both must pass. Write your solutions in the cells below and run them, then run the "
        "last cell of the notebook."))
    for p in bank["pro"]:
        cells.append(nbf.v4.new_markdown_cell(f"### Pro problem: {p['title']}\n\n{p['prompt']}"))
        cells.append(nbf.v4.new_code_cell((p["solution"] if solved else p["starter"]).rstrip("\n")))

    cells.append(nbf.v4.new_markdown_cell(
        "## Get your result\n\nRun the next two cells. The first one is the grading code, you do not need to read it. "
        "The second one contains the answer key (encoded, so you do not see the answers by accident) and shows your result."))
    with open(os.path.join(HERE, "scoring.py"), encoding="utf-8") as f:
        cells.append(nbf.v4.new_code_cell(f.read().rstrip("\n")))

    stripped = {
        "version": bank["version"], "tier_units": bank["tier_units"], "topics": bank["topics"],
        "questions": [{k: (({o: "" for o in q["options"]}) if k == "options" else v)
                       for k, v in q.items() if k in ("id", "number", "tier", "topic", "type", "weight", "answer", "cases", "explanation", "options")}
                      for q in bank["questions"]],
        "pro": [{k: p[k] for k in ("id", "title", "cases")} for p in bank["pro"]],
    }
    key = scoring.encode_bank(stripped)
    cells.append(nbf.v4.new_code_cell(
        "from IPython.display import HTML, display\n\n"
        f'ANSWER_KEY = "{key}"\n'
        "BANK = decode_bank(ANSWER_KEY)\n"
        "result = grade(globals(), BANK)\n"
        "display(HTML(render(result, BANK)))"))
    cells.append(nbf.v4.new_markdown_cell("## Pro challenge result\n\nRun this after solving the two Pro problems (it only counts with a perfect 100)."))
    cells.append(nbf.v4.new_code_cell("pro = grade_pro(globals(), BANK, result)\ndisplay(HTML(render_pro(pro)))"))

    if solved:
        cells.append(nbf.v4.new_code_cell('assert result["score"] == 100 and pro["pro"], (result["score"], pro)'))

    for index, cell in enumerate(cells):
        cell["id"] = f"cell{index:03d}"          # stable ids, so rebuilding gives an identical file
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                      "language_info": {"name": "python"}}
    return nb


if __name__ == "__main__":
    if "--solved" in sys.argv:
        target = sys.argv[sys.argv.index("--solved") + 1]
        nbf.write(build(solved=True), target)
    else:
        nbf.write(build(solved=False), os.path.join(HERE, "level_test.ipynb"))
    print("notebook written")
