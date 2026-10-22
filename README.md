# Python by Practice

Learn Python by writing it. Every lesson is a notebook with short exercises that **check your answer automatically**, so you always know whether you got it right.

> Level 1 (basics) is ready. Levels 2 and 3 are planned.

## How it works

Most beginners learn more from solving small problems than from reading about syntax, so the lessons are built around exercises. Each exercise has the same shape:

1. **Quick review**: a few lines about the concept, with an example.
2. **Task**: what to build, predict or fix.
3. **Your code**: write your answer in the code cell.
4. **Check**: run the check cell. It tells you if the answer is right.

The exercises come in different kinds, because reading, fixing and writing code are different skills:

| Kind | What you do |
|---|---|
| `Predict` | Read code and say what it will print *before* running it |
| `Fix` | Find and repair a bug (and learn to read error messages) |
| `Arrange` | Put scrambled lines in the right order |
| `Make` | Write code from scratch |
| `Challenge` | A harder exercise that combines ideas |
| `Your turn` | Free practice, no automatic check |

Every lesson (after the first) opens with a short warm-up that revisits earlier lessons, and ends with a recap and a list of common mistakes. More about the reasoning behind this in [docs/PEDAGOGY.md](docs/PEDAGOGY.md).

## Level 1: Basics

| # | Lesson | You will learn | Open |
|---|---|---|---|
| 01 | Hello, Python | `print`, comments, reading error messages | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/01_hello_python.ipynb) |
| 02 | Variables and data types | assignment, tracing code, `int` `float` `str` `bool`, conversions | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/02_variables_and_types.ipynb) |
| 03 | Numbers and operators | arithmetic, precedence, comparisons, `and` `or` `not` | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/03_numbers_and_operators.ipynb) |
| 04 | Strings | indexing, slicing, methods, f-strings | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/04_strings.ipynb) |
| 05 | Conditionals | `if` / `elif` / `else`, truthy and falsy values | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/05_conditionals.ipynb) |
| 06 | Loops | `for`, `while`, `range`, `break`, nested loops | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/06_loops.ipynb) |
| 07 | Functions | parameters, `return`, default values, scope | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/07_functions.ipynb) |
| 08 | Lists and tuples | list methods, copies vs references, unpacking | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/08_lists_and_tuples.ipynb) |
| 09 | Dictionaries and sets | lookups, counting, iterating, set operations | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/09_dictionaries_and_sets.ipynb) |
| 10 | Files and errors | `try` / `except`, reading and writing files | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/10_files_and_errors.ipynb) |
| 11 | Project: task manager | everything together, in a small command-line app | [Colab](https://colab.research.google.com/github/PMuradas/python-theory-and-exercises/blob/main/level-1-basics/11_project_task_manager.ipynb) |

About 70 exercises plus the project. No installation needed: open a lesson in Google Colab (or run the notebooks locally with Jupyter).

## How to use this repository

1. Open a lesson in Colab and run the first cell.
2. Work through the exercises in order. Try each one yourself before looking at anything else.
3. If you get stuck, use the hint, re-read the quick review, or paste your code into [Python Tutor](https://pythontutor.com) to watch it run step by step.
4. When you finish, compare with the notebook in [`solutions/`](solutions/). There is almost never only one right answer.

A note on the checks: in the early lessons they test one case, so after a check passes, try other values yourself to make sure your code really works.

## Using AI while you learn

AI assistants are useful, but studies on beginners suggest they can improve the code you hand in without always improving what you understand. Some habits that keep the learning in:

- Try the exercise yourself first. Get stuck for a while: that is the useful part.
- Ask for a hint or an explanation, not for the full solution.
- After any help, close the chat and write the solution again from scratch.
- Explain the code in your own words. If you cannot, you are not done yet.

## Roadmap

- [x] **Level 1: Basics**
- [ ] **Level 2: Intermediate**: comprehensions, modules and packages, virtual environments, classes and objects, JSON and CSV, `pathlib`, regular expressions, debugging, testing with `pytest`
- [ ] **Level 3: Advanced**: iterators and generators, decorators, context managers, type hints, concurrency, packaging, performance

## Contributing

Found a mistake, an unclear explanation or a better exercise? Please open an issue or a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
