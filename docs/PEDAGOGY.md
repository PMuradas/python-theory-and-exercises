# How the course is designed

This page explains why the lessons look the way they do. It is a summary of ideas from computing education research and from existing courses, not a claim that any single method is proven best. Where the evidence is mixed, it says so.

## Design principles

**1. Practice first, with a short review next to each exercise.**
Learners spend most of the time writing and reading code. Each exercise carries a few lines of review so nobody has to leave the page to remember a concept.

**2. Vary the kind of exercise.**
Lessons follow the spirit of [PRIMM](https://eprints.gla.ac.uk/229012) (Predict, Run, Investigate, Modify, Make), a structure for programming lessons whose authors report that starting with existing code, predicting and explaining what it does, helps novices gain confidence before writing their own. In a trial with 493 students aged 11 to 14 in 13 schools, teachers reported that PRIMM helped them support mixed-ability classes ([Sentance, Waite and Kallia, 2019](https://eprints.gla.ac.uk/229013)). Here that becomes:

- `Predict` exercises: read, predict, run, compare.
- `Fix` exercises: broken code to investigate. Research on erroneous worked examples suggests they are a promising way for novices to learn, more so than plain worked examples that students may not engage with ([NC State dissertation](https://repository.lib.ncsu.edu/server/api/core/bitstreams/8f0d5932-a8a4-41e5-9eea-a9f26dac9efa/content)).
- `Make` and `Challenge` exercises: write code, with increasing independence.

**3. Offer scaffolding between reading and writing.**
Moving from reading examples to writing code is hard, especially for people with lower confidence. `Arrange` exercises are Parsons problems: the right lines are given and the learner puts them in order. In studies, novices who used Parsons problems as optional scaffolding spent significantly less time on the related write-code problems, and those with lower self-efficacy were more likely to solve them ([ITiCSE 2023](https://par.nsf.gov/biblio/10510493)).

**4. Spend extra time where beginners go wrong.**
Research on novice misconceptions in Python keeps finding the same hotspots: variables, sequencing, conditionals and loops. One study with 5th graders found that spending more time on variables and sequencing reduced the known misconceptions, and recommends emphasising concepts over syntax ([Žanko, Mladenović and Krpan, 2022](https://www.bib.irb.hr/1172136)). That is why variables get a whole lesson (assignment, tracing, `b = a`), why lesson 8 returns to the "two names, one list" surprise, and why every lesson ends with a list of common mistakes. A catalogue of Python-specific errors is in [this ETH Zurich dissertation](https://www.research-collection.ethz.ch/server/api/core/bitstreams/ee1b9a6e-65ed-4f29-8278-0cad627377b8/content).

**5. Make code visible.**
Forming a mental model of how code runs step by step is one of the core skills for beginners. [Python Tutor](https://research.google/pubs/online-python-tutor-embeddable-web-based-program-visualization-for-cs-education/) draws that execution, and the lessons point to it when it helps most (assignment, lists).

**6. Revisit earlier material.**
Each lesson opens with a short warm-up on previous lessons, and later exercises reuse earlier ideas (for example, letter grades appear in lesson 5 as `if` statements and again in lesson 7 as a function). This is a light form of spaced and interleaved retrieval. A CS1 study that combined spaced and interleaved quizzes with reflection reported higher grades for students who used them ([Moraes et al., 2023](https://mountainscholar.org/items/55f9d5e8-8575-45e5-962b-bb563f71d9b4)). Another study in an engineering course found students rated retrieval practice as the most useful technique, but did not find significant differences in test scores ([ASEE 2024](https://peer.asee.org/incorporating-evidence-based-teaching-practices-in-an-engineering-course-to-improve-learning.pdf)). The evidence is promising but not conclusive, and the cost here is small.

**7. Keep exercises small and aligned with the concept.**
The [Exercism syllabus guide](https://exercism.org/docs/building/tracks/syllabus) separates *concept exercises* (teach one idea, quick to do) from open-ended *practice exercises*, and warns that a good concept exercise is usually a bad practice exercise and vice versa. Users of that platform also report frustration when practice exercises are much harder than the concept they are linked to. Here, exercises are written for the concept of their lesson and stay short; harder ones are labelled `Challenge`.

**8. Real-flavoured problems and a project at the end.**
[CS50P](https://cs50.harvard.edu/python) builds its problem sets around real-world problems, and [Automate the Boring Stuff](https://www.automatetheboringstuff.com) ends each chapter with practice projects. Level 1 ends the same way: a small task manager that uses everything.

**9. Simple, honest checks.**
Checks are plain `assert` statements inside the notebook, so they work in Colab with no extra tools and the learner can read them. Some autograders show failed test cases in a way that can encourage guess-and-check ([Otter Grader talk](https://pyvideo.org/jupytercon-2023/otter-grader-a-lightweight-solution-for-creating-and-grading-jupyter-notebooks.html)); here the check messages say what to look at, not what to type. Every solution notebook is executed automatically (see CONTRIBUTING.md) so a broken exercise is caught early.

**10. Learning with AI around.**
Studies of novices with AI code generators describe benefits (better code, more confidence) alongside risks (over-reliance, weaker independent problem solving). One 2025 controlled study found ChatGPT can improve code quality and efficiency for novices without uniformly improving conceptual understanding ([arXiv:2510.00946](https://arxiv.org/abs/2510.00946)). The README gives learners concrete habits for using AI without skipping the thinking.

## Limits of this design

- Most of the cited studies involve schools or university courses, not self-taught adults using notebooks. The principles are a reasonable starting point, not a guarantee.
- Checks in early lessons test one case. Learners are asked to try other values themselves.
- The course has not yet been tested with real beginners. Feedback is welcome.
